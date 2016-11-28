from rest_framework import pagination
from rest_framework import response
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Post, Author, Comment, FriendRequest, REMOTEHOST, Node
from django.contrib.auth.models import User


class FriendSerializer(serializers.ModelSerializer):
	#first_name = serializers.CharField(source='user.first_name')
	#last_name = serializers.CharField(source='user.last_name')

	class Meta:
		model = Author
		fields = [
			'id',
			'displayName',
			'avatar',
			'host',
			'github',
			'avatar',
		]


class RemoteAuthorSerializer(serializers.ModelSerializer):
	id = serializers.CharField()

	class Meta:
		model = Author
		fields = [
			'displayName',
			'id',
			'host',
			'url',
			'github',
			'avatar',
		]


class AuthorFriendSerializer(serializers.ModelSerializer):
	#first_name = serializers.CharField(source='user.first_name')
	#last_name = serializers.CharField(source='user.last_name')
	#local = serializers.BooleanField(source='is_local')

	class Meta:
		model = Author
		fields = [
			'displayName',
			'id',
			'host',
			'url',
			'github',
			'is_local',
			'avatar',
		]


class AuthorFriendToFriendsUrlSerializer(serializers.ModelSerializer):
	id = serializers.CharField()

	class Meta:
		model = Author
		fields = [
			'id'
		]


class AuthorSerializer(serializers.ModelSerializer):
	email = serializers.CharField(source='user.email')
	authors = RemoteAuthorSerializer(many=True)
	local = serializers.BooleanField(source="is_local")

	class Meta:
		model = Author
		fields = [
			'id',
			'displayName',
			'url',
			'host',
			'authors',
			'github',
			'email',
			'local',
			'avatar',
		]


class AuthorRetrieveSerializer(serializers.ModelSerializer):
	email = serializers.CharField(source='user.email')
	authors = RemoteAuthorSerializer(many=True)

	class Meta:
		model = Author
		fields = [
			'id',
			'displayName',
			'url',
			'host',
			'authors',
			'github',
			'email',
		]


class AuthorNetworkSerializer(serializers.ModelSerializer):
	authors = AuthorFriendSerializer(many=True)

	class Meta:
		model = Author
		fields = [
			'authors'
		]


class FriendsField(serializers.Field):

	def to_internal_value(self, data):
		pass

	def to_native(self, value):
		return value.id

	def to_representation(self, value):
		return value.id

	#def get_choices(self, include_blank=True, blank_choice=BLANK_CHOICE_DASH, limit_choices_to=None):
	#	pass


class AuthorFriendListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Author
		fields = [
			'authors'
		]


class AuthorFriendSpecialListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Author
		fields = [
			'authors',
			'id'
		]


class AuthorFriendRequestSerializer(serializers.ModelSerializer):
	id = serializers.CharField()

	class Meta:
		model = Author
		fields = [
			'id',
			'host',
			'displayName'
		]


class FriendFriendRequestSerializer(serializers.ModelSerializer):
	id = serializers.CharField()

	class Meta:
		model = Author
		fields = [
			'id',
			'host',
			'displayName',
			'url'
		]


class RemoteRequestSerializer(serializers.ModelSerializer):
	author = AuthorFriendRequestSerializer(source='sender')
	friend = FriendFriendRequestSerializer(source='receiver')

	class Meta:
		model = FriendRequest
		fields = [
			'author',
			'friend'
		]


class FullAuthorSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.username')
	email = serializers.CharField(source='user.email')
	first_name = serializers.CharField(source='user.first_name')
	last_name = serializers.CharField(source='user.last_name')
	password = serializers.CharField(source='user.password', style={'input_type': 'password'})

	class Meta:
		model = Author
		fields = [
			'id',
			'displayName',
			'username',
			'password',
			'email',
			'first_name',
			'last_name',
			'github',
			'avatar',
			'date_created',
			'avatar',
			'host',
		]

	def create(self, validated_data):
		user_data = validated_data.pop('user')
		user = User.objects.create(**user_data)
		user.set_password(user_data['password'])
		user.save()
		author = Author.objects.create(user=user, **validated_data)
		author.url = REMOTEHOST + "/author/" + str(author.id)
		author.is_active = False
		author.save()
		return author


