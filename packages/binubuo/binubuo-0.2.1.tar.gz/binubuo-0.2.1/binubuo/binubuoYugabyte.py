import psycopg2
import json
import logging
from binubuo import binubuo
from binubuo.BinubuoTemplate import BinubuoTemplate

class binubuoYugabyte(binubuo):
    def __init__(self, binubuokey, dbname=None, dbuser=None, dbpwd=None, dbfullConnection=None):
        super().__init__(binubuokey)
        self.binubuokey = binubuokey
        self.dbuser = dbuser
        self.dbpwd = dbpwd
        self.dbname = dbname
        self.dbfullConnection = dbfullConnection
        self.max_sample_size = 100
        self.connected = False
        self.binuObj = binubuo(binubuokey)
        self.show_messages = False

    def setup_logging(self):
        # Create the logger
        self.logger = logging.getLogger(__name__)
        # Logger settings and levels
        self.logger.setLevel(logging.INFO)
        # Logger formatter and handler
        file_handler = logging.FileHandler(filename='binubuo.log', mode='a')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        # Add the handler to the logger
        self.logger.addHandler(file_handler)

    def connect(self):
        try:
            if self.dbfullConnection is None:
                #if self.dbpwd is None:
                #    self.connection = psycopg2.connect(dbname=self.dbname, user=self.dbuser)
                #else:
                #    self.connection = psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpwd)
                print("Currently binubuoYugabyte only supports connections to YugabyteDB with a preconnected psycopg2 connection.")
            else:
                self.connection = self.dbfullConnection
            self.connected = True
        except:
            self.logger.error("Error: Failed to connect to database. Please make sure you have a connection before using other methods.")
            self.connection = None

    def connectSecondary(self, dbname=None, dbuser=None, dbpwd=None, dbfullConnection=None):
        try:
            if dbfullConnection is None:
                #if dbpwd is None:
                #    self.secondary_connection = psycopg2.connect(dbname=dbname, user=dbuser)
                #else:
                #    self.secondary_connection = psycopg2.connect(dbname=dbname, user=dbuser, password=dbpwd)
                print("Currently binubuoYugabyte only supports connections to YugabyteDB with a preconnected psycopg2 connection.")
            else:
                self.secondary_connection = dbfullConnection
            self.connected_secondary = True
        except:
            self.logger.error("Error: Failed to connect to secondary/alternate database. Please check your connection details and try again.")
            self.secondary_connection = None

    def columnGeneratorComments(self, table_name, comments, override=False):
        self.m("Create comments on table [" + table_name + "]. Comments=" + str(comments) + ".", tolog=True)
        if self.connected:
            comment_count_sql = self.load_resource("yugabyte_count_comments.sql")
            working_cursor = self.connection.cursor()
            working_cursor.execute(comment_count_sql, (table_name,))
            cursor_result = working_cursor.fetchone()
            self.logger.debug("Comments: " + str(cursor_result[0]))
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
                    ordered_col_sql = self.load_resource("yugabyte_comments_ordered.sql")
                    ordered_col_cursor.execute(ordered_col_sql, (table_name,))
                    for cid, cname in ordered_col_cursor:
                        self.logger.debug("Working on col: " + cname)
                        try:
                            colcomment = comments.split(",")[cid - 1]
                            col_add_stmt = "comment on column " + table_name + "." + cname + " is '" + colcomment + "';"
                            self.logger.debug("Comment command: " + col_add_stmt)
                            working_cursor.execute(col_add_stmt)
                        except:
                            # Aint no comment for this column. Just ignore
                            pass
                self.connection.commit()
                self.m("Comments for table [" + table_name +"] successfully created.", indent=True, tolog=False)

    def calculateSampleSize(self, table_name):
        sub_sample_cursor = self.connection.cursor()
        sub_sample_size_stmt = self.load_resource("yugabyte_table_rows.sql")
        sub_sample_cursor.execute(sub_sample_size_stmt, (table_name,))
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
        self.logger.info("Sample size of " + str(sub_sample_size_cal_cust) + " calculated for " + str(sub_sample_size_cal[0]) + " rows.")
        # Yugabyte needds a rowcount, since they do not support tablesample and xmin
        sub_sample_size_cal_cust = round(max(1, sub_sample_size_cal_cust * int(sub_sample_size_cal[0])))
        return sub_sample_size_cal_cust

    def tableIsAnalyzed(self, table_name):
        table_analyze_check_cursor = self.connection.cursor()
        table_analyze_check_stmt = self.load_resource("yugabyte_table_analyzed.sql")
        table_analyze_check_cursor.execute(table_analyze_check_stmt, (table_name,))
        table_analyze_check_val = table_analyze_check_cursor.fetchone()
        is_analyzed = table_analyze_check_val[0]
        if is_analyzed is None:
            self.logger.error("Table %s is not analyzed. Binubuo depends on statistics, so please analyze table for full functionality.", table_name)
            if self.binubuo_config['DATABASE']['force_analyze'] == 'yes':
                self.logger.info("Parameter force_analyze is yes. Analyze table [%s].", table_name)
                table_analyze_do_cursor = self.connection.cursor()
                table_analyze_do_cursor.execute("analyze " + table_name + ";")
                self.connection.commit()
                is_analyzed = "analyzed now"
        else:
            self.logger.info("Table [%s] was last anayzed %s.", table_name, str(is_analyzed))
        return is_analyzed

    def tableSize(self, table_name):
        table_size_cursor = self.connection.cursor()
        if self.tableIsAnalyzed(table_name) is not None:
            table_size_size_stmt = self.load_resource("yugabyte_table_rows.sql")
        else:
            table_size_size_stmt = self.load_resource("yugabyte_table_rows_not_analysed.sql")
        table_size_cursor.execute(table_size_size_stmt, (table_name,))
        table_size_size_cal = table_size_cursor.fetchone()
        table_size_size_cal = table_size_size_cal[0]
        self.logger.info("Table size of %s is %s rows.", table_name, str(table_size_size_cal))
        return table_size_size_cal

    def templateFromTable(self, table_name, use_comments=True, use_infer=False, use_sample_data=False, output_type="json"):
        self.m("Create template from table [" + table_name + "]. Infer=" + str(use_infer) + " Sampledata=" + str(use_sample_data) + ".", tolog=True)
        table_template = BinubuoTemplate()
        table_exist = self.table_exist(table_name)
        if not table_exist:
            self.m("Table name entered does not exist. templateFromTable can only be used on existing tables.")
            quit()
        # Table exists
        if table_exist:
            table_template = BinubuoTemplate()
            table_templateTable = table_name
            if not use_infer:
                self.m("Using simple method to create columns.", indent=True, tolog=False)
                working_cursor = self.connection.cursor()
                generic_column_meta_sql = self.load_resource("yugabyte_column_meta_simple.sql")
                working_cursor.execute(generic_column_meta_sql, (table_name,))
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
                if self.tableIsAnalyzed(table_name) is None:
                    self.m("Table " + table_name + " is not analyzed. Please run [analyze " + table_name + ";]", indent=True, tolog=False)
                self.m("Using infer method to create columns.", indent=True, tolog=False)
                if use_sample_data:
                    sub_sample_size_cal_cust = self.calculateSampleSize(table_name)
                working_cursor = self.connection.cursor()
                if use_sample_data:
                    columns_meta_stmt = self.load_resource("yugabyte_column_meta_plus_sample.sql")
                else:
                    columns_meta_stmt = self.load_resource("yugabyte_column_meta_plus_standard.sql")
                working_cursor.execute(columns_meta_stmt, (table_name, table_name,))
                for col_name, col_infer_meta in working_cursor:
                    self.logger.info("Column to infer: " + col_name)
                    self.logger.debug("Infer: " + col_infer_meta["table_name"])
                    main_meta = col_infer_meta
                    if use_sample_data:
                        self.m("Sampling data on column [" + col_name +"].", indent=True, tolog=False)
                        sub_sample_cursor = self.connection.cursor()
                        # Merge the sample data.
                        sub_sample_stmt = self.load_resource("yugabyte_column_sample_data.sql").format(r_col_name=col_name, r_table_name=table_name, r_table_sample_size=sub_sample_size_cal_cust)
                        sub_sample_cursor.execute(sub_sample_stmt)
                        for sample_data_array in sub_sample_cursor:
                            # Now add the sample data as a real array.
                            if sample_data_array[0] is not None:
                                main_meta["sample_values"] = sample_data_array[0]
                        if main_meta["column_is_reference"] == 1:
                            self.m("Column [" + col_name +"] is foreign key. Create key distribution histogram.", indent=True, tolog=False)
                            rel_sample_size_cal_cust = self.calculateSampleSize(main_meta["reference_table"])
                            rel_sample_cursor = self.connection.cursor()
                            rel_sample_stmt = self.load_resource("yugabyte_foreign_key_histogram.sql").format(col_name = main_meta["column_name"], tab_name = table_name, ref_col_name = main_meta["reference_column"], ref_tab_name = main_meta["reference_table"], ref_sample = rel_sample_size_cal_cust)
                            # Fill in the histogram data
                            self.logger.info("Column is a foreign key. Build relation histogram")
                            self.logger.debug("Relation histogram query: " + rel_sample_stmt)
                            rel_sample_cursor.execute(rel_sample_stmt)
                            for ref_sample_data_array in rel_sample_cursor:
                                if ref_sample_data_array[0] is not None:
                                    self.logger.debug("Foreign key histogram: ")
                                    self.logger.debug(ref_sample_data_array[0])
                                    main_meta["reference_histogram"] = ref_sample_data_array[0]
                    # We get back the entire json of inferred column
                    # Init column and call infer endpoint
                    table_template.init_column(column_name=col_name)
                    self.logger.debug("Infer: " + json.dumps(main_meta))
                    x_response = self.infer_generator(json.dumps(main_meta))
                    self.logger.debug(x_response)
                    # The response is the column json as a string format. Call replace_column_from_json
                    table_template.replace_column_from_json(col_name, json.dumps(x_response))
                # Once we are done, we can validate the template and return it.
                self.m("Template for table [" + table_name +"] successfully created.", indent=True, tolog=False)
                if output_type.upper() == "JSON":
                    table_template.validate_template()
                    table_template.complete_template()
                    return table_template.template_JSON
                else:
                    return table_template


    def quick_fetch_table(self
            , table_name, use_comments=True, use_infer=False
            , use_sample_data=False, use_tuple_return=False
            , output_csv=False, output_type="screen", output_name="same"
            , rows="same"):
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
                generic_column_meta_sql = self.load_resource("yugabyte_column_meta_simple.sql")
                working_cursor.execute(generic_column_meta_sql, (table_name,))
                for cname, cdtype, cdgenerator, ccomment, crows, cnumnulls, cnumdist, cnullable, cavglen in working_cursor:
                    self.template.init_column(column_name=cname, column_type="generated", column_datatype=cdtype)
                    if ccomment is not None and use_comments:
                        quick_fetch_columns_array.append(ccomment)
                    else:
                        quick_fetch_columns_array.append(cdgenerator)
                # Once we are done, we can call the quick fetch.
                quick_fetch_columns = ",".join(quick_fetch_columns_array)
                # Before fetching, set rows if needed.
                if rows == "same":
                    # TODO: Set to current rowcount
                    self.drows(10)
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
                        quick_insert_cursor.executemany(quick_insert_stmt, resp_cols)
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
        build_insert_stmt = self.load_resource("yugabyte_build_insert.sql")
        insert_stmt_cursor.execute(build_insert_stmt, (source_table,))
        cursor_result = insert_stmt_cursor.fetchone()
        if target_table is not None:
            insert_stmt = "insert into " + target_table + " " + cursor_result[1]
        else:
            insert_stmt = "insert into " + source_table + " " + cursor_result[1]
        insert_stmt = insert_stmt.replace("d_d_s_r", "%s")
        self.logger.debug("Insert stmt: " + insert_stmt)
        return insert_stmt

    def table_exist(self, table_name, use_secondary=False):
        if use_secondary and self.connected_secondary:
            use_conn = self.secondary_connection
        else:
            use_conn = self.connection
        assert_table_sql = self.load_resource("yugabyte_assert_table.sql")
        assert_table_cursor = use_conn.cursor()
        self.logger.debug("Before cursor check source")
        table_exist = False
        assert_table_cursor.execute(assert_table_sql, (table_name,))
        cursor_result = assert_table_cursor.fetchone()
        if cursor_result[0]:
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
        ddl_stmt = self.load_resource("yugabyte_table_ddl.sql")
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
            if target_db is None:
                table_ddl = "create table " + loc_target_table.lower() + " as select * from " + source_table.lower() + " where 1=2"
            else:
                table_ddl = self.ddl_from_table(source_table)
                # Replace with target
                table_ddl = table_ddl.replace('CREATE TABLE ' + source_table + '', 'CREATE TABLE ' + loc_target_table.upper() + '')
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
                pass
            else:
                try:
                    self.drows(int(data_rows))
                except:
                    self.drows(int(10))
            # Get new rows.
            if copy_method == "quickfetch":
                rows_bind = self.quick_fetch_table(table_name=source_table, use_tuple_return=True)
                self.logger.info("Rows returned for insert: " + str(len(rows_bind)))
                target_work_cursor.executemany(insert_stmt, rows_bind)
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
                rows_bind = self.binuObj.dataset(dataset_name=dset_name, response_type="tuple")
                if rows_bind is not None:
                    self.logger.info("Rows returned for insert: " + str(len(rows_bind)))
                    target_work_cursor.executemany(insert_stmt, rows_bind)
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
                insert_cursor.executemany(insert_stmt, rows_bind)
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
        header_stmt = self.load_resource("yugabyte_columns_ordered.sql")
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
        sample_stmt = self.load_resource("yugabyte_sample_select.sql").format(r_rows = ','.join(headers), r_table = table_name, r_limit = '3')
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
        hierachy_stmt = self.load_resource("yugabyte_table_hierachy_schema.sql")
        working_cursor.execute(hierachy_stmt, (schema_name, schema_name,))
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
            depends_stmt = self.load_resource("yugabyte_foreign_key_depends.sql")
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