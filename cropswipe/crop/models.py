# django package
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# in app package
from user.models import User

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    project_pic1 = models.ImageField(upload_to="")
    project_pic2 = models.ImageField(upload_to="", blank=True, null=True)
    project_pic3 = models.ImageField(upload_to="", blank=True, null=True)
    description = models.TextField()
    goal_amount = models.PositiveIntegerField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = GenericRelation('Comment', related_query_name='project')

    def __str__(self):
        return self.title[:20]

class Funding(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    supporter = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    comment_obj = GenericForeignKey('content_type', 'object_id')
    # product 추후에 도입 필요
    def __str__(self):
        return self.content[:20]
    
class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    like_obj = GenericForeignKey('content_type', 'object_id')

class Review(models.Model):
    RATING_CHOICES = (
        (0, '☆☆☆☆☆'),
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    )
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    