class UpdateAuthorSerializer(serializers.ModelSerializer):
	email = serializers.CharField(source='user.email', allow_blank=True, allow_null=True)
	first_name = serializers.CharField(source='user.first_name', allow_blank=True, allow_null=True)
	last_name = serializers.CharField(source='user.last_name', allow_blank=True, allow_null=True)
	password = serializers.CharField(source='user.password', style={'input_type': 'password'},
									 allow_blank=True, allow_null=True)
	uid = serializers.CharField(source='user.id', read_only=True, allow_blank=True)
	github = serializers.CharField(allow_blank=True, allow_null=True)

	class Meta:
		model = Author
		fields = [
			'uid',
			'password',
			'email',
			'first_name',
			'last_name',
			'github',
			'avatar',
		]

	def update(self, instance, validated_data):
		user_data = validated_data.pop('user', None)
		user = User.objects.get(id=instance.user.id)
		user.email = self.value_or_keep(user.email, user_data['email'])
		user.first_name = self.value_or_keep(user.first_name, user_data['first_name'])
		user.last_name = self.value_or_keep(user.last_name, user_data['last_name'])
		if user_data['password'] != "":
			user.set_password(user_data['password'])
		instance.github = self.value_or_keep(instance.github, validated_data.get('github', instance.github))
		instance.avatar = self.value_or_keep(instance.avatar, validated_data.get('avatar', instance.avatar))
		user.save()
		instance.save()
		return instance

	@staticmethod
	def value_or_keep(field, value):
		if value == "":
			return field
		return value


class CommentSerializer(serializers.ModelSerializer):
	author = RemoteAuthorSerializer()
	#query = serializers.CharField(allow_blank=True, allow_null=True)
	post = serializers.URLField(source='post.source', allow_blank=True)

	class Meta:
		model = Comment
		fields = [
			'author',
			'comment',
			'pubdate',
			'id',
			'contentType',
			'post',
		]




class CreateCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = [
			'id',
			'comment',
			'contentType'
		]


class PostSerializer(serializers.ModelSerializer):
	comments = CommentSerializer(many=True)
	author = RemoteAuthorSerializer()

	class Meta:
		model = Post
		fields = [
			'id',
			'published',
			'title',
			'description',
			'contentType',
			'content',
			'source',
			'origin',
			'author',
			'comments',
			'visibility',
			'image'
		]

class LocalPostSerializer(serializers.ModelSerializer):
	comments = CommentSerializer(many=True)
	author = AuthorSerializer()

	class Meta:
		model = Post
		fields = [
			'id',
			'published',
			'title',
			'description',
			'contentType',
			'content',
			'source',
			'origin',
			'author',
			'comments',
			'visibility',
			'image',

		]


class ListCommentsSerializer(serializers.ModelSerializer):
	comments = CommentSerializer(many=True)

	class Meta:
		model = Post
		fields = [
			'comments',
		]


class RemotePostAuthorSerializer(serializers.ModelSerializer):
	github = serializers.CharField(required=False, allow_null=True)
	host = serializers.CharField(required=False)
	id = serializers.CharField(required=False)
	displayName = serializers.CharField(required=False)
	url = serializers.CharField(required=False)
	class Meta:
		model = Author
		fields = [
			'id',
			'host',
			'displayName',
			'url',
			'github',
		]


class RemotePostCommentSerializer(serializers.ModelSerializer):
	pass


class RemotePostSerializer(serializers.ModelSerializer):
	count = serializers.IntegerField(required=False, allow_null=True)
	origin = serializers.CharField(required=False, allow_null=True)
	contentType = serializers.CharField(required=False, allow_null=True)
	description = serializers.CharField(allow_blank= True,required=False, allow_null=True)
	author = RemotePostAuthorSerializer(required=False, allow_null=True)
	title = serializers.CharField(required=False, allow_null=True)
	comments = RemotePostCommentSerializer(required=False, many=True, allow_null=True)
	next = serializers.CharField(required=False, allow_null=True)
	content = serializers.CharField(required=False, allow_null=True)
	source = serializers.CharField(required=False, allow_null=True)
	visibility = serializers.CharField(required=False, allow_null=True)
	published = serializers.CharField(required=False, allow_null=True)
	id = serializers.UUIDField(required=False, allow_null=True)
	categories = serializers.Field(required=False, allow_null=True)
	previous = serializers.CharField(required=False, allow_null=True)

	class Meta:
		model = Post
		fields = [
			'count',
			'origin',
			'contentType',
			'description',
			'author',
			'title',
			'comments',
			'next',
			'content',
			'source',
			'visibility',
			'published',
			'id',
			'categories',
			'previous'
		]


