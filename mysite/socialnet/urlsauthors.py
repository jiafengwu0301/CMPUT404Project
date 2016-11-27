from django.conf.urls import url

from . import viewsauthors, viewsposts

urlpatterns = [
	url(r'^$', viewsauthors.AuthorListView.as_view(), name='author_list'),
	url(r'^create/$', viewsauthors.AuthorCreateView.as_view(), name='author_create'),
	url(r'^posts/$', viewsposts.CurrentAuthorPostListView.as_view(), name='post_author_list'),
	url(r'^(?P<pk>[^/]+)/$', viewsauthors.AuthorRetrieveView.as_view(), name='author_detail'),
	url(r'^(?P<pk>[^/]+)/update/$', viewsauthors.AuthorUpdateView.as_view(), name='author_update'),
	url(r'^(?P<pk>[^/]+)/posts/$', viewsposts.PostByAuthorListView.as_view(), name='author_posts'),
	url(r'^(?P<pk>[^/]+)/network/$', viewsauthors.AuthorNetworkView.as_view(), name='author_network'),
	url(r'^friend_request/(?P<pk>[^/]+)/$',
	    viewsauthors.SendFriendRequestView.as_view({'post': 'send_request'}), name='send_f_request'),
	url(r'^friends/friend_requests/$', viewsauthors.FriendRequestByAuthorView.as_view(), name='f_request_by_author'),
	url(r'^friends/unfriend/(?P<pk>[^/]+)/$',
	    viewsauthors.UnfriendView.as_view({'delete': 'unfriend'}), name='f_request_by_author'),
	url(r'^friend_request/accept/(?P<pk>[^/]+)/$',
	    viewsauthors.AcceptFriendRequestView.as_view({'post': 'accept_request'}), name='acc_f_request'),
	url(r'^friend_request/reject/(?P<pk>[^/]+)/$',
	    viewsauthors.AcceptFriendRequestView.as_view({'delete': 'reject_request'}), name='acc_f_request'),
]
