from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from shutil import copyfile
from contextlib import contextmanager
from models import S2EOutput
import subprocess
import os
import signal
import tempfile
import shutil
import s2e_web.S2E_settings as settings
from threading import Timer


def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			#TODO use in stage 2
			#with make_temporary_directory() as tmpdir:
			tmpdir = "temp-dir/"	
			has_s2e_error, s2e_error = handle_uploaded_file(tmpdir, request.FILES["config_file"], request.FILES["binary_file"])
			output = S2EOutput("s2e-last/")

			return render(request, 'display_log.html', {'warnings': output.warnings, 'messages' : output.messages, 'info' : output.info, 'debug' : output.debug, 'has_s2e_error': has_s2e_error, 's2e_error': s2e_error})
	else:
		form = UploadFileForm()
	return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(tmpdir, config, binary):	
	write_file_to_disk_and_close(tmpdir + settings.S2E_CONFIG_LUA_FILE_NAME, config)
	write_file_to_disk_and_close(tmpdir + settings.S2E_BINARY_FILE_NAME, binary)
		
	has_s2e_error, s2e_error = launch_S2E(tmpdir)

	os.remove(tmpdir + settings.S2E_CONFIG_LUA_FILE_NAME)
	os.remove(tmpdir + settings.S2E_BINARY_FILE_NAME)

	return has_s2e_error, s2e_error


def write_file_to_disk_and_close(path, w_file):
	with open(path, 'wb+') as destination:
		for chunk in w_file.chunks():
			destination.write(chunk)
	destination.close()
	w_file.close()


@contextmanager
def make_temporary_directory():
	tmpdir = tempfile.mkdtemp()
	try:
		yield tmpdir
	finally:
		shutil.rmtree(tmpdir)

def launch_S2E(tmpdir):
	
	#s2e_new_project_command = "s2e new_project -i " + settings.S2E_IMAGE_NAME + " "  + tmpdir + settings.S2E_BINARY_FILE_NAME 
	
		
	s2e_command = "sh " + settings.S2E_PROJECT_FOLDER_PATH + settings.S2E_BINARY_FILE_NAME  + "/launch-s2e.sh"
	
	
	#s2e_command = settings.S2E_QEMU_SYSTEM_PATH + " -net none " + \
	#			  settings.S2E_IMAGE_SNAP_PATH + " -loadvm " + settings.S2E_IMAGE_SNAP_EXT + \
	#			  " -s2e-config-file " + tmpdir + settings.S2E_CONFIG_LUA_FILE_NAME
	
	
	#p = subprocess.Popen([s2e_new_project_command, ""], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=settings.S2E_ENVIRONEMENT_FOLDER_PATH)
	#has_err = p.returncode
	#if(has_err != 0):
	#	out, err = p.communicate()
	#	return has_err, err



	shutil.copyfile(tmpdir + settings.S2E_CONFIG_LUA_FILE_NAME, settings.S2E_PROJECT_FOLDER_PATH + settings.S2E_BINARY_FILE_NAME + "/" + settings.S2E_ENV_CONFIG_LUA_NAME)
	shutil.copyfile(tmpdir + settings.S2E_BINARY_FILE_NAME, settings.S2E_PROJECT_FOLDER_PATH + settings.S2E_BINARY_FILE_NAME + "/" + settings.S2E_BINARY_FILE_NAME)
	
	
	kill = lambda process: kill_process(process)
	
	p = subprocess.Popen([s2e_command, ""], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=settings.S2E_PROJECT_FOLDER_PATH + settings.S2E_BINARY_FILE_NAME, preexec_fn=os.setsid)
	
	#TODO add an option for the timeout
	my_timer = Timer(600, kill, [p])
	 
	out, err = "timer timout", ""
	try:
		my_timer.start()
		out, err = p.communicate()
	finally:
		my_timer.cancel()
	
		
	return p.returncode, out + err
	
	
def kill_process(process):
	print("process killed after timeout")
	os.killpg(os.getpgid(process.pid), signal.SIGTERM)


