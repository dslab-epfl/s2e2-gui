from django.shortcuts import render
import s2e_web.S2E_settings as settings
import json
import os
from django.http import HttpResponseServerError, HttpResponse
from django.http.response import Http404
from launch_s2e import launch_s2e, write_file_to_disk_and_close
from s2e_web import S2E_settings
from models import S2ELaunchException
import models
import utils
from django.utils.encoding import smart_text

LIST_TYPE = "list"
BOOLEAN_TYPE = "bool"
INT_TYPE = "int"
STRING_TYPE = "string"
STRING_LIST_TYPE = "stringList"
ACCEPTED_TYPES = [BOOLEAN_TYPE, INT_TYPE, STRING_TYPE, STRING_LIST_TYPE, LIST_TYPE]

TYPE_KEY = "type"
DESCRIPTION_KEY = "description"
CONTENT_KEY = "content"


plugins = None
configure_plugins_html = None

def configurePlugins(request):
    global plugins
    global configure_plugins_html
    
        
    if(plugins == None):
        with open(settings.S2E_PLUGIN_JSON_CONFIG_FILE, "r") as jsonFile:
            plugins = json.load(jsonFile)
    
    if (request.method == 'POST'):
        
        if(request.POST["method"] == "get_last_result"):
            
            s2e_has_error = 0;
            s2e_output_dir = settings.S2E_PROJECT_FOLDER_PATH + settings.S2E_BINARY_FILE_NAME + "/s2e-last/"
            
            custom_data = models.CustomAnalysisData()
            custom_data.get_from_disk(s2e_output_dir)
                        
            return render_output(s2e_has_error, "", s2e_output_dir, custom_data.data, request)
            
            
        elif(request.POST["method"] == "run_s2e"):
            
            try:
                # Generate an unique name
                timeout = request.POST["timeout"]                
                request_data = json.loads(request.POST["data"]);
                tmpdir = "temp-dir/"
                                
                selectedPlugins = getSelectedPlugins(request_data)
                selectedPluginsConfig = getPluginsConfig(request_data, selectedPlugins)
                
                generateConfigFile(selectedPlugins, selectedPluginsConfig, tmpdir)
                write_file_to_disk_and_close(tmpdir + settings.S2E_BINARY_FILE_NAME, request.FILES["binary_file"])
                
                has_s2e_error, s2e_error, killed_by_timeout = launch_s2e(tmpdir, timeout)
                
                os.remove(tmpdir + settings.S2E_CONFIG_LUA_FILE_NAME)
                os.remove(tmpdir + settings.S2E_BINARY_FILE_NAME)
                
                s2e_output_dir = settings.S2E_PROJECT_FOLDER_PATH + settings.S2E_BINARY_FILE_NAME + "/s2e-last/"
                
                models.generate_lcov_files(s2e_output_dir)
                
                custom_data = models.CustomAnalysisData(killed_by_timeout)
                custom_data.save_to_disk(s2e_output_dir)            
                
                return render_output(has_s2e_error, s2e_error, s2e_output_dir, custom_data.data, request)
                            
            except AttributeError as err:
                print(err)
                return HttpResponseServerError()
            except S2ELaunchException as err:
                print(err)
                return HttpResponseServerError()
                
        
        return HttpResponse(status = 404)
    

            
    else:
        #TODO change to cache data
        #if(configure_plugins_html == None):
        configure_plugins_html = render(request, 'configure_plugins/index.html', {'plugins': plugins, 'pluginsJson': json.dumps(plugins)})
        
        return configure_plugins_html

def getPluginsConfig(request_data, selectedPlugins):    
    # TODO make checks to disallow bad configs
    
        
    return request_data
    

def getSelectedPlugins(request_data):
    global plugins
    selectedPlugins = []
    
    for plugin in plugins:
        if(plugin["name"] in request_data.keys()):
            selectedPlugins.append(plugin)
            
    return selectedPlugins
    

