from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import uuid
import unicodedata

# Create your models here.

LOCALHOST = "http://127.0.0.1:8000"
REMOTEHOST = "http://socialnets404.herokuapp.com"


class Node(models.Model):
	node_url = models.URLField()
	access_to_posts = models.BooleanField()
	access_to_images = models.BooleanField()

	def __str__(self):
		return str(self.node_url)


class Author(models.Model):
	displayName = models.CharField(blank=True, null=True, max_length=255)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	github = models.CharField(max_length=255)
	avatar = models.URLField(blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	authors = models.ManyToManyField("self", blank=True, related_name='friends')
	host = models.URLField(default="http://socialnets404.herokuapp.com/")
	url = models.URLField(default="http://socialnets404.herokuapp.com/")

	def __str__(self):
		return self.user.username

	def is_local(self):
		try:
			return str(self.host.split("/")[2]) == LOCALHOST.split("/")[2] or\
			        str(self.host.split("/")[2]) == REMOTEHOST.split("/")[2]
		except IndexError:
			return False


class FriendRequest(models.Model):
	sender = models.ForeignKey(Author, related_name="sender", on_delete=models.CASCADE)
	receiver = models.ForeignKey(Author, related_name="receiver", on_delete=models.CASCADE)


class Post(models.Model):

	title = models.CharField(max_length=40, default="Title", blank=True)
	source = models.URLField(default="http://socialnets404.herokuapp.com/")
	origin = models.URLField(default="http://socialnets404.herokuapp.com/")
	description = models.CharField(max_length=40, default="description", blank=True)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	published = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(Author, blank=True, null=True)
	content = models.CharField(max_length=255)
	visibility = models.CharField(default='PUBLIC', max_length=10)
	contentType = (
		("text/plain", 'text/plain'),
		("text/x-markdown", 'text/x-markdown')
	)
	image = models.URLField(blank=True)
	contentType = models.CharField(max_length=15, choices=contentType, default="text/plain")

	def __str__(self):
		try:
			return self.author.user.username + " on " + str(self.published)
		except:
			return "anonymous on " + str(self.published)


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
	contentType = (
		("text/plain", 'text/plain'),
		("text/x-markdown", 'text/x-markdown')
	)
	contentType = models.CharField(max_length=15, choices=contentType, default="text/plain")

	def __str__(self):
		return self.author.user.username + " on post from " + self.post.author.user.username
