# Restframework
from rest_framework import serializers
# in app
from .models import Project, Comment, PrivatePrice, PublicPrice
from user.serializers import UserSerializer

# Project Serializer
class ProjectListlSerializer(serializers.ModelSerializer):
    # extra fields
    is_like = serializers.SerializerMethodField()
    private_price = serializers.SerializerMethodField()
    public_price = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    start_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    end_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    # meta class
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['cur_amount', 'cnt_supporter', 'is_active']
    # method for serializermethodfield
    def get_is_like(self, obj):
        user = self.context['user']
        if user.is_authenticated:
            is_like = obj.likes.filter(user=user)
            if is_like: return True
            else: return False
        return None
    def get_private_price(self, obj):
        private_price = obj.private_prices.order_by('price')
        serializer = PrivatePriceSerializer(private_price, many=True)
        if serializer.data:
            value = serializer.data[0]
        else:
            value = None
        return value
    def get_public_price(self, obj):
        public_price = obj.public_prices.order_by('price')
        serializer = PublicPriceSerializer(public_price, many=True)
        if serializer.data:
            value = serializer.data[0]
        else:
            value = None
        return value

# Project Serializer
class MyProjectlSerializer(serializers.ModelSerializer):
    # extra fields
    author = UserSerializer(read_only=True)
    start_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    end_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    # meta class
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['cur_amount', 'cnt_supporter', 'is_active']

class ProjectDetailSerializer(serializers.ModelSerializer):
    # extra fields
    is_like = serializers.SerializerMethodField()
    likes_cnt = serializers.SerializerMethodField()
    private_price = serializers.SerializerMethodField()
    public_price = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    start_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    end_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    # meta class
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['cur_amount', 'cnt_supporter', 'is_active']
    # method for serializermethodfield
    def get_is_like(self, obj):
        user = self.context['user']
        if user.is_authenticated:
            is_like = obj.likes.filter(user=user)
            if is_like: return True
            else: return False
        return None
    def get_likes_cnt(self, obj):
        value = len(obj.likes.all())
        return value
    def get_private_price(self, obj):
        private_price = obj.private_prices.order_by('price')
        serializer = PrivatePriceSerializer(private_price, many=True)
        value = serializer.data
        return value
    def get_public_price(self, obj):
        public_price = obj.public_prices.order_by('price')
        serializer = PublicPriceSerializer(public_price, many=True)
        value = serializer.data
        return value

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_cnt = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'updated_at', 'likes_cnt', 'is_like']
    # method for serializermethodfield
    def get_likes_cnt(self, obj):
        value = len(obj.likes.all())
        return value
    
    def get_is_like(self, obj):
        user = self.context['user']
        if user.is_authenticated:
            is_like = obj.likes.filter(user=user)
            if is_like: return True
            else: return False
        return None

class PrivatePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivatePrice
        fields = '__all__'
        read_only_fields = ['project']

class PublicPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicPrice
        fields = '__all__'
        read_only_fields = ['project']