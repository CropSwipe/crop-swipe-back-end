from django.urls import path
from .views import *

urlpatterns = [
    path('posts', PostListView.as_view()),
    path('posts/<int:pk>', PostDetailView.as_view()),
]