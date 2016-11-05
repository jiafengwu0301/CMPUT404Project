from django.conf.urls import url, include
from . import viewsauthors
from . import viewsposts
from django.views.generic.base import TemplateView

urlpatterns = [
	url(r'^$', TemplateView.as_view(template_name = "index.html"), name='index'),
	url(r'^posts/', include('socialnet.urlsposts')),
	url(r'^authors/', include('socialnet.urlsauthors')),
	url(r'^comments/', include('socialnet.urlscomments')),
	url(r'^auth/', viewsauthors.AuthorAuthenticationView.as_view(), name='auth'),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

# 127.0.0.1:8000/posts/create/
# 127.0.0.1:8000/posts
# 127.0.0.1:8000/posts/[id]
# 127.0.0.1:8000/posts/[id]/update/
# 127.0.0.1:8000/posts/[id]/destroy/
# 127.0.0.1:8000/posts/author/[id]
