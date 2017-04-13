//setup the right menu according to the chechbox
var leftMenuChildren = document.getElementById("left-menu-div").children;
for(var i = 0; i < leftMenuChildren.length; ++i){
	if(leftMenuChildren[i].tagName == "INPUT"){
		if(leftMenuChildren[i].type == "hidden"){			
			leftMenuChildren[i].value = "";
		}else if(leftMenuChildren[i].type == "checkbox"){
			leftMenuChildren[i].checked = false;			
		}
	}
}

function generatePluginConfigOption(plugin){
	var inside_div = document.createElement("div");
	inside_div.id = plugin["name"];
	inside_div.className = "normal";
	inside_div.style.display="none"
	
	var plugin_name = document.createElement("center");
	plugin_name.innerHTML = "<b>" + plugin["name"] + "</b>";
	inside_div.appendChild(plugin_name);
	
	var plugin_description = document.createElement("center");
	plugin_description.innerHTML = plugin["description"];
	inside_div.appendChild(plugin_description);   

	var config_body;
	if($.isEmptyObject(plugin["configOption"])){
		config_body = document.createElement("label");
		config_body.innerHTML = "This plugin as not configuration options."
	}else{
		config_body = document.createElement("div");
		config_body.className = "normal";
		generate_html_per_type(config_body, plugin, plugin["configOption"]); 
	}
	inside_div.appendChild(config_body);   

	document.getElementById("right-menu-div").append(inside_div);
}

function generate_html_per_type(parent, plugin, config_option){
	$.each(config_option, function(attr_key, attr_value){
		var header = document.createElement("p");
		header.className = "normal";
		header.innerHTML = "<b>" + attr_key + "</b> :" + attr_value["description"];
		parent.appendChild(header);	
		
		if(attr_value["type"] == "int"){
			generate_html_for_int(parent, plugin["name"], attr_key);
		}else if(attr_value["type"] == "bool"){
			generate_html_for_bool(parent, plugin["name"], attr_key);
		}else if(attr_value["type"] == "string"){
			generate_html_for_string(parent, plugin["name"], attr_key);
		}else if(attr_value["type"] == "list"){
			generate_html_for_list(parent, plugin, attr_key, attr_value);
		}else if(attr_value["type"] == "intList"){
			generate_html_for_intList(parent, plugin, attr_key, attr_value);
		}else{
			var error = document.createElement("label");
			error.className = "error";
			error.innerHTML = "Unrecognized type:" + attr_value["type"];  
			parent.appendChild(error);
		}
		
	})
}

function generate_html_for_int(parent, plugin_name, attr_key){
	var input = document.createElement("input");
	input.setAttribute("type", "number");
	input.className = "list_element";
	input.name = plugin_name + ":" + attr_key + uniqueId
	
	parent.appendChild(input);
}

function generate_html_for_bool(parent, plugin_name, attr_key){
	var label1 = document.createElement("label");
	var input1 = document.createElement("input");
	input1.setAttribute("type", "radio");
	input1.value = "true";
	input1.checked = "checked";
	input1.className = "normal";
	input1.name = plugin_name + ":" + attr_key + uniqueId;
	label1.appendChild(input1);
	label1.appendChild(document.createTextNode("True"));

	var label2 = document.createElement("label");
	var input2 = document.createElement("input");
	input2.setAttribute("type", "radio");
	input2.value = "false";
	input2.className = "normal";
	input2.name = plugin_name + ":" + attr_key + uniqueId;
	label2.appendChild(input2);
	label2.appendChild(document.createTextNode("False"));
	
	parent.appendChild(label1);
	parent.appendChild(label2);
}

function generate_html_for_string(parent, plugin_name, attr_key){
	var input = document.createElement("input");
	input.setAttribute("type", "text");
	input.className = "normal";
	input.name = plugin_name + ":" + attr_key + uniqueId
	
	parent.appendChild(input);
}

