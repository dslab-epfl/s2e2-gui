$(document).ready(function(){

    /****************************************************** This is the 'menu' listener **/	
    $(".mainActionButton").click(function(){
        $("#menu").addClass("reduced");

        var target = $(this).data("target");
        $(".mainContainer").removeClass("open");
        $("#" + target).addClass("open");
    });
    
    
	display_stats(window.data_runstats);

});

function display_stats(stats){
	var lines = stats.split("\n");
	
	var table = document.createElement('tbody');
	table.setAttribute("id", "stats_table");
	
	for (var lineIndex = 0; lineIndex < lines.length; ++lineIndex){
        var tr = document.createElement('tr');
    	tr.setAttribute("id", "stats_table_tr");
    	if(lines[lineIndex] != ""){    		
    		var columns = lines[lineIndex].split(",");
    		for (var columnIndex = 0; columnIndex < columns.length; ++columnIndex){
    			var td = document.createElement('td');
    			td.setAttribute("id", "stats_table_td");
    			td.appendChild(document.createTextNode(columns[columnIndex]));
    			tr.appendChild(td);
    		}
    		table.appendChild(tr);
    	}
	}
	
	$("#stats").html(table);
}