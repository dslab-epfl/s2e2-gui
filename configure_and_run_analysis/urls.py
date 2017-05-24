from views import handleRequest
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', handleRequest),
]
