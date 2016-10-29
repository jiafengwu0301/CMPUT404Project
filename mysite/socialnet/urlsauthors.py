from django.conf.urls import url

from . import viewsauthors, viewsposts

urlpatterns = [
	url(r'^$', viewsauthors.AuthorListView.as_view(), name='author_list'),
	url(r'^create/$', viewsauthors.AuthorCreateView.as_view(), name='author_list'),
	url(r'^(?P<pk>\d+)/$', viewsauthors.AuthorRetrieveView.as_view(), name='author_detail'),
	url(r'^(?P<pk>\d+)/posts/$', viewsposts.PostByAuthorListView.as_view(), name='author_posts'),
]