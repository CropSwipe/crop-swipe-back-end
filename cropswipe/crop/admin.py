from django.contrib import admin
# in app
from .models import Project, Comment, Funding

# Register your models here.
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Funding)