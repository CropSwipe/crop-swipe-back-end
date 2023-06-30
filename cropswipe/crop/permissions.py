from rest_framework import permissions
from .models import PrivatePrice, PublicPrice

class IsProjectOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class IsPriceOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.project.author == request.user

class IsCommentOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "DELETE"]:
            return obj.author == request.user