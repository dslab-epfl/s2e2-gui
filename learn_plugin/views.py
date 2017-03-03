from django.shortcuts import render
from django.http.response import HttpResponseNotFound
from apps import LearnPluginConfig as conf

# Create your views here.
def test_test_test(request):
    #print(conf.name)
    return HttpResponseNotFound()
