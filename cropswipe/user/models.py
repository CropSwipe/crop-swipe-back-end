# load django package
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager # Abstractuser load

# Create your models here.
class UserManager(BaseUserManager):
    # common user creation
    def create_user(self, email, nickname, phone, password=None):
        if not email:
            raise ValueError('must have user email')
        if not nickname:
            raise ValueError('must have user nickname')
        if not phone:
            raise ValueError('must have user phone')
        user = self.model(
            email = self.normalize_email(email),
            nickname = nickname,
            phone = phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    # super user creation
    def create_superuser(self, email, nickname, phone, password=None):
        user = self.create_user(
            email = email,
            nickname = nickname,
            phone = phone,
            password = password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    objects = UserManager()
    # Custom Field
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=30,unique=True)
    nickname = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    following = models.ManyToManyField('self', symmetrical=False, blank=True)
    # Necessary Field
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # User 모델 식별을 위한 필드 설정
    USERNAME_FIELD = 'email'
    # 필수로 작성해야 되는 필드
    REQUIRED_FIELDS = ['nickname', 'phone']

    def has_perm(self, perm, obj=None):
       return self.is_admin

    def has_module_perms(self, app_label):
       return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin