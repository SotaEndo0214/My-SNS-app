from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    user_vali = UnicodeUsernameValidator()

    # 名前
    username = models.CharField(_('username'), max_length=50, unique=True)
    # メールアドレス
    email = models.EmailField(_('email address'), unique=True)
    # ユーザーアイコン画像
    icon_image = models.ImageField(upload_to='icon/', blank=True, default='icon/default.jpg')
    # バイオグラフィー
    biography = models.CharField(max_length=200, blank=True)
    # 登録日時
    date_joined = models.DateTimeField(default=timezone.now)
    # 管理者フラグ
    is_staff = models.BooleanField(_('staff status'), default=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Message(models.Model):
    # 投稿者
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 親コメント
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    # 投稿内容
    context = models.TextField(max_length=200)
    # 投稿画像
    image = models.ImageField(upload_to='image/', blank=True)
    # いいね数
    good = models.IntegerField(default=0)
    # 投稿日時
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.context
