from django.urls import path
from .views import *

urlpatterns = [
    path('/projects', ProjectListView.as_view()),
    path('/projects/<int:pk>', ProjectDetailView.as_view()),
    path('/projects/<int:pk>/comments', CommentListView.as_view()),
    path('/projects/<int:ppk>/comments/<int:cpk>', CommentDetailView.as_view()),
    path('/projects/<int:pk>/fundings', FundingListView.as_view()),
    path('/projects/<int:pk>/purchases', PurchaseListView.as_view()),
    #path('/projects/<int:pk>/funding')
]