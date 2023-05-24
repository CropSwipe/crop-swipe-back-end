# django
from django.shortcuts import get_object_or_404
# Restfraemwork
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# in app
from .models import Project
from .serializers import ProjectSerializer

# Create your views here.
class ProjectListView(APIView):
    # GET
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # POST
    def post(self, request):
        data = request.data
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
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