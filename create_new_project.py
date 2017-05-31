import json
import sys
import os
import subprocess

def main(args):

    if len(args) < 3:
        print("Usage: %s /path/to/s2e/env <new_project_name> [-h] [-i IMAGE] [-d] [-s] [-f]" % args[0])
        sys.exit(1)
    
    s2e_env_path = os.path.realpath(args[1])
    project_name = args[2]
    
    # Check that the given S2E environment is legitimate
    if not os.path.isfile(os.path.join(s2e_env_path, 's2e.yaml')):
        print('ERROR: %s is not an S2E environment' % s2e_env_path)
        sys.exit(1)
    
    # Check that the given project exists in the environment
    project_path = os.path.join(s2e_env_path, 'projects', project_name)
    if os.path.isdir(project_path):
        print('ERROR: %s already exist as a project' % project_name)
        sys.exit(1)
        
    #TODO check that this works with len(args) < 3 
    create_project(s2e_env_path, project_name, args[3:])
    
    setup_paths(s2e_env_path, project_name)


def create_project(s2e_env_path, project_name, args_rem):
    #TODO change this to display custom help and to parse the arguments
    parsed_args = ""
    for arg in args_rem: 
        parsed_args += str(arg) + " "
    
    s2e_create_project_command = "s2e new_project -e " + s2e_env_path + " -n " + project_name + " " + parsed_args + " tutorial_binary/tutorial_binary"
    
    p = subprocess.Popen([s2e_create_project_command, ""], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    out, err = p.communicate()
    
    
    if(p.returncode != 0):
        print(out)
        print(err)
        print("")
        print("ERROR: unable to create new project")
        sys.exit(1)


def setup_paths(s2e_env_path, project_name):
    json_data = {"S2E_ENVIRONEMENT_FOLDER_PATH" : s2e_env_path,
                 "S2E_PROJECT_NAME" : project_name}
    
    with open("s2e_web/S2E_settings.json", "wb+") as json_file:
        json.dump(json_data, json_file)
    
if __name__ == '__main__':
    main(sys.argv)
