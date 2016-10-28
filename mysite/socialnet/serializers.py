from rest_framework import serializers
from .models import Post, Author

class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'id',
			'published_date',
			'author',
			'text',
			'public', 
		]

class AuthorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Author
		fields = [
			'id',
			'user',
			'github',
			'avatar',
			'date_created',
			'friends',
			'friend_requests',
		]

			
