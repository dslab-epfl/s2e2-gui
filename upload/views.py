from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from shutil import copyfile
from contextlib import contextmanager
import os
import tempfile
import shutil


S2E_QEMU_SYSTEM_PATH = "../../build/qemu-release/i386-s2e-softmmu/qemu-system-i386"
S2E_IMAGE_SNAP_PATH = "../../test/s2e_disk-raw.s2e"
# The name ".s2e." in the image file
S2E_IMAGE_SNAP_EXT = "ready"
S2E_CONFIG_LUA_FILE_NAME = "config.lua"
S2E_BINARY_FILE_NAME = "binary"
S2E_BOOTSTRAP_FILE_NAME = "bootstrap"


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
	#used in stage 2
	#with make_temporary_directory() as tmpdir:
	tmpdir = "temp-dir/"	

	write_file_to_disk_and_close(tmpdir + S2E_CONFIG_LUA_FILE_NAME, config)
	write_file_to_disk_and_close(tmpdir + S2E_BINARY_FILE_NAME, binary)
	launch_S2E(tmpdir)


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
	os.system(S2E_QEMU_SYSTEM_PATH + " -net none " + S2E_IMAGE_SNAP_PATH + " -loadvm " + S2E_IMAGE_SNAP_EXT + " -s2e-config-file " + tmpdir + S2E_CONFIG_LUA_FILE_NAME + " -s2e-verbose")


