function appendElementsToTable(table, elements){
	
	var tr = document.createElement('tr');
	for(var i = 0 ; i < elements.length; ++i){
		var td = document.createElement('td');
		td.appendChild(document.createTextNode(elements[i]))
		tr.appendChild(td);
	}
	table.appendChild(tr);
	
}


function display_data_from_server(data){
	document.open("text/html");
	document.write(data.html);
	document.close();
		
	window.data_runstats = data.stats;
	window.data_icount = data.icount;
}