import json
from _testcapi import raise_exception
from itertools import chain
import requests
from django.contrib.auth.models import User
from django.core import exceptions as django_exceptions
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from requests.auth import HTTPBasicAuth
from rest_framework import generics, permissions, response, status, views
from rest_framework import viewsets
from rest_framework.decorators import detail_route
import uuid

from . import permissions as my_permissions
from .models import Author, FriendRequest, Node, PostVisibility
from .serializers import FullAuthorSerializer, AuthenticateSerializer, \
	UpdateAuthorSerializer, AuthorNetworkSerializer, AuthorSerializer, \
	FriendRequestSerializer, RemoteRequestSerializer, AuthorFriendListSerializer, AuthorFriendSpecialListSerializer


class AuthorListView(generics.ListAPIView):
	queryset = Author.objects.all()
	serializer_class = AuthorSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsAdminOrIsLocalUser]


class AuthorCreateView(generics.CreateAPIView):
	queryset = Author.objects.all()
	serializer_class = FullAuthorSerializer
	permission_classes = [permissions.AllowAny]


class AuthorUpdateView(generics.UpdateAPIView):
	queryset = Author.objects.all()
	serializer_class = UpdateAuthorSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForModifyAuthor]


class AuthorRetrieveView(generics.RetrieveAPIView):
	queryset = Author.objects.all()
	serializer_class = AuthorSerializer
	permission_classes = [permissions.IsAuthenticated]


class AuthorAuthenticationView(views.APIView):
	queryset = Author.objects.all()
	serializer_class = AuthenticateSerializer

	def post(self, request):
		data = request.data
		serializer = AuthenticateSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer.data
			return response.Response(new_data, status=status.HTTP_200_OK)
		return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorNetworkView(generics.RetrieveAPIView):
	queryset = Author.objects.all()
	serializer_class = AuthorNetworkSerializer


class AuthorFriendListView(viewsets.ModelViewSet):
	queryset = Author.objects.all()
	serializer_class = AuthorFriendListSerializer

	def retrieve(self, request, *args, **kwargs):
		self.serializer_class = AuthorFriendListSerializer
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		data = serializer.data
		data['query'] = 'friends'
		return response.Response(data, status=status.HTTP_200_OK)

	def is_friend(self,request, *args, **kwargs):
		self.serializer_class = AuthorFriendSpecialListSerializer
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		to_be_removed = []
		data = request.data
		count = 0
		for aid in data['authors']:
			is_friend = False
			for friend in instance.authors.all():
				if aid == str(friend.id):
					print aid + " is equals to " + str(friend.id)
					is_friend = True
				else:
					print aid + " is not equals to " + str(friend.id)

			if not is_friend:
				print aid + " and " + str(instance.id) + " are not friends at all."
				to_be_removed.append(count)
			count += 1
		for i in reversed(to_be_removed):
			print i
			data['authors'].pop(i)
		return response.Response(data['authors'], status=status.HTTP_200_OK)


class SendFriendRequestView(viewsets.ModelViewSet):
	serializer_class = AuthorNetworkSerializer

	def get_queryset(self):
		result_list = FriendRequest.objects.filter(receiver=self.request.user.author)
		return result_list

	@detail_route(methods=['post'])
	def send_request(self, request, **kwargs):
		try:
			author = request.user.author
			receiver = get_object_or_404(Author, id=kwargs['pk'])
			try:
				FriendRequest.objects.get(sender=author, receiver=author)
				return response.Response(status=status.HTTP_400_BAD_REQUEST)
			except django_exceptions.ObjectDoesNotExist:
				pass
			friendRequest = FriendRequest.objects.create(sender=author, receiver=receiver)
			friendRequest.save()
			return response.Response(status=status.HTTP_202_ACCEPTED)
		except AttributeError:
			return response.Response(status=status.HTTP_400_BAD_REQUEST)


