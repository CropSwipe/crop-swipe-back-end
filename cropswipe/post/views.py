from django.shortcuts import render, get_object_or_404
# Create your views here.
# in restframework
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
# in post app
from .models import Post, Comment, Like
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
        self.check_object_permissions(self.request, post)
        return post
    # GET
    def get(self, request, pk):
        post = self.get_object(pk)
        like_cnt = len(Like.objects.filter(post=post))
        is_like = None
        user = request.user
        # 해당 사용자 게시물 좋아요 여부 판단
        if user.is_authenticated:
            like = Like.objects.filter(post=post, user=request.user)
            if like: is_like = True
            else: is_like = False
        # 시리얼라이징
        serializer = PostSerializer(post)
        # 반환 데이터 생성
        response_data = {
            'post': serializer.data,
            'is_like': is_like,
            'like_cnt': like_cnt
        }
        return Response(response_data, status=status.HTTP_200_OK)
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

class PostLikeProcessView(APIView):
    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            user = request.user
            like = Like.objects.filter(user=user, post=post)
            if like: 
                return Response({"error_message": "Like already exists."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                Like.objects.create(user=user, like_obj=post)
                return Response({"message": f"Success Post({pk}):User({user}):Like Post"}, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return Response({"error_message": f"Post-{pk} doesn't exist."},status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            user = request.user
            like = Like.objects.get(user=user, post=post)
            like.delete()
            return Response({"message": f"Success Post({pk}):User({user}):Like Delete"}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"error_message": f"Post-{pk} doesn't exist."},status=status.HTTP_404_NOT_FOUND)
        except Like.DoesNotExist:
            return Response({"error_message": "Like doesn't exist."},status=status.HTTP_404_NOT_FOUND)

class CommentListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # GET
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            comments = Comment.objects.filter(post = post)
            serializer = CommentSerializer(comments, many=True, context={'user': request.user})
            response_data = {
                'comments_count': len(comments), # add comment count data
                'comments': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"error_message": f"Post-{pk} doesn't exist."},status=status.HTTP_404_NOT_FOUND)
    # POST
    def post(self, request, pk):
        try:
            user = request.user
            data = request.data
            serializer = CommentSerializer(data=data, context={'user': request.user})
            post = Post.objects.get(pk=pk)
            if serializer.is_valid():
                serializer.save(author=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"error_message": f"Post-{pk} doesn't exist."},status=status.HTTP_404_NOT_FOUND)

class CommentDetailView(APIView):
    permission_classes = [IsOwnerPermission]
    # get object func
    def get_object(self, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(self.request, comment)
        return comment
    # patch
    def patch(self, request, ppk, cpk):
        data = request.data
        comment = self.get_object(cpk)
        serializer = CommentSerializer(data=data, instance=comment)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE
    def delete(self, request, ppk, cpk):
        comment = self.get_object(cpk)
        comment.delete()
        return Response({"message":"Success Comment Delete"}, status=status.HTTP_204_NO_CONTENT)

class CommentLikeProcessView(APIView):
    def post(self, request, ppk, cpk):
        try:
            post = Post.objects.get(pk=ppk)
            comment = Comment.objects.get(pk=cpk)
            user = request.user
            like = Like.objects.filter(user=user, comment=comment)
            # 이미 좋아요 눌렀을 경우
            if like: 
                return Response({"error_message": "Like already exists."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                Like.objects.create(user=user, like_obj=comment)
                return Response({"message": f"Success Post({ppk}):Comment({cpk}):User({user}):Like Post"}, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return Response({"error_message": f"Post-{ppk} doesn't exist."},status=status.HTTP_404_NOT_FOUND)
        except Comment.DoesNotExist:
            return Response({"error_message": f"Comment-{cpk} doesn't exist."},status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, ppk, cpk):
        try:
            post = Post.objects.get(pk=ppk)
            comment = Comment.objects.get(pk=cpk)
            user = request.user
            like = Like.objects.get(user=user, comment=comment)
            like.delete()
            return Response({"message": f"Success Post({ppk}):Comment({cpk}):User({user}):Like Delete"}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"error_message": f"Post-{ppk} doesn't exist."},status=status.HTTP_404_NOT_FOUND)
        except Comment.DoesNotExist:
            return Response({"error_message": f"Comment-{cpk} doesn't exist."},status=status.HTTP_404_NOT_FOUND)
        except Like.DoesNotExist:
            return Response({"error_message": "Like doesn't exist."},status=status.HTTP_404_NOT_FOUND)