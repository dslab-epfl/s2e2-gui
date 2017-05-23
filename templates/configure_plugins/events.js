$(document).ready(function(){
	$("#button_run").click(function(event){
				
		var form = $("#validation_form");
		var is_form_valid = true;		
		
		if($("#id_binary_file")[0].checkValidity() == false){
			is_form_valid = false;
		}
		if($("#timeout_value")[0].checkValidity() == false){
			is_form_valid = false;
		}
		
		var inputs = $(".plugin_div.open").find("input");
		
		for(var i = 0; i < inputs.length; ++i){
			if(inputs[i].checkValidity() == false){
				console.log(inputs[i]);
				is_form_valid = false;
			}
		}
		
		if(is_form_valid == true){
			parse_and_post_data();
		}
		
	});
	
	$("#validation_form").submit(function(e){
		e.preventDefault();
	});
		
});