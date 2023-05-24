from django.contrib import admin
# in app
from .models import Project, Comment

# Register your models here.
admin.site.register(Project)
admin.site.register(Comment)