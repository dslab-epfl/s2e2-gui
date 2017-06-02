
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

//Handle a button class change
function buttonChangeHandler(button){
	var plugin = pluginMap.get(button.name);
	var jButton = $(button);
	
	if(jButton.hasClass("active")){
		var jDiv = $("#" + button.name);
		jDiv.addClass("open");
		jDiv.slideDown();
		
		for(var i = 0; i < plugin.dependencies.length; ++i){
			var dep = pluginMap.get(plugin.dependencies[i]);
			
			if(dep != undefined){				
				dep.depCount += 1;
				
				var dependencyButton = document.getElementById("button_" + plugin.dependencies[i]);
				var jDepButton = $(dependencyButton);
				
				//disable button and if state changed, handle change
				jDepButton.addClass("disabled");
				
				if(jDepButton.hasClass("active") == false){
					jDepButton.addClass("active");
					
					buttonChangeHandler(dependencyButton);
				}
			}
		}
	}else{
		var jDiv = $("#" + button.name);
		jDiv.removeClass("open");
		jDiv.slideUp();
		
		for(var i = 0; i < plugin.dependencies.length; ++i){
			var dep = pluginMap.get(plugin.dependencies[i]);
			
			if(dep != undefined){
				dep.depCount -= 1;
				
				var dependencyButton = document.getElementById("button_" + plugin.dependencies[i]);
				var jDepButton = $(dependencyButton);
				
				if(dep.depCount == 0){
					jDepButton.removeClass("disabled");
					
					if(jDepButton.hasClass("active") != dep.isChecked){
						jDepButton.toggleClass("active");
						
						buttonChangeHandler(dependencyButton);
					}
				}
			}
		}
	}
}