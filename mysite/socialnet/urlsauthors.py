from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^/authors/$', views.AuthorListView.as_view(), name='author_create'),
	url(r'^/authors/(?P<author>\d+)/$', views.AuthorProfileView.as_view(), name='author_profile')
	url(r'^/authors/(?P<author>\d+)/update/$', views.AuthorUpdateProfileView.as_view(), name='author_profile_update')

]

