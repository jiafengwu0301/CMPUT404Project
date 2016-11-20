from django.conf.urls import url

from . import viewsauthors, viewsposts

urlpatterns = [
	url(r'^$', viewsauthors.AuthorListView.as_view(), name='author_list'),
	url(r'^create/$', viewsauthors.AuthorCreateView.as_view(), name='author_list'),
	url(r'^(?P<pk>[^/]+)/$', viewsauthors.AuthorRetrieveView.as_view(), name='author_detail'),
	url(r'^(?P<pk>[^/]+)/update/$', viewsauthors.AuthorUpdateView.as_view(), name='author_update'),
	url(r'^(?P<pk>[^/]+)/posts/$', viewsposts.PostByAuthorListView.as_view(), name='author_posts'),
	url(r'^(?P<pk>[^/]+)/network/$', viewsauthors.AuthorNetworkView.as_view(), name='author_network'),
	url(r'^friend_request/(?P<pk>[^/]+)/$', viewsauthors.AuthorFriendRequestView.as_view({'post': 'send_request'}),
	    name='author_f_request'),
]
