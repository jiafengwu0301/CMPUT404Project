from rest_framework import permissions
from .models import Post, Comment, Author


class IsOwnerForModifyPost(permissions.BasePermission):
    message = 'You must be this author to update it.'

    def has_object_permission(self, request, view, obj):
        return obj.author.user.id == request.user.id


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
        actualPost = Post.objects.get(id=view.kwargs['pk'])
        return request.user.author.id == actualPost.author.id or actualPost.public


class IsCommentFromAPublicPost(permissions.BasePermission):
    message = "post not public for you to read it Comments."

    def has_permission(self, request, view):
        actualPost = Post.objects.get(id=Comment.objects.get(id=view.kwargs['pk']).post.id)
        return request.user.author.id == actualPost.author.id or actualPost.public


class IsOwnerForModifyComment(permissions.BasePermission):
    message = "You cant modify a comment that is not yours"

    def has_object_permission(self, request, view, obj):
        actualComment = Comment.objects.get(id=view.kwargs['pk'])
        actualPost = actualComment.post
        return request.user.author.id == actualComment.author.id or \
               request.user.author.id == actualPost.author.id


class IsOwnerForModifyAuthor(permissions.BasePermission):
    message = "You cant modify an author that is not you"

    def has_object_permission(self, request, view, obj):
        return Author.objects.get(id=request.user.author.id) == \
               Author.objects.get(id=view.kwargs['pk'])
