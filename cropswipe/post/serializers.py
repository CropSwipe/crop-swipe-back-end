# in restframework
from rest_framework import serializers
# in django app
from .models import Post, Comment
from user.serializers import UserSerializer

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at']