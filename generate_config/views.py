from django.shortcuts import render
import s2e_web.S2E_settings as settings
import json
import os
from django.http import HttpResponseServerError, HttpResponse
from django.http.response import Http404
from upload.views import launch_S2E, write_file_to_disk_and_close
from upload.models import S2EOutput
from s2e_web import S2E_settings
import models

plugins = None
configure_plugins_html = None

def configurePlugins(request):
    global plugins
        
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
                
        
        return HttpResponse(status = 404)
    

            
    else:
        #TODO need to cache the resulting page and plugins config
        if(configure_plugins_html == None):
            configure_plugins_html = render(request, 'configure_plugins.html', {'plugins': plugins, 'configuration_menu' : (models.generate_plugin_configuration_menu(plugins))})
        
        return configure_plugins_html

def getPluginsConfig(request, selectedPlugins):
    pluginsConfig = {}
    
    for plugin in selectedPlugins:
        tmpPluginConfig = {}
        for attrConfig in plugin["configOption"]:
            tmpPluginConfig[attrConfig] = request.POST.get(plugin["name"] + ":" + attrConfig)
        
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
    configFileContent += '\t "HostFiles" ' + "\n"
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
                if(index == attributeLen - 1):
                    configContent += "\t" + configKey + " = " + configValue +  "\n"
                else:
                    configContent += "\t" + configKey + " = " + configValue +  ",\n"
                    
            
            configContent += "}\n\n"
    
    return configContent
    
def write_string_to_disk_and_close(path, string):
    with open(path, 'wb+') as destination:
            destination.write(string)
    destination.close()
    
            
