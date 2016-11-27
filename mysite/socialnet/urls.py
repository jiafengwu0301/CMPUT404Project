from django.conf.urls import url, include
from . import viewsauthors
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
	url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
	url(r'^posts/', include('socialnet.urlsposts')),
	url(r'^author/', include('socialnet.urlsauthors')),
	url(r'^comments/', include('socialnet.urlscomments')),
	url(r'^auth/', viewsauthors.AuthorAuthenticationView.as_view(), name='auth'),
	url(r'^api-auth', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^friendrequest$',
	    viewsauthors.SendRemoteFriendRequestView.as_view({'post': 'send_request'}), name='send_rf_request'),
	url(r'^friends/(?P<pk>[^/]+)$', viewsauthors.
	    AuthorFriendListView.as_view({'get': 'retrieve', 'post': 'is_friend'}), name='author_friends'),
	url(r'^friends/(?P<pk1>[^/]+)/(?P<pk2>[^/]+)$', viewsauthors.
	    AuthorIsFriendListView.as_view({'get': 'is_friend'}), name='is_friend'),
	url(r'^nodes/$', views.NodeListView.as_view(), name='node'),
	url(r'^nodes/create/$', views.NodeCreateView.as_view(), name='node_create'),
	url(r'^nodes/destroy/(?P<pk>[^/]+)/$', views.NodeDestroyView.as_view(), name='node_destroy'),
]
