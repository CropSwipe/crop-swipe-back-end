from django.shortcuts import render, get_object_or_404
# Create your views here.
# in restframework
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
# in post app
from .models import Post, Comment
from user.models import User
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerPermission

class PostListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        data = request.data
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    permission_classes = [IsOwnerPermission]
    # get post object
    def get_object(self, pk):
        post = get_object_or_404(Post, pk=pk)
        return post
    # GET
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # PATCH
    def patch(self, request, pk):
        data = request.data
        post = self.get_object(pk)
        serializer = PostSerializer(data=data, instance=post, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # GET
    def get(self, request, pk):
        comments = Comment.objects.filter(post__id = pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # POST
    def post(self, request, pk):
        try:
            data = request.data
            serializer = CommentSerializer(data=data)
            post = Post.objects.get(pk=pk)
            if serializer.is_valid():
                serializer.save(author=request.user, comment_obj=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return Response({"error_message": f"Comment-{pk} doesn't exist."},status=status.HTTP_404_NOT_FOUND)

class CommentDetailView(APIView):
    permission_classes = [IsOwnerPermission]
    # get object func
    def get_object(self, pk):
        comment = get_object_or_404(Comment, pk=pk)
        return comment
    # patch
    def patch(self, request, ppk, cpk):
        data = request.data
        comment = self.get_object(cpk)
        serializer = CommentSerializer(data=data, instance=comment)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    # DELETE
    def delete(self, request, ppk, cpk):
        comment = self.get_object(cpk)
        comment.delete()
        return Response({"message":"Success Comment Delete"}, status=status.HTTP_204_NO_CONTENT)