def generateConfigFile(selectedPlugins, selectedPluginsConfig, tmpdir):
    # Generate the base s2e config
    configFileContent = "s2e = {\n"
    configFileContent += "\t kleeArgs = {}\n"
    configFileContent += "}\n\n"
    
    # Generate the plugin list
    configFileContent += "plugins = {\n"
    
    for plugin in selectedPlugins:
        configFileContent += '\t"' + plugin["name"] + '"' + ",\n"
    
    
    # add the HostFiles plugin, it is used to run the analysis
    configFileContent += '\t "HostFiles" ' + ",\n"
    # add the Vmi plugin, it is used to run the analysis
    configFileContent += '\t "Vmi" ' + ",\n"
    # add BaseInstructions to the list
    configFileContent += '\t "BaseInstructions" ' + "\n"
    
    configFileContent += "}\n\n"
    
    
    configFileContent += generate_plugins_configurations(selectedPluginsConfig)
    configFileContent += generate_HostFiles_config(tmpdir)
    configFileContent += generate_Vmi_config(tmpdir)
    configFileContent += add_linux_monitor_config()
    
    utils.write_string_to_disk_and_close(tmpdir + settings.S2E_CONFIG_LUA_FILE_NAME, configFileContent)

def add_linux_monitor_config():
    out =  "dofile('library.lua')\n"
    out +=  'add_plugin("LinuxMonitor")\n'
    out += 'pluginsConfig.LinuxMonitor = {\n'
    out += '-- Kill the execution state when it encounters a segfault\n'
    out += '    terminateOnSegFault = true,\n'
    out += '-- Kill the execution state when it encounters a trap\n'
    out += 'terminateOnTrap = true,\n'
    out += '}\n'    
    return out

    
def generate_HostFiles_config(tmpdir):
    configContent = ""
    configContent += "pluginsConfig.HostFiles = {\n"
    configContent += "\t baseDirs = {\"" + S2E_settings.S2E_PROJECT_FOLDER_PATH + S2E_settings.S2E_BINARY_FILE_NAME + "\"},\n"
    configContent += "\t allowWrite = true,\n"
    configContent += "}\n"
    
    return configContent

def generate_Vmi_config(tmpdir):
    configContent = ""
    configContent += "pluginsConfig.Vmi = {\n"
    configContent += "\t baseDirs = {\"" + S2E_settings.S2E_PROJECT_FOLDER_PATH + S2E_settings.S2E_BINARY_FILE_NAME + "\"}\n"
    configContent += "}\n"
    
    return configContent
    
def generate_plugins_configurations(selectedPluginsConfig):
    configContent = ""
    configContent += "pluginsConfig = {}\n\n"
    for plugin, configs in selectedPluginsConfig.items():
        attributeLen = len(configs.items())
        if(attributeLen > 0):
            configContent += "pluginsConfig." + plugin + " = {\n"
            
            configContent += translate_to_lua(configs)
            
            configContent += "}\n\n"
    
    return configContent
    

def translate_to_lua(configs, level=1):
    output = ""
    configsLen = len(configs.items())
    
    for index, (configKey, configValue) in enumerate(configs.items()):
        if(configKey == ""):
            raise S2ELaunchException("configuration key is empty")
            
        for i in range(level):
            output += "\t"    
        
        output += str(configKey) + "="
        
        if type(configValue) is dict:
            output += "{\n" + translate_to_lua(configValue, level + 1)
            for i in range(level):
                output += "\t"
            output += "}"
            
        elif type(configValue) is list:
            listLen = len(configValue)
            output += " {"
            for listIndex, listElem in enumerate(configValue):
                output += listElem
                if(listIndex != listLen - 1):
                    output += ", "
            output += "}"
        
        else:
            output += str(configValue)
            
        if(index != configsLen - 1):
            output += ","
        
        output += "\n"
        
        
    return output
    
           
def render_output(has_s2e_error, s2e_error, s2e_output_dir, custom_data, request):
    output = models.S2EOutput(has_s2e_error, s2e_output_dir)
    stats = models.generate_stats(s2e_output_dir)     
    has_coverage, line_coverage_path = models.get_lcov_path()
    icount = models.generate_icount_files(s2e_output_dir)
    
    html_data_dictionary =  {'warnings': smart_text(output.warnings, encoding="utf-8", errors="ignore"), 
                        'info' : smart_text(output.info, encoding="utf-8", errors="ignore"), 
                        'debug' : smart_text(output.debug, encoding="utf-8", errors="ignore"), 
                        'has_s2e_error': has_s2e_error != 0, 
                        's2e_error': s2e_error,
                        'line_coverage_exist' : has_coverage,
                        'line_coverage_report_path' : line_coverage_path,
                        'custom_data' : custom_data}
    
    html_page = str(render(request, 'display_log/index.html', html_data_dictionary))
    
    return HttpResponse(json.dumps({"stats" : smart_text(stats, encoding="utf-8", errors="ignore"), 
                                    "html" :  html_page[39:],
                                    "icount" : icount})) 


 
