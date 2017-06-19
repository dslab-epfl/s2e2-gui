from display_all_analysis.views import handleRequest
from django.conf.urls import url

urlpatterns = [
    url(r'^$', handleRequest),
]
