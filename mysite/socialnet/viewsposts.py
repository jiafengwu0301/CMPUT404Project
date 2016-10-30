from itertools import chain
from django.http import HttpResponse
from rest_framework import generics, permissions
from . import permissions as my_permissions
from .models import Post
from .serializers import PostSerializer, CreatePostSerializer


# Create your views here.


def index(request):
	return HttpResponse("204 No Content")


# PUT a new Post. Requires authentication (Prove you are the owner by sending object)
class PostCreateView(generics.CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = CreatePostSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(author=self.request.user.author)


# List of posts that are visible for the user
class PostListView(generics.ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		result_list = list(chain(Post.objects.filter(public=True),
		                         Post.objects.filter(author=self.request.user.author, public=False)))
		return result_list


# List of Posts of the user or the visible posts of other users
class PostByAuthorListView(generics.ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer()
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		author = self.kwargs['pk']
		if int(author) == self.request.user.author.id:
			result_list = Post.objects.filter(author=self.request.user.author)
		else:
			result_list = Post.objects.filter(author=author, public=True)
		return result_list


# Return a single post if the post is public or if you are the owner
class PostRetrieveView(generics.RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerOrIsPublicPost]


# PUT an Update. Requires authentication (Prove you are the owner by sending object)
class PostUpdateView(generics.UpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = CreatePostSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, my_permissions.IsOwnerForModifyPost]


# DELETE an post. Requires authentication (Prove you are the owner by sending object)
class PostDestroyView(generics.DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, my_permissions.IsOwnerForModifyPost]
