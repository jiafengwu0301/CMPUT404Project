# Create your tests here.
from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User
from socialnet.models import *
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from .viewsauthors import *
from .viewsposts import *
import base64
#from .testsutil import *
# class CreateSuperUser(TestCase):
#

class AuthorApiTest(APITestCase):

    def test_create_user(self):
        factory = APIRequestFactory()
        data = {
            "username": "testUser1",
            "password": "testUser123",
            "email": "testUser1@email.com",
            "first_name": "testUser1",
            "last_name": "Usertest1",
            "github": "testUser1@github.com"
        }
        request = factory.post('/socialnet/authors/create/', data, format='json')
        view = AuthorCreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code,201)

class PostApiTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username = 'testUser1', password = 'testUser123')
        self.user.set_password('testUser345')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.author = Author.objects.create(user = self.user, github = 'testUser1.github')
        #print self.user.password


    def test_post(self):

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION = 'Basic '+ base64.b64encode('testUser1:testUser345'))
        response = self.client.post('/socialnet/posts/create/' ,{
                        "text": "worked asdas asdasd",
                        "public": "true"
        })
        self.assertEqual(response.status_code, 201)
        self.pid = response.data['id']
        print self.pid

        #test get posts
        response = self.client.get('/socialnet/posts/%s/' % self.pid, {}, format='json')
        self.assertEqual(response.status_code, 200)
        #delete posts
        response = self.client.delete('/socialnet/posts/%s/destroy/' % self.pid, {}, format='json')
        self.assertEqual(response.status_code, 204)

class CommentsApiTest(APITestCase):
    def setUp(self):
        #create an user
        self.user = User.objects.create_user(username = 'testUser1', password = 'testUser123')
        self.user.set_password('testUser345')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.author = Author.objects.create(user = self.user, github = 'testUser1.github')

        #create a post
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION = 'Basic '+ base64.b64encode('testUser1:testUser345'))
        response = self.client.post('/socialnet/posts/create/' ,{
                        "text": "worked asdas asdasd",
                        "public": "true"
        })
        self.pid = response.data['id']

    def test_create_comment(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION = 'Basic '+ base64.b64encode('testUser1:testUser345'))
        response = self.client.post('/socialnet/posts/%s/comments/create/' % self.pid, {
            "text": "i love dog"
        })
        self.cid = response.data['id']
        self.assertEqual(response.status_code, 201)
        print self.cid

        #test to get comments
        response = self.client.get('/socialnet/posts/%s/' % self.pid, {}, format = 'json')
        self.assertEqual(response.status_code, 200)
        comments = response.data['comments']
        self.assertTrue(comments[0]['text'] != None)

        #test delete the comment
        response = self.client.delete('/socialnet/comments/%s/destroy/' % self.cid)
        self.assertEqual(response.status_code, 204)
