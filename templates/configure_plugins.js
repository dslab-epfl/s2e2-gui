//setup the right menu according to the chechbox
var leftMenuChildren = document.getElementById("left-menu-div").children;
for(var i = 0; i < leftMenuChildren.length; ++i){
	if(leftMenuChildren[i].tagName == "INPUT" && leftMenuChildren[i].type == "checkbox" && leftMenuChildren[i].checked == true){
		checkboxClickHandler(leftMenuChildren[i]);
	}
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


