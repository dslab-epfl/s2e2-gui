var unique_id = 0;
var is_analysis_launched = false;

/**
 * Generate a div with the options for the given plugin
 * 
 * @param plugin
 * 		The plugin we want to generate.
 * @returns void
 */
function generatePluginConfigOption(plugin){
	var inside_div = document.createElement("div");
	inside_div.id = plugin["name"];
	inside_div.className = "plugin_div";
	
	var plugin_name = document.createElement("H1");
	plugin_name.className = "right_menu_plugin_name";
	plugin_name.appendChild(document.createTextNode(plugin["name"]));
	inside_div.appendChild(plugin_name);
	
	var plugin_description = document.createElement("H3");
	plugin_description.className = "right_menu_plugin_description";
	plugin_description.appendChild(document.createTextNode(plugin["description"]));
	inside_div.appendChild(plugin_description);   

	var config_body;
	if($.isEmptyObject(plugin["configOption"])){
		config_body = document.createElement("label");
		config_body.className = "normal";
		config_body.innerHTML = "This plugin has no configuration option."
	}else{
		config_body = document.createElement("div");
		config_body.className = "normal";
		generate_html_per_type(config_body, plugin, plugin["configOption"]); 
	}
	inside_div.appendChild(config_body);   

	document.getElementById("right-menu-div").append(inside_div);
}

/**
 * Generate the html for the plugin given the type of the option.
 * 
 * @param parent
 * 		The object we want to append the data to.
 * @param plugin
 * 		The plugin we currently are generating the options of.
 * @param config_option
 * 		The current configuration option to decide the type of element to generate.
 * @returns void
 */
function generate_html_per_type(parent, plugin, config_option){
	$.each(config_option, function(attr_key, attr_value){
		var container_div = document.createElement("div");
		container_div.className = "right_menu_container";
		
		var header = document.createElement("span");
		header.className = "attribute_title";
		header.appendChild(document.createTextNode(attr_key + ":"));
		
		var header_descr = document.createElement("span");
		header_descr.className = "attribute_description";
		header_descr.appendChild(document.createTextNode(attr_value["description"]))
		header_descr.appendChild(document.createElement("BR"));
		
		container_div.appendChild(header_descr);
		container_div.appendChild(header);
		
		parent.appendChild(container_div);
		
		if(attr_value["type"] == "int"){
			generate_html_for_int(container_div, plugin["name"], attr_key);
		}else if(attr_value["type"] == "bool"){
			generate_html_for_bool(container_div, plugin["name"], attr_key);
		}else if(attr_value["type"] == "string"){
			generate_html_for_string(container_div, plugin["name"], attr_key);
		}else if(attr_value["type"] == "list"){
			generate_html_for_list(container_div, plugin, attr_key, attr_value);
		}else if(attr_value["type"] == "intList"){
			generate_html_for_intList(container_div, plugin, attr_key, attr_value);
		}else if(attr_value["type"] == "stringList"){
			generate_html_for_stringList(container_div, plugin, attr_key, attr_value);
		}else{
			var error = document.createElement("label");
			error.className = "error";
			error.innerHTML = "Unrecognized type:" + attr_value["type"];  
			container_div.appendChild(error);
		}
		
		parent.appendChild(document.createElement("BR"));
		
	})
}

/**
 * Generate the html in case the required option value is an int
 * @param parent
 * 		The element we want to append to.
 * @param plugin_name
 * 		The plugin name.
 * @param attr_key
 * 		The attribute key.
 * @returns
 */
function generate_html_for_int(parent, plugin_name, attr_key){
	var input = document.createElement("input");
	input.required = "required";
	input.setAttribute("type", "number");
	input.className = "normal";
	input.name = attr_key;
	input.data_key = attr_key;
	
	parent.appendChild(input);
}

/**
 * Generate the html in case the required option value is a boolean
 * @param parent
 * 		The element we want to append to.
 * @param plugin_name
 * 		The plugin name.
 * @param attr_key
 * 		The attribute key.
 * @returns
 */
