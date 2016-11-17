from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to=settings.STATIC_ROOT, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    following = models.ManyToManyField("self", blank=True, symmetrical=False, related_name='following2')
    followers = models.ManyToManyField("self", blank=True, symmetrical=False, related_name='followers2')

    def __str__(self):
        return self.user.username


class Post(models.Model):
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author)
    text = models.CharField(max_length=255)
    public = models.BooleanField(default=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.author.user.username + " on " + str(self.published_date)


class Comment(models.Model):
    author = models.ForeignKey(Author)
    post = models.ForeignKey(Post, related_name='comments')
    text = models.CharField(max_length=255)
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.author.user.username + " on post from " + self.post.author.user.username
