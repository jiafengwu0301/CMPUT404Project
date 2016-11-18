from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Post, Author, Comment
from django.contrib.auth.models import User


class AuthorFriendSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Author
        fields = [
            'id',
            'first_name',
            'last_name',
            'avatar',
            'host',
            'github',
        ]


class AuthorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    following = AuthorFriendSerializer(many=True)
    followers = AuthorFriendSerializer(many=True)

    class Meta:
        model = Author
        fields = [
            'id',
            'first_name',
            'last_name',
            'github',
            'avatar',
            'following',
            'followers',
            'email',
        ]


class AuthorNetworkSerializer(serializers.ModelSerializer):
    following = AuthorFriendSerializer(many=True)
    followers = AuthorFriendSerializer(many=True)

    class Meta:
        model = Author
        fields = [
            'following',
            'followers',
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
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'github',
            'avatar',
            'date_created',
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])
        user.save()
        author = Author.objects.create(user=user, **validated_data)
        return author


class UpdateAuthorSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', allow_blank=True, allow_null=True)
    first_name = serializers.CharField(source='user.first_name', allow_blank=True, allow_null=True )
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


class CommentAuthorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Author
        fields = [
            'first_name',
            'last_name',
            'avatar',
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = CommentAuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'author',
            'text',
        ]


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
        ]


class PostSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='author.user.first_name')
    last_name = serializers.CharField(source='author.user.last_name')
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'published_date',
            'author',
            'text',
            'public',
            'first_name',
            'last_name',
            'comments',
            'image'
        ]


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'published_date',
            'text',
            'public',
            'image'
        ]


class FriendsAuthorSerializer(serializers.ModelSerializer):
    friends = AuthorFriendSerializer(many=True)

    class Meta:
        model = Author
        fields = [
            'friends',
        ]


class FriendRequestsAuthorSerializer(serializers.ModelSerializer):
    friend_requests = AuthorFriendSerializer(many=True)

    class Meta:
        model = Author
        fields = [
            'friend_requests',
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])
        user.save()
        author = Author.objects.create(user=user, **validated_data)
        return author


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
        except:
            raise ValidationError("Incorrect login/password.")
        if user.check_password(password):
            attrs['author'] = user.author
            return attrs
        raise ValidationError("Incorrect login/password.")
