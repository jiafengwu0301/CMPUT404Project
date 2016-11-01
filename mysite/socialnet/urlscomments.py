
from django.conf.urls import url

from . import viewsposts

urlpatterns = [
	url(r'^$', viewsposts.CommentListView.as_view(), name='comments_list'),
	url(r'^(?P<pk>\d+)/$', viewsposts.CommentRetrieveView.as_view(), name='comment_destroy'),
	url(r'^(?P<pk>\d+)/destroy/$', viewsposts.CommentDestroyView.as_view(), name='comment_destroy'),
]