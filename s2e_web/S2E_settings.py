import os
import settings
from django.conf import settings

# Needs to an S2E environement path
S2E_ENVIRONMENT_FOLDER_PATH = settings.S2E_ENVIRONMENT_FOLDER_PATH

# The configuration file for the plugins    
S2E_PLUGIN_JSON_CONFIG_FILE =  os.path.join(os.getcwd(), "result.json")

S2E_PROJECT_FOLDER_PATH = os.path.join(S2E_ENVIRONMENT_FOLDER_PATH, 'projects')
S2E_BINARY_FOLDER_PATH = os.path.join(S2E_ENVIRONMENT_FOLDER_PATH, 'binary')

EXECUTION_TRACE_PARSER_SCRIPT_PATH = os.path.join(os.getcwd(), "tools/execution_tracer/execution_trace_parser.py")
