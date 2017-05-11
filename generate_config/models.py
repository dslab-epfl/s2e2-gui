from __future__ import unicode_literals

from django.db import models
import subprocess
import s2e_web.S2E_settings as settings


class S2ELaunchException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
    
def generate_plugin_specific_output(selected_plugins):
    output = ""
    
    return output

def generate_stats(s2e_out_dir):
    stats = None
    with open(s2e_out_dir + "run.stats", 'r') as destination:
        stats = destination.read()
        
    return stats
        
def generate_lcov_files(s2e_out_dir):
    generate_coverage_file = "s2e coverage lcov binary"
    p = subprocess.Popen([generate_coverage_file, ""], shell=True, cwd=settings.S2E_ENVIRONEMENT_FOLDER_PATH)
    p.communicate()
    
    if(p.returncode != 0):
        print("error in coverage gen")
        return
    
    generate_lcov_command = "genhtml -o lcov_html coverage.info"
    p = subprocess.Popen([generate_lcov_command, ""], shell=True, cwd=settings.S2E_PROJECT_FOLDER_PATH + settings.S2E_BINARY_FILE_NAME + "/s2e-last")
    p.communicate()
    
    if(p.returncode != 0):
        print("error in html gen")
    

def get_lcov_path():
    return settings.S2E_BINARY_FILE_NAME + "/s2e-last/lcov_html/index.html"