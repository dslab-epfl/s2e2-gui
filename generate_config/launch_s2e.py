import s2e_web.S2E_settings as settings
import shutil
import subprocess
import os
import signal
from threading import Timer


def launch_s2e(tmpdir, timeout):
    
    s2e_command = "sh " + settings.S2E_PROJECT_FOLDER_PATH + settings.S2E_BINARY_FILE_NAME  + "/launch-s2e.sh"
    shutil.copyfile(tmpdir + settings.S2E_CONFIG_LUA_FILE_NAME, settings.S2E_PROJECT_FOLDER_PATH + settings.S2E_BINARY_FILE_NAME + "/" + settings.S2E_ENV_CONFIG_LUA_NAME)
    shutil.copyfile(tmpdir + settings.S2E_BINARY_FILE_NAME, settings.S2E_PROJECT_FOLDER_PATH + settings.S2E_BINARY_FILE_NAME + "/" + settings.S2E_BINARY_FILE_NAME)
    
    
    kill = lambda process: kill_process(process)
    
    p = subprocess.Popen([s2e_command, ""], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=settings.S2E_PROJECT_FOLDER_PATH + settings.S2E_BINARY_FILE_NAME)
    p.killed_by_timeout = False
    
    my_timer = Timer(int(timeout), kill, [p])
     
    out, err = "", ""
    try:
        my_timer.start()
        out, err = p.communicate()
    finally:
        my_timer.cancel()
    
        
    return p.returncode, out + err, p.killed_by_timeout
    
    
def kill_process(process):
    print("process killed after timeout")

    os.kill(process.pid, signal.SIGTERM)
    
    #this is a hack ask why this works
    os.kill(process.pid + 3, signal.SIGTERM)
    
    process.returncode = 0;
    process.killed_by_timeout = True


def write_file_to_disk_and_close(path, w_file):
    with open(path, 'wb+') as destination:
        for chunk in w_file.chunks():
            destination.write(chunk)
    destination.close()
    w_file.close()
    
    