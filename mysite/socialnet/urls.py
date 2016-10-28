from django.conf.urls import url, include

from . import views
from . import viewsauthor

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^posts/create/$', views.PostCreateView.as_view(), name='post_create'),
	url(r'^posts/$', views.PostListView.as_view(), name='post_list'),
	url(r'^posts/author/(?P<author>\d+)/$', views.PostByAuthorListView.as_view(), name='post_list_by_author'),
	url(r'^posts/(?P<pk>\d+)/$', views.PostRetrieveView.as_view(), name='post_detail'),
	url(r'^posts/(?P<pk>\d+)/update/$', views.PostUpdateView.as_view(), name='post_update'),
	url(r'^posts/(?P<pk>\d+)/destroy/$', views.PostDestroyView.as_view(), name='post_destroy'),
	
	url(r'^authors/', include('socialnet.urlsauthors')),
]

# What should be working url(r'^socialnet/', include('socialnet.urls')),

#127.0.0.1:8000/posts/create/
#127.0.0.1:8000/posts
#127.0.0.1:8000/posts/[id]
#127.0.0.1:8000/posts/[id]/update/
#127.0.0.1:8000/posts/[id]/destroy/
#127.0.0.1:8000/posts/author/[id]
