from django.conf.urls import url

from . import views
from . import viewsauthor

urlpatterns = [
	url(r'^$', viewsauthor.AuthorListView.as_view(), name='author_create'),
	url(r'^(?P<author>\d+)/$', viewsauthor.AuthorRetrieveView.as_view(), name='author_profile'),
	url(r'^(?P<author>\d+)/update/$', viewsauthor.AuthorUpdateView.as_view(), name='author_update'),
]