function generate_html_for_bool(parent, plugin_name, attr_key){
	uniqueId++;
	
	var label1 = document.createElement("label");
	var input1 = document.createElement("input");
	input1.setAttribute("type", "radio");
	input1.value = "true";
	input1.checked = "checked";
	input1.className = "normal";
	input1.name = plugin_name + ":" + attr_key + uniqueId;
	input1.data_key = attr_key;
	label1.appendChild(input1);
	label1.appendChild(document.createTextNode("True"));

	var label2 = document.createElement("label");
	var input2 = document.createElement("input");
	input2.setAttribute("type", "radio");
	input2.value = "false";
	input2.className = "normal";
	input2.name = plugin_name + ":" + attr_key + uniqueId;
	input2.data_key = attr_key;
	label2.appendChild(input2);
	label2.appendChild(document.createTextNode("False"));
		
	parent.appendChild(label1);
	parent.appendChild(label2);
}

/**
 * Generate the html in case the required option value is a string
 * @param parent
 * 		The element we want to append to.
 * @param plugin_name
 * 		The plugin name.
 * @param attr_key
 * 		The attribute key.
 * @returns
 */
function generate_html_for_string(parent, plugin_name, attr_key){
	uniqueId++;
	
	var input = document.createElement("input");
	input.setAttribute("type", "text");
	input.className = "normal";
	input.required = "required";
	input.name = plugin_name + ":" + attr_key + uniqueId;
	input.data_key = attr_key;
	
	parent.appendChild(input);
}

/**
 * Generate the html in case the required option value is a list
 * @param parent
 * 		The element we want to append to.
 * @param plugin_name
 * 		The plugin name.
 * @param attr_key
 * 		The attribute key.
 * @returns
 */
function generate_html_for_list(parent, plugin, attr_key, attr_value){
	var input = document.createElement("input");
	input.setAttribute("type", "button");
	input.className = "normal";
	input.value = "add " + attr_key;
	input.data_content = attr_value["content"];
	input.data_plugin = plugin;
	input.data_div = plugin["name"] + ":" + attr_key + uniqueId;
	input.data_key = attr_key;
	input.onclick = function(){generate_html_for_list_onclick(this);};
	
	var delete_button = create_delete_button(plugin, attr_key);
	
	var div = document.createElement("div");
	div.className = "container_list";
	div.id = "div_" + plugin["name"] + ':' + attr_key + uniqueId;
	div.data_key = attr_key;
	
	parent.appendChild(input);
	parent.appendChild(delete_button);
	parent.appendChild(div);
}

/**
 * What a button for a list should do in case it is clicked.
 * 
 * @param button
 * 		The clicked button
 * @returns
 */
function generate_html_for_list_onclick(button){
	var parent = document.getElementById("div_" + button.data_div);
		
	uniqueId++;
	
	var element_div = document.createElement("div");
	element_div.className = "list_element";
	
	var key_label = document.createElement("label");
	key_label.appendChild(document.createTextNode(button.data_key + " key : "));
	key_label.className = "normal";
	element_div.appendChild(key_label);
	
	var key_input = document.createElement("input");
	key_input.setAttribute("type", "text");
	key_input.required = "required";
	key_input.name = button.data_plugin["name"] + ":" + button.data_key + uniqueId;
	key_input.className = "normal";
	key_input.pattern = "([A-Z]|[a-z])\\w*";
	key_input.title="a valid key without whitespace and with no leading digit"
	element_div.appendChild(key_input);
	
	generate_html_per_type(element_div, button.data_plugin, button.data_content);
	parent.appendChild(element_div);
}


/**
 * Generate the html in case the required option value is a list of integers
 * @param parent
 * 		The element we want to append to.
 * @param plugin_name
 * 		The plugin name.
 * @param attr_key
 * 		The attribute key.
 * @returns
 */
