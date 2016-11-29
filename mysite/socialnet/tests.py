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

class HostTest(APITestCase):
    def test_host(self):
        factory = APIRequestFactory()
        request = factory.get('/posts/', {}, format = 'json')
        self.assertEqual(request.get_host(), 'testserver')

class AuthorApiTest(APITestCase):

    def test_create_user(self):
        factory = APIRequestFactory()
        data = {
            "displayName": "fijiwater",
            "username": "testUser1",
            "password": "testUser123",
            "email": "testUser1@email.com",
            "first_name": "testUser1",
            "last_name": "Usertest1",
            "github": "testUser1@github.com"
        }
        request = factory.post('/author/create', data, format='json')
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
        self.uid = self.author.id


    def test_post(self):

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION = 'Basic '+ base64.b64encode('testUser1:testUser345'))
        response = self.client.post('/posts/create' ,{
                        "title": "first post",
                        "description": "this is my first post",
                        "content_type": "text/markdown",
                        "content": "this is my first post for test"
        })
        self.assertEqual(response.status_code, 201)


        #test get posts
        response = self.client.get('/posts', {}, format='json')
        self.assertEqual(response.status_code, 200)
        request_msg = response.data['posts']
        self.post_id = request_msg[0]['id']
        # print self.post_id

        #test get a single post with post_id
        response = self.client.get('/posts/%s' % self.post_id, {}, format ='json')
        self.assertEqual(response.status_code, 200)

        #test all the posts of a single user that are public
        response = self.client.get('/author/%s/posts' % self.uid, {}, format = 'json')
        self.assertEqual(response.status_code, 200)

        #test update a post
        response = self.client.put('/posts/%s/update' % self.post_id, {
            "title": "update post",
            "description": "this is an updated msg",
            "content_type": "text/markdown",
            "content": "this is the msg for update posts"
        })
        self.assertEqual(response.status_code, 200)

        #delete posts
        response = self.client.delete('/posts/%s/destroy' % self.post_id, {}, format='json')
        self.assertEqual(response.status_code, 204)

class CommentsAndFriendsApiTest(APITestCase):
    def setUp(self):
        #create an user
        self.user = User.objects.create_user(username = 'testUser1', password = 'testUser123')
        self.user.set_password('testUser345')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.author = Author.objects.create(user = self.user, github = 'testUser1.github')

        self.uid1 = self.author.id

        self.user2 = User.objects.create_user(username = 'testUser2', password = 'testUser999')
        self.user2.set_password('testUser000')
        self.user2.is_superuser = True
        self.user2.is_staff = True
        self.user2.save()
        self.author2 = Author.objects.create(user = self.user2, github = 'testUser2.github')


        self.uid2 = self.author2.id

        #create a post
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION = 'Basic '+ base64.b64encode('testUser1:testUser345'))
        response = self.client.post('/posts/create' ,{
                        "title": "first post",
                        "description": "this is my first post",
                        "content_type": "text/markdown",
                        "content": "this is my first post for test"
        })
        response = self.client.get('/posts', {}, format='json')
        request_msg = response.data['posts']
        self.post_id = request_msg[0]['id']
        # print self.post_id

    def test_create_comment(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION = 'Basic '+ base64.b64encode('testUser1:testUser345'))
        response = self.client.post('/posts/%s/comments/create' % self.post_id, {
            "comment": "here is my first comment",
            "content_type": "text/markdown"
        })
        self.assertEqual(response.status_code, 201)

        #get the id of comment
        self.comment_id = response.data['id']

        # test to get comments
        response = self.client.get('/posts/%s' % self.post_id, {}, format = 'json')
        self.assertEqual(response.status_code, 200)
        comments = response.data['comments']
        self.assertTrue(comments[0]['id'] != None)

        #test to get a comment
        response = self.client.get('/comments/%s' % self.comment_id, {}, format = 'json')
        self.assertEqual(response.status_code, 200)

        #test delete the comment
        response = self.client.delete('/comments/%s/destroy' % self.comment_id)
        self.assertEqual(response.status_code, 204)

    def test_send_friend_request(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION = 'Basic '+ base64.b64encode('testUser1:testUser345'))
        #test to send a friend request
        response = self.client.post('/author/friend_request/%s' % self.uid2, {}, format = 'json')
        self.assertEqual(response.status_code, 202)
        # print self.uid2

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION = 'Basic '+ base64.b64encode('testUser2:testUser000'))
        #test get friend request list

        response = self.client.get('/author/friends/friend_requests', {}, format = 'json')
        self.assertEqual(response.status_code, 200)

        #test accept friend request
        response = self.client.post('/author/friend_request/accept/%s' % self.uid1, {}, format = 'json')
        self.assertEqual(response.status_code, 202)

        #test get friend list for user2, since user1 and user2 are friends now
        response = self.client.get('/author/%s/network' % self.uid2, {}, format = 'json')
        self.assertEqual(response.status_code, 200)

        #test unfriend a friend
        response = self.client.delete('/author/friends/unfriend/%s' % self.uid1, {}, format = 'json')
        self.assertEqual(response.status_code, 202)

        #test get the friend list for user 2 again,
        response = self.client.get('/author/%s/network' % self.uid2, {}, format = 'json')
        self.assertEqual(response.status_code, 200)
        request = response.data['authors']
        self.assertTrue(request == [])


    def test_reject_friend_requests(self):

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION = 'Basic '+ base64.b64encode('testUser1:testUser345'))
        #test to send a friend request
        response = self.client.post('/author/friend_request/%s' % self.uid2, {}, format = 'json')
        self.assertEqual(response.status_code, 202)

        #test reject friend request
        response = self.client.delete('/author/friend_request/reject/%s' % self.uid1, {}, format = 'json')
        self.assertEqual(response.status_code, 202)