'''	{
	u'count': 0,
	u'origin': u'http://ssrapp.herokuapp.com/posts/9e57f33a-9dbf-4afe-bda1-3a065a2a69ad',
	u'contentType': u'text/plain',
	u'description': u'',
	u'author': {
				u'url': u'http://ssrapp.herokuapp.com/author/5d50bfad-58e7-4ea7-9c22-0bada2673530',
				u'host': u'http://ssrapp.herokuapp.com/',
				u'github': None,
				u'displayName': u'admin',
				u'id': u'5d50bfad-58e7-4ea7-9c22-0bada2673530'
			   },
	u'title': u'ssr post',
	u'comments': [],
	u'next': u'http://ssrapp.herokuapp.com/posts/9e57f33a-9dbf-4afe-bda1-3a065a2a69ad/comments/',
	u'content': u'ssrpost',
	u'source': u'http://ssrapp.herokuapp.com/posts/9e57f33a-9dbf-4afe-bda1-3a065a2a69ad',
	u'visibility': u'PUBLIC',
	u'published': u'2016-11-23T02:39:25.452646',
	u'id': u'9e57f33a-9dbf-4afe-bda1-3a065a2a69ad',
	u'categories': None,
	u'previous': None
	}
'''


class CreatePostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'id',
			'title',
			'description',
			'contentType',
			'content',
			'image',
			'visibility'
		]


class FriendsAuthorSerializer(serializers.ModelSerializer):
	authors = AuthorFriendSerializer(many=True)

	class Meta:
		model = Author
		fields = [
			'authors',
		]


class FriendRequestSerializer(serializers.ModelSerializer):
	sender = AuthorFriendSerializer()
	receiver = AuthorFriendSerializer()

	class Meta:
		model = FriendRequest
		depth = 1
		fields = [
			'sender',
			'receiver',
		]


class AuthenticateSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.username')
	password = serializers.CharField(source='user.password', style={'input_type': 'password'})
	author = AuthorSerializer(allow_null=True, read_only=True)

	class Meta:
		model = User
		depth = 1
		fields = [
			'username',
			'password',
			'author',
		]
		extra_kwargs = {"password": {"write_only": True}}

	def validate(self, attrs):
		validation_data = dict(attrs)['user']
		username = validation_data.get('username', None);
		password = validation_data.get('password', None);
		try:
			user = User.objects.get(username=username)
			author = Author.objects.get(user=user)
		except:
			raise ValidationError("Incorrect login/password.")
		if user.check_password(password):
			if author.is_active:
				attrs['author'] = user.author
				return attrs
			else:
				raise ValidationError("User not Active.")
		raise ValidationError("Incorrect login/password.")


class NodeSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.username')
	password = serializers.CharField(source='user.password', style={'input_type': 'password'}, write_only=True)
	rcred_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = Node
		fields = [
			'id',
			'username',
			'password',
			'rcred_username',
			'rcred_password',
			'node_url',
			'access_to_posts'
		]

	def create(self, validated_data):
		user = validated_data.pop('user')
		username = user['username']
		print username
		password = user['password']
		print password
		rcred_username = validated_data.pop('rcred_username')
		rcred_password = validated_data.pop('rcred_password')
		node_url = validated_data.pop('node_url')
		access_to_posts = validated_data.pop('access_to_posts')
		user = User.objects.create(username=username, email="notusing@email.com")
		user.username = username
		user.set_password(password)
		user.save()
		node = Node.objects.create(rcred_username=rcred_username, rcred_password=rcred_password,
		                           node_url=node_url, access_to_posts=access_to_posts, user=user)
		node.save()
		return node