class SendRemoteFriendRequestView(viewsets.ViewSet):
	serializer_class = RemoteRequestSerializer
	queryset = FriendRequest.objects.all()
	permission_classes = [permissions.IsAuthenticated]

	def send_to_remote(self, url, data, node):
		r = requests.post(url, json=data, auth=(node.rcred_username, node.rcred_password))
		return r

	def makeAuthor(self, data, node_url):
		print "Making author"
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
		                               host=node_url, url=node_url+"/author/"+id)
		return author

	@detail_route(methods=['post'])
	def send_request(self, request):
		# check if node is allowed. if not, 403
		try:
			try :
				data = json.loads(json.dumps(request.data))
				print data
				author_host = data['author']['host']
				friend_host = data['friend']['host']
				is_json = True
			except:
				author_host = str(request.data['author.host'])
				friend_host = str(request.data['friend.host'])
			try:
				author_host = author_host.split("/", 3)[2]
				friend_host = friend_host.split("/", 3)[2]
			except:
				pass
			node_author = Node.objects.get(node_url="http://"+author_host)
			node_friend = Node.objects.get(node_url="http://"+friend_host)
		except django_exceptions.ObjectDoesNotExist:
			return response.Response(status=status.HTTP_403_FORBIDDEN)
		# check if json is ok. if yes, get authors that are trying to be friends
		serializer = RemoteRequestSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			data = serializer.data
			try:
				author = Author.objects.get(id=data['author']['id'])
			except django_exceptions.ObjectDoesNotExist:
				author = self.makeAuthor(data['author'], node_author.node_url)
			try:
				friend = Author.objects.get(id=data['friend']['id'])
			except django_exceptions.ObjectDoesNotExist:
				friend = self.makeAuthor(data['friend'], node_friend.node_url)
			#check if there its for accept or not. if not, add the friend request
			try:
				friendRequest = FriendRequest.objects.get(sender=author, receiver=friend)
				friendRequest.delete()
				author.authors.add(friend)
				post_visibilities = PostVisibility.objects.filter(post__author=author)
				for pv in post_visibilities:
					if pv.post.visibility == 'FRIENDS' or pv.post.visibility == 'FOAF':
						PostVisibility.objects.create(post=pv.post, author=friend)
						if pv.post.visibility == 'FOAF':
							for f in friend.authors:
								PostVisibility.objects.create(post=pv.post, author=f)
				return response.Response(status=status.HTTP_202_ACCEPTED)
			except django_exceptions.ObjectDoesNotExist:
				try:
					FriendRequest.objects.get(sender=friend, receiver=author)
				except django_exceptions.ObjectDoesNotExist:
					FriendRequest.objects.create(sender=friend, receiver=author)
			try:
				data['query'] = 'friendrequest'
				res = self.send_to_remote(node_author.node_url+'/friendrequest', data, node_author)
				return response.Response(res, status=status.HTTP_200_OK)

			except:
				return response.Response("REMOTE SERVER ERROR", status=status.HTTP_503_SERVICE_UNAVAILABLE)


class FriendRequestByAuthorView(generics.ListAPIView):
	serializer_class = FriendRequestSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		result_list = FriendRequest.objects.filter(receiver=self.request.user.author)
		result_list = list(chain(result_list, FriendRequest.objects.filter(sender=self.request.user.author)))
		return result_list


class AcceptFriendRequestView(viewsets.ModelViewSet):
	serializer_class = AuthorNetworkSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForAccessAuthor]

	def get_queryset(self):
		result_list = FriendRequest.objects.filter(receiver=self.request.user.author)
		return result_list

	@detail_route(methods=['post'])
	def accept_request(self, request, **kwargs):
		receiver = request.user.author
		sender = get_object_or_404(Author, id=kwargs['pk'])
		friend_req = get_object_or_404(FriendRequest, sender=sender)
		friend_req.delete()
		receiver.authors.add(sender)
		post_visibilities = PostVisibility.objects.filter(post__author=receiver)
		for pv in post_visibilities:
			if pv.post.visibility == 'FRIENDS' or pv.post.visibility == 'FOAF':
				PostVisibility.objects.create(post=pv.post, author=sender)
				if pv.post.visibility == 'FOAF':
					for f in sender.authors:
						PostVisibility.objects.create(post=pv.post, author=f)
		return response.Response(status=status.HTTP_202_ACCEPTED)

	@detail_route(methods=['delete'])
	def reject_request(self, request, **kwargs):
		receiver = request.user.author
		sender = get_object_or_404(Author, id=kwargs['pk'])
		friend_req = get_object_or_404(FriendRequest, sender=sender)
		friend_req.delete()
		return response.Response(status=status.HTTP_202_ACCEPTED)


class UnfriendView(viewsets.ModelViewSet):
	serializer_class = AuthorNetworkSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForAccessAuthor]

	def get_queryset(self):
		result_list = FriendRequest.objects.filter(receiver=self.request.user.author)
		return result_list

	@detail_route(methods=['delete'])
	def unfriend(self, request, **kwargs):
		unfriender = request.user.author
		unfriended = get_object_or_404(Author, id=kwargs['pk'])
		unfriender.authors.remove(unfriended)
		return response.Response(status=status.HTTP_202_ACCEPTED)


class AuthorIsFriendListView(viewsets.ModelViewSet):
	queryset = Author.objects.all()
	serializer_class = AuthorFriendListSerializer

	def is_friend(self,request, *args, **kwargs):
		author1 = get_object_or_404(Author, id=kwargs['pk1'])
		author2 = get_object_or_404(Author, id=kwargs['pk2'])
		is_friend = False
		for friend in author1.authors.all():
			if str(friend.id) == str(author2.id):
				is_friend = True
		res = {
			'query': "friends",
			'authors': [str(author1.id), str(author2.id)],
			'friends': is_friend
		}
		return response.Response(res, status=status.HTTP_200_OK)
