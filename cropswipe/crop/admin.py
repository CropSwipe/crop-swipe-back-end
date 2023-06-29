from django.contrib import admin
# in app
from .models import Project, Comment, Funding, Like, PrivatePrice, PublicPrice

# Register your models here.
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Funding)
admin.site.register(Like)
admin.site.register(PrivatePrice)
admin.site.register(PublicPrice)