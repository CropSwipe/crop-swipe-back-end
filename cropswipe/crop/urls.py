from django.urls import path
from .views import *

urlpatterns = [
    # project api
    path('/projects', ProjectListView.as_view()),
    path('/projects/<int:pk>', ProjectDetailView.as_view()),
    path('/projects/<int:pk>/likes', ProjectLikeProcessView.as_view()),
    # comment api
    path('/projects/<int:pk>/comments', CommentListView.as_view()),
    path('/projects/<int:ppk>/comments/<int:cpk>', CommentDetailView.as_view()),
    path('/projects/<int:ppk>/comments/<int:cpk>/likes', CommentLikeProcessView.as_view()),
    # myproject api
    path('/myprojects', MyProjectListView.as_view()),
    path('/myprojects/<int:pk>', MyProjectDetailView.as_view()),
    path('/myprojects/<int:pk>/private/prices', MyProjectPrivatePriceListView.as_view()),
    path('/myprojects/<int:project_pk>/private/prices/<int:price_pk>', MyProjectPrivatePriceDetailView.as_view()),
    path('/myprojects/<int:pk>/public/prices', MyProjectPublicPriceListView.as_view()),
    path('/myprojects/<int:project_pk>/public/prices/<int:price_pk>', MyProjectPublicPriceDetailView.as_view()),
]