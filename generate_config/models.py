from __future__ import unicode_literals

from django.db import models

CLASS_NORMAL = "normal"
CLASS_ERROR = "error"
CLASS_INSIDE_DIV = "inside"
CLASS_LIST_ELEMENT_DIV = "list_element"


class S2ELaunchException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def generate_plugin_configuration_menu(plugins):
    html_output = ""
    
    for plugin in plugins:
        html_output += '<div id="'+ plugin["name"] + '" class="' + CLASS_NORMAL + '">\n'
        html_output += '<center><b>' +  plugin["name"] + '</b></center>\n'
        html_output += '<center>' + plugin["description"] + '</center><br>\n'
        
        config_option_len = len(plugin["configOption"])
        if(config_option_len == 0):
            html_output += '<label class="' + CLASS_NORMAL + '">This plugin as not configuration options.</label><br>\n'
        else:
            #For each attribute type, generate a way to select that type
            html_output += generate_html_per_type(plugin, plugin["configOption"])
        
        html_output += '</div>'
        
    return html_output

def generate_html_per_type(plugin, config_option, uniqueId = "", first_level=True):
    html_output = ""
    
    for attr_key, attr_value in config_option.items():
        html_output += '<p style="margin-left:10px"><b>' + attr_key + '</b> : ' + attr_value["description"] + '</p>'
        
        if (attr_value["type"] == "int"):
            html_output += '<input type="number" class="' + CLASS_NORMAL +'" name="' + plugin["name"] + ':' + attr_key + uniqueId + '">'
            
        elif(attr_value["type"] == "bool"):
            html_output += '<input type="radio" class="' + CLASS_NORMAL +'" name="' + plugin["name"] + ':' + attr_key + uniqueId + '" value="true" checked> True'
            html_output += '<input type="radio" class="' + CLASS_NORMAL +'" name="' + plugin["name"] + ':' + attr_key + uniqueId + '" value="false"> False'
        
        elif(attr_value["type"] == "string"):
            html_output += '<input type="text" class="' + CLASS_NORMAL +'" name="' + plugin["name"] + ':' + attr_key + uniqueId + '">'
        
        elif(attr_value["type"] == "list"):
            html_output += '<input type="button" class="' + CLASS_NORMAL +'" value="add ' + attr_key + '" onclick="' + plugin["name"] + "_" + attr_key + uniqueId + '()">'
            
            #need to escape the ending script tag if inside a script tag
            if(first_level):
                html_output += '<script type="text/javascript"> function ' + plugin["name"] + "_" + attr_key + uniqueId + "(){" + generate_list_javascript(plugin, attr_key, attr_value, first_level) + '}</script>'
            else :
                html_output += str('<script type="text/javascript"> alert("hello"); function ' + plugin["name"] + "_" + attr_key).encode("string-escape") + uniqueId + "(){" + generate_list_javascript(plugin, attr_key, attr_value, first_level) + '}<\/script>'
                
            html_output += '<div class="' + CLASS_INSIDE_DIV + '" id="div_'+ plugin["name"] + ':' + attr_key + uniqueId + '"></div>'
          
        else:
            html_output += '<label class="' + CLASS_ERROR +'">Unrecognized type:' + attr_value["type"] + '</label>'
        
    return html_output

#TODO put the name of the module and send it to the server
def generate_list_javascript(plugin, attr_key, attr_value, first_level=True):
    key_text = '<label class="' + CLASS_LIST_ELEMENT_DIV + '">Element Key : </label>' 
    key_label = '<input type="text" id="' + plugin["name"] + ":" + attr_key + '\'+uniqueId+\'" name="' + plugin["name"] + ":" + attr_key +'\'+uniqueId+\'" value="" />'
    div_inner_html = '<div class=' + CLASS_LIST_ELEMENT_DIV + '>'
    
    div_inner_html += generate_html_per_type(plugin, attr_value["content"], "'+uniqueId+'", False)
    
    div_inner_html += '</div>';    
    
    output = 'uniqueId = uniqueId + 1;'
    if(first_level):
        output += 'document.getElementById(\'div_' + plugin["name"] + ':' + attr_key + '\').innerHTML+=\'' + key_text + key_label + div_inner_html + '\';'
    else:
        #output += 'document.getElementById(\'div_' + plugin["name"] + ':' + attr_key + '\').append(\'' + key_text + key_label + div_inner_html + '\');'
        output += str('document.getElementById(\'div_' + plugin["name"] + ':' + attr_key).encode("string-escape") + "'+uniqueId+'" + str('\').append(\'' + key_text + key_label + div_inner_html + '\');').encode("string-escape")
        #output += 'document.getElementById(\'div_' + plugin["name"] + ':' + attr_key + "'+uniqueId+'" + '\').append(\'' + key_text + key_label + div_inner_html + '\');'        
    
    return output
    
    
        
        