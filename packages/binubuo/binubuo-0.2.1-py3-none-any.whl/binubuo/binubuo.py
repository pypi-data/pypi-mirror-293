import configparser
from stat import filemode
import requests
import json
import uuid
import hashlib
import logging
import pkgutil
import configparser
import os
from pathlib import Path

class binubuo:
    def __init__(self, apikey=None):
        self.rapidapi_key = None
        self.binubuo_key = None
        self.error_string = None
        self.unique_url_path = None
        self.setup_logging()
        if(apikey is None):
            # print("No API key specified. Please set api key before making calls to binubuo.")
            pass
        else:
            self.key(apikey)
        self.__readconfig()
        self.show_messages = True

    def m(self, message, indent=False, tolog=False):
        """
        This is method used to output text to the screen.

        :param message: The is the message you want to display
        :param indent: If you want to indent the output. Default [False].
        :param tolog: If you want the message to be written to the logfile also. Default [False].
        """
        if self.show_messages:
            if indent:
                print("  -> " + message)
            else:
                print("-> " + message)
        if tolog:
            self.logger.info(message)

    def setup_logging(self):
        """
        This will setup the logger for the class and method invocations.
        
        """
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

    def set_message(self, show=False):
        self.show_messages = show

    def load_resource(self, resource_name, resource_type="SQL"):
        """
        Load a resource file associated with Binubuo.
        
        :param resource_name: The name of the resource file.
        :param resource_type: The type of the resource. Default [SQL].
        """
        self.logger.debug("Loading resource %s from resource_type %s", resource_name, resource_type)
        resource_url = resource_type + "/" + resource_name
        try:
            resource_data = pkgutil.get_data(__name__, resource_url)
            return resource_data.decode('utf-8')
        except:
            self.logger.error("Failed to load resource: %s", resource_url)

    def __set_unique_url(self):
        self.__setheaders()
        self.resp = requests.request("GET", self.baseurl + '/binubuo-actions/get-unique-url-path', headers=self.headers)
        if self.resp.ok:
            self.response_json = json.loads(self.resp.text)
            for key, value in self.response_json.items():
                if key == 'unique_url':
                    self.unique_url_path = value
                    self.logger.info("Unique url: %s", self.unique_url_path)
        else:
            if self.resp.status_code == 404:
                self.logger.error("Unique url endpoint not found: %s/binubuo-actions/get-unique-url-path", self.baseurl)
            else:
                self.logger.critical("Unique url communication failure", exc_info=1)

    def __set_temp_key(self):
        # Asking to set a temporary key outside of regular user scope.
        fp_val1 = str(uuid.getnode())
        fp_val2 = hashlib.md5(fp_val1.encode())
        fp_s = fp_val2.hexdigest()
        # We need to change the host, since we have to go direct to binubuo.
        self.binubuo_host = "binubuo.com"
        self.baseurl = "https://" + self.binubuo_host + '/api'
        # Set headers
        self.binubuo_key = fp_s
        self.__setheaders()
        # Send key request
        self.resp = requests.request("POST", self.baseurl + '/binubuo-actions/get-temp-key', headers=self.headers)
        # instead of printing key, send request to get back actual temp key using fp_s
        if self.resp.ok:
            self.response_json = json.loads(self.resp.text)
            for key, value in self.response_json.items():
                # Getting the temporary key back we set it
                if key == "temp_key":
                    self.binubuo_key = value
                if key == 'unique_url':
                    self.unique_url_path = value
        else:
            if self.resp.status_code == 404:
                self.logger.error("Temp key creation endpoint not found: %s/binubuo-actions/get-temp-key", self.baseurl)
            else:
                self.logger.critical("Temp key communication failure", exc_info=1)

    def create_account(self, account_name, account_email, user_name=None):
        """
        Create an account on Binubuo.com from the python client.
        
        :param account_name: Name of the account you want to create.
        :param account_email: The email associated with the account.
        :param user_name: If you want the user name of the account to be different than account name.
        """
        # Creating account directly from python client is only supported against binubuo.com directly.
        u_password_1 = input("Choose a password for your account: ")
        u_password_2 = None
        while u_password_2 != u_password_1:
            u_password_2 = input("Re-enter password to validate: ")
        fp_val1 = str(uuid.getnode())
        fp_val2 = hashlib.md5(fp_val1.encode())
        fp_s = fp_val2.hexdigest()
        self.binubuo_host = "binubuo.com"
        self.baseurl = "https://" + self.binubuo_host + '/api'
        query_string = {"account_name": account_name}
        query_string["account_email"] = account_email
        query_string["account_pwd"] = u_password_1
        if (user_name is not None):
            query_string["user_name"] = user_name
        headers = {}
        headers["x-binubuo-key"] = fp_s
        self.resp = requests.request("POST", self.baseurl + '/binubuo-actions/create-account', headers=headers, params=query_string)
        if self.resp.ok:
            self.response_json = json.loads(self.resp.text)
            self.challenge_hash = self.response_json["challenge_id"]
            print("Please got to this url in your browser: " + self.response_json["challenge_url"])
            challenge_response = input("Please input the code displayed in the above URL: ")
            query_string = {"challenge": self.challenge_hash}
            query_string["response"] = challenge_response
            self.resp = requests.request("POST", self.baseurl + '/binubuo-actions/verify-account', headers=headers, params=query_string)
            if self.resp.ok:
                # We now have the actual key 
                self.response_json = json.loads(self.resp.text)
                self.key(self.response_json["binubuo_key"])
                print("Your API key for Binubuo is (please save it.): " + self.binubuo_key)
            else:
                if self.resp.status_code == 401:
                    self.logger.warning("Verify account called wrong. Unauthorized")
                else:
                    self.logger.critical("Communication failure in verify-account", exc_info=1)
        else:
            if self.resp.status_code == 401:
                self.logger.warning("Create account called wronng. Unauthorized")
            else:
                self.logger.critical("Communication failure in create-account", exc_info=1)

    def key(self, key=None):
        """
        Set or unset the Binubuo key used for requests.
        
        :param key: The key to set. Dont use if you want to unset the curernt key.
        """
        if len(key.split('-')) > 1:
            # We know that we have a temporary key.
            self.binubuo_key = key
            self.binubuo_host = "binubuo.com"
            self.baseurl = "https://" + self.rapidapi_host + '/api'
            self.__set_unique_url()
        elif(key is not None):
            rapid = 0
            for c in key:
                if c.islower():
                    rapid = 1
            if rapid == 1:
                self.rapidapi_key = key
                self.rapidapi_host = "binubuo.p.rapidapi.com"
                self.baseurl = "https://" + self.rapidapi_host
            else:
                self.binubuo_key = key
                self.binubuo_host = "binubuo.com"
                self.baseurl = "https://" + self.binubuo_host + '/api'
            self.__set_unique_url()
        else:
            self.logger.info("Key unset. Please set key before making calls to binubuo.")

    def __readconfig(self):
        current_dir_obj = Path(os.getcwd())
        current_dir_config = current_dir_obj / "binubuo.conf"
        config_exists = False
        if current_dir_config.exists():
            # Check for config file in current directory
            config_location = current_dir_config
            config_exists = True
        if "HOME" in os.environ:
            home_dir_obj = Path(os.environ["HOME"])
            home_dir_config = home_dir_obj / "binubuo.conf"
            if home_dir_config.exists():
                # Check for config file in users HOME
                config_location = home_dir_config
                config_exists = True
        if "BINUBUO_HOME" in os.environ:
            # Look for config file here
            bhome_obj = Path(os.environ["BINUBUO_HOME"])
            bhome_config = bhome_obj / "binubuo.conf"
            if bhome_config.exists():
                config_location = bhome_config
                config_exists = True
        # If we had a config file load it.
        if config_exists:
            self.binubuo_config = configparser.ConfigParser()
            self.binubuo_config.read(config_location)
        else:
            # No config file exists, just set defaults if needed
            self.binubuo_config = configparser.ConfigParser()
            self.binubuo_config['OUTPUTS'] = {'dependency_warnings': 'yes', 'log_level': 'INFO'}
            self.binubuo_config['GENERATOR'] = {'generator_rows': '1'}
            # Removed standard parameters.
            self.binubuo_config['DATASET'] = {'dataset_rows': '10'}
            self.binubuo_config['DATABASE'] = {'force_analyze': 'no'}
            self.binubuo_config['DATABASE'] = {'use_standard_datasets_as_source': 'no'}
        # Now set the class variables based on config.
        if(self.rapidapi_key is not None):
            self.rapidapi_host = "binubuo.p.rapidapi.com"
            self.baseurl = "https://" + self.rapidapi_host
        elif(self.binubuo_key is not None):
            self.binubuo_host = "binubuo.com"
            self.baseurl = "https://" + self.binubuo_host + '/api'
        else:
            # No key set. Base direct settings.
            self.binubuo_host = "binubuo.com"
            self.baseurl = "https://" + self.binubuo_host + '/api'
        self.default_generator_rows = int(self.binubuo_config.get('GENERATOR', 'generator_rows', fallback='1'))
        self.default_dataset_rows = int(self.binubuo_config.get('DATASET', 'dataset_rows', fallback='10'))
        self.locale_set = self.binubuo_config.get('PARAMETERS', 'locale', fallback=None)
        self.tag_set = self.binubuo_config.get('PARAMETERS', 'tag', fallback=None)
        self.tz_set = self.binubuo_config.get('PARAMETERS', 'tz', fallback=None)
        self.csv_set = None
        self.session_id_set = None
        self.load_as = "json"
        self.generator_dict_cache = 0
        self.dataset_dict_cache = 0
        self.dict_cache = {}
        self.qf = 0
        self.post_data = None
        self.category = None
        self.dataset_type = "/"
        self.dummy_set = 1

    def __setheaders(self):
        self.headers = {}
        if(self.rapidapi_key is not None):
            self.headers["x-rapidapi-host"] = self.rapidapi_host
            self.headers["x-rapidapi-key"] = self.rapidapi_key
        elif(self.binubuo_key is not None):
            self.headers["x-binubuo-key"] = self.binubuo_key

    def __check_key_status_before_run(self):
        if self.binubuo_key is None and self.rapidapi_key is None:
            # Seems we are beeing called and no key is set.
            # Generate a temp key and alert user.
            self.__set_temp_key()
            if self.binubuo_config.get('OUTPUTS', 'dependency_warnings', fallback='Yes') == 'Yes':
                print("WARNING: Calling without a fixed key set. Will run on temporary key. Please remember to set key")
                print("If you do not have a key, you can always create one with the create_account method.")
                print("See details here: https://binubuo.com/ords/r/binubuo_ui/binubuo/python-client")


    def call_binubuo(self, rest_path, query_string, request_type="GET"):
        """
        The main method to call Binubuo. It will set necesarry headers and parameters for you.
        
        :param rest_path: The path of the REST call.
        :param query_string: A dictionary of query parameters for the REST URL.
        :param request_type: The type of HTTP request. Default [GET]
        """
        self.__check_key_status_before_run()
        self.__setheaders()
        if request_type == "GET":
            if(self.locale_set is not None):
                query_string["locale"] = self.locale_set
            if(self.tag_set is not None):
                query_string["tag"] = self.tag_set
            if(self.tz_set is not None):
                query_string["tz"] = self.tz_set
            if(self.category is None) and (self.csv_set is not None):
                query_string["csv"] = 1
            if(self.session_id_set is not None):
                query_string["bsession"] = self.session_id_set
        if(self.category is not None):
            req_url = self.baseurl + self.category.lower() + rest_path.lower()
        else:
            req_url = self.baseurl + self.dataset_type.lower() + rest_path.lower()
        self.logger.info("URL Called: %s", req_url)
        if request_type == "GET":
            self.resp = requests.request(request_type, req_url, headers=self.headers, params=query_string)
        else:
            if self.post_data is not None:
                self.resp = requests.request(request_type, req_url, headers=self.headers, params=query_string, json=json.loads(self.post_data))
            else:
                self.resp = requests.request(request_type, req_url, headers=self.headers, params=query_string)  
        if self.resp.ok:
            self.logger.debug("Raw response: " + self.resp.text)
            if self.load_as == "json":
                self.response_json = json.loads(self.resp.text)
            elif(self.category is None) and (self.csv_set is not None):
                self.response_csv = self.resp.text
            else:
                # Default to loads json
                self.response_json = json.loads(self.resp.text)
        else:
            if self.resp.status_code == 403:
                try:
                    error_json = json.loads(self.resp.text)
                    self.error_string = error_json["string_out"]
                    self.logger.error(self.error_string)
                except:
                    self.logger.warning("Invalid API key specified.")
                    self.error_string = "Invalid API key specified."
            elif self.resp.status_code == 401:
                try:
                    error_json = json.loads(self.resp.text)
                    self.error_string = error_json["string_out"]
                    self.logger.error(self.error_string)
                except:
                    self.logger.warning("Authorization failure")
                    self.error_string = "Authorization failure"
            elif self.resp.status_code == 404:
                self.logger.warning("Generator/Dataset path not found: %s", rest_path)
                self.error_string = "Generator/Dataset path not found: " + rest_path
            else:
                self.logger.error("Full error response: " + self.resp.text)
                self.error_string = "Communication failure"

    def call_binubuo_to_file(self, rest_path, query_string):
        """
        Method to call Binubuo and have the result directly written to file. 
        It will set necesarry headers and parameters for you. Only works for GET requests.
        
        :param rest_path: The path of the REST call.
        :param query_string: A dictionary of query parameters for the REST URL.
        """
        self.__check_key_status_before_run()
        self.__setheaders()
        if(self.locale_set is not None):
            query_string["locale"] = self.locale_set
        if(self.tag_set is not None):
            query_string["tag"] = self.tag_set
        if(self.tz_set is not None):
            query_string["tz"] = self.tz_set
        if(self.session_id_set is not None):
            query_string["bsession"] = self.session_id_set
        if(self.category is None) and (self.csv_set is not None):
            query_string["csv"] = 1
        if(self.category is not None):
            url_call = self.baseurl + self.category + rest_path
            #self.resp = requests.request("GET", self.baseurl + self.category + rest_path, headers=self.headers, params=query_string)
        else:
            url_call = self.baseurl + self.dataset_type + rest_path
            #self.resp = requests.request("GET", self.baseurl + self.dataset_type + rest_path, headers=self.headers, params=query_string)
        with requests.get(url_call, stream=True, headers=self.headers, params=query_string) as br:
            br.raise_for_status()
            with open(self.file_name, 'wb') as bf:
                for chunk in br.iter_content(chunk_size=8192):
                    bf.write(chunk)

    def tz(self, tz=None):
        """
        Set or unset the timezone used for requests.
        
        :param tz: The timezone to set. Format follows ISO-8601.
        """
        if tz:
            self.tz_set = tz
            self.logger.info("Timezone changed to %s", str(tz))
        else:
            self.tz_set = self.binubuo_config.get('PARAMETERS', 'tz', fallback=None)

    def session_id(self, session_id=None):
        """
        Set or unset the timezone used for requests.
        
        :param session_id: The timezone to set. Format follows ISO-8601.
        """
        if session_id:
            self.session_id_set = session_id
            self.logger.info("Session ID changed to %s", str(session_id))
        else:
            self.session_id_set = self.binubuo_config.get('PARAMETERS', 'session_id', fallback=None)

    def locale(self, locale=None):
        """
        Set or unset the locale used for requests.
        
        :param locale: The locale to set. Format is lowercase two letter iso code.
        """
        if locale:
            self.locale_set = locale
            self.logger.info("Locale changed to %s", locale)
        else:
            self.binubuo_config.get('PARAMETERS', 'locale', fallback=None)

    def tag(self, tag=None):
        """
        Set or unset the tag used for requests.
        
        :param tag: The tag to set.
        """
        if tag:
            self.tag_set = tag
            self.logger.info("Tag changed to %s", tag)
        else:
            self.tag_set = self.binubuo_config.get('PARAMETERS', 'tag', fallback=None)

    def csv(self, csv=None):
        """
        Set or unset the csv flag.
        
        :param csv: The csv set either to a value to write CSV, or [None] as do not write CSV.
        """
        self.csv_set = csv
        if csv:
            self.load_as = 'csv'
            self.logger.info("Output type set to CSV")
        else:
            self.load_as = 'json'

    def grows(self, rows=1):
        """
        Set the default number of rows for all generator requests.
        
        :param rows: The rows to set.
        """
        if rows:
            self.default_generator_rows = rows
            self.logger.info("Generator rows changed to %s", str(rows))
        else:
            self.default_generator_rows = int(self.binubuo_config.get('GENERATOR', 'generator_rows', fallback='1'))

    def drows(self, rows=10):
        """
        Set the default number of rows for all dataset requests.
        
        :param rows: The rows to set.
        """
        if rows:
            self.default_dataset_rows = rows
            self.logger.info("Dataset rows changed to %s", str(rows))
        else:
            self.default_dataset_rows = int(self.binubuo_config.get('DATASET', 'dataset_rows', fallback='10'))

    def get_generator_response_value(self):
        if self.default_generator_rows == 1:
            # Request a single value directly.
            self.generator_response_value = list(list(self.response_json.values())[0][0].values())[0]
        else:
            # Request for more values. Make response into a list and return
            self.generator_response_value = []
            for prime_key in self.response_json:
                for idx, val in enumerate(self.response_json[prime_key]):
                    for key, value in val.items():
                        self.generator_response_value.append(value)

    def get_dataset_response_value(self, response_type="list"):
        if ((type(self.response_json) is dict) and list(self.response_json.keys())[0] == "dataset_stored_location"):
            self.response_clean = self.response_json
            # Set data is in storage
            self.logger.info("Result to large for direct. Please pickup in file: %s", self.response_json["dataset_stored_location"])
            self.dataset_response_value = self.response_clean
            print("Requested number of rows " + str(self.default_dataset_rows) + " is to large for online request.")
            print("Data is currently being generated in the background on the server.")
            print("Your request is estimated to complete in " + self.response_json["expected_completion_in_seconds"] + " seconds and then you can fetch your data at:")
            # self.response_json["expected_completion_in_seconds"]
            print(self.response_json["dataset_stored_location"])
        else:
            if (self.dataset_type.find("data/standard") >= 0 or self.qf == 1) and (self.csv_set is None):
                # Purify result
                try:
                    for standard_key in self.response_json:
                        self.response_clean = self.response_json[standard_key]
                except:
                    # For some reason we are missing the standard key
                    self.response_clean = self.response_json
            elif(self.csv_set is not None):
                self.response_clean = self.response_csv
            else:
                self.response_clean = self.response_json
            if response_type == "list":
                self.dataset_response_value = []
                if (self.csv_set is None):
                    for rows in self.response_clean:
                        self.dataset_response_value.append(list(rows.values()))
                else:
                    for line in self.response_clean.splitlines():
                        #self.dataset_response_value.append(line.rstrip().split(','))
                        self.dataset_response_value.append(line.rstrip())
            elif response_type == "tuple":
                self.dataset_response_value = []
                if (self.csv_set is None):
                    for rows in self.response_clean:
                        self.dataset_response_value.append(tuple(list(rows.values())))
                else:
                    for line in self.response_clean.splitlines():
                        self.dataset_response_value.append(tuple(line.rstrip().split(',')))
            elif response_type == "json":
                self.dataset_response_value = self.response_clean

    def dataset_sample(self, dataset_name, dataset_type="custom", dataset_category=None):
        """
        Get a sample of 3 rows from a dataset, to see how data looks.
        
        :param dataset_name: The dataset name to get samples from.
        """
        # Set rows to 3
        self.drows(3)
        # Get the data
        self.dataset(dataset_name=dataset_name, dataset_type=dataset_type, dataset_category=dataset_category, response_type="json")
        # Print title
        print("**************************************************************************")
        print("** Dataset data sample: " + dataset_name.upper())
        print("**************************************************************************")
        # Extract row one for headers
        row_1 = self.dataset_response_value[0]
        headers = []
        headers_deco = []
        for key, value in row_1.items():
            headers.append(key)
        row_format = "{:>15}" * (len(headers))
        for x in range (len(headers)):
            headers_deco.append(" ==============")
        print(row_format.format(*headers))
        print(row_format.format(*headers_deco))
        for rows in self.dataset_response_value:
            row_data = []
            for key, value in rows.items():
                row_data.append(str(value)[0:14])
            print(row_format.format(*row_data))
        

    def dataset_exists(self, dataset):
        """
        Check if a given dataset name exists as a custom dataset.
        
        :param dataset: The dataset name to check existence.
        """
        if self.dataset_dict_cache == 0:
            # Only call if we have not cached already
            self.list_datasets(1)
            if self.resp.ok:
                pass
            else:
                self.logger.warning(self.error_string)
        d_exist = False
        for idx, val in enumerate(self.dict_cache["datasets"]):
                for key, value in val.items():
                    if key == "DATASET_WEBSERVICE_NAME":
                        if value.upper() == dataset.upper():
                            if self.dict_cache["datasets"][idx]["DATASET_TYPE_NAME"] == "Custom Dataset":
                                d_exist = True
        return d_exist

    def standard_dataset_exists(self, dataset, category=None):
        """
        Check if a given dataset name exists as a custom dataset.
        
        :param dataset: The dataset name to check existence.
        """
        if category is None:
            category = self.binubuo_config.get('DATABASE', 'use_standard_category_if_duplicate', fallback=None)
        if self.dataset_dict_cache == 0:
            # Only call if we have not cached already
            self.list_datasets(1)
            if self.resp.ok:
                pass
            else:
                self.logger.warning(self.error_string)
        d_exist = None
        for idx, val in enumerate(self.dict_cache["datasets"]):
                for key, value in val.items():
                    if key == "DATASET_WEBSERVICE_NAME":
                        if value.upper() == dataset.upper():
                            if category is None:
                                if self.dict_cache["datasets"][idx]["DATASET_TYPE_NAME"] == "Standard Dataset":
                                    d_exist = self.dict_cache["datasets"][idx]["DATASET_CATEGORY_NAME"]
                            else:
                                if self.dict_cache["datasets"][idx]["DATASET_TYPE_NAME"] == "Standard Dataset" and self.dict_cache["datasets"][idx]["DATASET_CATEGORY_NAME"].upper() == category.upper():
                                    d_exist = self.dict_cache["datasets"][idx]["DATASET_CATEGORY_NAME"]
        return d_exist

    def __print_dir_list(self, type_in="generators", only_cache=0):
        # Purify result only if we are getting from outside cache
        if (type_in == "generators" and self.generator_dict_cache == 0) or (type_in == "datasets" and self.dataset_dict_cache == 0):
            for standard_key in self.response_json:
                self.response_clean = self.response_json[standard_key]
                self.dict_cache[type_in] = self.response_clean
        else:
            # Dealing with an already cached request. Just load from cache
            self.response_clean = self.dict_cache[type_in]
        if type_in == "generators":
            if only_cache == 0:
                print("{:<20} {:<30} {:<60}".format('Category:', 'Function:', 'URL:'))
                print("{:<20} {:<30} {:<60}".format('===================', '=============================', '=========================================================='))
            for idx, val in enumerate(self.response_clean):
                for key, value in val.items():
                    if key == "GENERATOR_CATEGORY_NAME":
                        ws_cat = value
                    if key == "GENERATOR_WEBSERVICE_NAME":
                        ws_func = value
                if only_cache == 1:
                    self.generator_dict_cache = 1
                else:
                    api_avail = self.baseurl + "/generator/" + ws_cat.lower() + "/" + ws_func.lower()
                    print("{:<20} {:<30} {:<60}".format(ws_cat, ws_func, api_avail))
        elif type_in == "datasets":
            if only_cache == 0:
                print("{:<10} {:<20} {:<30} {:<60}".format('Type:', 'Category:', 'Dataset:', 'URL:'))
                print("{:<10} {:<20} {:<30} {:<60}".format('=========', '===================', '=============================', '=========================================================='))
            for idx, val in enumerate(self.response_clean):
                for key, value in val.items():
                    if key == "DATASET_TYPE_NAME":
                        ws_type = value.split(' ')[0]
                    if key == "DATASET_CATEGORY_NAME":
                        if value == "Custom":
                            ws_cat = ""
                        else:
                            ws_cat = value
                    if key == "DATASET_WEBSERVICE_NAME":
                        ws_func = value
                if only_cache == 1:
                    self.dataset_dict_cache = 1
                else:
                    if ws_type == "Custom":
                        api_avail = self.baseurl + "/data/custom/" + self.unique_url_path + "/" + ws_func.lower()
                    elif ws_type == "Standard":
                        api_avail = self.baseurl + "/data/standard/" + ws_cat + "/" + ws_func.lower()
                    print("{:<10} {:<20} {:<30} {:<60}".format(ws_type, ws_cat, ws_func, api_avail))


    def list_generators(self, only_cache=0):
        """
        Show a list of all known generators.
        
        :param only_cache: If set to 1, only cache will be updated. Nothing will be displayed.
        """
        self.category = None
        self.dataset_type = "/"
        rest_path = "generator/"
        query_string = {}
        if self.generator_dict_cache == 0:
            # Only call if we have not cached already
            self.call_binubuo(rest_path, query_string)
            if self.resp.ok:
                pass
            else:
                self.logger.warning(self.error_string)
        self.__print_dir_list("generators", only_cache)

    def list_datasets(self, only_cache=0):
        """
        Show a list of all known datasets.
        
        :param only_cache: If set to 1, only cache will be updated. Nothing will be displayed.
        """
        self.category = None
        self.dataset_type = "/"
        rest_path = "data/"
        query_string = {}
        if self.dataset_dict_cache == 0:
            # Only call if we have not cached already
            self.call_binubuo(rest_path, query_string)
            if self.resp.ok:
                pass
            else:
                self.logger.warning(self.error_string)
        self.__print_dir_list("datasets", only_cache)

    def generate(self, category, function):
        """
        Generate a value from one of the random data generators.
        
        :param category: The category the generator belongs to.
        :param function: The actual generator to get data from.
        """
        # Incase called directly
        self.category = "/generator/" + category
        rest_path = "/" + function
        query_string = {"rows": self.default_generator_rows}
        self.call_binubuo(rest_path, query_string)
        if self.resp.ok:
            self.get_generator_response_value()
            return self.generator_response_value
        else:
            return self.error_string

    def dataset(self, dataset_name, dataset_type="custom", dataset_category=None, response_type="list", **webargs):
        """
        Generate a set of rows from one of the datasets.
        
        :param dataset_name: The name of the dataset.
        :param dataset_type: The type of the dataset. Defaults to [custom]
        :param dataset_category: The category of the dataset. Used for standard datasets only.
        :param response_type: Choose if you want output as [list], tuple or json.
        """
        self.category = None
        if dataset_type.lower() == "custom":
            self.dataset_type = "/data/custom/" + self.unique_url_path
        elif dataset_type.lower() == "standard":
            self.dataset_type = "/data/standard/" + dataset_category
        rest_path = "/" + dataset_name
        query_string = {"rows": self.default_dataset_rows}
        # Add all custom URL parameters
        for param, value in webargs.items():
            self.logger.debug("Called with custom parameter: %s and with value: %s", param, value)
            query_string[param] = value
        self.call_binubuo(rest_path, query_string)
        if self.resp.ok:
            self.get_dataset_response_value(response_type)
            return self.dataset_response_value
        else:
            return self.error_string

    def dataset_to_file(self, dataset_name, file_name="same", dataset_type="custom", dataset_category=None):
        """
        Generate a set of rows from one of the datasets and write to a file.
        
        :param dataset_name: The name of the dataset.
        :param file_name: The name of the file. Defaults to same as dataset_name if not specified.
        :param dataset_type: The type of the dataset. Defaults to [custom]
        :param dataset_category: The category of the dataset. Used for standard datasets only.
        """
        self.m("Creating synthetic data to file, using [" + dataset_name + "] dataset.", tolog=True)
        self.category = None
        if file_name == "same":
            if(self.csv_set is None):
                self.file_name = dataset_name + ".json"
            else:
                self.file_name = dataset_name + ".csv"
        else:
            self.file_name = file_name
        if dataset_type == "custom":
            self.dataset_type = "/data/custom/" + self.unique_url_path
        elif dataset_type == "standard":
            self.dataset_type = "/data/standard/" + dataset_category.lower()
        rest_path = "/" + dataset_name.lower()
        query_string = {"rows": self.default_dataset_rows}
        self.call_binubuo_to_file(rest_path, query_string)
        self.m("Synthetic file [" + self.file_name + "] created successfully.", indent=True, tolog=True)

    def quick_fetch(self, columns="first_name,last_name,address,city", response_type="list"):
        """
        Quick fetch data based on a comma separated list of generators.
        
        :param columns: The list of generators separated by commas.
        :param response_type: Choose if you want output as [list], tuple or json.
        """
        self.logger.info("Quick fetch called with: %s", columns)
        self.category = None
        self.dataset_type = "/data/custom"
        rest_path = "/quick_fetch"
        query_string = {"rows": self.default_dataset_rows}
        query_string["cols"] = columns
        self.call_binubuo(rest_path, query_string)
        if self.resp.ok:
            self.qf = 1
            self.get_dataset_response_value(response_type)
            self.logger.info("After values looked at: %s", str(len(self.dataset_response_value)))
            self.qf = 0
            return self.dataset_response_value
        else:
            return self.error_string

    def quick_fetch_to_file(self, columns="first_name,last_name,address,city", file_name="same"):
        """
        Quick fetch data based on a comma separated list of generators directly into a file.
        
        :param columns: The list of generators separated by commas.
        :param file_name: Choose what name you want for the file. Defaults to the list of columns.
        """
        self.m("Creating synthetic data to file, using quickfetch.", tolog=True)
        self.category = None
        if file_name == "same":
            if(self.csv_set is None):
                self.file_name = "quick_fetch-" + columns.replace(',', '-') + ".json"
            else:
                self.file_name = "quick_fetch-" + columns.replace(',', '-') + ".csv"
        else:
            if(self.csv_set is None):
                if file_name.find('.json') < 0:
                    self.file_name = file_name + ".json"
            else:
                if file_name.find('.csv') < 0:
                    self.file_name = file_name + ".csv"
        self.dataset_type = "/data/custom"
        rest_path = "/quick_fetch"
        query_string = {"rows": self.default_dataset_rows}
        query_string["cols"] = columns
        self.call_binubuo_to_file(rest_path, query_string)
        self.m("Synthetic file [" + self.file_name + "] created successfully.", indent=True, tolog=True)

    def infer_generator(self, column_meta):
        """
        Based on metadata of a table column, infer what Binubuo generator has the best fit.
        
        :param column_meta: The metadata to infer from.
        """
        self.category = None
        self.dataset_type = "/binubuo-actions"
        rest_path = "/infer-column-generator"
        query_string = {}
        self.post_data = column_meta
        self.logger.debug("About to infer: %s", self.post_data)
        self.call_binubuo(rest_path, query_string, "POST")
        # Always POST responsibility to reset post_data
        self.post_data = None
        # Entire generator is in json reponse
        return self.response_json

    def create_dataset(self, dataset_name, dataset_meta):
        """
        Submit a Binubuo dataset JSON schema and create a dataset.
        
        :param dataset_name: The name of the dataset.
        :param dataset_meta: The JSON schema to build the dataset from.
        """
        self.m("Create dataset [" + dataset_name + "].", tolog=True)
        self.category = None
        self.dataset_type = "/"
        rest_path = "data/"
        query_string = {"schemaname": dataset_name}
        self.logger.info("About to post dataset: %s", dataset_name)
        self.logger.debug("Dataset create metadata: %s", dataset_meta)
        self.post_data = dataset_meta
        self.call_binubuo(rest_path, query_string, "POST")
        # Reset post immediately after call no matter the status
        self.post_data = None
        # After dataset is created, we make sure the dict is reset and updated.
        if self.resp.ok:
            self.dataset_dict_cache = 0
            self.list_datasets(1)
            self.m("Dataset [" + dataset_name + "] created successfully.", indent=True, tolog=True)
            api_avail = self.baseurl + "/data/custom/" + self.unique_url_path + "/" + dataset_name.lower()
            self.m("API endpoint deployed at: " + api_avail, indent=True, tolog=True)
        else:
            self.m("Dataset [" + dataset_name + "] creation failed. Please see log for details.", indent=True, tolog=True)

    def create_superset(self, superset_meta):
        """
        Submit a Binubuo superset JSON schema and create the superset.
        
        :param superset_meta: The JSON schema to build the superset from.
        """
        self.category = None
        self.dataset_type = "/binubuo-actions"
        rest_path = "/superset-definition"
        query_string = {}
        self.post_data = superset_meta
        self.logger.debug("About to send superset: %s", self.post_data)
        self.call_binubuo(rest_path, query_string, "POST")
        # Always POST responsibility to reset post_data
        self.post_data = None
        # Entire generator is in json reponse
        return self.response_json

    def get_superset(self, superset_name, scale=1):
        """
        Get the superset definition, with list of datasets, order and size
        
        :param superset_name: The name of the superset to fetch
        :param scale: the scale of the superset size. Defaults to [1]
        """
        self.category = None
        self.dataset_type = "/binubuo-actions"
        rest_path = "/superset-data"
        query_string = {"setname": superset_name}
        query_string["scale"] = scale
        self.call_binubuo(rest_path, query_string)
        if self.resp.ok:
            return self.response_json

    def create_session(self):
        """
        Get a session handle, that can be used for supersets
        """
        self.category = None
        self.dataset_type = "/binubuo-actions"
        rest_path = "/create-session"
        query_string = {}
        self.call_binubuo(rest_path, query_string)
        if self.resp.ok:
            return self.response_json

    def remove_session(self):
        """
        Get a session handle, that can be used for supersets
        """
        self.category = None
        self.dataset_type = "/binubuo-actions"
        rest_path = "/remove-session"
        query_string = {}
        self.call_binubuo(rest_path, query_string)
        if self.resp.ok:
            return self.response_json