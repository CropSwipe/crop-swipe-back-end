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
    comments = GenericRelation('Comment', related_query_name='post')

    def __str__(self):
        return self.title[:20]

class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='+')
    object_id = models.PositiveIntegerField()
    comment_obj = GenericForeignKey('content_type', 'object_id')
    # product 추후에 도입 필요
    def __str__(self):
        return self.content[:20]