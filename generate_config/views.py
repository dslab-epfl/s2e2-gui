from django.shortcuts import render
import s2e_web.S2E_settings as settings
import json
import os
from django.http import HttpResponseServerError, HttpResponse
from django.http.response import Http404
from upload.views import launch_S2E, write_file_to_disk_and_close
from upload.models import S2EOutput
from s2e_web import S2E_settings
from models import S2ELaunchException
import models

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
        try:
            # Generate an unique name
            request_data = json.loads(request.POST["data"]);
            tmpdir = "temp-dir/"
            
            selectedPlugins = getSelectedPlugins(request_data)
            selectedPluginsConfig = getPluginsConfig(request_data, selectedPlugins)
            
            generateConfigFile(selectedPlugins, selectedPluginsConfig, tmpdir)
            write_file_to_disk_and_close(tmpdir + settings.S2E_BINARY_FILE_NAME, request.FILES["binary_file"])
            
            has_s2e_error, s2e_error = launch_S2E(tmpdir)

            #TODO uncomment
            #os.remove(tmpdir + settings.S2E_CONFIG_LUA_FILE_NAME)
            os.remove(tmpdir + settings.S2E_BINARY_FILE_NAME)

            output = S2EOutput("s2e-last/")

            return render(request, 'display_log.html', {'warnings': output.warnings, 'messages' : output.messages, 'info' : output.info, 'debug' : output.debug, 'has_s2e_error': has_s2e_error, 's2e_error': s2e_error})
            


                        
        except AttributeError:
            return HttpResponseServerError()
        except S2ELaunchException as err:
            print(err)
            return HttpResponseServerError()
                
        
        return HttpResponse(status = 404)
    

            
    else:
        #TODO change to cache data
        #if(configure_plugins_html == None):
        configure_plugins_html = render(request, 'configure_plugins.html', {'plugins': plugins, 'pluginsJson': json.dumps(plugins)})
        
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
    # TODO add more options
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
    # add BaseInstructions to the list
    configFileContent += '\t "BaseInstructions" ' + "\n"
    
    configFileContent += "}\n\n"
    
    
    configFileContent += generate_plugins_configurations(selectedPluginsConfig)
            
    configFileContent += generate_HostFiles_config(tmpdir)
    
    write_string_to_disk_and_close(tmpdir + settings.S2E_CONFIG_LUA_FILE_NAME, configFileContent)
    
    
def generate_HostFiles_config(tmpdir):
    configContent = ""
    configContent += "pluginsConfig.HostFiles = {\n"
    configContent += "\t baseDirs = {\"" + S2E_settings.S2E_ANALYSIS_ROOT_DIR + tmpdir + "\"}\n"
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
    
#TODO make recursive
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
    

def write_string_to_disk_and_close(path, string):
    with open(path, 'wb+') as destination:
            destination.write(string)
    destination.close()
    
            
