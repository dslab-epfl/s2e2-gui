var timer;

$(document).ready(function(){
	$("#button_run").click(function(event){

		$("#button_run_hidden").click()



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
			$("#countdown_label").html($("#timeout_value").val())
			$("#countdown_label").show();
			$("#countdown_label_descr").show();
			timer = setInterval(decrease_countdown, 1000);

			parse_and_post_data();
		}

	});

	$("#header_form").submit(function(e){
		e.preventDefault();
	});

	$("#content_form").submit(function(e){
		e.preventDefault();
	});

});

function decrease_countdown(){
	var countdown_label = $("#countdown_label");

	var value = countdown_label.html() - 1;

	countdown_label.html(value);

	if(value <= 0){
		clearInterval(timer);

		$("#countdown_label_descr").hide();
		countdown_label.hide();
	}
}

/**
 * Send a configuration file with the current configuration
 * @returns
 */
function save_config(){

	var is_form_valid = true;

	var inputs = $(".plugin_div.open").find("input");

	for(var i = 0; i < inputs.length; ++i){
		if(inputs[i].checkValidity() == false){
			console.log(inputs[i]);
			is_form_valid = false;
		}
	}

	if(is_form_valid == true){
		parse_and_get_config_file();
	}
}

function load_config(){

}