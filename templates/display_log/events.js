$(document).ready(function(){

    $(".mainActionButton").click(function(){
        $("#menu").addClass("reduced");

        var target = $(this).data("target");
        $(".mainContainer").removeClass("open");
        $("#" + target).addClass("open");
    });
    
    
	display_stats(window.data_runstats);
	display_icount(window.data_icount);
	
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