from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework import generics, permissions, response, status, views
from .models import Author
from .serializers import AuthorSerializer, FullAuthorSerializer, AuthenticateSerializer, FriendsAuthorSerializer, \
	FriendRequestsAuthorSerializer
from . import permissions as my_permissions


class AuthorListView(generics.ListAPIView):
	queryset = Author.objects.all()
	serializer_class = AuthorSerializer
	permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class AuthorCreateView(generics.CreateAPIView):
	queryset = Author.objects.all()
	serializer_class = FullAuthorSerializer
	permission_classes = [permissions.AllowAny]


class AuthorRetrieveView(generics.RetrieveAPIView):
	queryset = Author.objects.all()
	serializer_class = AuthorSerializer
	permission_classes = [permissions.IsAuthenticated]


class AuthorAuthenticationView(views.APIView):
	queryset = Author.objects.all()
	serializer_class = AuthenticateSerializer

	def post(self, request, *args, **kwargs):
		data = request.data
		serializer = AuthenticateSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer.data
			return response.Response(new_data, status=status.HTTP_200_OK)
		return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FriendsAuthorView(generics.RetrieveAPIView):
	queryset = Author.objects.all()
	serializer_class = FriendsAuthorSerializer
	permission_classes = [permissions.IsAuthenticated]


class FriendRequestsAuthorView(viewsets.ModelViewSet):
	#queryset = Author.objects.all()
	serializer_class = FriendRequestsAuthorSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForAccessAuthor]

	def get_queryset(self):
		result_list = Author.objects.filter(id=self.request.user.author.id)
		return result_list

	@detail_route(methods=['put'])
	def add_friend_request(self, request):
		friend_requests = request.user.author.friend_requests
		serializer = FriendRequestsAuthorSerializer(data=request.data)
		if serializer.is_valid():
			friend_requests += request.data
			friend_requests.save()
			return friend_requests


class SendFriendRequestAuthorView(generics.CreateAPIView):
	queryset = Author.objects.all()
	serializer_class = FriendRequestsAuthorSerializer
	permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwnerForAccessAuthor]
