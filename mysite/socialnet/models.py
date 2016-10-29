from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver


# Create your models here.

class Author(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	github = models.CharField(max_length=255)
	avatar = models.ImageField(upload_to=settings.STATIC_ROOT, blank=True)
	date_created = models.DateField(auto_now_add=True)
	friends = models.ManyToManyField("self", blank=True)
	friend_requests = models.ManyToManyField("self", blank=True)

	def __str__(self):
		return self.user.username


class Post(models.Model):
	published_date = models.DateField(auto_now_add=True)
	author = models.ForeignKey(Author)
	text = models.CharField(max_length=255)
	public = models.BooleanField(default=True)

	def __str__(self):
		return self.author.user.username + " on " + str(self.published_date)


class Comment(models.Model):
	author = models.ForeignKey(Author)
	post = models.ForeignKey(Post)
	text = models.CharField(max_length=255)
	published_date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.author.user.username + " on post from " + self.post.author.user.username
