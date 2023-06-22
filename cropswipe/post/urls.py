from django.urls import path
from .views import *

urlpatterns = [
    path('posts', PostListView.as_view()),
    path('posts/<int:pk>', PostDetailView.as_view()),
    path('posts/<int:pk>/comments', CommentListView.as_view()),
    path('posts/<int:ppk>/comments/<int:cpk>', CommentDetailView.as_view()),
]