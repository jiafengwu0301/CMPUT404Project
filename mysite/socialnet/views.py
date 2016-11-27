from rest_framework import generics, permissions

from . import serializers
from .models import Author, Node
from .serializers import AuthorFriendSerializer


class NodeCreateView(generics.CreateAPIView):
	queryset = Node.objects.all()
	serializer_class = serializers.NodeSerializer


class NodeDestroyView(generics.DestroyAPIView):
	queryset = Node.objects.all()
	serializer_class = serializers.NodeSerializer

	def perform_destroy(self, instance):
		user = instance.user
		user.delete()


class NodeListView(generics.ListAPIView):
	queryset = Node.objects.all()
	serializer_class = serializers.NodeSerializer
	permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
