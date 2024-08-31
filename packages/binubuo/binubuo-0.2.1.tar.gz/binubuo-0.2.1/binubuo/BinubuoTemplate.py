# Helper class to create datasets
import json
import logging

class BinubuoTemplate:
    def __init__(self, generator_cache=None):
        self.init_template()
        if(generator_cache is not None):
            self.generator_cache = generator_cache
            self.generator_cache_loaded = 1
        self.show_messages = False
        self.setup_logging()

    def m(self, message):
        if self.show_messages:
            print(message)

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

    def set_message(self, show=False):
        self.show_messages = show

    def init_template(self):
        # Create the base dictionary for the dataset.
        self.ds_base = {}
        self.ds_base["columns"] = []
        self.columns = {}
        self.generator_cache_loaded = 0
        self.validate_errors = 0
        self.validate_run = 0
        self.template_JSON = None

    def __init_generated(self):
        tmpl = {}
        tmpl["column_name"] = "**"
        tmpl["column_type"] = "**"
        tmpl["column_datatype"] = "**"
        tmpl["generator"] = "**"
        tmpl["arguments"] = "--"
        tmpl["column_rule"] = "--"
        return tmpl

    def __init_fixed(self):
        tmpl = {}
        tmpl["column_name"] = "**"
        tmpl["column_type"] = "**"
        tmpl["column_datatype"] = "**"
        tmpl["fixed_value"] = "**"
        return tmpl

    def init_column(self, column_name, column_type="generated", column_datatype="string"):
        lowered_name = column_name.lower()
        if column_type.upper() == "GENERATED":
            self.columns[lowered_name] = self.__init_generated()
        elif column_type.upper() == "FIXED":
            self.columns[lowered_name] = self.__init_fixed()
        else:
            self.columns[lowered_name] = {}
        self.columns[lowered_name]["column_name"] = lowered_name
        self.columns[lowered_name]["column_type"] = column_type.lower()
        self.columns[lowered_name]["column_datatype"] = column_datatype

    def set_column_attribute(self, column_name, attr_name, attr_val):
        lowered_name = column_name.lower()
        self.columns[lowered_name][attr_name] = attr_val

    def replace_column_from_json(self, column_name, json_str):
        self.logger.info("Raw input to replace: %s", json_str)
        lowered_name = column_name.lower()
        self.columns[lowered_name] = json.loads(json_str)

    def show_missing_attributes(self, column_name=None):
        print("{:<20} {:<20} {:<30}".format('Column:', 'Status:', 'Attribute:'))
        print("{:<20} {:<20} {:<30}".format('===================', '===================', '============================='))
        if(column_name is not None):
            lowered_name = column_name.lower()
            # just show the specific fields in this column
            for col_key in self.columns[lowered_name]:
                if self.columns[lowered_name][col_key] == "**":
                    print("{:<20} {:<20} {:<30}".format(lowered_name, 'REQUIRED', col_key))
                if self.columns[cols][col_key] == "--":
                    print("{:<20} {:<20} {:<30}".format(lowered_name, 'Optional', col_key))
        else:
            # column not specified. Show for all
            for cols in self.columns:
                for col_key in self.columns[cols]:
                    if self.columns[cols][col_key] == "**":
                        print("{:<20} {:<20} {:<30}".format(cols.lower(), 'REQUIRED', col_key))
                    if self.columns[cols][col_key] == "--":
                        print("{:<20} {:<20} {:<30}".format(cols.lower(), 'Optional', col_key))


    def set_column_generator_from_cache(self, column_name, cache_name):
        if self.generator_cache_loaded == 1:
            validate_string = cache_name.upper()
            found_generator = None
            current_generator = None
            # cache is loaded. Do search
            for idx, val in enumerate(self.generator_cache):
                for key, value in val.items():
                    if key == "GENERATOR_CALL":
                        current_generator = value
                    if (key == "GENERATOR_WEBSERVICE_NAME" and value.upper() == validate_string) or (key == "GENERATOR_NAME" and value.upper() == validate_string):
                        found_generator = 1
                if found_generator == 1:
                    self.columns[column_name]["generator"] = current_generator
                    found_generator = None
        else:
            self.logger.warning("WARNING: Cache is not loaded. No actions taken.")

    def validate_template(self):
        self.validate_run = 1
        for cols in self.columns:
            for col_key in self.columns[cols]:
                if self.columns[cols][col_key] == "**":
                    self.logger.error("ERROR: Required attribute: %s in column: %s has no value.", col_key, cols)
                    self.validate_errors = self.validate_errors + 1
                if self.columns[cols][col_key] == "--":
                    self.logger.warning("WARNING: Optional attribute: %s in column: %s has no value and will not be used.", col_key, cols)

    def complete_template(self, accept_errors=0):
        if (self.validate_run == 1 and self.validate_errors > 0 and accept_errors == 0):
            self.logger.error("ERROR: Template has errors. Please fix and validate before completing template.")
            # Reset validation and error count
            self.validate_run = 0
            self.validate_errors = 0
        elif (self.validate_run == 0 and accept_errors == 0):
            self.logger.error("ERROR: Template has not been validated. Please validate and fix any potential errors before completing template.")
        elif (accept_errors == 1) or (self.validate_run == 1 and self.validate_errors == 0 and accept_errors == 0):
            # We completed the validation. Loop trough columns, remove optional not filled out and create template text.
            for cols in self.columns:
                pop_list = []
                for col_key in self.columns[cols]:
                    if self.columns[cols][col_key] == "--":
                        pop_list.append(col_key)
                # Remove from dict after marking, since we cannot pop during iteration.
                for idx, val in enumerate(pop_list):
                    self.columns[cols].pop(val)
                # Optionals removed. Trust the rest. Append to list.
                self.ds_base["columns"].append(self.columns[cols])
            # All columns added. Create the JSON text for dataset creation.
            self.template_JSON = json.dumps(self.ds_base)