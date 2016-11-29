import datetime
import json
import uuid
from itertools import chain

import requests
from django.contrib.auth.models import User
from django.core import exceptions as django_exceptions
from django.http import HttpResponse
from rest_framework import generics, permissions, response, status
from rest_framework import pagination
from rest_framework import viewsets
from rest_framework.decorators import detail_route

from . import permissions as my_permissions
from .models import Post, Comment, Node, REMOTEHOST, LOCALHOST, Author, PostVisibility
from .serializers import PostSerializer, CreatePostSerializer, CommentSerializer, CreateCommentSerializer, \
	RemotePostSerializer, LocalPostSerializer, RemoteCommentSerializer, GetCommentSerializer


class PostPagination(pagination.PageNumberPagination):
	page_size = 5
	page_size_query_param = 'size'
	max_page_size = 50

	def get_paginated_response(self, data):
		return response.Response({
			'query': 'posts',
			'count': self.page.paginator.count,
			'size': self.page_size,
			'next': self.get_next_link(),
			'previous': self.get_previous_link(),
			'posts': data
		})


class CommentPagination(pagination.PageNumberPagination):
	page_size = 5
	page_size_query_param = 'size'
	max_page_size = 50

	def get_paginated_response(self, data):
		if self.request.method == 'GET':
			return response.Response({
				'query': 'comments',
				'size': self.page_size,
				'count': self.page.paginator.count,
				'next': self.get_next_link(),
				'previous': self.get_previous_link(),
				'comments': data
			})
		elif self.request.method == 'POST':
			return response.Response({
				'query': 'addComment',
				'size': self.page_size,
				'count': self.page.paginator.count,
				'next': self.get_next_link(),
				'previous': self.get_previous_link(),
				'comments': data
			})


# Create your views here.


def index(request):
	return HttpResponse("204 No Content")


# POST a new Post. Requires authentication (Prove you are the owner by sending object)
class PostCreateView(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = CreatePostSerializer
	permission_classes = [permissions.IsAuthenticated]

	@detail_route(methods=['post'])
	def create_post(self, request):
		data = request.data
		author = request.user.author
		serializer = CreatePostSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			post = serializer.save()
			post.author = author
			post.source = REMOTEHOST + "/posts/" + str(post.id)
			post.origin = post.source
			post.save()

			# visibility
			if post.visibility == 'FRIENDS':
				for a in author.authors.all():
					PostVisibility.objects.create(author=a, post=post, visible=True)

			if post.visibility == 'FOAF':
				for a in author.authors.all():
					PostVisibility.objects.create(author=a, post=post, visible=True)
					for b in a.authors.all():
						PostVisibility.objects.create(author=b, post=post, visible=True)

			return response.Response(status=status.HTTP_201_CREATED)
		return response.Response(status=status.HTTP_400_BAD_REQUEST)


class PostListView(generics.ListAPIView):
	serializer_class = PostSerializer
	pagination_class = PostPagination
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsNodeSeeingIt]

	def get_queryset(self):
		result_list = Post.objects.filter(visibility="PUBLIC")
		return result_list


# List of posts that are visible for the user
class CurrentAuthorPostListView(generics.ListAPIView):
	serializer_class = LocalPostSerializer
	pagination_class = PostPagination
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		public_posts = Post.objects.filter(visibility="PUBLIC")
		server_only = Post.objects.filter(visibility="SERVERONLY")
		try:
			my_private_posts = Post.objects.filter(author=self.request.user.author).exclude(visibility="PUBLIC")
			posts_i_can_see = Post.objects.filter(postvisibility__author=self.request.user.author,
			                                      postvisibility__visible=True)
			result_list = list(chain(public_posts, my_private_posts, posts_i_can_see, server_only))
		except AttributeError:
			result_list = list(chain(public_posts, server_only))
		return result_list


class RemotePostListView(viewsets.ViewSet):
	serializer_class = RemotePostSerializer
	pagination_class = PostPagination

	def list(self, request):
		nodes = Node.objects.all()
		remote_json_posts = {}
		for node in nodes:
			print str(node)
			if str(node) != LOCALHOST and str(node) != REMOTEHOST:
				print "PASSED"
				if node.access_to_posts:
					try:
						r = requests.get(str(node) + "/posts", auth=(node.rcred_username, node.rcred_password),
						                 timeout=3)
					except:
						pass
					try:
						if r.status_code == 200:
							remote_json_posts[str(node)] = r.json()
					except:
						pass
				else:
					print "NO ACCESS"
		return response.Response(remote_json_posts, status=status.HTTP_200_OK)


