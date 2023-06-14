from django.urls import path
from .views import *

urlpatterns = [
    path('login/kakao/', kakao_login),
    path('login/kakao/callback/', kakao_callback),
    path('login/kakao/auth/', KakaoLogin.as_view()),
]