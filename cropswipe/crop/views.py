# django
from django.shortcuts import get_object_or_404
# Restfraemwork
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
# in app
from .models import Project, Comment, Like, PrivatePrice, PublicPrice
from .serializers import ProjectListlSerializer, ProjectDetailSerializer, MyProjectlSerializer, CommentSerializer, PrivatePriceSerializer, PublicPriceSerializer
from .permissions import IsProjectOwnerPermission, IsPriceOwnerPermission, IsCommentOwnerPermission
from user.serializers import UserSerializer

# Create your views here.
class ProjectListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # GET
    def get(self, request):
        projects = Project.objects.filter(is_active=True)
        user = request.user
        serializer = ProjectListlSerializer(projects, many=True, context={'user': user})
        return Response(serializer.data, status=status.HTTP_200_OK)
    # POST
    def post(self, request):
        data = request.data
        user = request.user
        serializer = ProjectListlSerializer(data=data, context={'user': user})
        if serializer.is_valid():
            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetailView(APIView):
    permission_classes = [AllowAny]
    # Get Project object func
    def get_project(self, pk):
        project = get_object_or_404(Project, pk=pk) # 객체가 없으면 404 Return
        self.check_object_permissions(self.request, project)
        return project
    # GET
    def get(self, request, pk):
        project = self.get_project(pk)
        user = request.user
        # is_acitve == False Project rejection
        if(project.is_active == False):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectDetailSerializer(project, context={'user': user})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectLikeProcessView(APIView):
    # get object function
    def get_object(self, pk):
        project = get_object_or_404(Project, pk=pk)
        return project
    # POST
    def post(self, request, pk):
        try:
            project = self.get_object(pk)
            user = request.user
            like = Like.objects.get(user=user, project=project)
            return Response({"error_message": "Like already exists."}, status=status.HTTP_400_BAD_REQUEST)
        except Like.DoesNotExist:
            Like.objects.create(user=user, like_obj=project)
            return Response({"message": f"Success Post({pk}):User({user}):Like Post"}, status=status.HTTP_201_CREATED)
    def delete(self, request, pk):
        try:
            project = self.get_object(pk)
            user = request.user
            like = Like.objects.get(user=user, project=project)
            like.delete()
            return Response({"message": f"Success Post({pk}):User({user}):Like Delete"}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"error_message": "Like doesn't exist."},status=status.HTTP_404_NOT_FOUND)

