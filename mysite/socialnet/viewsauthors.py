from itertools import chain

from django.core import exceptions as django_exceptions
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, response, status, views
from rest_framework import viewsets
from rest_framework.decorators import detail_route

from . import permissions as my_permissions
from .models import Author, FriendRequest
from .serializers import FullAuthorSerializer, AuthenticateSerializer, \
	UpdateAuthorSerializer, AuthorNetworkSerializer, AuthorFriendSerializer, FriendRequestSerializer


class AuthorListView(generics.ListAPIView):
	queryset = Author.objects.all()
	serializer_class = AuthorFriendSerializer


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
	serializer_class = AuthorFriendSerializer
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


class SendFriendRequestView(viewsets.ModelViewSet):
	serializer_class = AuthorNetworkSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForAccessAuthor]

	def get_queryset(self):
		result_list = FriendRequest.objects.filter(receiver=self.request.user.author)
		return result_list

	@detail_route(methods=['post'])
	def send_request(self, request, **kwargs):
		author = request.user.author
		receiver = get_object_or_404(Author, id=kwargs['pk'])
		friendRequest = FriendRequest.objects.create(sender=author, receiver=receiver)
		friendRequest.save()
		return response.Response(status=status.HTTP_202_ACCEPTED)


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
		receiver.friends.add(sender)
		return response.Response(status=status.HTTP_202_ACCEPTED)

	@detail_route(methods=['delete'])
	def reject_request(self, request, **kwargs):
		receiver = request.user.author
		sender = get_object_or_404(Author, id=kwargs['pk'])
		friend_req = get_object_or_404(FriendRequest, sender=sender)
		friend_req.delete()
		return response.Response(status=status.HTTP_202_ACCEPTED)
		#unfriender = request.user.author
		#unfriended = get_object_or_404(Author, id=kwargs['pk'])
		#unfriender.friends.remove(unfriended)
		#return response.Response(status=status.HTTP_202_ACCEPTED)


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
		unfriender.friends.remove(unfriended)
		return response.Response(status=status.HTTP_202_ACCEPTED)