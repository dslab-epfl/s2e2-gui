from __future__ import unicode_literals

from django.db import models

CLASS_NORMAL = "normal"
CLASS_ERROR = "error"
CLASS_INSIDE_DIV = "inside"
CLASS_LIST_ELEMENT_DIV = "list_element"


def generate_plugin_configuration_menu(plugins):
    html_output = ""
    
    for plugin in plugins:
        html_output += '<div id="'+ plugin["name"] + '" class="' + CLASS_NORMAL + '">\n'
        html_output += '<center><b>' +  plugin["name"] + '</b></center>\n'
        html_output += '<center>' + plugin["description"] + '</center><br>\n'
        
        config_option_len = len(plugin["configOption"])
        if(len == 0):
            html_output += '<label class="' + CLASS_NORMAL + '">This plugin as not configuration options.</label><br>\n'
        else:
            #For each attribute type, generate a way to select that type
            for attr_key, attr_value in plugin["configOption"].items():
                html_output += '<p style="margin-left:10px"><b>' + attr_key + '</b> : ' + attr_value["description"] + '</p>\n'
                
                if (attr_value["type"] == "int"):
                    html_output += '<input type="number" class="' + CLASS_NORMAL +'" name="' + plugin["name"] + ':' + attr_key + '">\n'
                    
                elif(attr_value["type"] == "bool"):
                    html_output += '<input type="radio" class="' + CLASS_NORMAL +'" name="' + plugin["name"] + ':' + attr_key + '" value="true" checked> True\n'
                    html_output += '<input type="radio" class="' + CLASS_NORMAL +'" name="' + plugin["name"] + ':' + attr_key + '" value="false"> False\n'
                
                elif(attr_value["type"] == "string"):
                    html_output += '<input type="text" class="' + CLASS_NORMAL +'" name="' + plugin["name"] + ':' + attr_key + '">\n'
                
                elif(attr_value["type"] == "list"):
                    html_output += '<input type="button" class="' + CLASS_NORMAL +'" value="add ' + attr_key + '" onclick="' + plugin["name"] + "_" + attr_key + '()">\n'
                    html_output += '<script type="text/javascript"> function ' + plugin["name"] + "_" + attr_key + "(){" + generate_list_javascript(plugin, attr_key, attr_value) + '}</script>'
                    html_output += '<div class="' + CLASS_INSIDE_DIV + '" id="div_'+ plugin["name"] + ':' + attr_key + '"></div>'
                  
                else:
                    html_output += '<label class="' + CLASS_ERROR +'">Unrecognized type:' + attr_value["type"] + '</label>\n'
        
        html_output += '</div>'
        
    return html_output

#TODO put the name of the module and send it to the server
def generate_list_javascript(plugin, attr_key, attr_value):
    div_inner_html = '<div class=' + CLASS_LIST_ELEMENT_DIV + '>'
    
    for content_key, content_value in attr_value["content"].items():
        div_inner_html += '<p style="margin-left:10px"><b>' + content_key + '</b> : ' + content_value["description"] + '</p>'
        
        if (content_value["type"] == "int"):
            div_inner_html += '<input type="number" class="' + CLASS_NORMAL +'" name="' + plugin["name"] + ':' + content_key + '">'
            
        elif(content_value["type"] == "bool"):
            div_inner_html += '<input type="radio" class="' + CLASS_NORMAL +'" name="' + plugin["name"] + ':' + content_key + '" value="true" checked> True'
            div_inner_html += '<input type="radio" class="' + CLASS_NORMAL +'" name="' + plugin["name"] + ':' + content_key + '" value="false"> False'
        
        elif(content_value["type"] == "string"):
            div_inner_html += '<input type="text" class="' + CLASS_NORMAL +'" name="' + plugin["name"] + ':' + content_key + '">'
        
        elif(content_value["type"] == "list"):
            div_inner_html += '<input type="button" class="' + CLASS_NORMAL +'" value="add ' + content_key + '" onclick="' + generate_list_javascript(plugin, content_key, content_value) + '">'
            div_inner_html += '<div class="' + CLASS_INSIDE_DIV + '" id="div_'+ plugin["name"] + ':' + content_key + '"></div>'
          
        else:
            div_inner_html += '<label class="' + CLASS_ERROR +'">Unrecognized type:' + content_value["type"] + '</label>'
    div_inner_html += '</div>';    
    
    
    output = ""
    output += "document.getElementById('div_" + plugin["name"] + ":" + attr_key + "').innerHTML+='" + div_inner_html + "';"
    
    return output
    
    
        
        