# myproject view
class MyProjectListView(APIView):
    # GET
    def get(self, request):
        user = request.user
        projects = Project.objects.filter(author=user)
        serializer = MyProjectlSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MyProjectDetailView(APIView):
    permission_classes = [IsProjectOwnerPermission]
    # get project obj
    def get_object(self, pk):
        project = get_object_or_404(Project, pk=pk)
        self.check_object_permissions(self.request, project)
        return project
    # GET
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = MyProjectlSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # PATCH
    def patch(self, request, pk):
        project = self.get_object(pk)
        data = request.data
        serializer = MyProjectlSerializer(data=data, instance=project, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE
    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response({"message": "Success deletion of project."}, status=status.HTTP_204_NO_CONTENT)
    
# project private price view
class MyProjectPrivatePriceListView(APIView):
    permission_classes = [IsProjectOwnerPermission]
    # get project function
    def get_object(self, pk):
        project = get_object_or_404(Project, pk=pk)
        self.check_object_permissions(self.request, project)
        return project
    # GET
    def get(self, request, pk):
        project = self.get_object(pk)
        prices = PrivatePrice.objects.filter(project=project)
        serializer = PrivatePriceSerializer(prices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # POST
    def post(self, request, pk):
        data = request.data
        project = self.get_object(pk)
        serializer = PrivatePriceSerializer(data=data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyProjectPrivatePriceDetailView(APIView):
    permission_classes = [IsPriceOwnerPermission]
    # get object function
    def get_object(self, price_pk):
        price = get_object_or_404(PrivatePrice, pk=price_pk)
        self.check_object_permissions(self.request, price)
        return price
    # patch
    def patch(self, request, project_pk, price_pk):
        data = request.data
        price = self.get_object(price_pk)
        serializer = PrivatePriceSerializer(data=data, instance=price, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # delete
    def delete(self, request, project_pk, price_pk):
        price = self.get_object(price_pk)
        price.delete()
        return Response({"message": "Success deletion of privateprice"}, status=status.HTTP_204_NO_CONTENT)
        
# project public price view
class MyProjectPublicPriceListView(APIView):
    permission_classes = [IsProjectOwnerPermission]
    # get project function
    def get_object(self, pk):
        project = get_object_or_404(Project, pk=pk)
        self.check_object_permissions(self.request, project)
        return project
    # GET
    def get(self, request, pk):
        project = self.get_object(pk)
        prices = PublicPrice.objects.filter(project=project)
        serializer = PublicPriceSerializer(prices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # POST
    def post(self, request, pk):
        data = request.data
        project = self.get_object(pk)
        serializer = PublicPriceSerializer(data=data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyProjectPublicPriceDetailView(APIView):
    permission_classes = [IsPriceOwnerPermission]
    # get project function
    def get_object(self, price_pk):
        price = get_object_or_404(PublicPrice, pk=price_pk)
        self.check_object_permissions(self.request, price_pk)
        return price
    # patch
    def patch(self, request, project_pk, price_pk):
        data = request.data
        price = self.get_object(price_pk)
        serializer = PublicPriceSerializer(data=data, instance=price, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # delete
    def delete(self, request, project_pk, price_pk):
        price = self.get_object(price_pk)
        price.delete()
        return Response({"message": "Success deletion of publicprice"}, status=status.HTTP_204_NO_CONTENT)

# comment view
class CommentListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # get object function
    def get_object(self, pk):
        project = get_object_or_404(Project, pk=pk)
        return project
    # GET
    def get(self, request, pk):
        project = self.get_object(pk)
        user = request.user
        comments = Comment.objects.filter(project=project)
        serializer = CommentSerializer(comments, many=True, context={'user': user})
        response_data = {
            'comments_count': len(comments), # add comments length
            'comments': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    # POST
    def post(self, request, pk):
        user = request.user
        data = request.data
        project = self.get_object(pk)
        serializer = CommentSerializer(data=data, context={'user': user})
        if serializer.is_valid():
            serializer.save(author=user, project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    permission_classes = [IsCommentOwnerPermission]
    # PATCH
    def get_object(self, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(self.request, comment)
        return comment
    # patch
    def patch(self, request, ppk, cpk):
        data = request.data
        comment = self.get_object(cpk)
        serializer = CommentSerializer(data=data, instance=comment, partial=True, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE
    def delete(self, request, ppk, cpk):
        comment = self.get_object(cpk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CommentLikeProcessView(APIView):
    # get objects function
    def get_object(self, cpk):
        comment = get_object_or_404(Comment, pk=cpk)
        return comment
    # POST
    def post(self, request, ppk, cpk):
        try:
            comment = self.get_object(cpk)
            user = request.user
            like = Like.objects.get(user=user, comment=comment)
            return Response({"error_message": "Like already exists."}, status=status.HTTP_400_BAD_REQUEST)
        except Like.DoesNotExist:
            Like.objects.create(user=user, like_obj=comment)
            return Response({"message": f"Success Project({ppk}):Comment({cpk}):User({user}):Like Post"}, status=status.HTTP_201_CREATED)
    # DELETE
    def delete(self, request, ppk, cpk):
        try:
            comment = self.get_object(cpk)
            user = request.user
            like = Like.objects.get(user=user, comment=comment)
            like.delete()
            return Response({"message": f"Success Project({ppk}):Comment({cpk}):User({user}):Like Delete"}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"error_message": "Like doesn't exist."},status=status.HTTP_404_NOT_FOUND)

# order view
class PrivateOrderView(APIView):
    # get object
    def get_object(self, pk):
        private_price = get_object_or_404(PrivatePrice, pk=pk)
        return private_price
    # GET
    def get(self, request):
        try:
            price_id = request.GET['id']
            quantity = int(request.GET['quantity'])
            supporter = request.user
            private_price = self.get_object(price_id)
            serializer = UserSerializer(supporter)
            response_data = {
                'project_title': private_price.project.title,
                'item_content': private_price.content,
                'item_price': (private_price.price * quantity),
                'supporter': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error_message': f'{e}'},status=status.HTTP_400_BAD_REQUEST)