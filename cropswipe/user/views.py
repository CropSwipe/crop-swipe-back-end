from django.shortcuts import redirect
from django.http import JsonResponse
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework import status
from cropswipe.settings import get_secret
from .models import User
from .serializers import UserSerializer
import requests, json

# Authentication Code Request
def kakao_login(request):
    client_id = get_secret("SOCIAL_AUTH_KAKAO_CLIENT_ID")
    redirect_uri = get_secret("SOCIAL_AUTH_KAKAO_REDIRECT_URI")
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=account_email,profile_image,profile_nickname"
    )

# Access Token Request
def kakao_callback(request):
    client_id = get_secret("SOCIAL_AUTH_KAKAO_CLIENT_ID")
    redirect_uri = get_secret("SOCIAL_AUTH_KAKAO_REDIRECT_URI")
    # Query string 으로부터 code 가져오기
    code = request.GET.get("code")

    # request access token
    url = "https://kauth.kakao.com/oauth/token"
    headers = {"Cotent-type": "application/x-www-form-urlencoded;charset=utf-8"}
    datas = {
        "grant_type" : "authorization_code",
        "client_id" : client_id,
        "redirect_uri" : redirect_uri,
        "code" : code
    }
    # Response python 객체 반환
    token_request = requests.post(url, data=datas, headers=headers)
    token_response_json = token_request.json()

    # 에러 여부 체크
    error = token_response_json.get("error", None)
    if error is not None:
        raise json.JSONDecodeError(error)
    
    # access token 가져오기
    access_token = token_response_json.get("access_token")
    url = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization" : f"Bearer {access_token}"}
    # information request
    profile_request = requests.post(url, headers=headers)
    profile_response_json = profile_request.json()

    # parsing info
    kakao_account = profile_response_json.get('kakao_account')
    email = kakao_account.get('email', None) # 비즈니스로 전환 시 이메일 필수 항목으로 전환 가능
    profile = kakao_account.get('profile')
    nickname = profile.get('nickname')
    profile_image = profile.get('thumbnail_image_url')
    try:
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)
        print(social_user.provider)
        if social_user.provider != 'kakao':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        data = {'code':code, 'access_token':access_token}
        authentication = requests.post("http://127.0.0.1:8000/api/v1/user/login/kakao/auth/", data=data)
        authentication_json = authentication.json()
        return JsonResponse(authentication_json)
    except User.DoesNotExist:
        data = {'code':code, 'access_token':access_token}
        authentication = requests.post("http://127.0.0.1:8000/api/v1/user/login/kakao/auth/", data=data)
        authentication_json = authentication.json()
        user = User.objects.get(email=email)
        user.nickname = nickname
        user.save()
        serializer = UserSerializer(user)
        authentication_json['user'] = serializer.data
        return JsonResponse(authentication_json)
    except SocialAccount.DoesNotExist:
        return JsonResponse({'err_msg': 'email already exists but not social account'}, status=status.HTTP_400_BAD_REQUEST)
    
class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    callback_url =  'http://127.0.0.1/api/v1/user/login/kakao/callback/'
    client_class = OAuth2Client