function generate_html_for_intList(parent, plugin, attr_key, attr_value){
	var input = document.createElement("input");
	input.setAttribute("type", "button");
	input.className = "normal";
	input.value = "add " + attr_key;
	input.data_div = plugin["name"] + ":" + attr_key + uniqueId;
	input.data_name = attr_key;
	input.onclick = function(){generate_html_for_intList_onclick(this);};
	
	var delete_button = create_delete_button(plugin, attr_key);

	var div = document.createElement("div");
	div.className = "container";
	div.id = "div_" + plugin["name"] + ':' + attr_key + uniqueId;
	div.data_name = attr_key;
	
	parent.appendChild(input);
	parent.appencChild(delete_button)
	parent.appendChild(div);
}

/**
 * Create and return a delete button for the given plugin and for the given attribute key.
 * @param plugin The plugin to generate the button for.
 * @param attr_key The attribute key to generate the button for.
 * @returns A delete button.
 */
function create_delete_button(plugin, attr_key){
	var delete_button = document.createElement("input");
	delete_button.setAttribute("type", "button");
	delete_button.className = "normal";
	delete_button.value = "remove " + attr_key;
	delete_button.data_div = plugin["name"] + ":" + attr_key + uniqueId;
	delete_button.data_name = attr_key;
	delete_button.onclick = function(){$(document.getElementById("div_" + this.data_div)).children().last().remove()};
	
	return delete_button
}

/**
 * What a button for an integer list should do in case it is clicked.
 * 
 * @param button
 * 		The clicked button
 * @returns
 */
function generate_html_for_intList_onclick(button){
	var parent = document.getElementById("div_" + button.data_div);
		
	uniqueId++;
	
	var input = document.createElement("input");
	input.setAttribute("type", "number");
	input.required = "required";
	input.className = "normal";
	input.name = button.data_name + uniqueId;
	
	parent.appendChild(input);
}

/**
 * Generate the html in case the required option value is a list of strings
 * @param parent
 * 		The element we want to append to.
 * @param plugin_name
 * 		The plugin name.
 * @param attr_key
 * 		The attribute key.
 * @returns
 */
function generate_html_for_stringList(parent, plugin, attr_key, attr_value){
	var input = document.createElement("input");
	input.setAttribute("type", "button");
	input.className = "normal";
	input.value = "add " + attr_key;
	input.data_div = plugin["name"] + ":" + attr_key + uniqueId;
	input.data_name = attr_key;
	input.onclick = function(){generate_html_for_stringList_onclick(this);};
	
	var delete_button = create_delete_button(plugin, attr_key);
	
	var div = document.createElement("div");
	div.className = "container";
	div.id = "div_" + plugin["name"] + ':' + attr_key + uniqueId;
	div.data_name = attr_key;
	
	parent.appendChild(input);
	parent.appendChild(delete_button);
	parent.appendChild(div);
}

/**
 * What a button for an list of string should do in case it is clicked.
 * 
 * @param button
 * 		The clicked button
 * @returns
 */
function generate_html_for_stringList_onclick(button){
	var parent = document.getElementById("div_" + button.data_div);
		
	uniqueId++;
	
	var input = document.createElement("input");
	input.setAttribute("type", "text");
	input.className = "normal"
	input.required = "required";
	input.name = button.data_name + uniqueId;
	
	parent.appendChild(input);
}

/**
 * Parse the DOM data and create a json tree to send to the server and get the config.lua file.
 * @returns
 */
function parse_and_get_config_file(){
	var middle_token = $('input[name="csrfmiddlewaretoken"]').attr("value");
	
	var json_to_send = parse_data();
	
    var form = $('<form method="POST" action=".">');

    form.append($('<input type="hidden" name="csrfmiddlewaretoken" value="' + middle_token + '">'))
	form.append($('<input type="hidden" name="data" value=\'' + JSON.stringify(json_to_send) + '\'>'))
	form.append($('<input type="hidden" name="method" value="get_config">'))
            
    $('#body').append(form);
    
    form.submit();
    
    form.remove();
}


/**
 * Parse the DOM data and create a json tree to send to the server to run the analysis.
 * @returns
 */
