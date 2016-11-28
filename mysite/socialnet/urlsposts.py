from django.conf.urls import url

from . import viewsposts

urlpatterns = [
	url(r'^$', viewsposts.PostListView.as_view(), name='post_list'),
	url(r'^/remote$', viewsposts.RemotePostListView.as_view({'get': 'list'}), name='post_r_list'),
	url(r'^/create$', viewsposts.PostCreateView.as_view({'post': 'create_post'}), name='post_create'),
	url(r'^/(?P<pk>[^/]+)$', viewsposts.PostRetrieveView.as_view(), name='post_detail'),
	url(r'^/(?P<pk>[^/]+)/comments/$', viewsposts.CommentsByPostIdView.as_view({'get': 'list', 'post': 'create'}), name='post_comments'),
	url(r'^/(?P<pk>[^/]+)/update$', viewsposts.PostUpdateView.as_view(), name='post_update'),
	url(r'^/(?P<pk>[^/]+)/destroy$', viewsposts.PostDestroyView.as_view(), name='post_destroy'),
	url(r'^/(?P<pk>[^/]+)/comments/create$', viewsposts.CommentCreateView.as_view(), name='comment_create'),
]
