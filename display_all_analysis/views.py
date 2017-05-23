from django.http import HttpResponse
from django.shortcuts import render
from models import Analysis
import os
import s2e_web.S2E_settings as settings
from generate_config.views import displayAnalysisInDir


def upload_file(request):
		
	if (request.method == 'GET'):
		
		#a = Analysis(s2e_num=1, binary_checksum=1000, binary_name="name")
		#a.save()
		#print(Analysis.objects.remove())
		#Analysis.objects.all().delete()
		return render(request, 'display_all_analysis/index.html', {"analysis" : Analysis.objects.all()})
	
	elif (request.method == 'POST'):
		
		s2e_num = request.POST["s2e_num"]
		return displayAnalysisInDir(request, s2e_num)
	

