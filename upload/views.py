from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import os
from shutil import copyfile

def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
				handle_uploaded_file(request.FILES["config_file"], request.FILES["binary_file"])
				return render(request, 'success.html', {'form': form})
	else:
		form = UploadFileForm()
	return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(config, binary):
	with open('S2E_files/config.lua', 'wb+') as destination:
		for chunk in config.chunks():
			destination.write(chunk)
	destination.close()
	config.close()
	with open('S2E_files/binary', 'wb+') as destination:
		for chunk in binary.chunks():
			destination.write(chunk)
	destination.close()
	binary.close()

	


