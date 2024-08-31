from genericpath import isfile
import pkg_resources
import os
import configparser
from pathlib import Path

from .binubuo import binubuo
from .BinubuoTemplate import BinubuoTemplate

config_exists = False
config_location = "In house"

# Check if we have configuration somewhere else than home directory
current_dir_obj = Path(os.getcwd())
current_dir_config = current_dir_obj / "binubuo.conf"
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

if config_exists:
    binubuo_config = configparser.ConfigParser()
    binubuo_config.read(config_location)
else:
    binubuo_config = configparser.ConfigParser()
    binubuo_config['OUTPUTS'] = {'dependency_warnings': 'yes'}

# Get packages available for us. We need to check if the pre-requisites for the different database
# options are available when importing them.
pkgs_installed = {pkg.key for pkg in pkg_resources.working_set}

# Oracle requirements
oracle_required = {'cx-oracle'}
oracle_missing = oracle_required - pkgs_installed

if oracle_missing:
    if binubuo_config.get('OUTPUTS', 'dependency_warnings', fallback='yes') == 'yes':
        print("Oracle client not installed. Please install cx_Oracle for Oracle support.")
else:
    from .binubuoOracle import binubuoOracle

# Postgres requirements
postgres_required = {'psycopg2'}
postgres_missing = postgres_required - pkgs_installed

if postgres_missing:
    # Check for binary also
    postgres_bin_required = {'psycopg2-binary'}
    postgres_bin_missing = postgres_bin_required - pkgs_installed
    if postgres_bin_missing:
        if binubuo_config['OUTPUTS']['dependency_warnings'] == 'yes':
            print("Postgres client not installed. Please install Psycopg2 for Postgres support.")
    else:
        from .binubuoPostgres import binubuoPostgres
else:
    from .binubuoPostgres import binubuoPostgres

# yugabyte requirements
yugabyte_required = {'psycopg2'}
yugabyte_missing = yugabyte_required - pkgs_installed

if yugabyte_missing:
    # Check for binary also
    yugabyte_bin_required = {'psycopg2-binary'}
    yugabyte_bin_missing = yugabyte_bin_required - pkgs_installed
    if yugabyte_bin_missing:
        if binubuo_config['OUTPUTS']['dependency_warnings'] == 'yes':
            print("yugabyte client not installed. Please install Psycopg2 for YugabyteDB support.")
    else:
        from .binubuoYugabyte import binubuoYugabyte
else:
    from .binubuoYugabyte import binubuoYugabyte

# SQL Server requirements
sqlserver_required = {'pyodbc'}
sqlserver_missing = sqlserver_required - pkgs_installed

if sqlserver_missing:
    if binubuo_config['OUTPUTS']['dependency_warnings'] == 'yes':
        print("SQL Server client not installed. Please install pyodbc for SQL Server support.")
else:
    from .binubuoSQLServer import binubuoSQLServer

# Excel requirements
excel_required = {'openpyxl'}
excel_missing = excel_required - pkgs_installed

if excel_missing:
    if binubuo_config['OUTPUTS']['dependency_warnings'] == 'yes':
        print("Excel library not installed. Please install openpyxl for Excel support.")
else:
    from .binubuoExcel import binubuoExcel

# Always prepare CSV
from .binubuoCSV import binubuoCSV