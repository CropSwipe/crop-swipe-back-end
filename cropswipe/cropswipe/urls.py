"""cropswipe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from allauth.account.views import confirm_email
#from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/crop', include('crop.urls')),
    path('api/v1/user/', include('dj_rest_auth.urls')),
    path('api/v1/user/registration/', include('dj_rest_auth.registration.urls')),
    path('api/v1/user/', include('allauth.urls')),
    path('api/v1/user/', include('user.urls')),
    path('api/v1/post/', include('post.urls')),
    path('api/v1/payment/', include('payment.urls')),
    #url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
]
