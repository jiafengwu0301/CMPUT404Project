from django.conf.urls import url, include
from . import viewsauthors

from . import viewsposts

urlpatterns = [
	url(r'^$', viewsposts.index, name='index'),
	url(r'^posts/', include('socialnet.urlsposts')),
	url(r'^authors/', include('socialnet.urlsauthors')),
	url(r'^auth/', viewsauthors.AuthorAuthenticationView.as_view(), name='auth'),
	url(r'^api-auth/', include('rest_framework.urls',
	                           namespace='rest_framework')),
]

#127.0.0.1:8000/posts/create/
#127.0.0.1:8000/posts
#127.0.0.1:8000/posts/[id]
#127.0.0.1:8000/posts/[id]/update/
#127.0.0.1:8000/posts/[id]/destroy/
#127.0.0.1:8000/posts/author/[id]