from rest_framework import permissions
from .models import Post


class IsOwnerForModifyPost(permissions.BasePermission):
	message = 'You must be this author to update it.'

	def has_object_permission(self, request, view, obj):
		return obj.author.user.id == request.user.id


class IsOwnerOrIsPublicPost(permissions.BasePermission):
	message = 'You cant see it.'

	def has_object_permission(self, request, view, obj):
		return obj.author.user.id == request.user.id or obj.public


class IsOwnerForAuthenticateAuthor(permissions.BasePermission):
	message = "You can't access personal data from a user that is not you."

	def has_object_permission(self, request, view, obj):
		return obj.user.id == request.user.id


class IsOwnerForAccessAuthor(permissions.BasePermission):
	message = "You can't access personal data from a user that is not you."

	def has_object_permission(self, request, view, obj):
		return obj.user.id == request.user.id


class IsPostPublicOrOwner(permissions.BasePermission):
	message = "post not public for you to read it properties."

	def has_permission(self, request, view):
		actualPost = Post.objects.get(id=view.kwargs['postpk'])
		return request.user.author.id == actualPost.author.id or actualPost.public
