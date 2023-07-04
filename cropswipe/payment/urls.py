from django.urls import path
from .views import *

urlpatterns = [
    path('kakaopay/ready', KakaopayReadyView.as_view()),
    path('kakaopay/approve', KakaoApproveView.as_view()),
]