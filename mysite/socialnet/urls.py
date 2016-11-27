from django.conf.urls import url, include
from . import viewsauthors
from . import viewsposts
from django.views.generic.base import TemplateView

urlpatterns = [
	url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
	url(r'^posts/', include('socialnet.urlsposts')),
	url(r'^author/', include('socialnet.urlsauthors')),
	url(r'^comments/', include('socialnet.urlscomments')),
	url(r'^auth/', viewsauthors.AuthorAuthenticationView.as_view(), name='auth'),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^friendrequest/$',
	    viewsauthors.SendRemoteFriendRequestView.as_view({'post': 'send_request'}), name='send_rf_request'),

]
