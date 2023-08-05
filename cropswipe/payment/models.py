from django.db import models
from user.models import User
from crop.models import PublicPrice

# Create your models here.
class KakaoPayment(models.Model):
    payment_type = [
        (0, 'CARD'),
        (1, 'MONEY'),
    ]
    tid = models.CharField(max_length=50)
    payment_method_type = models.IntegerField(choices=payment_type)
    amount = models.IntegerField()
    item_name = models.CharField(max_length=100)
    item_code = models.IntegerField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField()
    approved_at = models.DateTimeField()

class Order(models.Model):
    supporter = models.ForeignKey(User, on_delete=models.CASCADE)
    public_price = models.ForeignKey(PublicPrice, on_delete=models.CASCADE)
    receiver_name = models.CharField(max_length=5)
    receiver_post_number = models.CharField(max_length=50)
    receiver_main_address = models.CharField(max_length=50)
    receiver_sub_address = models.CharField(max_length=50)
    receiver_phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)