# Restframework
from rest_framework import serializers
# in app
from .models import Project, Comment, Funding, PrivatePrice, PublicPrice
from user.serializers import UserSerializer
# Project Serializer
class ProjectSerializer(serializers.ModelSerializer):
    # extra fields
    private_price = serializers.SerializerMethodField()
    public_price = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    # meta class
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['cur_amount', 'cnt_supporter', 'is_active']
    # method for serializermethodfield
    def get_private_price(self, obj):
        private_price = obj.private_prices.all()
        serializer = PrivatePriceSerializer(private_price, many=True)
        value = serializer.data
        return value
    def get_public_price(self, obj):
        public_price = obj.public_prices.all()
        serializer = PublicPriceSerializer(public_price, many=True)
        value = serializer.data
        return value
    
# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at']

class FundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funding
        fields = '__all__'

class PrivatePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivatePrice
        fields = '__all__'

class PublicPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicPrice
        fields = '__all__'