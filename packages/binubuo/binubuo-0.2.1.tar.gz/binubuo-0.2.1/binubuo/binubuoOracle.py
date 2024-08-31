import cx_Oracle
import sys
import json
import ast
import logging
from binubuo import binubuo
from binubuo.BinubuoTemplate import BinubuoTemplate

class binubuoOracle(binubuo):
    def __init__(self, binubuokey, dbuser, dbpwd, dbdsn, dbconfig=None, dbfullConnection=None):
        super().__init__(binubuokey)
        self.binubuokey = binubuokey
        self.dbuser = dbuser
        self.dbpwd = dbpwd
        self.dbdsn = dbdsn
        self.dbconfig = dbconfig
        self.dbfullConnection = dbfullConnection
        self.max_sample_size = 100
        self.connected = False
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
                if self.dbconfig is not None:   
                    cx_Oracle.init_oracle_client(config_dir=self.dbconfig)
                self.connection = cx_Oracle.connect(user=self.dbuser, password=self.dbpwd, dsn=self.dbdsn)
            else:
                self.connection = self.dbfullConnection
            self.connected = True
            # Set defaults
            working_cursor = self.connection.cursor()
            stmt = self.load_resource("oracle_nls_date_format.sql")
            self.logger.info(stmt)
            working_cursor.execute(stmt)
            stmt = self.load_resource("oracle_nls_timestamp_format.sql")
            self.logger.info(stmt)
            working_cursor.execute(stmt)
            stmt = self.load_resource("oracle_nls_timestamp_tz_format.sql")
            self.logger.info(stmt)
            working_cursor.execute(stmt)
        except:
            self.logger.error("Error: Failed to connect to database. Please make sure you have a connection before using other methods.")
            self.connection = None

    def connectSecondary(self, dbuser, dbpwd, dbdsn, dbconfig=None, dbfullConnection=None):
        try:
            if dbfullConnection is None:
                if dbconfig is not None:
                    try: 
                        cx_Oracle.init_oracle_client(config_dir=dbconfig)
                    except:
                        # If Client Library already loaded (with the primary connection) ignore the error here
                        pass
                self.secondary_connection = cx_Oracle.connect(user=dbuser, password=dbpwd, dsn=dbdsn)
            else:
                self.secondary_connection = dbfullConnection
            self.connected_secondary = True
            working_cursor = self.secondary_connection.cursor()
            stmt = self.load_resource("oracle_nls_date_format.sql")
            self.logger.info(stmt)
            working_cursor.execute(stmt)
            stmt = self.load_resource("oracle_nls_timestamp_format.sql")
            self.logger.info(stmt)
            working_cursor.execute(stmt)
            stmt = self.load_resource("oracle_nls_timestamp_tz_format.sql")
            self.logger.info(stmt)
            working_cursor.execute(stmt)
        except:
            self.logger.error("Error: Failed to connect to secondary/alternate database. Please check your connection details and try again.")
            self.secondary_connection = None

    def calculateSampleSize(self, table_name):
        sub_sample_cursor = self.connection.cursor()
        sub_sample_size_stmt = self.load_resource("oracle_table_rows.sql")
        sub_sample_cursor.execute(sub_sample_size_stmt, tabname = table_name.upper())
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
        table_size_size_stmt = self.load_resource("oracle_table_rows.sql")
        table_size_cursor.execute(table_size_size_stmt, tabname = table_name.upper())
        table_size_size_cal = table_size_cursor.fetchone()
        table_size_size_cal = table_size_size_cal[0]
        self.logger.info("Table size of %s is %s rows.", table_name, str(table_size_size_cal))
        return table_size_size_cal

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
                generic_column_meta_sql = self.load_resource("oracle_column_meta_simple.sql")
                working_cursor.execute(generic_column_meta_sql, tabname = table_name.upper())
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
                    columns_meta_stmt = self.load_resource("oracle_column_meta_plus_sample.sql")
                else:
                    columns_meta_stmt = self.load_resource("oracle_column_meta_plus_standard.sql")
                self.logger.debug("Statement to get column data: %s", columns_meta_stmt)
                working_cursor.execute(columns_meta_stmt, tabname = table_name.upper())
                for col_name, col_infer_meta in working_cursor:
                    self.logger.info("Column to infer: %s", col_name)
                    # If we are allowed sample data. Now is the time to fetch individual samples
                    if use_sample_data:
                        self.m("Sampling data on column [" + col_name +"].", indent=True, tolog=False)
                        sub_sample_cursor = self.connection.cursor()
                        # Merge the sample data.
                        # First parse the main column metadata
                        main_meta = json.loads(col_infer_meta)
                        sub_sample_stmt = self.load_resource("oracle_column_sample_data.sql").format(r_col_name=col_name, r_table_name=table_name, r_table_sample_size=sub_sample_size_cal_cust)
                        self.logger.debug("Statement to get column (%s) sample data: %s", col_name, sub_sample_stmt)
                        sub_sample_cursor.execute(sub_sample_stmt)
                        sample_data = sub_sample_cursor.fetchone()
                        # First we get the sample data as a clob string
                        sample_data_clob_str = sample_data[0].read()
                        # Convert to a list so we can add for real.
                        sample_data_clob_str = ast.literal_eval(sample_data_clob_str)
                        # Now add the sample data as a real array.
                        main_meta["sample_values"] = sample_data_clob_str
                        if main_meta["column_is_reference"] == 1:
                            self.m("Column [" + col_name +"] is foreign key. Create key distribution histogram.", indent=True, tolog=False)
                            rel_sample_size_cal_cust = self.calculateSampleSize(main_meta["reference_table"])
                            rel_sample_cursor = self.connection.cursor()
                            rel_sample_stmt = self.load_resource("oracle_foreign_key_histogram.sql").format(col_name = main_meta["column_name"], tab_name = table_name, ref_col_name = main_meta["reference_column"], ref_tab_name = main_meta["reference_table"], ref_sample = rel_sample_size_cal_cust)
                            self.logger.info("Column is a foreign key. Build relation histogram")
                            self.logger.debug("Relation histogram query: %s", rel_sample_stmt)
                            rel_sample_cursor.execute(rel_sample_stmt)
                            rel_sample_data = rel_sample_cursor.fetchone()
                            self.logger.debug("Foreign key histogram: ")
                            rel_sample_data_clob_str = rel_sample_data[0].read()
                            self.logger.debug(rel_sample_data_clob_str)
                            rel_sample_data_clob_str = ast.literal_eval(rel_sample_data_clob_str)
                            main_meta["reference_histogram"] = rel_sample_data_clob_str
                    else:
                        main_meta = json.loads(col_infer_meta)
                    # We now have every column and its metadata. Send to API endpoint to do intelligent infer.
                    # We get back the entire json of inferred column
                    # Init column
                    table_template.init_column(column_name=col_name)
                    # Try calling infer endpoint
                    self.logger.info("Infer: %s", json.dumps(main_meta))
                    x_response = self.infer_generator(json.dumps(main_meta))
                    self.logger.info(x_response)
                    # The response is the column json as a string format. Call replace_column_from_json
                    table_template.replace_column_from_json(col_name, json.dumps(x_response))
                self.m("Template for table [" + table_name +"] successfully created.", indent=True, tolog=False)
                # Once we are done, we can validate the template and return it.
                if output_type.upper() == "JSON":
                    table_template.validate_template()
                    table_template.complete_template()
                    return table_template.template_JSON
                else:
                    return table_template

    def columnGeneratorComments(self, table_name, comments, override=False):
        self.m("Create comments on table [" + table_name + "]. Comments=" + str(comments) + ".", tolog=True)
        if self.connected:
            comment_count_sql = self.load_resource("oracle_count_comments.sql")
            working_cursor = self.connection.cursor()
            working_cursor.execute(comment_count_sql, tabname = table_name.upper())
            cursor_result = working_cursor.fetchone()
            if (cursor_result[0] > 0 or not override) or (cursor_result[0] == 0):
                # Let us go ahead and set comment generators as requested.
                if (comments.find('=') > 0):
                    # Named notation
                    for cn in comments.split(","):
                        colname = cn.split("=")[0].strip()
                        colcomment = cn.split("=")[1].strip()
                        col_add_stmt = "comment on column " + table_name + "." + colname + " is '" + colcomment + "'"
                        working_cursor.execute(col_add_stmt)
                else:
                    # Just split and follow column order. Ignore any column outside of split length
                    ordered_col_cursor = self.connection.cursor()
                    ordered_col_sql = self.load_resource("oracle_comments_ordered.sql")
                    ordered_col_cursor.execute(ordered_col_sql, tabname = table_name.upper())
                    for cid, cname in ordered_col_cursor:
                        try:
                            colcomment = comments.split(",")[cid - 1]
                            col_add_stmt = "comment on column " + table_name + "." + cname + " is '" + colcomment + "'"
                            working_cursor.execute(col_add_stmt)
                        except:
                            # Aint no comment for this column. Just ignore
                            pass
                self.m("Comments for table [" + table_name +"] successfully created.", indent=True, tolog=False)

    def quick_fetch_table(self
            , table_name, use_comments=True, use_infer=False
            , use_sample_data=False, use_tuple_return=False
            , output_csv=False, output_type="screen", output_name="same"
            , rows="source"):
        self.template = BinubuoTemplate()
        table_exist = self.table_exist(table_name)
        # Table exists
        if table_exist:
            quick_fetch_columns_array = []
            if not use_infer:
                # No webservice call to generate template.
                working_cursor = self.connection.cursor()
                generic_column_meta_sql = self.load_resource("oracle_column_meta_simple.sql")
                working_cursor.execute(generic_column_meta_sql, tabname = table_name.upper())
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
                    self.logger.info("Length is: %s", str(len(resp_cols)))
                    self.logger.info(resp_cols)
                    if output_type.lower() == "screen":
                        return resp_cols
                    else:
                        # We need to insert.
                        quick_insert_stmt = self.build_insert_statement(table_name, output_name_real)
                        quick_insert_cursor = self.connection.cursor()
                        bulk_limit = int(self.binubuo_config.get('DATABASE', 'oracle_bulk_size', fallback='400'))
                        if len(resp_cols) < bulk_limit:
                            # One execute
                            self.logger.info("Bulk limit [%s] is higher than actual row count [%s]. No need to split executemany.", str(bulk_limit), str(len(resp_cols)))
                            quick_insert_cursor.executemany(quick_insert_stmt, resp_cols)
                            self.logger.info("Rows inserted: %s", str(len(resp_cols)))
                        else:
                            # Split up to smaller parts
                            self.logger.info("Bulk limit [%s] is lower than actual row count [%s]. Split to multiple executemany.", str(bulk_limit), str(len(resp_cols)))
                            splitted_arrays = [resp_cols[i:i+bulk_limit] for i in range(0, len(resp_cols), bulk_limit)]
                            for bulks in splitted_arrays:
                                quick_insert_cursor.executemany(quick_insert_stmt, bulks)
                                self.logger.info("Rows inserted: %s", str(len(bulks)))
                        self.connection.commit()
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
        build_insert_stmt = self.load_resource("oracle_build_insert.sql")
        insert_stmt_cursor.execute(build_insert_stmt, tabname=source_table.upper())
        cursor_result = insert_stmt_cursor.fetchone()
        if target_table is not None:
            insert_stmt = "insert into " + target_table.lower() + " " + cursor_result[0]
        else:
            insert_stmt = "insert into " + source_table.lower() + " " + cursor_result[0]
        self.logger.debug("Insert stmt: %s", insert_stmt)
        return insert_stmt

    def table_exist(self, table_name, use_secondary=False):
        if use_secondary and self.connected_secondary:
            use_conn = self.secondary_connection
        else:
            use_conn = self.connection
        assert_table_sql = self.load_resource("oracle_assert_table.sql")
        # SOURCE work
        assert_table_cursor = use_conn.cursor()
        table_exist = False
        try:
            assert_table_cursor.execute(assert_table_sql, tabname = table_name.upper())
            table_exist = True
            self.logger.info("Table %s asserted and it exists", table_name)
        except:
            table_exist = False
            self.logger.warning("Table %s asserted and it does not exists", table_name)
        return table_exist

    def ddl_from_table(self, table_name):
        ddl_cursor = self.connection.cursor()
        ddl_stmt = self.load_resource("oracle_prepare_dbms_metadata.sql")
        # Set the transformation rules for DDL extraction.
        ddl_cursor.execute(ddl_stmt)
        # Extract DDL
        ddl_stmt = self.load_resource("oracle_table_ddl.sql")
        ddl_cursor.execute(ddl_stmt, tabname = table_name.upper())
        ddl_out_str = ddl_cursor.fetchone()
        ddl_out_str = ddl_out_str[0].read()
        return ddl_out_str

    def copy_table(self, source_table, target_table=None, copy_method="quickfetch"
            , drop_target_if_exist=False, alternate_dataset_name=False
            , use_comments=True, use_infer=False, use_sample_data=False
            , data_rows="source", target_db=None):
        working_cursor = self.connection.cursor()
        if target_db is None:
            target_work_cursor = self.connection.cursor()
        else:
            target_work_cursor = self.secondary_connection.cursor()
        source_table_exist = self.table_exist(source_table)
        # TARGET work
        # If target_table is none, we will create a copy with same name plus '_copy' appended to it.
        if target_table is None:
            loc_target_table = source_table + "_copy"
        else:
            loc_target_table = target_table
        self.m("Create copy [" + loc_target_table + "] of table [" + source_table + "]. Infer=" + str(use_infer) + " Sampledata=" + str(use_sample_data) + ".", tolog=True)
        target_table_exist = self.table_exist(loc_target_table) if target_db is None else self.table_exist(loc_target_table, True)
        if target_table_exist:
            if drop_target_if_exist:
                remove_target_stmt = "drop table " + loc_target_table.lower() + " purge"
                self.logger.debug("Dropping target %s with stmt: %s", loc_target_table, remove_target_stmt)
                target_work_cursor.execute(remove_target_stmt)
                target_table_exist = False
            else:
                self.logger.error("Target table exist cannot create.")
        if source_table_exist and not target_table_exist:
            # Source is there and target is not there. Good to go.
            # First we create an empty copy table
            # If local database we can use create as select ...
            # If secondary database, we do extract DDL
            if target_db is None:
                table_ddl = "create table " + loc_target_table.lower() + " as select * from " + source_table.lower() + " where 1=2"
            else:
                # We need to extract from primary the stmt to build in secondary
                table_ddl = self.ddl_from_table(source_table.upper())
                # Now we just need to replace tablename, since the DDL will be source table name
                table_ddl = table_ddl.replace('"' + source_table.upper() + '"', '"' + loc_target_table.upper() + '"')
            self.logger.debug("Create table stmt: %s", table_ddl)
            target_work_cursor.execute(table_ddl)
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
                if rows_bind is not None:
                    self.logger.info("Rows returned for insert: %s", str(len(rows_bind)))
                    target_work_cursor.executemany(insert_stmt, rows_bind)
            elif copy_method == "dataset":
                dset_name = source_table if not alternate_dataset_name else alternate_dataset_name
                if not self.dataset_exists(dset_name):
                    self.dataset_from_table(dset_name, use_comments, use_infer, use_sample_data)
                # Call the dataset for the rows.
                rows_bind = self.dataset(dataset_name=dset_name, response_type="tuple")
            # Insert the rows
            if rows_bind is not None:
                self.logger.info("Rows returned for insert: %s", str(len(rows_bind)))
                bulk_limit = int(self.binubuo_config.get('DATABASE', 'oracle_bulk_size', fallback='400'))
                if len(rows_bind) < bulk_limit:
                    # One execute
                    self.logger.info("Bulk limit [%s] is higher than actual row count [%s]. No need to split executemany.", str(bulk_limit), str(len(rows_bind)))
                    target_work_cursor.executemany(insert_stmt, rows_bind)
                    self.logger.info("Rows inserted: %s", str(len(rows_bind)))
                else:
                    # Split up to smaller parts
                    self.logger.info("Bulk limit [%s] is lower than actual row count [%s]. Split to multiple executemany.", str(bulk_limit), str(len(rows_bind)))
                    splitted_arrays = [rows_bind[i:i+bulk_limit] for i in range(0, len(rows_bind), bulk_limit)]
                    for bulks in splitted_arrays:
                        target_work_cursor.executemany(insert_stmt, bulks)
                        self.logger.info("Rows inserted: %s", str(len(bulks)))
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
                self.logger.info("Rows returned for insert: %s", str(len(rows_bind)))
                bulk_limit = int(self.binubuo_config.get('DATABASE', 'oracle_bulk_size', fallback='400'))
                if len(rows_bind) < bulk_limit:
                    # One execute
                    self.logger.info("Bulk limit [%s] is higher than actual row count [%s]. No need to split executemany.", str(bulk_limit), str(len(rows_bind)))
                    insert_cursor.executemany(insert_stmt, rows_bind)
                    self.logger.info("Rows inserted: %s", str(len(rows_bind)))
                else:
                    # Split up to smaller parts
                    self.logger.info("Bulk limit [%s] is lower than actual row count [%s]. Split to multiple executemany.", str(bulk_limit), str(len(rows_bind)))
                    splitted_arrays = [rows_bind[i:i+bulk_limit] for i in range(0, len(rows_bind), bulk_limit)]
                    for bulks in splitted_arrays:
                        insert_cursor.executemany(insert_stmt, bulks)
                    self.logger.info("Rows inserted: %s", str(len(bulks)))
                self.connection.commit()
        else:
            self.logger.warning("Table does not exist. Unable to insert.")

    def table_sample(self, table_name):
        # Print title
        print("**************************************************************************")
        print("** Table data sample: " + table_name.upper())
        print("**************************************************************************")
        # Get header data
        headers = []
        headers_trimmed = []
        headers_deco = []
        header_stmt = self.load_resource("oracle_columns_ordered.sql")
        working_cursor = self.connection.cursor()
        working_cursor.execute(header_stmt, tabname = table_name.upper())
        for cname in working_cursor:
            headers.append(cname[0])
            headers_trimmed.append(cname[0][0:14])
        row_format = "{:>15}" * (len(headers))
        for x in range (len(headers)):
            headers_deco.append(" ==============")
        print(row_format.format(*headers_trimmed))
        print(row_format.format(*headers_deco))
        sample_stmt = self.load_resource("oracle_sample_select.sql").format(r_rows = ','.join(headers), r_table = table_name, r_limit = '3')
        working_cursor.execute(sample_stmt)
        for rows in working_cursor:
            row_data = []
            for col_data in rows:
                row_data.append(str(col_data)[0:14])
            print(row_format.format(*row_data))

    def compare_table_to_dataset(self, table_name, dataset_name):
        self.table_sample(table_name)
        self.dataset_sample(dataset_name)

    def build_schema_dataset(self, schema_name=None, use_comments=True, use_infer=False, use_sample_data=False, alternate_setname=None):
        # Prepare object for superset JSON registration
        working_cursor = self.connection.cursor()
        if schema_name is None:
            user_stmt = self.load_resource("oracle_current_user.sql")
            working_cursor.execute(user_stmt)
            for user in working_cursor:
                schema_name_set = user[0]
        superset_json = {}
        if not alternate_setname:
            superset_json["Setname"] = schema_name_set
        else:
            superset_json["Setname"] = alternate_setname
        self.m("Create API dataset for schema [" + schema_name_set + "]. Infer=" + str(use_infer) + " Sampledata=" + str(use_sample_data) + ".", tolog=True)
        superset_json["tables"] = []
        # Grab the tables in the correct order.
        hierachy_stmt = self.load_resource("oracle_table_hierachy_schema.sql")
        working_cursor.execute(hierachy_stmt)
        for tab, dependson, level in working_cursor:
            # No matter if we have an existing dataset or not
            # We need to add to the superset
            table_def = {}
            table_def["table_name"] = tab
            table_def["table_level"] = level
            table_def["table_size"] = self.tableSize(tab)
            # Add dependents for size ratio calculations
            an_array = []
            depends_cursor = self.connection.cursor()
            depends_stmt = self.load_resource("oracle_foreign_key_depends.sql")
            depends_cursor.execute(depends_stmt, tabname = tab.upper())
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
        self.m("API dataset for schema [" + schema_name_set + "] successfully created.", tolog=True)

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
                create_table_stmt = "create table " + table_name_set + " ("
                # Oracle datatype translation dictionary
                translation_dict = {'string': 'varchar2(4000)'
                    , 'time': 'timestamp'
                    , 'text': 'clob'}
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
                self.m("Table " + table_name_set + " from dataset [" + dataset_name + "] created successfully.", tolog=True)
                try:
                    if rows > 0:
                        self.insert_from_dataset(dataset_name, table_name_set, rows, category, **webargs)
                except:
                    self.logger.debug("Either zero rows supplied or rows parameter not a number.")

    def create_schema_dataset(self, schema_name, scale=1, create_tables=True
        , create_copy=False, create_copy_suffix="_copy", data_tag="same_data"):
        self.m("Create superset from schema [" + schema_name + "]. At scale=" + str(scale) + ".", tolog=True)
        # If current tag is not null keep it, else set and reset back to none after.
        reset_tag = False
        if self.tag_set is None:
            self.tag(data_tag)
            reset_tag = True
        table_copies = []
        # First get the superset metadata
        superset = self.get_superset(schema_name, scale)
        # Get a session id and set it.
        session_id = self.create_session()
        session_id = session_id["bsession"]
        self.session_id(session_id)
        # Find out what type we are building
        superset_category = superset['settype'].lower()
        self.logger.debug("Category for superset: %s", superset_category)
        # Then traverse the datasets in order
        for idx, val in enumerate(superset['datasets']):
            dataset_name = superset['datasets'][idx]["dataset_name"]
            dataset_rows = superset['datasets'][idx]["scaled_size"]
            self.logger.info("Building dataset %s", dataset_name)
            # Build kwargs array for dataset
            dataset_kwargs = {}
            #if "dataset_inputs" in superset['datasets'][idx]:
            #    for idx2, val2 in enumerate(superset['datasets'][idx]["dataset_inputs"]):
            #        dataset_kwargs[superset['datasets'][idx]["dataset_inputs"][idx2]["input_id_name"]] = superset['datasets'][idx]["dataset_inputs"][idx2]["input_id_value"]
            if create_tables:
                if self.table_exist(dataset_name):
                    table_copies.append(dataset_name)
                    self.logger.debug("Adding %s to copy list for constraint replacement", dataset_name)
                    copy_name = dataset_name + create_copy_suffix
                    if create_copy and not self.table_exist(copy_name):
                        self.table_from_dataset(dataset_name=dataset_name, table_name=copy_name, rows=dataset_rows, category=superset_category)
                    else:
                        self.logger.warning("Failed to create copy table [%s] because copy table already exists", copy_name)
                else:
                    self.table_from_dataset(dataset_name=dataset_name, rows=dataset_rows, category=superset_category)
        # Now all datasets are tables. Let us add unqiue keys
        if create_tables:
            working_cursor = self.connection.cursor()
            # Add unqiue keys
            self.m("Adding primary keys.", True)
            for idx, val in enumerate(superset['unique keys']):
                exec_stmt = val.lower()
                self.logger.debug("Original constraint stmt: %s", exec_stmt)
                for x_val in table_copies:
                    fstr = "table " + x_val.lower() + " add"
                    self.logger.debug("Check if %s exists in %s", fstr, exec_stmt)
                    if exec_stmt.find(fstr) > 0:
                        # Replace val
                        exec_stmt = exec_stmt.replace(fstr, "table " + x_val.lower() + create_copy_suffix + " add")
                        exec_stmt = exec_stmt.replace(" unique", create_copy_suffix + " unique")
                self.logger.debug("Adding unique key: %s", exec_stmt)
                working_cursor.execute(exec_stmt)
            # Add foreign keys
            self.m("Adding foreign keys.", True)
            for idx, val in enumerate(superset['foreign keys']):
                exec_stmt = val.lower()
                for x_val in table_copies:
                    fstr1 = "table " + x_val.lower() + " add"
                    if exec_stmt.find(fstr1) > 0:
                        # Replace val
                        exec_stmt = exec_stmt.replace(fstr1, "table " + x_val.lower() + create_copy_suffix + " add")
                        exec_stmt = exec_stmt.replace(" foreign", create_copy_suffix + " foreign")
                    fstr2 = "references " + x_val.lower()
                    if exec_stmt.find(fstr2) > 0:
                        # Replace val
                        exec_stmt = exec_stmt.replace(fstr2, "references " + x_val.lower() + create_copy_suffix)
                self.logger.debug("Adding foreign key: %s", exec_stmt)
                try:
                    working_cursor.execute(exec_stmt)
                except:
                    self.logger.debug("Failed to add foreign key - %s", exec_stmt)
        if reset_tag:
            self.tag()
        session_id = self.remove_session()
        self.m("Superset from schema [" + schema_name + "] created successfully.", tolog=True)