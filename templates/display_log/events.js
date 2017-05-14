$(document).ready(function(){

    $(".mainActionButton").click(function(){
        var target = $(this).data("target");
        $("#menu button.active").removeClass("active");
        $(this).addClass("active");
        
        $("body > .mainContainer").removeClass("open");
        $("#" + target).addClass("open");
    });
    
    
	display_stats(window.data_runstats);
	display_icount(window.data_icount);
	
	createCustomLogDisplay("warning_log");
	createCustomLogDisplay("debug_log");
	createCustomLogDisplay("info_log");
	
	var iFrame = document.getElementById("line_coverage_iframe");
    resizeIFrameToFitContent(iFrame);
	
});

function resizeIframe(obj) {
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
}


$(".log_select").change(function(){
	var jquery_this = $(this);
	var target = jquery_this.data("target");
		
	$("#" + target + " .mainContainer").removeClass("open");
	$("#" + target + "_" + jquery_this.val()).addClass("open");
});

function display_stats(stats){
	var lines = stats.split("\n");
	
	var table = document.createElement('tbody');
	
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
	
}

