$(document).ready(function(){

    $(".mainActionButton").click(function(){
    	var j_this = $(this);
        var target = j_this.data("target");
        $("#menu button.active").removeClass("active");
        j_this.addClass("active");
        
        $("body > .mainContainer").removeClass("open");
        $("#" + target).addClass("open");
        
        var j_body = $("#html");
        
        j_body.removeClass("warning")
        j_body.removeClass("info")
        j_body.removeClass("debug")
        var id = j_this.data("target");
        if(id == "warning_log"){
        	j_body.addClass("warning");
        }else if(id == "info_log"){
        	j_body.addClass("info");        	
        }else if(id == "debug_log"){
        	j_body.addClass("debug");
        }
        
    });
    
    $(".log_select").change(function(){
    	var jquery_this = $(this);
    	var target = jquery_this.data("target");
    		
    	$("#" + target + " .mainContainer").removeClass("open");
    	$("#" + target + "_" + jquery_this.val()).addClass("open");
    });
    
    $("#graph_img_select").change(function(){
    	var jquery_this = $(this);
    	var image_display = $("#image_display");
    	
        image_display.attr("src", jquery_this.val()); 
    });
    
    $("#backButton").click(function(){
    	window.location.href = "../";
    });
    
    
	display_stats(window.data_runstats);
	display_icount(window.data_icount);
	
	createCustomLogDisplay("warning_log");
	createCustomLogDisplay("debug_log");
	var info_line_by_state = createCustomLogDisplay("info_log");
	    
    displayFinalStatusCode(info_line_by_state);
});

/**
 * Resize an Iframe.
 */
function resizeIframe(obj) {
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
}


/**
 * Displays the statistics in a table.
 */
function display_stats(stats){
	var lines = stats.split("\n");
	
	var table = document.createElement('tbody');
	table.id = "statistics_table"
	
	for (var lineIndex = 0; lineIndex < lines.length; ++lineIndex){
        var tr = document.createElement('tr');
    	if(lines[lineIndex] != ""){    		
    		var columns = lines[lineIndex].split(",");
    		for (var columnIndex = 0; columnIndex < columns.length; ++columnIndex){
    			var td = document.createElement('td');
    			td.appendChild(document.createTextNode(columns[columnIndex]));
    			tr.appendChild(td);
    		}
    		table.appendChild(tr);
    	}
	}
	
	$("#stats").html(table);
}

/**
 * Displays the instruction count in a table
 */
function display_icount(icount){
	
	if(icount === null){
		var message_title = document.createElement("H4");
		message_title.appendChild(document.createTextNode("No instruction count data found :"))
		
		var message_body = document.createElement("P");
		message_body.appendChild(document.createTextNode("To have an instruction count table, make sure to enable InstructionCounter"))
		
		document.getElementById("icount").appendChild(message_title);
		document.getElementById("icount").appendChild(message_body);
	}else{		
		var table = document.createElement('tbody');
		table.className = "centered";	
 
		// headers
		var tr = document.createElement('tr');
		
		var th1 = document.createElement('th')
		th1.appendChild(document.createTextNode("State ID"));
		
		var th2 = document.createElement('th')
		th2.appendChild(document.createTextNode("Instruction count"));
		
		tr.appendChild(th1);
		tr.appendChild(th2);
		
		table.appendChild(tr);
		
		// table content
		for(var state_id in icount){
			appendElementsToTable(table, [state_id, icount[state_id]]);
		}
		
		$("#icount").html(table);
	}
	
}

/**
 * Display the logs in a custom way.
 * Each logs gets sorted by state.
 */
function createCustomLogDisplay(div_id){
	
		var re = /\[State \d+\]/g;
				
		var warning_array = $("#" + div_id + "_all").html().split(/<br>|<p>|<\/p>/);
		var line_by_state = {};
		var last_matched_state = null;
		
		for(var i = 0; i < warning_array.length; ++i){
			var text_line = warning_array[i];
			var matched_state = text_line.match(re);
			
			if(matched_state != null){
				last_matched_state = matched_state[0].substr(7, matched_state[0].length - 8);
			}
						
			if(last_matched_state != null){
				var state_array = line_by_state[last_matched_state];
				if(state_array == undefined){
					state_array = [];
					line_by_state[last_matched_state] = state_array;
				}
				state_array.push(text_line);
			}
		}
		
		for(var key in line_by_state){
			var div = document.createElement("DIV");
			div.id = div_id + "_" + key;
			div.className = "mainContainer";
			var text_array = line_by_state[key];
			
			for(var i = 0; i < text_array.length; ++i){
				div.appendChild(document.createTextNode(text_array[i]));
				div.appendChild(document.createElement("BR"));
			}
			$("#" + div_id).append(div);
			
			var option_entry = document.createElement("OPTION");
			option_entry.value = key;
			option_entry.appendChild(document.createTextNode("State " + key));
			$("#" + div_id + "_select").append(option_entry);	
		}
		
		return line_by_state;
}

/**
 * Display a table in the overview to print the final message an status code for every states.
 */
function displayFinalStatusCode(info_line_by_state){
	
	var status_reg_exp = /status: \dx\d*/;
	var status_by_state = {};
	var message_reg_exp = /message: ".*"/;
	var message_by_state = {};
	var term_reg_exp = /Terminating state early: .*/;
	
	for(var key in info_line_by_state){
		var text_array = info_line_by_state[key];
		
		status_by_state[key] = "Terminated by timeout";
		message_by_state[key] = "";
				
		for(var i = 0; i < text_array.length; ++i){
			var text_line = text_array[i];
			
			var matched = text_line.match(status_reg_exp);
			if(matched != null){
				var status_to_extract = matched[0];
				status_by_state[key] = status_to_extract.substr(8, status_to_extract.length - 8);
			}
			
			var matched_message = text_line.match(message_reg_exp);
			if(matched_message != null){
				var message_to_extract = matched_message[0];
				message_by_state[key] = message_to_extract.substr(10, message_to_extract.length - 11);
			}
			
			var matched_term = text_line.match(term_reg_exp);
			if(matched_term != null){
				var term_to_extract = matched_term[0];
				message_by_state[key] = term_to_extract.substr(25, term_to_extract.length - 25);
				status_by_state[key] = -1;
			}
		}
	}
	
	var table = document.createElement('tbody');
	table.className = "centered";
	
	var tr = document.createElement("TR");
	
	var th_state = document.createElement("TH");
	th_state.appendChild(document.createTextNode("State"));
	tr.appendChild(th_state);

	var th_status = document.createElement("TH");
	th_status.appendChild(document.createTextNode("Status"));
	tr.appendChild(th_status);

	var th_message = document.createElement("TH");
	th_message.appendChild(document.createTextNode("Message"));
	tr.appendChild(th_message);
	
	table.appendChild(tr);
		
	for(var key in status_by_state){
		var tr_in = document.createElement("TR");
		
		var td_state = document.createElement("TD");
		td_state.appendChild(document.createTextNode(key));
		tr_in.appendChild(td_state);
		
		var td_status = document.createElement("TD");
		var status_message = status_by_state[key];
		if(status_message != "0x0" && status_message != "0"){
			tr_in.className = "error";
		}
		td_status.appendChild(document.createTextNode(status_message));
		tr_in.appendChild(td_status);

		var td_message = document.createElement("TD");
		td_message.appendChild(document.createTextNode(message_by_state[key]));
		tr_in.appendChild(td_message);
				
		table.appendChild(tr_in);
	}
	
	$("#overview").append(table);
}

