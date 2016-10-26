from rest_framework import serializers
from .models import Post

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