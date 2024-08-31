import csv
import logging
import json
import os
import datetime as dt
from statistics import mean
import decimal
from pathlib import Path
from binubuo import binubuo
from binubuo.BinubuoTemplate import BinubuoTemplate

class binubuoCSV(binubuo):
    def __init__(self, binubuokey):
        super().__init__(binubuokey)
        self.binubuokey = binubuokey
        self.max_sample_size = 100
        self.connected = False
        self.show_messages = True

    def setup_logging(self):
        # Create the logger
        self.logger = logging.getLogger(__name__)
        # Logger settings and levels
        self.logger.setLevel(logging.DEBUG)
        # Logger formatter and handler
        file_handler = logging.FileHandler(filename='binubuo.log', mode='a', encoding='utf8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        # Add the handler to the logger
        self.logger.addHandler(file_handler)

    def csv_line_count(self, fname):
        with open(fname) as f:
            return sum(1 for line in f)

    def can_float(self, x):
        try:
            float(x)
            return True
        except:
            return False

    def is_date_string(self, str):
        date_fmts = ('%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%d-%m-%Y %H:%M:%S','%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y','%b %d, %Y','%b %d, %Y','%B %d, %Y','%B %d %Y','%m/%d/%Y','%m/%d/%y','%b %Y','%B%Y','%b %d,%Y')
        parsed = []
        if str is not None:
            for fmt in date_fmts:
                try:
                    t = dt.datetime.strptime(str, fmt)
                    parsed.append((str, fmt, t)) 
                    break
                except ValueError as err:
                    pass
        return parsed

    def get_file_csv_dialect(self, fname):
        try:
            self.logger.debug("Find dialect for %s", fname)
            with open(fname, newline='', encoding='utf-8') as csvfile:
                self.current_dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)
                self.logger.debug("Dialect found for %s", fname)
                self.logger.debug("CSV Dialect - Delimiter: '%s', Doublequote: '%s', Escapechar: '%s', Lineterminator: '%s', Quotechar: '%s'", self.current_dialect.delimiter, str(self.current_dialect.doublequote), self.current_dialect.escapechar, self.current_dialect.lineterminator, self.current_dialect.quotechar)
                # Here we need to see if we are actually quoting, and set the corresponding dialect attribute.
                # csv.QUOTE_ALL : Writer to quote all fields.
                # csv.QUOTE_MINIMAL : Writer to quote fields that contain special characters
                # csv.QUOTE_NONNUMERIC: Writer quotes all fields except numeric fields.
                # csv.QUOTE_NONE: Writer does not quote any fields and no special processing is required from the Reader object.
                row_length = None
                count_quotechars = None
                count = 0
                while True:
                    count += 1
                    line = csvfile.readline()
                    row_length = line.count(self.current_dialect.delimiter) + 1
                    row_quote_count = line.count(self.current_dialect.quotechar)/2
                    self.logger.debug('Row element lenght: %s, Quoted element count: %s for row [%s]', row_length, row_quote_count, line)
                    if count > 10:
                        break
                    if row_quote_count >= row_length:
                        count_quotechars = csv.QUOTE_ALL
                    elif row_quote_count > 0 and row_quote_count < row_length:
                        count_quotechars = csv.QUOTE_NONNUMERIC
                    else:
                        count_quotechars = csv.QUOTE_NONE
                # Now set the value for the dialect
                self.logger.debug("Quoting set as: %s", count_quotechars)
                self.current_dialect.quoting = count_quotechars
        except Exception as e:
            self.logger.error("Error %s happened during read.", e)

    def templateFromFile(self, file_name, known_header=None, output_type="json"):
        self.m("Create template from csv file [" + file_name + "].", tolog=True)
        table_template = BinubuoTemplate()
        # Open file and go through it.
        try:
            with open(file_name, newline='', encoding='utf-8') as csvfile:
                self.logger.info("File %s opened successfully", file_name)
                # Get the row count
                row_count = self.csv_line_count(file_name)
                self.logger.info("File %s has %s rows.", file_name, row_count)
                # Extract metadata
                self.current_dialect = csv.Sniffer().sniff(csvfile.read(1024))
                # Reset file pointer
                csvfile.seek(0)
                if known_header is not None:
                    self.current_has_header = known_header
                else:
                    self.current_has_header = csv.Sniffer().has_header(csvfile.read(1024))
                # Reset file pointer
                csvfile.seek(0)
                self.current_reader = csv.reader(csvfile, self.current_dialect)
                csv_sample_store = {}
                self.logger.debug("Start loading the sample store.")
                for count, row in enumerate(self.current_reader):
                    # Sample data store setup
                    if count == 0:
                        if self.current_has_header:
                        # Setup data store with header names
                            self.logger.debug("setting up data store with named headers")
                            for head_count, head_value in enumerate(row):
                                self.logger.debug("Creating store with header %s", head_value)
                                csv_sample_store[head_value] = []
                        else:
                            # Setup data stor with generated header names
                            self.logger.debug("setting up data store with generated headers")
                            for head_count, head_value in enumerate(row):
                                head_name = "c" + str(head_count)
                                self.logger.debug("Creating store with header %s", head_name)
                                csv_sample_store[head_name] = []
                    # Loop over rows. 
                    if count == int(self.binubuo_config.get('CSV', 'max_row_sample', fallback=100)):
                        break
                    else:
                        # We are in the sampling count, so split out the values to the columns
                        if self.current_has_header and count == 0:
                            pass
                        else:
                            for col_count, col_name in enumerate(csv_sample_store):
                                if not row[col_count]:
                                    csv_sample_store[col_name].append(None)
                                else:
                                    csv_sample_store[col_name].append(row[col_count])
            # Now we have the sample store. Enumerate each to get infer data.
            self.logger.debug("Enumerate sample store for infer JSON generation")
            for count, idx in enumerate(csv_sample_store):
                self.m("Sampling data on column [" + idx +"].", indent=True, tolog=False)
                self.logger.debug("Sample data for col %s: %s", idx, csv_sample_store[idx])
                infer_meta = {}
                self.logger.debug("Start creating infer JSON for column %s", idx)
                infer_meta["column_name"] = idx
                infer_meta["table_name"] = Path(file_name).stem
                # Nulls before checking for datatype
                self.logger.debug("before null check")
                infer_meta["column_nulls"] = sum(x is None for x in csv_sample_store[idx])
                if infer_meta["column_nulls"] > 0:
                    infer_meta["column_nullable"] = "Y"
                else:
                    infer_meta["column_nullable"] = "N"
                # Datatype check
                nums_chk = [x for x in csv_sample_store[idx] if self.can_float(x)]
                self.logger.debug("Numbers checked: %s", nums_chk)
                self.logger.debug("before datatype check")
                if len(nums_chk) == len(csv_sample_store[idx]) or len(nums_chk) == (len(csv_sample_store[idx]) - infer_meta["column_nulls"]):
                    infer_meta["column_datatype"] = "number"
                    infer_meta["column_number_decimals"] = round(mean([decimal.Decimal(str(x)).as_tuple().exponent for x in nums_chk])*-1)
                else:
                    # TODO: Here we need to check if it is a date, before we just set it to string
                    # Checking for date format is very intensive. So as soon as we have one fail (len(0)) returned from the checker, we give up.
                    is_date = None
                    date_format = None
                    for str_num, str_val in enumerate(csv_sample_store[idx]):
                        self.logger.debug("About to date check %s", str_val)
                        has_date_format = self.is_date_string(str_val)
                        if len(has_date_format) == 0:
                            is_date = False
                            break
                        else:
                            is_date = True
                            date_format = has_date_format[0][1]
                            self.logger.debug("Found format: %s", date_format)
                    if is_date:
                        infer_meta["column_datatype"] = "date"
                    else:
                        infer_meta["column_datatype"] = "string"
                self.logger.debug("before data metadata settings")
                infer_meta["table_level_rowcount"] = row_count
                infer_meta["table_level_avg_row_length"] = ""
                infer_meta["column_level_avg_col_length"] = round(sum( map(len, map(str, csv_sample_store[idx])) ) / len(csv_sample_store[idx]))
                infer_meta["column_data_length"] = "4000"
                infer_meta["column_number_precision"] = ""
                # Unique list
                u_set = set(csv_sample_store[idx])
                u_list = (list(u_set))
                # Bug with unique. For now ignore
                #if len(u_list) == len(csv_sample_store[idx]):
                #    infer_meta["column_is_unique"] = "yes"
                #    infer_meta["column_distinct_count"] = len(csv_sample_store[idx])
                #else:
                infer_meta["column_is_unique"] = "no"
                infer_meta["column_distinct_count"] = len(csv_sample_store[idx]) - len(u_list)
                self.logger.debug("before data low/high settings")
                if infer_meta["column_datatype"] == "number":
                    infer_meta["column_low_value"] = min([float(x) for x in nums_chk])
                    infer_meta["column_high_value"] = max([float(x) for x in nums_chk])
                elif infer_meta["column_datatype"] == "date":
                    self.logger.debug("Just before date min/max")
                    infer_meta["column_low_value"] = min([dt.datetime.strptime(x, date_format) for x in csv_sample_store[idx] if x is not None]).strftime('%Y-%m-%d %H:%M:%S')
                    infer_meta["column_high_value"] = max([dt.datetime.strptime(x, date_format) for x in csv_sample_store[idx] if x is not None]).strftime('%Y-%m-%d %H:%M:%S')
                elif infer_meta["column_datatype"] == "string":
                    infer_meta["column_low_value"] = min([x for x in csv_sample_store[idx] if x is not None])
                    infer_meta["column_high_value"] = max([x for x in csv_sample_store[idx] if x is not None])
                if infer_meta["column_datatype"] == "number":
                    infer_meta["sample_values"] = nums_chk
                else:
                    infer_meta["sample_values"] = csv_sample_store[idx]
                self.logger.debug("Infer: %s", json.dumps(infer_meta))
                table_template.init_column(column_name=idx)
                x_response = self.infer_generator(json.dumps(infer_meta))
                self.logger.info("Infer result: %s", x_response)
                table_template.replace_column_from_json(idx, json.dumps(x_response))
            self.m("Template for csv file [" + file_name +"] successfully created.", indent=True, tolog=False)
            if output_type.upper() == "JSON":
                table_template.validate_template()
                table_template.complete_template()
                return table_template.template_JSON
            else:
                return table_template
        except Exception as e:
            self.logger.error("Error %s happened during read.", e)

    def dataset_from_csv(self, file_name, known_header=None):
        dset_name = Path(file_name).stem.lower()
        dset_template = self.templateFromFile(file_name, known_header)
        self.create_dataset(dset_name, dset_template)

    def copy_csv(self, file_name, new_name
            , drop_target_if_exist=False, data_rows="source"
            , known_header=None):
        self.m("Create copy [" + new_name + "] of CSV  [" + file_name + "].", tolog=True)
        dset_name = Path(file_name).stem
        can_create = False
        self.logger.debug("Before checking existence")
        if not self.dataset_exists(dset_name):
            self.dataset_from_csv(file_name, known_header)
        # Always get fresh dialect.
        self.logger.debug("Before contained dialect check")
        self.get_file_csv_dialect(file_name)
        self.logger.debug("Received dialect and quoting is: %s", self.current_dialect.quoting)
        self.logger.debug("Check if %s already exists", new_name)
        if os.path.exists(new_name):
            if drop_target_if_exist:
                # remove file
                self.logger.debug("%s already exists, but allow dropped set. Removing file.", new_name)
                os.remove(new_name)
                can_create = True
        else:
            self.logger.debug("%s does not exists.", new_name)
            can_create = True
        if can_create:
            # Set the rows
            if data_rows == "source":
                self.drows(self.csv_line_count(file_name))
            else:
                self.drows(int(data_rows))
            # Get the data
            csv_data = self.dataset(dset_name)
            with open(new_name, 'w', encoding='UTF8', newline='') as fp:
                writer = csv.writer(fp, self.current_dialect)
                # TODO: Handle header
                self.logger.debug("About to write %s rows in batch mode to %s", len(csv_data), new_name)
                writer.writerows(csv_data)
            self.m("Copy " + new_name + " created successfully.", tolog=True)
