from django.contrib import admin

# Register your models here.
from .models import Author, Post, Comment, FriendRequest, PostVisibility, Node

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(FriendRequest)
admin.site.register(PostVisibility)
admin.site.register(Node)
