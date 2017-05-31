function run_new_analysis(){
	window.location.href = "../";
}

/**
 * Displays the analysis data for the clicked line
 * 
 * @param tr 
 * 		The line that was clicked
 * @returns
 */
function display_analysis(td){
	var s2e_num = $(td).parent().data("s2e_num");
	var binary_name = $(td).parent().data("binary_name");
		
	var middle_token = $('input[name="csrfmiddlewaretoken"]').attr("value");
	
	var form_data = new FormData();
	form_data.append("csrfmiddlewaretoken", middle_token);
	form_data.append("s2e_num", s2e_num);
	form_data.append("binary_name", binary_name);
	form_data.append("method", "display");
	
	$('html,body').css('cursor','wait');
	
	$.ajax({
			  type: "POST",
			  url: ".",
			  data: form_data,
			  processData: false,
			  contentType: false,
			  success: function(data){
				  display_data_from_server(JSON.parse(data))
			  }
	});
}

function delete_analysis(td){
	var s2e_num = $(td).parent().data("s2e_num");
	var binary_name = $(td).parent().data("binary_name");

	var middle_token = $('input[name="csrfmiddlewaretoken"]').attr("value");
	
	var form_data = new FormData();
	form_data.append("csrfmiddlewaretoken", middle_token);
	form_data.append("s2e_num", s2e_num);
	form_data.append("binary_name", binary_name);
	form_data.append("method", "remove");
	
	$('html,body').css('cursor','wait');
	
	$.ajax({
			  type: "POST",
			  url: ".",
			  data: form_data,
			  processData: false,
			  contentType: false,
			  success: function(data){
				  $(td).parent().remove();
				  $('html,body').css('cursor','auto');
			  }
	});
}
	