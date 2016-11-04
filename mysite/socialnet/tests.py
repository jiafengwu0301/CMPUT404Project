#
# from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
#
# from .serializers import AuthorSerializer
#
# class CreateUserTest(APITestCase):
#     def setUp(self):
#         self.superuser = User.objects.create_superuser('admin', 'admin123', 'admin@email.com')
#         self.assertTrue(self.superuser.is_staff)
#         # self.assertTrue(self.admin.is_admin)
#         self.assertTrue(self.superuser.is_superuser)
#         self.superuser.save()
#         self.client.login(username = 'admin', password = 'admin123')
#         self.data = {'username': 'mike', 'first_name': 'Mike', 'last_name': 'Tyson'}
#     def test_can_create_user(self):
#         repsonse = self.client.post(reverse('user-list'), self.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
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