function parse_and_post_data(){
	if(!is_analysis_launched){		
		var middle_token = $('input[name="csrfmiddlewaretoken"]').attr("value");
		
		var json_to_send = parse_data();
		
		var file = document.getElementById("id_binary_file").files[0];
		var form_data = new FormData();
		form_data.append("binary_file", file);
		form_data.append("binary_name", file.name);
		form_data.append("csrfmiddlewaretoken", middle_token);
		form_data.append("data", JSON.stringify(json_to_send));
		form_data.append("method", "run_s2e");
		form_data.append("timeout", $("#timeout_value").val());
		
		$('html,body').css('cursor','wait');
				
		$.ajax({
			type: "POST",
			url: ".",
			data: form_data,
			processData: false,
			contentType: false,
			success: function(data){
				display_data_from_server(JSON.parse(data));
			},
			error: function(data){
				alert("error " + data.status + ": " + data.responseText);
				$('html,body').css('cursor','auto');
				is_analysis_launched = false;
			}
		});
		
		is_analysis_launched = true;
	}
	
}

/**
 * Gets the full json tree of current configuration 
 * @returns the json tree
 */
function parse_data(){
	var json_to_send = {};
	
	var data_to_parse = document.getElementById("right-menu-div").childNodes;
	
	$.each( data_to_parse, function( i, el ) {
		if(el.style != undefined){			
			if(el.style.display == "block"){
				var test = parse_DOM(el.childNodes);
				json_to_send[el.id] = test;
			}
		}
	});	
	
	return json_to_send;
}

/**
 * Parse the DOM_array to create the json tree.
 * 
 * @param DOM_array
 * 		The array to parse.
 * @returns
 * 		The json tree to send to the server.
 */
function parse_DOM(DOM_array){
	var json_to_send = {};
	$.each ( DOM_array, function( i, el){
		
		if(el.tagName == "DIV"){
			//lists
			if(el.className == "container_list"){
				var parsed_children = parse_div_list(el.childNodes);
				json_to_send[el.data_key] = parsed_children;
				
			//intList and stringList
			}else if(el.className == "container"){
				
				json_to_send[el.data_name] = parse_div_container_list(el.childNodes);
				
			}else{				
				if(el.hasChildNodes()){
					var parsed_DOM = parse_DOM(el.childNodes);
					if(parsed_DOM.length != 0){				
						json_to_send = $.extend(json_to_send, parsed_DOM);
					}
				}
			}
			
		}else if(el.tagName == "INPUT"){
			
			if(el.type == "radio"){
				if(el.checked == true){
					var json_var = {};
					json_var[el.data_key] = el.value;
					json_to_send = $.extend(json_to_send, json_var);
				}
			}else if(el.type == "button"){
				
			}else{
				var json_var = {};
				json_var[el.data_key] = el.value;
				json_to_send = $.extend(json_to_send, json_var);
			}
			
		}else{			
			if(el.hasChildNodes()){
				var parsed_DOM = parse_DOM(el.childNodes);
				if(parsed_DOM.length != 0){				
					json_to_send = $.extend(json_to_send, parsed_DOM);
				}
			}
		}
		
		
		
	});
	
	return json_to_send;
}

/**
 * Parse the div for the list type
 * @param children.
 * 		The children of the element div.
 * @returns the partial json tree.
 */
function parse_div_list(children){
	var output = {};
	
	$.each(children, function(i, el){
		var key = el.childNodes[1].value;
		output[key] = parse_DOM([].slice.call(el.childNodes, 2));
	})
	
	return output
}
/**
 * Parse the container div for the integer list and string list types.
 * @param children
 * 		Children of the list element div
 * @returns the partial json tree.
 */
function parse_div_container_list(children){
	var output = [];
	
	$.each(children, function(i, el){
		output.push(el.value);
	})
	
	return output
}

/**
 * Retirect to the page to see the analysis history.
 * @returns
 */
function see_last_result(){
	
	window.location.href = "../display_all_analysis";
	
}






