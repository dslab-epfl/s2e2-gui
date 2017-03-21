from views import configurePlugins
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', configurePlugins),
]
