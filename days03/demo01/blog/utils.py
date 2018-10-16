import random, string,redis
import hashlib
import hmac
import logging
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter


from django.conf import settings
from django.core.cache import cache
from . import models
from  django.shortcuts import render

redis.StrictRedis()

#获取随机的4个字符
def getRandomChar(count=4):
    # 生成随机字符串
    #  string 模块包含各种字符串，以下为小写字母加数字
    ran = string.ascii_lowercase + string.digits + string.ascii_uppercase
    char = ''
    for i in range(count):
        char += random.choice(ran)
    return char


# 返回一个随机的 RGB 颜色，红绿蓝0`255,从最暗到最亮
def getRandomColor():
    return (random.randint(50,150),random.randint(50,150),random.randint(50,150))


#创建图片
def create_code():
    # 创建图片，模式，大小（宽高），背景色
    img = Image.new('RGB', (120,30), (255,255,255))
    #创建画布
    draw = ImageDraw.Draw(img)
    # 设置字体
    font = ImageFont.truetype('arial.ttf', 25)

    code = getRandomChar()
    # 将生成的字符画在画布上
    try:
        for t in range(4):
            draw.text((30*t+5,0),code[t],getRandomColor(),font)
    except Exception as e:
        print(e)

    # 生成干扰点，防止机器识别
    for _ in range(random.randint(0,50)):
    # 位置，颜色
        draw.point((random.randint(0, 120),  random.randint(0, 30)),fill=getRandomColor())

    # 使用模糊滤镜使图片模糊
    img = img.filter(ImageFilter.BLUR)
    # 保存
    # img.save(''.join(code)+'.jpg','jpeg')
    return img,code




def hash_by_md5(pwd):
    md5=hashlib.md5(pwd.encode("utf-8"))
    md5.update(settings.MD5_SALT.encode("utf-8"))
    return md5.hexdigest()


def hmac_by_md5(pwd):
    return hmac.new(pwd.encode('utf-8'),settings.MD5_SALT.encode("utf-8"),"MD5").hexdigest()


def getAllArticle(isChenge=False):
    print("查询数据")
    article = cache.get("allArticle")
    if article is None or isChenge:
        print("缓存无数据，查询数据库")
        article = models.Article.objects.all().order_by("publishTime")
        print("数据库中查询到数据，同步到缓存中")
        cache.set("allArticle", article)

    return article


def getMyArticle(u_id,isChenge=False):
    print("查询数据1")
    article = cache.get("myArticle")

    if article is None or isChenge:
        print("缓存无数据，查询数据库1")
        article = models.Article.objects.filter(author=u_id)
        print("数据库中查询到数据，同步到缓存中1")
        cache.set("myArticle", article)

    return article


def require_login(fn):
    def inner(request,*args, **kwargs):
        if request.session.has_key("loginUser"):
            logging.warning("该用户已经登录，视图函数正常访问")
            return fn(request,*args, **kwargs)
        else:
            logging.warning("当前操作需要登录才能执行，请先登录")
            return render(request, "blog/login.html", {"msg": "当前操作必须登录，请先登录系统"})
    return inner


def clear_html_re(content):
    s_content = re.sub(r"</?(.*?)>","",content)
    return s_content