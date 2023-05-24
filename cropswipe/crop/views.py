# django
from django.shortcuts import get_object_or_404
# Restfraemwork
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# in app
from .models import Project, Comment
from user.models import User
from .serializers import ProjectSerializer, CommentSerializer

# Create your views here.
class ProjectListView(APIView):
    # GET
    def get(self, request):
        projects = Project.objects.filter(is_active=True)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # POST
    def post(self, request):
        data = request.data
        serializer = ProjectSerializer(data=data)
        request.user = User.objects(pk=1)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetailView(APIView):
    # Get Project object func
    def get_project(self, pk):
        project = get_object_or_404(Project, pk=pk) # 객체가 없으면 404 Return
        return project
    # GET
    def get(self, request, pk):
        project = self.get_project(pk)
        # is_acitve == False Project rejection
        if(project.is_active == False):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # PATCH
    def patch(self, request, pk):
        data = request.data
        project = self.get_project(pk)
        serializer = ProjectSerializer(data=data, instance=project, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE
    def delete(self, request, pk):
        project = self.get_project(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentListView(APIView):
    # GET
    def get(self, request, pk):
        try:
            comments = Comment.objects.filter(project__id = pk)
            serializer = CommentSerializer(comments, many=True)
            response_data = {
                'comments_count': len(comments), # add comment count data
                'comments': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    # POST
    def post(self, request, pk):
        try:
            data = request.data
            serializer = CommentSerializer(data=data, partial=True)
            project = Project.objects.get(pk=pk)
            if serializer.is_valid():
                serializer.save(author=request.user, comment_obj = project)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CommentDetailView(APIView):
    # PATCH
    def patch(self, request, ppk, cpk):
        try:
            data = request.data
            comment = Comment.objects.get(pk=cpk)
            serializer = CommentSerializer(data=data, instance=comment, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    # DELETE
    def delete(self, request, ppk, cpk):
        try:
            comment = Comment.objects.get(pk=cpk)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)