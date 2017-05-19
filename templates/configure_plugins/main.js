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
		var header = document.createElement("span");
		header.className = "attribute_title";
		header.appendChild(document.createTextNode(attr_key + ":"));
		var header_descr = document.createElement("span");
		header_descr.className = "attribute_description";
		header_descr.appendChild(document.createTextNode(attr_value["description"]))
		parent.appendChild(header);	
		parent.appendChild(header_descr);
		parent.appendChild(document.createElement("BR"));
		
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
		}else if(attr_value["type"] == "stringList"){
			generate_html_for_stringList(parent, plugin, attr_key, attr_value);
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
	input.className = "normal";
	input.name = attr_key
	
	parent.appendChild(input);
}

function generate_html_for_bool(parent, plugin_name, attr_key){
	var label1 = document.createElement("label");
	var input1 = document.createElement("input");
	input1.setAttribute("type", "radio");
	input1.value = "true";
	input1.checked = "checked";
	input1.className = "normal";
	input1.name = attr_key;
	label1.appendChild(input1);
	label1.appendChild(document.createTextNode("True"));

	var label2 = document.createElement("label");
	var input2 = document.createElement("input");
	input2.setAttribute("type", "radio");
	input2.value = "false";
	input2.className = "normal";
	input2.name = attr_key;
	label2.appendChild(input2);
	label2.appendChild(document.createTextNode("False"));
	
	parent.appendChild(label1);
	parent.appendChild(label2);
}

function generate_html_for_string(parent, plugin_name, attr_key){
	var input = document.createElement("input");
	input.setAttribute("type", "text");
	input.className = "normal";
	input.name = attr_key;
	
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
	input.data_key = attr_key;
	input.onclick = function(){generate_html_for_list_onclick(this);};
	
	var div = document.createElement("div");
	div.className = "container_list";
	div.id = "div_" + plugin["name"] + ':' + attr_key + uniqueId;
	
	parent.appendChild(input);
	parent.appendChild(div);
}

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
	key_input.name = button.data_plugin["name"] + ":" + button.data_key + uniqueId;
	key_input.className = "normal";
	element_div.appendChild(key_input);
	
	generate_html_per_type(element_div, button.data_plugin, button.data_content);
	parent.appendChild(element_div);
}

function generate_html_for_intList(parent, plugin, attr_key, attr_value){
	var input = document.createElement("input");
	input.setAttribute("type", "button");
	input.className = "normal";
	input.value = "add " + attr_key;
	input.data_div = plugin["name"] + ":" + attr_key + uniqueId;
	input.data_name = attr_key;
	input.onclick = function(){generate_html_for_intList_onclick(this);};
	
	var div = document.createElement("div");
	div.className = "container";
	div.id = "div_" + plugin["name"] + ':' + attr_key + uniqueId;
	div.data_name = attr_key;
	
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

function generate_html_for_stringList(parent, plugin, attr_key, attr_value){
	var input = document.createElement("input");
	input.setAttribute("type", "button");
	input.className = "normal";
	input.value = "add " + attr_key;
	input.data_div = plugin["name"] + ":" + attr_key + uniqueId;
	input.data_name = attr_key;
	input.onclick = function(){generate_html_for_stringList_onclick(this);};
	
	var div = document.createElement("div");
	div.className = "container";
	div.id = "div_" + plugin["name"] + ':' + attr_key + uniqueId;
	div.data_name = attr_key;
	
	parent.appendChild(input);
	parent.appendChild(div);
}

function generate_html_for_stringList_onclick(button){
	var parent = document.getElementById("div_" + button.data_div);
		
	uniqueId++;
	
	var input = document.createElement("input");
	input.setAttribute("type", "text");
	input.className = "normal"
	input.name = button.data_name + uniqueId;
	
	parent.appendChild(input);
}

function submit_data(){
	
	var form = $("#validation_form");
	form.validate();
	
	if(form.valid()){
		parse_and_post_data();
	}
	
}

function parse_and_post_data(){
	var middle_token = $('input[name="csrfmiddlewaretoken"]').attr("value");
	var data_to_parse = document.getElementById("right-menu-div").childNodes;
	var json_to_send = {};
	
	$.each( data_to_parse, function( i, el ) {
		if(el.style != undefined){			
			if(el.style.display == "block"){
				var test = parse_DOM(el.childNodes);
				json_to_send[el.id] = test;
			}
		}
	});	

	
	var file = document.getElementById("id_binary_file").files[0];
	var form_data = new FormData();
	form_data.append("binary_file", file);
	form_data.append("csrfmiddlewaretoken", middle_token);
	form_data.append("data", JSON.stringify(json_to_send));
	form_data.append("method", "run_s2e");
	form_data.append("timeout", $("#timeout_value").val())
	
	document.getElementById("spinner").appendChild(document.createElement("p"));
	
	$.ajax({
			  type: "POST",
			  url: "http://localhost:8000/",
			  data: form_data,
			  processData: false,
			  contentType: false,
			  success: function(data){				  
				  display_data_from_server(JSON.parse(data));
		      }
			});
	
}

function parse_DOM(DOM_array){
	var json_to_send = {};
	$.each ( DOM_array, function( i, el){
		
		if(el.tagName == "DIV"){
			if(el.className == "container_list"){
				
				var parsed_children = parse_div_list(el.childNodes);
				json_to_send = $.extend(json_to_send, parsed_children);
				
				
			}else if(el.className == "container"){
				
				console.log(el);
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
					json_var[el.name] = el.value;
					json_to_send = $.extend(json_to_send, json_var);
				}
			}else if(el.type == "button"){
				
			}else{
				var json_var = {};
				json_var[el.name] = el.value;
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


function parse_div_list(children){
	var output = {};
	
	$.each(children, function(i, el){
		var key = el.childNodes[1].value;
		output[key] = parse_DOM([].slice.call(el.childNodes, 2));
	})
	
	return output
}

function parse_div_container_list(children){
	var output = [];
	
	$.each(children, function(i, el){
		output.push(el.value);
	})
	
	return output
}

function see_last_result(){
	
	var middle_token = $('input[name="csrfmiddlewaretoken"]').attr("value");
	
	var form_data = new FormData();
	form_data.append("csrfmiddlewaretoken", middle_token);
	form_data.append("method", "get_last_result");
		
	$.ajax({
			  type: "POST",
			  url: "http://localhost:8000/",
			  data: form_data,
			  processData: false,
			  contentType: false,
			  success: function(data){
				  display_data_from_server(JSON.parse(data))
		      }
			});
	
}

function display_data_from_server(data){
	document.open("text/html");
	document.write(data.html);
	document.close();
	
	window.data_runstats = data.stats;
	window.data_icount = data.icount;
}





