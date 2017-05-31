import os

# Needs to be the S2E environement path
S2E_ENVIRONEMENT_FOLDER_PATH = "/home/davide/tmp/s2e/"


# The configuration file for the plugins    
S2E_PLUGIN_JSON_CONFIG_FILE = "result.json"

S2E_PROJECT_FOLDER_PATH = os.path.join(S2E_ENVIRONEMENT_FOLDER_PATH, 'projects')
S2E_BINARY_FOLDER_PATH = os.path.join(S2E_ENVIRONEMENT_FOLDER_PATH, 'binary')

EXECUTION_TRACE_PARSER_SCRIPT_PATH = os.path.join(os.getcwd(), "tools/execution_tracer/execution_trace_parser.py")
#S2E_ENV_CONFIG_LUA_NAME = "s2e-config.lua"

#S2E_BINARY_FILE_NAME = "tutorial_binary"

#S2E_BINARY_PATH = os.path.join(S2E_PROJECT_FOLDER_PATH, S2E_PROJECT_NAME, S2E_BINARY_FILE_NAME)
#S2E_CONFIG_LUA_PATH = os.path.join(S2E_PROJECT_FOLDER_PATH, S2E_PROJECT_NAME, S2E_ENV_CONFIG_LUA_NAME)