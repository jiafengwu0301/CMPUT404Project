from itertools import chain
from django.http import HttpResponse
from rest_framework import generics, permissions, views, response, status
from . import permissions as my_permissions
from .models import Post, Comment
from .serializers import PostSerializer, CreatePostSerializer, CommentSerializer, CreateCommentSerializer


# Create your views here.


def index(request):
	return HttpResponse("204 No Content")


# POST a new Post. Requires authentication (Prove you are the owner by sending object)
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
		public_posts = Post.objects.filter(public=True)
		my_private_posts = Post.objects.filter(author=self.request.user.author, public=False)
		result_list = list(chain(public_posts, my_private_posts))
		return result_list


# List of Posts of the user or the visible posts of other users
class PostByAuthorListView(generics.ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
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
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsPostPublicOrOwner]


# PUT an Update. Requires authentication (Prove you are the owner by sending object)
class PostUpdateView(generics.UpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = CreatePostSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForModifyPost]


# DELETE an post. Requires authentication (Prove you are the owner by sending object)
class PostDestroyView(generics.DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForModifyPost]


# POST a new comment in the post designated in the URL.
class CommentCreateView(generics.CreateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CreateCommentSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsPostPublicOrOwner]

	def perform_create(self, serializer):
		currentPost = Post.objects.get(id=self.kwargs['pk'])
		serializer.save(author=self.request.user.author, post=currentPost)


# GET all the comments. Admin only function
class CommentListView(generics.ListAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


# GET a single comment. Admin only function
class CommentRetrieveView(generics.RetrieveAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


# DELETE a comment. Requires authentication and owner of comment or post
class CommentDestroyView(generics.DestroyAPIView):
	queryset = Comment.objects.all()
	serializer_class = CreateCommentSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForModifyComment]
