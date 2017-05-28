from django.http import HttpResponse
from django.shortcuts import render
from models import Analysis
import s2e_web.S2E_settings as settings
import shutil
from configure_and_run_analysis.views import displayAnalysisInDir
from cups import HTTP_OK


def handleRequest(request):
	"""
	Handle the requests from the display_all_analysis page.
	"""
		
	if (request.method == 'GET'):
		return render(request, 'display_all_analysis/index.html', {"analysis" : Analysis.objects.all()})
	
	elif (request.method == 'POST'):
		if(request.POST["method"] == "display"):
			s2e_num = request.POST["s2e_num"]
			return displayAnalysisInDir(request, s2e_num)
		elif(request.POST["method"] == "remove"):
			s2e_num = request.POST["s2e_num"]
			Analysis.objects.filter(s2e_num=s2e_num).delete()
			
			s2e_output_dir_to_delete = settings.S2E_PROJECT_FOLDER_PATH + settings.S2E_BINARY_FILE_NAME + "/s2e-out-" + s2e_num + "/"
			shutil.rmtree(s2e_output_dir_to_delete)
			
			return HttpResponse(status=200)
		

