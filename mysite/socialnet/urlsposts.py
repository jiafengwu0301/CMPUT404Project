from django.conf.urls import url

from . import viewsposts

urlpatterns = [
	url(r'^$', viewsposts.PostListView.as_view(), name='post_list'),
	url(r'^create/$', viewsposts.PostCreateView.as_view(), name='post_create'),
	url(r'^(?P<pk>\d+)/$', viewsposts.PostRetrieveView.as_view(), name='post_detail'),
	url(r'^(?P<pk>\d+)/update/$', viewsposts.PostUpdateView.as_view(), name='post_update'),
	url(r'^(?P<pk>\d+)/destroy/$', viewsposts.PostDestroyView.as_view(), name='post_destroy'),
	#url(r'^comments/$', viewsposts.CommentListView.as_view(), name='all_comments'),
	url(r'^(?P<postpk>\d+)/comments/create/$', viewsposts.CreateCommentView.as_view(), name='post_comments'),

]
