from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Author
from .serializers import PostSerializer
from rest_framework.generics import (
	CreateAPIView,
	RetrieveAPIView,
	ListAPIView,
	UpdateAPIView,
	DestroyAPIView
	)
from rest_framework import permissions
# Create your views here.

def index(request):
    return HttpResponse("204 No Content")

class PostCreateView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

class PostListView(ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticated]

class PostByAuthorListView(ListAPIView):
	serializer_class = PostSerializer
	def get_queryset(self):
		author = self.kwargs['author']
		return Post.objects.filter(author=author)

class PostRetrieveView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

class PostUpdateView(UpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

class PostDestroyView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer


	


	


