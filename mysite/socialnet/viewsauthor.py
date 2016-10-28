from django.shortcuts import render
from django.http import HttpResponse
from .models import Author
from .serializers import AuthorSerializer
from rest_framework.generics import (
	CreateAPIView,
	RetrieveAPIView,
	ListAPIView,
	UpdateAPIView,
	DestroyAPIView
	)
from rest_framework import permissions


class AuthorListView(ListAPIView):
	#getting list of all authors
	serializer_class = AuthorSerializer
	queryset = Author.objects.all()

class AuthorRetrieveView(RetrieveAPIView):
	#getting specific author profile info
	serializer_class = AuthorSerializer
	queryset = Author.objects.all()


class AuthorUpdateView(UpdateAPIView):
 #getting specific authors update view
	serializer_class = AuthorSerializer
	queryset = Author.objects.all()
	




