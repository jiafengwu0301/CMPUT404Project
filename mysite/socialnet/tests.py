
from django.test import TestCase
from django.contrib.auth.models import User
from socialnet.models import *
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from .viewsauthors import *
from .viewsposts import *

class AuthorApiTest(APITestCase):

    def test_create_user(self):
        factory = APIRequestFactory()
        data = {
            "username": "absdbasbdab",
            "password": "sdsad12ad",
            "email": "sdanbv@email.com",
            "first_name": "asdgqwe",
            "last_name": "asdggqw",
            "github": "asdkjvc@github.com",
            "avatar": "null"
        }
        request = factory.post('/socialnet/authors/create/', data)
        view = AuthorCreateView.as_view()
        response = view(request)


    def test_create_post(self):
        factory = APIRequestFactory()
        data = {
            "detail": "i love big mac"
        }
        request = factory.post('/socialnet/posts/create', data)
        view = PostCreateView.as_view()
        response = view(request)
