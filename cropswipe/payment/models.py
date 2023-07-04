from django.db import models

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