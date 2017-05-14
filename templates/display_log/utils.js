function appendElementsToTable(table, elements){
	
	var tr = document.createElement('tr');
	for(var i = 0 ; i < elements.length; ++i){
		var td = document.createElement('td');
		td.appendChild(document.createTextNode(elements[i]))
		tr.appendChild(td);
	}
	table.appendChild(tr);
	
}