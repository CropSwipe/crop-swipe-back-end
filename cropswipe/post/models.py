from django.db import models
from user.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    post_pic1 = models.ImageField(upload_to="", blank=True, null=True)
    post_pic2 = models.ImageField(upload_to="", blank=True, null=True)
    post_pic3 = models.ImageField(upload_to="", blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = GenericRelation('Like', related_query_name='post')

    def __str__(self):
        return self.title[:20]

class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = GenericRelation('Like', related_query_name='comment')
    def __str__(self):
        return self.content[:20]

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_app_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='+')
    object_id = models.PositiveIntegerField()
    like_obj = GenericForeignKey('content_type', 'object_id')