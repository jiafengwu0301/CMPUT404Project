
from django.conf.urls import url

from . import viewsposts

urlpatterns = [
	url(r'^(?P<pk>[^/]+)/$', viewsposts.CommentRetrieveView.as_view(), name='comment_destroy'),
	url(r'^(?P<pk>[^/]+)/destroy/$', viewsposts.CommentDestroyView.as_view(), name='comment_destroy'),
]