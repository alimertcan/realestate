from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^register/$', register),
	url(r'^home/$', home),
    url(r'^register/success/$', register_success),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
]