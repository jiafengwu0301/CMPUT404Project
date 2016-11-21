from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import uuid

# Create your models here.


class Node(models.Model):
	node_url = models.URLField()
	access_to_posts = models.BooleanField()
	access_to_images = models.BooleanField()


class Author(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	github = models.CharField(max_length=255)
	avatar = models.URLField(blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	friends = models.ManyToManyField("self", blank=True, related_name='friends')
	host = models.URLField(default="http://127.0.0.1:8000/socialnet/")

	def __str__(self):
		return self.user.username


class FriendRequest(models.Model):
	sender = models.ForeignKey(Author, related_name="sender", on_delete=models.CASCADE)
	receiver = models.ForeignKey(Author, related_name="receiver", on_delete=models.CASCADE)


class Post(models.Model):
	title = models.CharField(max_length=40, default="Title", blank=True)
	host = models.URLField(default="http://127.0.0.1:8000/socialnet/")
	description = models.CharField(max_length=40, default="description", blank=True)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	published = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(Author)
	content = models.CharField(max_length=255)
	visibility = models.BooleanField(default=False)
	content_type = (
		("text/plain", 'text/plain'),
		("text/markdown", 'text/markdown')
	)
	image = models.URLField(blank=True)
	content_type = models.CharField(max_length=15, choices=content_type, default="text/plain")

	def __str__(self):
		return self.author.user.username + " on " + str(self.published)


class PostVisibility(models.Model):
	author = models.ForeignKey(Author)
	post = models.ForeignKey(Post)
	visible = models.BooleanField(default=True)


class Comment(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	author = models.ForeignKey(Author)
	post = models.ForeignKey(Post, related_name='comments')
	comment = models.CharField(max_length=255)
	pubdate = models.DateTimeField(auto_now_add=True)
	content_type = (
		("text/plain", 'text/plain'),
		("text/markdown", 'text/markdown')
	)
	content_type = models.CharField(max_length=15, choices=content_type, default="text/plain")

	def __str__(self):
		return self.author.user.username + " on post from " + self.post.author.user.username
