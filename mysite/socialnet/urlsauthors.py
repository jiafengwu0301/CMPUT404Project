from django.conf.urls import url

from . import viewsauthors, viewsposts

urlpatterns = [
	url(r'^$', viewsauthors.AuthorListView.as_view(), name='author_list'),
	url(r'^create/$', viewsauthors.AuthorCreateView.as_view(), name='author_list'),
	url(r'^(?P<pk>\d+)/$', viewsauthors.AuthorRetrieveView.as_view(), name='author_detail'),
	url(r'^(?P<pk>\d+)/posts/$', viewsposts.PostByAuthorListView.as_view(), name='author_posts'),
	url(r'^(?P<pk>\d+)/friends/$', viewsauthors.FriendsAuthorView.as_view(), name='author_posts'),
	url(r'^friend_requests/$', viewsauthors.FriendRequestsAuthorView.as_view({'put':'add_friend_request', 'get': 'list'}), name='author_posts'),
	#url(r'^(?P<pk>\d+)/friend_requests/add$', viewsauthors.SendFriendRequestAuthorView.add_.as_view(), name='author_posts'),
]
