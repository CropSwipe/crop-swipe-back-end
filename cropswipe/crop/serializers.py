# Restframework
from rest_framework import serializers
# in app
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {
            'author': {'read_only': True}
        }