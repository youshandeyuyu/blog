from datetime import datetime

from django.db import models

from DjangoUeditor.models import UEditorField

# from  tinymce.models import HTMLField
# Create your models here.

# class UsersManager(models.Manager):
#     def add_user(self,username,password,age,email):
#         return self.create(username=username,password=password,age=age,email=email)


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, verbose_name="用户名称")
    password = models.CharField(max_length=255, verbose_name="用户密码")
    age = models.IntegerField(default=18, verbose_name="用户年龄")
    nickname = models.CharField(max_length=255, null=True, blank=True, verbose_name="用户昵称")
    birthday = models.DateTimeField(auto_now_add=True, verbose_name="用户生日")
    email = models.EmailField(max_length=255, verbose_name="用户邮箱")
    # 默认是0 表示男生， 1表示女生
    gender = models.BooleanField(default=0)

    #头像
    # header = models.CharField(max_length=255, null=True,blank=True, verbose_name='用户头像')
    header = models.ImageField(upload_to='static/upload/herder',default='static/upload/3.jpg', verbose_name='用户头像')


    def __str__(self):
        return self.nickname


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, unique=True, verbose_name="标题")
    # content = HTMLField()
    content = UEditorField()
    publishTime = models.DateTimeField(auto_now_add=True, verbose_name="发表时间")
    modifyTime = models.DateField(auto_now=True, verbose_name="修改时间")
    remark=models.CharField(max_length=255,null=True, blank=True,verbose_name="摘要")


    #外键
    author = models.ForeignKey(Users,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

