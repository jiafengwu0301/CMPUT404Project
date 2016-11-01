from django.conf.urls import url

from . import viewsposts

urlpatterns = [
	url(r'^$', viewsposts.PostListView.as_view(), name='post_list'),
	url(r'^create/$', viewsposts.PostCreateView.as_view(), name='post_create'),
	url(r'^(?P<pk>\d+)/$', viewsposts.PostRetrieveView.as_view(), name='post_detail'),
	url(r'^(?P<pk>\d+)/update/$', viewsposts.PostUpdateView.as_view(), name='post_update'),
	url(r'^(?P<pk>\d+)/destroy/$', viewsposts.PostDestroyView.as_view(), name='post_destroy'),
	url(r'^(?P<pk>\d+)/comments/$', viewsposts.CommentsByPostView.as_view(), name='post_destroy'),

]
