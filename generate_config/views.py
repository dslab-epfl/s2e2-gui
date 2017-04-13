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
            tmpdir = "temp-dir/"
            
            selectedPlugins = getSelectedPlugins(request)
            selectedPluginsConfig = getPluginsConfig(request, selectedPlugins)
            
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
        configure_plugins_html = render(request, 'configure_plugins.html', {'plugins': plugins, 'pluginsJson': json.dumps(plugins)})
        #TODO need to cache the resulting page and plugins config
        if(configure_plugins_html == None):
            configure_plugins_html = render(request, 'configure_plugins.html', {'plugins': plugins, 'configuration_menu' : (models.generate_plugin_configuration_menu(plugins))})
        
        return configure_plugins_html

def getPluginsConfig(request, selectedPlugins):
    pluginsConfig = {}
    
    # TODO do it recursively to handle list of lists
    for plugin in selectedPlugins:
        tmpPluginConfig = {}
        for attrConfigKey, attrConfigValue in plugin["configOption"].items():
            if(attrConfigValue[TYPE_KEY] == LIST_TYPE):
                for key, value in request.POST.items():
                    listKey = plugin["name"] + ":" + attrConfigKey
                    if(key.startswith(listKey)):
                        uniqueId = key[len(listKey):]
                        if(uniqueId.isdigit()):
                            tmpContentConfig = {}
                            for contentKey, contentValue in attrConfigValue[CONTENT_KEY].items():
                                tmpContentConfig[contentKey] = request.POST.get(plugin["name"] + ":" + contentKey + uniqueId);
                                
                            tmpPluginConfig[value] = tmpContentConfig
            else:
                tmpPluginConfig[attrConfigKey] = request.POST.get(plugin["name"] + ":" + attrConfigKey)
        
        pluginsConfig[plugin["name"]] = tmpPluginConfig
        
    return pluginsConfig
    

def getSelectedPlugins(request):
    global plugins
    selectedPlugins = []
    
    for plugin in plugins:
        if("true" in request.POST.getlist(plugin["name"]) ):
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
            
            for index, (configKey, configValue) in enumerate(configs.items()):
                if(configKey == ""):
                    raise S2ELaunchException("configuration key is empty")
                    
                if type(configValue) is dict:
                    if(index == attributeLen - 1):
                        configContent += "\t" + str(configKey) + " = " + translate_dict_to_lua(configValue) + "\n"
                    else:
                        configContent += "\t" + str(configKey) + " = " + translate_dict_to_lua(configValue) + ",\n"
                else:
                    if(index == attributeLen - 1):
                        configContent += "\t" + str(configKey) + " = " + str(configValue) +  "\n"
                    else:
                        configContent += "\t" + str(configKey) + " = " + str(configValue) +  ",\n"
                    
            
            configContent += "}\n\n"
    
    return configContent
    
#TODO make recursive
def translate_dict_to_lua(dictionary):
    output = "{"
    dictionaryLen = len(dictionary.items())
    
    for index, (key, value) in enumerate(dictionary.items()):  
        if(key == ""):
            raise S2ELaunchException("configuration key is empty")
                  
        if(index == dictionaryLen - 1):
            output += "\t" + str(key) + " = " + str(value) + "\n"
        else:
            output += "\t" + str(key) + " = " + str(value) + ",\n"
            
    output += "}\n"
    
    return output
    

def write_string_to_disk_and_close(path, string):
    with open(path, 'wb+') as destination:
            destination.write(string)
    destination.close()
    
            
