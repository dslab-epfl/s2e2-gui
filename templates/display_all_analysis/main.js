function run_new_analysis(){
	window.location.href = "../";
}

function display_analysis(tr){
	var s2e_num = $(tr).data("s2e_num");
		
	var middle_token = $('input[name="csrfmiddlewaretoken"]').attr("value");
	
	var form_data = new FormData();
	form_data.append("csrfmiddlewaretoken", middle_token);
	form_data.append("s2e_num", s2e_num);
	
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