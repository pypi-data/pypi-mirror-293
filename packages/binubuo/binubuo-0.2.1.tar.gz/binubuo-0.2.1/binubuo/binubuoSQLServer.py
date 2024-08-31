from threading import main_thread
import pyodbc
import sys
import json
import ast
import time
import logging
from binubuo import binubuo
from binubuo.BinubuoTemplate import BinubuoTemplate

# Remove annoying incompatible warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

class binubuoSQLServer(binubuo):
    def __init__(self, binubuokey, dbserver, dbname, dbfullConnection=None):
        super().__init__(binubuokey)
        self.binubuokey = binubuokey
        self.dbserver = dbserver
        self.dbname = dbname
        self.dbfullConnection = dbfullConnection
        self.max_sample_size = 100
        self.connected = False
        self.binuObj = binubuo(binubuokey)
        self.show_messages = True

    def setup_logging(self):
        # Create the logger
        self.logger = logging.getLogger(__name__)
        # Logger settings and levels
        self.logger.setLevel(logging.DEBUG)
        # Logger formatter and handler
        file_handler = logging.FileHandler(filename='binubuo.log', mode='a')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        # Add the handler to the logger
        self.logger.addHandler(file_handler)

    def connect(self):
        try:
            if self.dbfullConnection is None:
                #self.connection = pyodbc.connect(Trusted_Connection='yes', driver = '{ODBC Driver 17 for SQL Server}',server = self.dbserver , database = self.dbname)
                #self.connection = pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server Native Client 11.0}',server = self.dbserver , database = self.dbname)
                self.connection = pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = self.dbserver , database = self.dbname)
            else:
                self.connection = self.dbfullConnection
            self.connected = True
            #self.connection.autocommit = True
            working_cursor = self.connection.cursor()
            stmt = self.load_resource("sqlserver_date_format.sql")
            self.logger.info(stmt)
            working_cursor.execute(stmt)
        except:
            self.m("Error: Failed to connect to database. Please make sure you have a connection before using other methods.")
            self.connection = None

    def connectSecondary(self, dbserver, dbname, dbfullConnection=None):
        try:
            if dbfullConnection is None:
                self.secondary_connection = pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server Native Client 11.0}',server = dbserver , database = dbname)
            else:
                self.secondary_connection = dbfullConnection
            self.connected_secondary = True
            working_cursor = self.connection.cursor()
            stmt = self.load_resource("sqlserver_date_format.sql")
            self.logger.info(stmt)
            working_cursor.execute(stmt)
        except:
            self.m("Error: Failed to connect to secondary/alternate database. Please check your connection details and try again.")
            self.secondary_connection = None

    def calculateSampleSize(self, table_name):
        sub_sample_cursor = self.connection.cursor()
        sub_sample_size_stmt = self.load_resource("sqlserver_table_rows.sql")
        sub_sample_cursor.execute(sub_sample_size_stmt, (table_name.upper(),))
        sub_sample_size_cal = sub_sample_cursor.fetchone()
        # Calculate the real sample size in percent
        if (int(sub_sample_size_cal[0]) > 0 and int(sub_sample_size_cal[0]) < self.max_sample_size):
            sub_sample_size_cal_cust = 99.99
        elif (int(sub_sample_size_cal[0]) > self.max_sample_size):
            # Calculate rough percentage of max sample size
            sub_sample_size_cal_cust = round((self.max_sample_size/int(sub_sample_size_cal[0])*100), 8)
        else:
            # In case of zero rows, we read all of nothing :)
            sub_sample_size_cal_cust = 99.99
        self.logger.info("Sample size of %s calculated for %s rows.", str(sub_sample_size_cal_cust), str(sub_sample_size_cal[0]))
        return sub_sample_size_cal_cust

    def tableSize(self, table_name):
        table_size_cursor = self.connection.cursor()
        table_size_size_stmt = self.load_resource("sqlserver_table_rows.sql")
        table_size_cursor.execute(table_size_size_stmt, (table_name.upper(),))
        table_size_size_cal = table_size_cursor.fetchone()
        table_size_size_cal = table_size_size_cal[0]
        self.logger.info("Table size of %s is %s rows.", table_name, str(table_size_size_cal))
        return table_size_size_cal

    def fixDataTypeForJSON(self, data_in):
        if str(type(data_in)) == "<class 'datetime.datetime'>":
            data_out = data_in.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif str(type(data_in)) == "<class 'bytes'>":
            # Let us restrict the size of the sample value, since we are just getting 
            # bytes as hex it could be huge.
            data_out = data_in.hex()[:30]
        elif str(type(data_in)) == "<class 'decimal.Decimal'>":
            data_out = float(data_in)
        elif str(type(data_in)) == "<class 'str'>":
            # Substring so we don't fill in sample values of huge documents.
            if len(data_in) > 250:
                data_out = data_in[:250]
            else:
                data_out = data_in
        else:
            data_out = data_in
        return data_out

    def templateFromTable(self, table_name, use_comments=True, use_infer=False, use_sample_data=False, output_type="json"):
        self.m("Create template from table [" + table_name + "]. Infer=" + str(use_infer) + " Sampledata=" + str(use_sample_data) + ".", tolog=True)
        table_template = BinubuoTemplate()
        # Let us validate the table name before we continue.
        table_exist = self.table_exist(table_name)
        # There are a number of different ways to branch out and do the template.
        # 1. Just use generic defaults for datatype.
        # 2. Use comments if available, and fall back to defaults if a column does not have a comment.
        # 3. Call the webservice with _only_ metadata to infer the generator
        # 4. Call the webservice with metadata _and_ sample data to infer the generator.
        if table_exist:
            self.templateTable = table_name.upper()
            if not use_infer:
                self.m("Using simple method to create columns.", indent=True, tolog=False)
                # No webservice call to generate template.
                working_cursor = self.connection.cursor()
                generic_column_meta_sql = self.load_resource("sqlserver_column_meta_simple.sql")
                working_cursor.execute(generic_column_meta_sql, (table_name.upper(),table_name.upper(),))
                for cname, cdtype, cdgenerator, ccomment, crows, cnumnulls, cnumdist, cnullable, cavglen in working_cursor:
                    table_template.init_column(column_name=cname, column_type="generated", column_datatype=cdtype)
                    if ccomment is not None and use_comments:
                        table_template.set_column_attribute(cname, "generator", ccomment)
                    else:
                        table_template.set_column_attribute(cname, "generator", cdgenerator)
                # Once we are done, we can validate the template and return it.
                self.m("Template for table [" + table_name +"] successfully created.", indent=True, tolog=False)
                if output_type.upper() == "JSON":
                    table_template.validate_template()
                    table_template.complete_template()
                    return table_template.template_JSON
                else:
                    return table_template
            else:
                # Placeholder to run the infer code.
                self.m("Using infer method to create columns.", indent=True, tolog=False)
                if use_sample_data:
                    sub_sample_size_cal_cust = self.calculateSampleSize(table_name)
                working_cursor = self.connection.cursor()
                if use_sample_data:
                    columns_meta_stmt = self.load_resource("sqlserver_column_meta_plus_sample.sql")
                else:
                    columns_meta_stmt = self.load_resource("sqlserver_column_meta_plus_standard.sql")
                self.logger.debug("Statement to get column data: %s", columns_meta_stmt)
                working_cursor.execute(columns_meta_stmt, (table_name.upper(),table_name.upper(),table_name.upper(),))
                # Stupid SQLServer does not allow for "per column" json.
                # So we are getting all and then looping over every array member which will be a column
                all_cols = ""
                for row in working_cursor:
                    all_cols = all_cols + row[0]
                self.logger.debug("Full text before json conversion: %s", all_cols)
                all_cols = json.loads(all_cols)
                self.logger.debug("Full json: %s", all_cols)
                table_size = self.tableSize(table_name)
                for idx, value in enumerate(all_cols):
                    self.logger.info("Column to infer: %s", value["column_name"])
                    sqlserver_schema = value["table_schema"]
                    # Get table size
                    main_meta = ""
                    # Because of sql servers wonderful obfuscated dictionary data we have to fetch some of the statistics data
                    # from dbcc calls. And even then we are not sure we can get any data. So enclose in try-except
                    # DBCC STATS_HEADER
                    try:
                        stats_cursor = self.connection.cursor()
                        column_stats_header_stmt = self.load_resource("sqlserver_column_stats_header.sql").format(schema_name = value["table_schema"], table_name = table_name, column_name = value["column_name"])
                        stats_header = stats_cursor.execute(column_stats_header_stmt).fetchall()
                        value["column_level_avg_col_length"] = int(stats_header[0][6])
                        self.logger.debug("Fetched stats header for col: %s, avg_col_len is: %s", value["column_name"], value["column_level_avg_col_length"])
                    except:
                        # Let us just make sure to close the ***** cursor and reopen
                        self.logger.debug("Error fetching stats header for col: %s.", value["column_name"])
                        stats_cursor.close()
                    try:
                        stats_cursor.close()
                    except:
                        pass
                    # DBCC HISTOGRAM
                    try:
                        stats_cursor = self.connection.cursor()
                        column_stats_histogram_stmt = self.load_resource("sqlserver_column_stats_histogram.sql").format(schema_name = value["table_schema"], table_name = table_name, column_name = value["column_name"])
                        stats_histogram_rows = stats_cursor.execute(column_stats_histogram_stmt).fetchall()
                        # Loop across all rows and collect and calculate some basic stats
                        lowest_val = self.fixDataTypeForJSON(stats_histogram_rows[0][0])
                        highest_val = self.fixDataTypeForJSON(stats_histogram_rows[0][0])
                        rows_at_lowest = stats_histogram_rows[0][2]
                        lowest_val_value = None
                        for histo_row in stats_histogram_rows:
                            if lowest_val is None and highest_val is not None:
                                lowest_val_value = self.fixDataTypeForJSON(histo_row[0])
                            highest_val = self.fixDataTypeForJSON(histo_row[0])
                        # Just check if both low and high is None, and if yes then all null.
                        # Else set the null percentage.
                        if lowest_val is None and highest_val is None:
                            # all nulls
                            value["column_nulls"] = 100
                        elif lowest_val is None and highest_val is not None:
                            value["column_nulls"] = round((rows_at_lowest/table_size)*100)
                            value["column_low_value"] = None
                            value["column_high_value"] = highest_val
                        else:
                            value["column_low_value"] = lowest_val_value
                            value["column_high_value"] = highest_val
                        self.logger.debug("Fetched stats header for col: %s, avg_col_len is: %s", value["column_name"], value["column_level_avg_col_length"])
                    except:
                        # Let us just make sure to close the ***** cursor and reopen
                        self.logger.debug("Error fetching stats histogram for col: %s.", value["column_name"])
                        stats_cursor.close()
                    try:
                        stats_cursor.close()
                    except:
                        pass
                    # If we are allowed sample data. Now is the time to fetch individual samples
                    if use_sample_data:
                        self.m("Sampling data on column [" + value["column_name"] +"].", indent=True, tolog=False)
                        sub_sample_cursor = self.connection.cursor()
                        # Merge the sample data.
                        # First parse the main column metadata
                        main_meta = value
                        if sub_sample_size_cal_cust < 5:
                            sub_sample_stmt = self.load_resource("sqlserver_column_sample_data_top.sql").format(r_col_name=value["column_name"], r_schema_name=value["table_schema"], r_table_name=table_name)
                        else:
                            sub_sample_stmt = self.load_resource("sqlserver_column_sample_data.sql").format(r_col_name=value["column_name"], r_schema_name=value["table_schema"], r_table_name=table_name, r_table_sample_size=sub_sample_size_cal_cust)
                        self.logger.debug("Statement to get column (%s) sample data: %s", value["column_name"], sub_sample_stmt)
                        # We need to make sure that we have a sample here in sqlserver, since a lot of the other
                        # statistics data we get in other databases are not readily available here.
                        if table_size > 0 and int(value["column_nulls"]) < 100:
                            self.logger.debug("Sampling to be done.")
                            got_sample_rows = False
                            try_sample_rows = 0
                            sample_arr = []
                            while not got_sample_rows:
                                sample_rows = sub_sample_cursor.execute(sub_sample_stmt).fetchall()
                                try_sample_rows = try_sample_rows + 1
                                self.logger.debug("Sample run: %s", try_sample_rows)
                                if len(sample_rows) > 0:
                                    self.logger.debug("We got %s rows.", len(sample_rows))
                                    got_sample_rows = True
                                else:
                                    if try_sample_rows > 10:
                                        self.logger.debug("Tried sampling 10 times without any rows. Breaking loop")
                                        value["column_nulls"] = 100
                                        value["column_low_value"] = 'Not extractable'
                                        value["column_high_value"] = 'Not extractable'
                                        sample_arr = []
                                        sample_rows = []
                                        break
                            do_text_validation = False
                            if len(sample_rows) > 0:
                                for sample_value in sample_rows:
                                    self.logger.debug("Type is %s", type(sample_value[0]))
                                    sample_arr.append(self.fixDataTypeForJSON(sample_value[0]))
                                    if str(type(sample_value[0])) == "<class 'str'>":
                                        do_text_validation = True
                            # Before we put the array with sample data, 
                            # we still need to check for combined size.
                            if do_text_validation:
                                comb_len = 0
                                avg_len = 0
                                for val in sample_arr:
                                    comb_len = comb_len + len(val)
                                avg_len = comb_len/len(sample_arr)
                                if comb_len > 20000:
                                    # Take 32000 divided by avg size elements only
                                    trim_elements = round(20000/avg_len)
                                    sample_arr = sample_arr[:trim_elements]
                        # Now add the sample data as a real array.
                        main_meta["sample_values"] = sample_arr
                        # Clear sample array for next check
                        sample_arr = []
                        sample_rows = []
                        if main_meta["column_is_reference"] == 1:
                            self.m("Column [" + value["column_name"] +"] is foreign key. Create key distribution histogram.", indent=True, tolog=False)
                            rel_sample_size_cal_cust = self.calculateSampleSize(main_meta["reference_table"])
                            ref_schema = self.table_sql_schema(main_meta["reference_table"])
                            rel_sample_cursor = self.connection.cursor()
                            self.logger.debug("Parameters for relation histogram. col_name=%s, schema_name=%s, tab_name=%s, ref_col_name=%s, ref_col_table=%s, ref_col_schema=%s, ref_sample=%s", main_meta["column_name"], sqlserver_schema, table_name, main_meta["reference_column"], main_meta["reference_table"], ref_schema, rel_sample_size_cal_cust)
                            if rel_sample_size_cal_cust > 5:
                                rel_sample_stmt = self.load_resource("sqlserver_foreign_key_histogram.sql").format(col_name = main_meta["column_name"], schema_name=sqlserver_schema, tab_name = table_name, ref_col_name = main_meta["reference_column"], ref_tab_name = main_meta["reference_table"], ref_sample = rel_sample_size_cal_cust, ref_schema_name = ref_schema)
                            else:
                                rel_sample_stmt = self.load_resource("sqlserver_foreign_key_histogram_top.sql").format(col_name = main_meta["column_name"], schema_name=sqlserver_schema, tab_name = table_name, ref_col_name = main_meta["reference_column"], ref_tab_name = main_meta["reference_table"], ref_schema_name = ref_schema)
                            self.logger.info("Column is a foreign key. Build relation histogram")
                            self.logger.debug("Relation histogram query: %s", rel_sample_stmt)
                            rel_sample_cursor.execute(rel_sample_stmt)
                            self.logger.debug("Rows affected: %s", rel_sample_cursor.rowcount)
                            all_ref_histo = ""
                            all_rows = rel_sample_cursor.fetchall()
                            for ref_histo_row in all_rows:
                                all_ref_histo = all_ref_histo + ref_histo_row[0]
                            self.logger.debug("Foreign key histogram: ")
                            rel_sample_data_clob_str = all_ref_histo
                            self.logger.debug("Histogram: %s", rel_sample_data_clob_str)
                            if len(rel_sample_data_clob_str) > 0:
                                rel_sample_data_clob_str = ast.literal_eval(rel_sample_data_clob_str)
                                main_meta["reference_histogram"] = rel_sample_data_clob_str
                            else:
                                self.logger.debug("Got zero rows from FK histogram sample query. Happens when the number of pages in the table is low.")
                    else:
                        main_meta = value
                    # We now have every column and its metadata. Send to API endpoint to do intelligent infer.
                    # We get back the entire json of inferred column
                    # Init column
                    table_template.init_column(column_name=value["column_name"])
                    # Try calling infer endpoint
                    self.logger.debug("Type of data to infer: %s", type(main_meta))
                    self.logger.info("Infer: %s", json.dumps(main_meta))
                    x_response = self.infer_generator(json.dumps(main_meta))
                    self.logger.info(x_response)
                    # The response is the column json as a string format. Call replace_column_from_json
                    table_template.replace_column_from_json(value["column_name"], json.dumps(x_response))
                self.m("Template for table [" + table_name +"] successfully created.", indent=True, tolog=False)
                # Once we are done, we can validate the template and return it.
                if output_type.upper() == "JSON":
                    table_template.validate_template()
                    table_template.complete_template()
                    return table_template.template_JSON
                else:
                    return table_template

    def columnGeneratorComments(self, table_name, comments, override=False):
        if self.connected:
            comment_count_sql = """select
                    count(exp.value)
                from 
                    INFORMATION_SCHEMA.COLUMNS ISC
                    left outer join sys.extended_properties exp on object_id(ISC.table_name) = exp.major_id and isc.ordinal_position = exp.minor_id
                WHERE
                    isc.table_name = ?
                and
                    exp.class_desc = 'OBJECT_OR_COLUMN'
                and
                    exp.name = 'MS_DESCRIPTION';"""
            working_cursor = self.connection.cursor()
            working_cursor.execute(comment_count_sql, (table_name,))
            cursor_result = working_cursor.fetchone()
            print(cursor_result)
            self.m("Comments: " + str(cursor_result[0]))
            if (cursor_result[0] > 0 or not override) or (cursor_result[0] == 0):
                # Let us go ahead and set comment generators as requested.
                if (comments.find('=') > 0):
                    # Named notation
                    for cn in comments.split(","):
                        colname = cn.split("=")[0].strip()
                        colcomment = cn.split("=")[1].strip()
                        col_add_stmt = """EXEC sp_addextendedproperty   
                            @name = N'MS_DESCRIPTION',   
                            @value = ?,  
                            @level0type = N'Schema', @level0name = 'dbo',  
                            @level1type = N'Table',  @level1name = ?,  
                            @level2type = N'Column', @level2name = ?"""
                        working_cursor.execute(col_add_stmt, (colcomment, table_name, colname))
                        self.connection.commit()
                else:
                    # Just split and follow column order. Ignore any column outside of split length
                    ordered_col_cursor = self.connection.cursor()
                    ordered_col_sql = "select ORDINAL_POSITION, COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where table_name = ? order by ORDINAL_POSITION asc;"
                    ordered_col_cursor.execute(ordered_col_sql, (table_name,))
                    comment_cursor = self.connection.cursor()
                    col_row = ordered_col_cursor.fetchone()
                    while col_row:
                        self.m("Working on col: " + col_row[1])
                        try:
                            colcomment = comments.split(",")[col_row[0] - 1]
                            col_add_stmt = """EXEC sp_addextendedproperty   
                                @name = N'MS_DESCRIPTION',   
                                @value = ?,  
                                @level0type = N'Schema', @level0name = 'dbo',  
                                @level1type = N'Table',  @level1name = ?,  
                                @level2type = N'Column', @level2name = ?"""
                            self.m("Comment command: " + col_add_stmt + "\nWith args: " + colcomment + " " + table_name + " " + col_row[1])
                            comment_cursor.execute(col_add_stmt, (colcomment, table_name, col_row[1]))
                        except:
                            # Aint no comment for this column. Just ignore
                            self.m("Soemthing went wrong here")
                        col_row = ordered_col_cursor.fetchone()
                    self.connection.commit()

    def quick_fetch_table(self
            , table_name, use_comments=True, use_infer=False
            , use_sample_data=False, use_tuple_return=False
            , output_csv=False, output_type="screen", output_name="same"
            , rows="source"):
        table_exist = self.table_exist(table_name)
        if table_exist:
            self.template = BinubuoTemplate()
            self.templateTable = table_name
        else:
            self.logger.error("Table name entered does not exist. templateFromTable can only be used on existing tables.")
            quit()
        # Table exists
        if table_exist:
            quick_fetch_columns_array = []
            if not use_infer:
                # No webservice call to generate template.
                working_cursor = self.connection.cursor()
                generic_column_meta_sql = self.load_resource("sqlserver_column_meta_simple.sql")
                working_cursor.execute(generic_column_meta_sql, (table_name.upper(),table_name.upper(),))
                for cname, cdtype, cdgenerator, ccomment, crows, cnumnulls, cnumdist, cnullable, cavglen in working_cursor:
                    self.template.init_column(column_name=cname, column_type="generated", column_datatype=cdtype)
                    if ccomment is not None and use_comments:
                        quick_fetch_columns_array.append(ccomment)
                    else:
                        quick_fetch_columns_array.append(cdgenerator)
                # Once we are done, we can call the quick fetch.
                quick_fetch_columns = ",".join(quick_fetch_columns_array)
                # Before fetching, set rows if needed.
                if rows == "source":
                    self.drows(self.tableSize(table_name))
                else:
                    try:
                        self.drows(int(rows))
                    except:
                        self.drows()
                if use_tuple_return or output_type.lower() == "table":
                    tuple_value = "tuple"
                else:
                    tuple_value = "list"
                if output_csv:
                    self.csv(1)
                if output_name == "same":
                    output_name_real = table_name
                else:
                    output_name_real = output_name
                if output_type.lower() == "screen" or output_type.lower() == "table":
                    resp_cols = self.quick_fetch(quick_fetch_columns, tuple_value)
                    self.logger.info("Length is: " + str(len(resp_cols)))
                    self.logger.debug(resp_cols)
                    if output_type.lower() == "screen":
                        return resp_cols
                    else:
                        # We need to insert.
                        quick_insert_stmt = self.build_insert_statement(table_name, output_name_real)
                        quick_insert_cursor = self.connection.cursor()
                        # For sqlserver, we need to disable identity insert restriction first
                        tab_schema = self.table_sql_schema(table_name)
                        quick_insert_cursor.execute('set identity_insert '+ tab_schema + '.' + output_name_real + ' on')
                        quick_insert_cursor.executemany(quick_insert_stmt, resp_cols)
                        self.connection.commit()
                        # Re-enable identity insert restriction
                        quick_insert_cursor.execute('set identity_insert '+ tab_schema + '.' + output_name_real + ' off')
                elif output_type.lower() == "file":
                    self.quick_fetch_to_file(quick_fetch_columns, output_name_real)
                # Reset required vals
                self.csv()
                self.drows()

    def dataset_from_table(self, table_name, use_comments=True, use_infer=False, use_sample_data=False):
        dset_template = self.templateFromTable(table_name, use_comments, use_infer, use_sample_data)
        # Create or replace the dataset
        self.create_dataset(table_name, dset_template)

    def build_insert_statement(self, source_table, target_table=None):
        insert_stmt_cursor = self.connection.cursor()
        build_insert_stmt = self.load_resource("sqlserver_build_insert.sql")
        insert_stmt_cursor.execute(build_insert_stmt, (source_table,))
        cursor_result = insert_stmt_cursor.fetchone()
        # For sql server we need the schema
        if target_table is not None:
            tab_schema = self.table_sql_schema(target_table)
            insert_stmt = "insert into " + tab_schema + "." + target_table + " " + cursor_result[0]
        else:
            tab_schema = self.table_sql_schema(source_table)
            insert_stmt = "insert into " + tab_schema + "." + source_table + " " + cursor_result[0]
        insert_stmt = insert_stmt.replace("d_d_s_r", "?")
        self.logger.debug("Insert stmt: " + insert_stmt)
        return insert_stmt

    def table_sql_schema(self, table_name):
        #
        get_schema_stmt_cursor = self.connection.cursor()
        get_schema_stmt = self.load_resource("sqlserver_get_table_schema.sql")
        get_schema_stmt_cursor.execute(get_schema_stmt, (table_name,))
        cursor_result = get_schema_stmt_cursor.fetchone()
        cursor_result = cursor_result[0]
        return cursor_result

    def table_has_identity(self, table_name):
        #
        get_schema_stmt_cursor = self.connection.cursor()
        get_schema_stmt = self.load_resource("sqlserver_table_has_identity.sql")
        get_schema_stmt_cursor.execute(get_schema_stmt, (table_name,))
        cursor_result = get_schema_stmt_cursor.fetchone()
        cursor_result = cursor_result[0]
        return cursor_result

    def table_exist(self, table_name, use_secondary=False):
        if use_secondary and self.connected_secondary:
            use_conn = self.secondary_connection
        else:
            use_conn = self.connection
        assert_table_sql = self.load_resource("sqlserver_assert_table.sql")
        # SOURCE work
        assert_table_cursor = use_conn.cursor()
        self.logger.debug("Before cursor check source")
        table_exist = False
        assert_table_cursor.execute(assert_table_sql, (table_name,))
        cursor_result = assert_table_cursor.fetchone()
        if cursor_result[0] == 1:
            table_exist = True
            self.logger.debug("Source exists")
        else:
            self.logger.info("Source table name entered does not exist. copy_table can only be used on existing tables.")
        return table_exist

    def ddl_from_table(self, table_name, use_secondary=False):
        if use_secondary and self.connected_secondary:
            use_conn = self.secondary_connection
        else:
            use_conn = self.connection
        ddl_cursor = use_conn.cursor()
        ddl_stmt = self.load_resource("sqlserver_table_ddl.sql")
        ddl_cursor.execute(ddl_stmt, (table_name,))
        ddl_out_str = ddl_cursor.fetchone()
        ddl_out_str = ddl_out_str[0]
        return ddl_out_str

    def copy_table(self, source_table, target_table=None, copy_method="quickfetch"
            , drop_target_if_exist=False, alternate_dataset_name=False
            , use_comments=True, use_infer=False, use_sample_data=False
            , data_rows="source", target_db=None):
        if target_db is None:
            target_work_cursor = self.connection.cursor()
        else:
            target_work_cursor = self.secondary_connection.cursor()
        source_table_exist = False
        target_table_exist = True
        self.logger.debug("Before cursor check source")
        working_cursor = self.connection.cursor()
        source_table_exist = self.table_exist(source_table)
        if source_table_exist:
            self.template = BinubuoTemplate()
            self.templateTable = source_table
        else:
            self.logger.error("Source table name entered does not exist. copy_table can only be used on existing tables.")
            quit()
        # If target_table is none, we will create a copy with same name plus '_copy' appended to it.
        if target_table is None:
            loc_target_table = source_table + "_copy"
        else:
            loc_target_table = target_table
        self.m("Create copy [" + loc_target_table + "] of table [" + source_table + "]. Infer=" + str(use_infer) + " Sampledata=" + str(use_sample_data) + ".", tolog=True)
        try:
            if target_db is None:
                target_table_exist = self.table_exist(loc_target_table)
            else:
                target_table_exist = self.table_exist(loc_target_table, True)
            if target_table_exist:
                self.logger.warning("Target table exist cannot create:")
                target_table_exist = True
                if drop_target_if_exist:
                    remove_target_stmt = "drop table " + loc_target_table.lower()
                    self.logger.info("Dropping target with stmt: " + remove_target_stmt)
                    target_work_cursor.execute(remove_target_stmt)
                    if target_db is None:
                        self.connection.commit()
                    else:
                        self.secondary_connection.commit()
                    target_table_exist = False
            else:
                self.logger.info("Target table does not exist.")
                target_table_exist = False
        except:
            target_table_exist = False
        self.logger.debug("Just before main continue check")
        if source_table_exist and not target_table_exist:
            # Source is there and target is not there. Good to go.
            # First we create an empty copy table
            tab_schema = self.table_sql_schema(source_table)
            if target_db is None:
                table_ddl = "select * into " + tab_schema + "." + loc_target_table.lower() + " from " + tab_schema + "."  + source_table.lower() + " where 1=2"
            else:
                table_ddl = self.ddl_from_table(source_table)
                # Replace with target
                table_ddl = table_ddl.replace('.' + source_table.lower() + ' ', '.' + loc_target_table.lower() + ' ')
            self.logger.debug("Create table stmt: " + table_ddl)
            target_work_cursor.execute(table_ddl)
            if target_db is None:
                self.connection.commit()
            else:
                self.secondary_connection.commit()
            # Table created. Build insert stmt
            insert_stmt = self.build_insert_statement(source_table, loc_target_table)
            # Set the rows
            if data_rows == "source":
                # Get the rowcount in the source table.
                self.drows(self.tableSize(source_table))
            else:
                try:
                    self.drows(int(data_rows))
                except:
                    self.drows(int(10))
            # Get new rows.
            if copy_method == "quickfetch":
                rows_bind = self.quick_fetch_table(table_name=source_table, use_tuple_return=True)
                self.logger.info("Rows returned for insert: " + str(len(rows_bind)))
                tab_schema = self.table_sql_schema(loc_target_table)
                target_work_cursor.execute('set identity_insert '+ tab_schema + '.' + loc_target_table + ' on')
                target_work_cursor.executemany(insert_stmt, rows_bind)
                target_work_cursor.execute('set identity_insert '+ tab_schema + '.' + loc_target_table + ' off')
                if target_db is None:
                    self.connection.commit()
                else:
                    self.secondary_connection.commit()
            elif copy_method == "dataset":
                if not alternate_dataset_name:
                    # Expect dataset name to be same as source table.
                    dset_name = source_table
                else:
                    dset_name = alternate_dataset_name
                # Create the dataset, if it does not exist
                if not self.dataset_exists(dset_name):
                    self.dataset_from_table(dset_name, use_comments, use_infer, use_sample_data)
                # Call the dataset for the rows.
                rows_bind = self.dataset(dataset_name=dset_name, response_type="tuple")
                if rows_bind is not None:
                    self.logger.info("Rows returned for insert: " + str(len(rows_bind)))
                    tab_schema = self.table_sql_schema(loc_target_table)
                    target_work_cursor.execute('set identity_insert '+ tab_schema + '.' + loc_target_table + ' on')
                    target_work_cursor.executemany(insert_stmt, rows_bind)
                    target_work_cursor.execute('set identity_insert '+ tab_schema + '.' + loc_target_table + ' off')
                if target_db is None:
                    self.connection.commit()
                else:
                    self.secondary_connection.commit()
                self.m("Synthetic table [" + loc_target_table +"] successfully created.", indent=True, tolog=False)

    def insert_from_dataset(self, dataset_name, table_name
        , data_rows="source", category="custom", **webargs):
        table_exist = self.table_exist(table_name)
        do_insert = False
        if table_exist:
            if data_rows == "source":
                # Get the rowcount in the source table.
                self.drows(self.tableSize(table_name))
            else:
                try:
                    self.drows(int(data_rows))
                except:
                    self.drows(int(10))
            # Create cursor and insert statement
            insert_cursor = self.connection.cursor()
            insert_stmt = self.build_insert_statement(table_name)
            if category == "custom":
                if self.dataset_exists(dataset_name):
                    # Custom dataset does not exists
                    rows_bind = self.dataset(dataset_name=dataset_name, response_type="tuple", **webargs)
                    do_insert = True
                elif self.standard_dataset_exists(dataset_name) is not None and self.binubuo_config['DATABASE']['use_standard_datasets_as_source'] == 'yes':
                    if self.binubuo_config.get('DATABASE', 'use_standard_category_if_duplicate', fallback=None) is None:
                        std_dataset_cat = self.standard_dataset_exists(dataset_name)
                    else:
                        std_dataset_cat = self.binubuo_config.get('DATABASE', 'use_standard_category_if_duplicate')
                    rows_bind = self.dataset(dataset_name=dataset_name, dataset_type="standard", dataset_category=std_dataset_cat, response_type="tuple", **webargs)
                    do_insert = True
                else:
                    self.logger.error("Dataset does not exist. Unable to insert.")
            else:
                if self.standard_dataset_exists(dataset_name, category).upper() == category.upper():
                    # We can do standard fetch
                    rows_bind = self.dataset(dataset_name=dataset_name, dataset_type="standard", dataset_category=category, response_type="tuple", **webargs)
                    do_insert = True
                else:
                    self.logger.error("Dataset does not exist. Unable to insert.")
            if do_insert and rows_bind is not None:
                self.logger.info("Rows returned for insert: " + str(len(rows_bind)))
                tab_schema = self.table_sql_schema(table_name)
                has_ident = self.table_has_identity(table_name)
                if has_ident == 1:
                    insert_cursor.execute('set identity_insert '+ tab_schema + '.' + table_name + ' on')
                insert_cursor.executemany(insert_stmt, rows_bind)
                if has_ident == 1:
                    insert_cursor.execute('set identity_insert '+ tab_schema + '.' + table_name + ' off')
                self.connection.commit()
        else:
            self.logger.error("Table does not exist. Unable to insert.")

    def table_sample(self, table_name):
        # Print title
        print("**************************************************************************")
        print("** Table data sample: " + table_name.upper())
        print("**************************************************************************")
        # Get header data
        headers = []
        headers_trimmed = []
        headers_deco = []
        header_stmt = self.load_resource("sqlserver_columns_ordered.sql")
        working_cursor = self.connection.cursor()
        working_cursor.execute(header_stmt, (table_name,))
        for cname in working_cursor:
            headers.append(cname[0])
            headers_trimmed.append(cname[0][0:14])
        row_format = "{:>15}" * (len(headers))
        for x in range (len(headers)):
            headers_deco.append(" ==============")
        print(row_format.format(*headers_trimmed))
        print(row_format.format(*headers_deco))
        tab_schema = self.table_sql_schema(table_name)
        sample_stmt = self.load_resource("sqlserver_sample_select.sql").format(r_limit = '3', r_rows = ','.join(headers), r_schema = tab_schema, r_table = table_name)
        working_cursor.execute(sample_stmt)
        for rows in working_cursor:
            row_data = []
            for col_data in rows:
                row_data.append(str(col_data)[0:14])
            print(row_format.format(*row_data))

    def compare_table_to_dataset(self, table_name, dataset_name):
        self.table_sample(table_name)
        self.dataset_sample(dataset_name)

    def build_schema_dataset(self, schema_name, use_comments=True, use_infer=False, use_sample_data=False, alternate_setname=None):
        self.m("Create API dataset for schema [" + schema_name + "]. Infer=" + str(use_infer) + " Sampledata=" + str(use_sample_data) + ".", tolog=True)
        # Prepare object for superset JSON registration
        superset_json = {}
        if not alternate_setname:
            superset_json["Setname"] = schema_name
        else:
            superset_json["Setname"] = alternate_setname
        superset_json["tables"] = []
        # Grab the tables in the correct order.
        working_cursor = self.connection.cursor()
        hierachy_stmt = self.load_resource("sqlserver_table_hierachy_schema.sql")
        all_rows = working_cursor.execute(hierachy_stmt).fetchall()
        for tabschema, tab, dependson, level in all_rows:
            # No matter if we have an existing dataset or not
            # We need to add to the superset
            table_def = {}
            table_def["table_name"] = tab
            table_def["table_level"] = level
            table_def["table_size"] = self.tableSize(tab)
            # Add dependents for size ratio calculations
            an_array = []
            depends_cursor = self.connection.cursor()
            depends_stmt = self.load_resource("sqlserver_foreign_key_depends.sql")
            depends_cursor.execute(depends_stmt, (tab,))
            for dep_tab in depends_cursor:
                an_object = {}
                an_object["local_col"] = dep_tab[2]
                an_object["remote_dataset"] = dep_tab[0]
                an_object["remote_col"] = dep_tab[1]
                an_array.append(an_object)    
            table_def["depends_on"] = an_array
            superset_json["tables"].append(table_def)
            if not self.dataset_exists(tab):
                self.logger.info("Building dataset for [%s] at level [%s].", tab, level)
                self.dataset_from_table(tab, use_comments, use_infer, use_sample_data)
            else:
                self.logger.info("Dataset for [%s] already exists", tab)
        # Now we have the whoel superset. Ship and create
        # TODO: Send to superset register service.
        self.logger.info("Superset data to store: %s", json.dumps(superset_json))
        superset_result = self.create_superset(json.dumps(superset_json))
        self.m("API dataset for schema [" + schema_name + "] successfully created.", tolog=True)

    def table_from_dataset(self, dataset_name, table_name=None, rows=0, category="custom", **webargs):
        self.m("Create table from dataset [" + dataset_name + "]. Number of rows=" + str(rows) + ".", tolog=True)
        self.logger.debug("Table from dataset using category: %s", category)
        # First we make sure that we have an up-to-date cache of datasets and metadata
        self.list_datasets(1)
        # Set the do_build
        do_build = False
        # Set the use standard
        use_standard = False
        # Now check if the dataset exists
        if category == "custom":
            if self.dataset_exists(dataset_name):
                do_build = True
            elif self.standard_dataset_exists(dataset_name) is not None and self.binubuo_config['DATABASE']['use_standard_datasets_as_source'] == 'yes':
                do_build = True
                use_standard = True
            else:
                self.m("Error: Dataset [" + dataset_name + "] does not exist.", tolog=True)
        else:
            if self.standard_dataset_exists(dataset_name, category).upper() == category.upper():
                do_build = True
                use_standard = True
            else:
                self.m("Error: Dataset [" + dataset_name + "] does not exist.", tolog=True)
        if do_build:
            if table_name is None:
                table_name_set = dataset_name
            else:
                table_name_set = table_name
            # Now check if the table exists
            if self.table_exist(table_name_set):
                self.logger.warning("Table [%s] does already exist. Either change name of requested table or drop existing.", table_name_set)
                # Here we should do "if allow drop, then drop"
            else:
                self.logger.info("About to create table [%s] from dataset definition", table_name_set)
                for idx, val in enumerate(self.dict_cache['datasets']):
                    for key, value in val.items():
                        if use_standard:
                            if key == "DATASET_WEBSERVICE_NAME" and value.lower() == dataset_name.lower():
                                if category == "custom":
                                    if self.dict_cache['datasets'][idx]["DATASET_TYPE_NAME"] == "Standard Dataset":
                                        dataset_cols = self.dict_cache['datasets'][idx]["DATASET_COLS"]
                                else:
                                    if self.dict_cache['datasets'][idx]["DATASET_TYPE_NAME"] == "Standard Dataset" and self.dict_cache['datasets'][idx]["DATASET_CATEGORY_NAME"].upper() == category.upper():
                                        dataset_cols = self.dict_cache['datasets'][idx]["DATASET_COLS"]
                        else:
                            if key == "DATASET_WEBSERVICE_NAME" and value.lower() == dataset_name.lower():
                                dataset_cols = self.dict_cache['datasets'][idx]["DATASET_COLS"]
                self.logger.info("Columns found for create table: %s", str(len(dataset_cols)))
                create_table_stmt = "create table dbo." + table_name_set + " ("
                # Oracle datatype translation dictionary
                translation_dict = {'string': 'nvarchar(4000)'
                    , 'time': 'datetime'
                    , 'text': 'nvarchar(max)'
                    , 'number': 'numeric(18,2)'}
                # loop over all columns and create the ddl for the table.
                cols_translated = []
                for idx, val in enumerate(dataset_cols):
                    trsl_datatype = dataset_cols[idx]["COL_DATATYPE"]
                    self.logger.debug("Add column [%s] of type [%s]", dataset_cols[idx]["COL_NAME"], trsl_datatype)
                    for word, replacement in translation_dict.items():
                        trsl_datatype = trsl_datatype.replace(word, replacement)
                    cols_translated.append(dataset_cols[idx]["COL_NAME"].lower() + " " + trsl_datatype)
                # Now all columns are done. Add to the statement
                all_cols = ','.join(cols_translated)
                create_table_stmt = create_table_stmt + all_cols + ")"
                self.logger.debug("Creating table: %s", create_table_stmt)
                working_cursor = self.connection.cursor()
                working_cursor.execute(create_table_stmt)
                self.connection.commit()
                self.m("Table " + table_name_set + " from dataset [" + dataset_name + "] created successfully.", tolog=True)
                try:
                    if rows > 0:
                        self.insert_from_dataset(dataset_name, table_name_set, rows, category, **webargs)
                except:
                    self.logger.debug("Either zero rows supplied or rows parameter not a number.")