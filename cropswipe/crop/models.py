# django package
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# in app package
from user.models import User

# Create your models here.
class Project(models.Model):
    CATEGORY_CHOICES = (
        ('채소류', '채소류'),
        ('과일류', '과일류'),
        ('버섯류', '버섯류'),
        ('축산물', '축산물'),
        ('쌀/잡곡/견과류', '쌀/잡곡/견과류'),
        ('수산물/건해산물', '수산물/건해산물')
    )

    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    title = models.CharField(max_length=100)
    project_pic1 = models.ImageField(upload_to="")
    project_pic2 = models.ImageField(upload_to="", blank=True, null=True)
    project_pic3 = models.ImageField(upload_to="", blank=True, null=True)
    description = models.TextField()
    goal_amount = models.PositiveIntegerField(verbose_name='목표금액')
    cur_amount = models.PositiveIntegerField(verbose_name='모인금액', default=0)
    cnt_supporter = models.PositiveIntegerField(verbose_name='후원자 수', default=0)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    likes = GenericRelation('Like', related_query_name='project')

    def __str__(self):
        return self.title[:20]

class PrivatePrice(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='private_prices')
    price = models.PositiveIntegerField()
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
class PublicPrice(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='public_prices')
    price = models.PositiveIntegerField()
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crop_comments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    likes = GenericRelation('Like', related_query_name='comment')
    def __str__(self):
        return self.content[:20]
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crop_app_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='+')
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
    