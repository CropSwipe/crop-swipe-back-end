# in restframework
from rest_framework import serializers
from rest_framework.serializers import ValidationError
# in django app
from .models import Post, Comment, Like
from user.serializers import UserSerializer
from .utils import bad_words
# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
    def validate_title(self, value):
        for word in bad_words:
            if word in value:
                raise ValidationError('제목에 욕설이 포함되어 있습니다.')
        return value
    def validate_content(self, value):
        for word in bad_words:
            if word in value:
                raise ValidationError('내용에 욕설이 포함되어 있습니다.')
        return value
# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_cnt = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'likes_cnt', 'is_like']
    # SerializerMethodField function
    def get_likes_cnt(self, obj):
        value = len(obj.likes.all())
        return value
    
    def get_is_like(self, obj):
        user = self.context['user']
        if user.is_authenticated:
            is_like = obj.likes.filter(user=user)
            if is_like: return True
            else: return False
        return None
    # validate function
    def validate_content(self, value):
        for word in bad_words:
            if word in value:
                raise ValidationError('내용에 욕설이 포함되어 있습니다.')
        return value