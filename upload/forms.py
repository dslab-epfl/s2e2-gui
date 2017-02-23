from django import forms

class UploadFileForm(forms.Form):
	config_file = forms.FileField()
	binary_file = forms.FileField()	
