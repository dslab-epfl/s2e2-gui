from __future__ import unicode_literals

from django.db import models
import subprocess
import s2e_web.S2E_settings as settings
import os
from xdiagnose.utils.url_io import data_from_url
import json
import utils
import tools.execution_tracer.execution_trace_parser as execution_parser

class S2EOutput():
    """
    This class is used to get the log files from disk
    """
    def __init__(self, s2e_out_dir):
        self.warnings = ""
        self.info = ""
        self.debug = ""
            
        with open(os.path.join(s2e_out_dir, "warnings.txt"), 'r') as destination:
            self.warnings = destination.read()
        with open(os.path.join(s2e_out_dir, "info.txt"), 'r') as destination:
            self.info = destination.read()
        with open(os.path.join(s2e_out_dir, "debug.txt"), 'r') as destination:
            self.debug = destination.read()

class S2ELaunchException(Exception):
    """
    Custom exception in case S2E fails to launch
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
    
def generate_stats(s2e_out_dir):
    """
    Reads the stats from the s2e output directory
    """
    stats = None
    try:
        with open(os.path.join(s2e_out_dir, "run.stats"), 'r') as destination:
            stats = destination.read()
    except IOError:
        return "No stats found"
        
    return stats
        
def generate_lcov_files(s2e_out_dir, binary_name):
    """
    Generate the line coverage files for the given output directory
    """
    generate_coverage_file = "s2e coverage lcov " + binary_name
    p = subprocess.Popen([generate_coverage_file, ""], shell=True, cwd=settings.S2E_ENVIRONMENT_FOLDER_PATH)
    p.communicate()
    
    if(p.returncode != 0):
        print("error in coverage generation")
        return
        
    generate_lcov_command = "genhtml -o lcov_html coverage.info"
    p = subprocess.Popen([generate_lcov_command, ""], shell=True, cwd=s2e_out_dir)
    p.communicate()
    
    if(p.returncode != 0):
        print("error in html generation")
    

def get_lcov_path(s2e_out_dir, s2e_num, binary_name):
    """
    If the line coverage report exist,
    gets the line coverage path to the index.html file.
    """
    line_cov_path = binary_name + "/s2e-out-" + str(s2e_num) + "/lcov_html/index.html"
    has_line_cov = os.path.isfile(os.path.join(settings.S2E_PROJECT_FOLDER_PATH, line_cov_path))
    
    return has_line_cov, line_cov_path

def generate_icount_files(s2e_out_dir):
    """
    Generate the instruction count data for the given output directory.
    """    
    file_path = os.path.join(s2e_out_dir, "ExecutionTracer.dat")
    
    if(not os.path.exists(file_path)):
        return
    
    data = execution_parser.main(file_path)
        
    if(data == None):
        return 
    
    instruction_count = {}
    runtimes = {}
    data_last_timestamp = 0
    timestamp_after_switch = 0
    for i in range(len(data)):
        data_icount = data[i]["iCount"]
        data_current_timestamp = data_icount["timestamp"]
        data_current_state = data_icount["stateId"]
        data_current_count = data_icount["count"]
        
        instruction_count[data_current_state] = data_current_count
            
        if(data_current_timestamp < data_last_timestamp):
            print("assumption wrong on timestamp : " + data_current_timestamp)
        
        data_last_timestamp = data_current_timestamp
        
    print(instruction_count)    
    
    return instruction_count
    
    
class CustomAnalysisData():
    """
    Class that stores all the custom data used for the GUI.
    """
    GUI_FILE_NAME = "GUI_data.json"
    
    def __init__(self, killed_by_timeout = False, has_s2e_error = False, function_paths = []):
        self.data = {"killed_by_timeout" : killed_by_timeout, "has_s2e_error" : has_s2e_error, "function_paths" : function_paths}
        
    def save_to_disk(self, s2e_output_dir):
        """
        Saves the data to the disk
        """
        utils.write_string_to_disk_and_close(os.path.join(s2e_output_dir, CustomAnalysisData.GUI_FILE_NAME), json.dumps(self.data))
        
    def get_from_disk(self, s2e_output_dir):
        """
        Gets the data from the disk
        """
        with open(os.path.join(s2e_output_dir, CustomAnalysisData.GUI_FILE_NAME), 'r') as destination:
            self.data = json.load(destination)
        
        