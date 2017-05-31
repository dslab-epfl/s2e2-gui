import os

# Needs to an S2E environement path
S2E_ENVIRONEMENT_FOLDER_PATH = "/home/davide/tmp/s2e/"


# The configuration file for the plugins    
S2E_PLUGIN_JSON_CONFIG_FILE = "result.json"

S2E_PROJECT_FOLDER_PATH = os.path.join(S2E_ENVIRONEMENT_FOLDER_PATH, 'projects')
S2E_BINARY_FOLDER_PATH = os.path.join(S2E_ENVIRONEMENT_FOLDER_PATH, 'binary')

EXECUTION_TRACE_PARSER_SCRIPT_PATH = os.path.join(os.getcwd(), "tools/execution_tracer/execution_trace_parser.py")
