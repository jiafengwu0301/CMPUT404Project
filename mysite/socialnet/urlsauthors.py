from django.conf.urls import url

from . import viewsauthors, viewsposts

urlpatterns = [
    url(r'^$', viewsauthors.AuthorListView.as_view(), name='author_list'),
    url(r'^create/$', viewsauthors.AuthorCreateView.as_view(), name='author_list'),
    url(r'^(?P<pk>\d+)/$', viewsauthors.AuthorRetrieveView.as_view(), name='author_detail'),
    url(r'^(?P<pk>\d+)/update/$', viewsauthors.AuthorUpdateView.as_view(), name='author_update'),
    url(r'^(?P<pk>\d+)/posts/$', viewsposts.PostByAuthorListView.as_view(), name='author_posts'),
    url(r'^(?P<pk>\d+)/network/$', viewsauthors.AuthorNetworkView.as_view(), name='author_network'),
    url(r'^follow/(?P<pk>\d+)/$', viewsauthors.AuthorFollowView.as_view({'put': 'follow'}),
        name='author_follow'),
    url(r'^unfollow/(?P<pk>\d+)/$', viewsauthors.AuthorUnfollowView.as_view({'put': 'unfollow'}),
        name='author_follow'),
]
