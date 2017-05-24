from django.http import HttpResponse
from django.shortcuts import render
from models import Analysis
import s2e_web.S2E_settings as settings
from configure_and_run_analysis.views import displayAnalysisInDir


def handleRequest(request):
	"""
	Handle the requests from the display_all_analysis page.
	"""
		
	if (request.method == 'GET'):
		return render(request, 'display_all_analysis/index.html', {"analysis" : Analysis.objects.all()})
	
	elif (request.method == 'POST'):
		s2e_num = request.POST["s2e_num"]
		return displayAnalysisInDir(request, s2e_num)
	

