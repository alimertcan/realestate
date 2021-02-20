from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^list/$',property_list,name="list"),
	url(r'^userpre/$',user_preferences,name="upref"),
    url(r'^usersee/userpre2/$',user_preferences2,name="upref2"),
	url(r'^usersee/$',user_see,name="usersee"),
    url(r'^create/$',property_create),
 	url(r'^(?P<id>\d+)/$', property_detail, name='detail'), 
    url(r'^(?P<id>\d+)/edit/$',property_update,name="update"),
   # url(r'^(?P<id>\d+)$',property_detail,name='detail'),
    url(r'^(?P<id>\d+)/delete/$',property_delete),
    url(r'^favorites/$',favorites),
    url(r'^likepage/$',likepage),
    url(r'^likepage2/$',likepage2),
    url(r'^message/$',mesajinbox,name="inboxno2"),
    url(r'^message/(?P<id>\d+)/delete/$',mesajdelete,name="inbox"),
    url(r'^message/(?P<id>\d+)/sent/$',mesaj,name="sendmessage"),
    url(r'^(?P<id>\d+)/like/$',Likeadd, name='likebutton'), 
    url(r'^(?P<id>\d+)/dislike/$',dislike, name='likebutton'), 
    url(r'^myproperty/$',myproperty),
    url(r'^filter/$',filtering),
    url(r'^filter2/$',colfilter),

]