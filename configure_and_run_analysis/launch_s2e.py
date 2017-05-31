import s2e_web.S2E_settings as settings
import shutil
import subprocess
import hashlib
import os
import signal
from threading import Timer
from display_all_analysis.models import Analysis


def launch_s2e(timeout, project_name):
    """
    Launch the s2e analysis with a given timeout 
    """
        
    s2e_command = "sh " + os.path.join(settings.S2E_PROJECT_FOLDER_PATH, project_name)  + "/launch-s2e.sh"
    #shutil.copyfile(tmpdir + settings.S2E_CONFIG_LUA_FILE_NAME, settings.S2E_CONFIG_LUA_PATH)
    #shutil.copyfile(tmpdir + settings.S2E_BINARY_FILE_NAME, settings.S2E_BINARY_PATH)
    
    kill = lambda process: kill_process(process)
    
    p = subprocess.Popen([s2e_command, ""], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.join(settings.S2E_PROJECT_FOLDER_PATH, project_name))
    p.killed_by_timeout = False
    
    my_timer = Timer(int(timeout), kill, [p])
     
    out, err = "", ""
    try:
        my_timer.start()
        out, err = p.communicate()
    finally:
        my_timer.cancel()
    
        
    return p.returncode, p.killed_by_timeout
    
    
def kill_process(process):
    """
    Kill the process if it exceed the time limit
    """
    print("Process killed after timeout")

    os.kill(process.pid, signal.SIGTERM)
    
    #XXX This is required to kill the qemu process, but should be fixed in something more reliable
    os.kill(process.pid + 3, signal.SIGTERM)
    
    process.returncode = 0;
    process.killed_by_timeout = True

def create_new_s2e_project(binary_path):
    s2e_create_project_command = "s2e new_project -e " + settings.S2E_ENVIRONEMENT_FOLDER_PATH + " " + binary_path
    
    p = subprocess.Popen([s2e_create_project_command, ""], shell=True)
    
    p.communicate()
    