function generate_html_for_list(parent, plugin, attr_key, attr_value){
	var input = document.createElement("input");
	input.setAttribute("type", "button");
	input.className = "normal";
	input.value = "add " + attr_key;
	input.data_content = attr_value["content"];
	input.data_plugin = plugin;
	input.data_div = plugin["name"] + ":" + attr_key + uniqueId;
	input.onclick = function(){generate_html_for_list_onclick(this);};
	
	var div = document.createElement("div");
	div.className = "container";
	div.id = "div_" + plugin["name"] + ':' + attr_key + uniqueId;
	
	parent.appendChild(input);
	parent.appendChild(div);
}

function generate_html_for_list_onclick(button){
	var parent = document.getElementById("div_" + button.data_div);
		
	uniqueId++;
	
	var element_div = document.createElement("div");
	element_div.className = "list_element";
	
	generate_html_per_type(element_div, button.data_plugin, button.data_content);
	parent.appendChild(element_div);
}

function generate_html_for_intList(parent, plugin, attr_key, attr_value){
	var input = document.createElement("input");
	input.setAttribute("type", "button");
	input.className = "normal";
	input.value = "add " + attr_key;
	input.data_div = plugin["name"] + ":" + attr_key + uniqueId;
	input.data_name = plugin["name"] + ":" + attr_key;
	input.onclick = function(){generate_html_for_intList_onclick(this);};
	
	var div = document.createElement("div");
	div.className = "container";
	div.id = "div_" + plugin["name"] + ':' + attr_key + uniqueId;
	
	parent.appendChild(input);
	parent.appendChild(div);
}

function generate_html_for_intList_onclick(button){
	var parent = document.getElementById("div_" + button.data_div);
		
	uniqueId++;
	
	var input = document.createElement("input");
	input.setAttribute("type", "number");
	input.className = "normal"
	input.name = button.data_name + uniqueId;
	
	parent.appendChild(input);
}

function checkboxClickHandler(checkbox){
	
	var plugin = pluginMap.get(checkbox.name);
	plugin.isChecked = checkbox.checked;
	document.getElementById("checkbox_value_" + checkbox.name).value=checkbox.checked;

	
	checkboxChangeHandler(checkbox);
	
}

//Handle a checkbox change
function checkboxChangeHandler(checkbox){
	var plugin = pluginMap.get(checkbox.name);
	
	if(checkbox.checked){
		document.getElementById(checkbox.name).style.display="block";
		
		for(var i = 0; i < plugin.dependencies.length; ++i){
			var dep = pluginMap.get(plugin.dependencies[i]);
			dep.depCount += 1;
			
			var dependencyCheckbox = document.getElementById("checkbox_" + plugin.dependencies[i]);
			
			//disable checkbox and if state changed, handle change
			dependencyCheckbox.disabled = true;
			if(dependencyCheckbox.checked == false){
				dependencyCheckbox.checked = true;
				document.getElementById("checkbox_value_" + dependencyCheckbox.name).value=dependencyCheckbox.checked;

				checkboxChangeHandler(dependencyCheckbox);
			}
			
		}
		
	}else{
		document.getElementById(checkbox.name).style.display="none"
		
		for(var i = 0; i < plugin.dependencies.length; ++i){
			var dep = pluginMap.get(plugin.dependencies[i]);
			dep.depCount -= 1;
			
			var dependencyCheckbox = document.getElementById("checkbox_" + plugin.dependencies[i]);
			
			if(dep.depCount == 0){
				dependencyCheckbox.disabled = false;
				
				//change occured
				if(dependencyCheckbox.checked != dep.isChecked){
					dependencyCheckbox.checked = dep.isChecked;
					document.getElementById("checkbox_value_" + dependencyCheckbox.name).value=dependencyCheckbox.checked
					
					checkboxChangeHandler(dependencyCheckbox);
				}
			}
		}
	}
}


