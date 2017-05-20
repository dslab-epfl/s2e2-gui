//setup the right menu according to the chechbox
/*var leftMenuChildren = document.getElementById("left-menu-div").children;
for(var i = 0; i < leftMenuChildren.length; ++i){
	if(leftMenuChildren[i].tagName == "INPUT"){
		if(leftMenuChildren[i].type == "hidden"){
			leftMenuChildren[i].value = "";
		}else if(leftMenuChildren[i].type == "checkbox"){
			leftMenuChildren[i].checked = false;			
		}
	}
}*/

//Handle button click
function buttonClickHandler(button){
		
	var jButton = $(button);
	if(!jButton.hasClass("disabled")){		
		jButton.toggleClass("active");
		var plugin = pluginMap.get(button.name);
		plugin.isChecked = jButton.hasClass("active");
		
		buttonChangeHandler(button);
	}
	
}

//Handle a button change
function buttonChangeHandler(button){
	var plugin = pluginMap.get(button.name);
	var jButton = $(button);
	
	if(jButton.hasClass("active")){
		var jDiv = $("#" + button.name);
		jDiv.addClass("open");
		jDiv.slideDown();
		//document.getElementById(button.name).style.display="block";
		
		for(var i = 0; i < plugin.dependencies.length; ++i){
			var dep = pluginMap.get(plugin.dependencies[i]);
			
			if(dep != undefined){				
				dep.depCount += 1;
				
				var dependencyButton = document.getElementById("button_" + plugin.dependencies[i]);
				var jDepButton = $(dependencyButton);
				
				//disable checkbox and if state changed, handle change
				//dependencyButton.disabled = true;
				jDepButton.addClass("disabled");
				
				if(jDepButton.hasClass("active") == false){
					//document.getElementById("checkbox_value_" + dependencyCheckbox.name).value=dependencyCheckbox.checked;
					jDepButton.addClass("active");
					
					buttonChangeHandler(dependencyButton);
				}
			}
		}
	}else{
		var jDiv = $("#" + button.name);
		jDiv.removeClass("open");
		jDiv.slideUp();
		//document.getElementById(checkbox.name).style.display="none"
		
		for(var i = 0; i < plugin.dependencies.length; ++i){
			var dep = pluginMap.get(plugin.dependencies[i]);
			
			if(dep != undefined){
				dep.depCount -= 1;
				
				var dependencyButton = document.getElementById("button_" + plugin.dependencies[i]);
				var jDepButton = $(dependencyButton);
				
				if(dep.depCount == 0){
					jDepButton.removeClass("disabled");
					//dependencyCheckbox.disabled = false;
					
					if(jDepButton.hasClass("active") != dep.isChecked){
						//dependencyCheckbox.checked = dep.isChecked;
						jDepButton.toggleClass("active");
						//document.getElementById("checkbox_value_" + dependencyCheckbox.name).value=dependencyCheckbox.checked
						
						buttonChangeHandler(dependencyButton);
					}
				}
			}
		}
	}
}