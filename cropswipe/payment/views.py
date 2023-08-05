from django.shortcuts import render, redirect
from cropswipe.settings import get_secret
import requests
# rest_framework module
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
class KakaopayReadyView(APIView):
    def get(self, request):
        admin_key = get_secret("SOCIAL_PAYMENT_KAKAO_ADMIN_KEY")
        authorization = f"KakaoAK {admin_key}"
        approve_url = get_secret("SOCIAL_PAYMENT_KAKAO_APPROVE_URL")
        fail_url = get_secret("SOCIAL_PAYMENT_KAKAO_FAIL_URL")
        cancel_url = get_secret("SOCIAL_PAYMENT_KAKAO_CANCEL_URL")
        url = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": authorization,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        params = {
            "cid": "TC0ONETIME",    # 테스트용 코드
            "partner_order_id": "1001",     # 주문번호
            "partner_user_id": "german",    # 유저 아이디
            "item_name": "양상추",        # 구매 물품 이름
            "quantity": "1",                # 구매 물품 수량
            "total_amount": "100",        # 구매 물품 가격
            "tax_free_amount": "0",         # 구매 물품 비과세
            "approval_url": approve_url,
            "cancel_url": cancel_url,
            "fail_url": fail_url,
        }
        res = requests.post(url, headers=headers, data=params)
        print(res.json())
        if res.status_code == 200:
            res_json = res.json()
            tid = res_json.get('tid')
            next_url_pc = res_json.get('next_redirect_pc_url')
            response_data = {
                "tid": tid,
                "next_url_pc": next_url_pc
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'message': 'Invalid request'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class KakaoApproveView(APIView):
    def post(self, request):
        admin_key = get_secret("SOCIAL_PAYMENT_KAKAO_ADMIN_KEY")
        authorization = f"KakaoAK {admin_key}"
        tid = request.GET['tid']
        pg_token = request.GET['pg_token']
        url = 'https://kapi.kakao.com/v1/payment/approve'
        headers = {
            "Authorization": authorization,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        params = {
            "cid": "TC0ONETIME",    # 테스트용 코드
            "tid": tid,
            "partner_order_id": "1001",     # 주문번호
            "partner_user_id": "german",    # 유저 아이디
            "pg_token": pg_token
        }
        res = requests.post(url, headers=headers, data=params)
        # 결제 승인시
        if res.status_code == 200:
            data = request.data # 수령인 이름, 주소, 번호 등의 정보
            res_json = res.json()
            return Response(res_json, status=status.HTTP_200_OK)
        else:
            response_data = {
                'message': 'Invalid request'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)