# List of Posts of the user or the visible posts of other users
class PostByAuthorListView(generics.ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		author_id = self.kwargs['pk']
		if author_id == str(self.request.user.author.id):
			result_list = Post.objects.filter(author=self.request.user.author)
		else:
			result_list = Post.objects.filter(author=author_id, visibility="PUBLIC")
		return result_list


# Return a single post if the post is public or if you are the owner
class PostRetrieveView(generics.RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [my_permissions.IsPostPublicOrOwner]


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


class CommentsByPostIdView(viewsets.ModelViewSet):
	permission_classes = [permissions.IsAuthenticated]
	pagination_class = CommentPagination
	serializer_class = RemoteCommentSerializer
	queryset = Comment.objects.all()

	def get_queryset(self):
		queryset = Comment.objects.filter(post__id=self.kwargs['pk'])
		return queryset

	def list(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		print queryset
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = GetCommentSerializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = GetCommentSerializer(queryset, many=True)
		return response.Response(serializer.data)

	def send_to_remote(self, url, data, node):
		r = requests.post(url, json=data, auth=(node.rcred_username, node.rcred_password))
		return r

	def makeAuthor(self, data, node_url):
		id = data['id']
		displayNamesplit = data['displayName'].split(" ")
		username = displayNamesplit[0] + id[0:7]
		first_name = username
		last_name = username
		email = username + "@nousageemail.com"
		try:
			user = User.objects.create(username=username,
			                           first_name=first_name, last_name=last_name, email=email)
		except:
			return User.objects.get(username=username)
		author = Author.objects.create(user=user, id=uuid.UUID(id),
		                               displayName=str(data['displayName']), github="noGitHUB",
		                               host=node_url, url=node_url + "/authors/" + id)
		return author

	def create(self, request, *args, **kwargs):
		print request.data
		author_is_remote = False
		try:
			try:
				print "HAHAHAHAHAHAHAHA"
				data = json.loads(json.dumps(request.data))
				author_host = data['comment']['author']['host']
			except:
				author_host = str(request.data['comment.author.host'])
			try:
				author_host = author_host.split("/", 3)[2]
			except:
				pass
			node_author = Node.objects.get(node_url="http://" + author_host)
		except django_exceptions.ObjectDoesNotExist:
			return response.Response(status=status.HTTP_403_FORBIDDEN)

		serializer = RemoteCommentSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			data = serializer.data

		try:
			author = Author.objects.get(id=data['comment']['author']['id'])
		except django_exceptions.ObjectDoesNotExist:
			author = self.makeAuthor(data['comment']['author'], node_author.node_url)
		post_id = kwargs['pk']
		try:
			post = Post.objects.get(id=post_id)
			comment = Comment.objects.create(post=post, author=author,
			                                 comment=data['comment']['comment'],
			                                 contentType=data['comment']['contentType'])
			return response.Response(status=status.HTTP_200_OK)
		except django_exceptions.ObjectDoesNotExist:
			request = data
			print request
			remote_node = Node.objects.get(node_url="http://" + data['post'].split("/", 3)[2])
			res = self.send_to_remote(data['post'] + '/comments', request, remote_node)
			return response.Response(res, status=status.HTTP_200_OK)
		#return response.Response("some error on response", status=status.HTTP_502_BAD_GATEWAY)

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


class PostCommentsRetrieveView(viewsets.ViewSet):
	serializer_class = RemotePostSerializer
	pagination_class = PostPagination

	def list(self, request):
		nodes = Node.objects.all()
		remote_json_posts = {}
		for url in nodes:
			if str(url) != LOCALHOST and str(url) != REMOTEHOST:
				r = requests.get(str(url) + "/posts", auth=(url.rcred_username, url.rcred_password))
				remote_json_posts[str(url)] = r.json()
		return response.Response(remote_json_posts, status=status.HTTP_200_OK)
