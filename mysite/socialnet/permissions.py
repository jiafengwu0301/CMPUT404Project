from rest_framework import permissions


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
