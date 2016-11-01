from django.test import TestCase
#create your test here
from __future__ import unicode_literals
from django.contrib.auth.models import User

from socialnet.models import *

class PostsTests(TestCase):

    def _plaintext_safe(self, model_to_test):


        """ Test if plaintext is safe: converts < > to &lt; &gt; etc.
        Additionally ignores \n it does not convert that to <br/>
        because the templates which use "linebreaksbr" already take care of that.
        """
        test_content = '#testing<b>\nno'
        test_expect = '#testing&lt;b&gt;<br/>no'
        model = model_to_test
        model.content = test_content
        model.markdown = False
        #idk, but here shouldnt be models.__str__ cannot found the retreive for
        #display post parts
        self.assertEqual(models.__str__(), test_expect)

    def is_markdown(self, model_to_test):
        test_content = '# testing\n<b>\n>test-block'
        test_expect = '<h1>testing</h1><br/><p>&lt;b&gt;</p><br/><blockquote><br/><p>test-block</p><br/></blockquote><br/>'
        model = model_to_test
        model.content = test_content
        model.markdown = True
        self.assertEqual(models.__str__(), test_expect)
        self.assertEqual(models.content,test_content)

    def test_posts(self):
        model = Post()
        self._plaintext_safe(model)
        self.is_markdown(model)

    def test_comments(self):
        model = Comment()
        self._plaintext_safe(model)
        self.is_markdown(model)

class AuthorsTest(TestCase):
    def setUp(self):
        # create user profile, the format is: username, email, password
        self.user1 = User.objects.create_user('user1', 'user1@email.com', 'user1')
        self.user2 = User.objects.create_user('user2', 'user2@email.com', 'user2')
        self.author1 = Author(user = self.user1)
        self.author1.save()
        self.author2 = Author(user = self.user2)
        self.author2.save()

    def test_create(self):
        #should create users
