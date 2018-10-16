from io import BytesIO
import uuid
import logging


from django.shortcuts import render
from django.shortcuts import redirect,reverse
from django.http import HttpResponse,JsonResponse


from . import models
from . import utils
# Create your views here.
from django.conf import settings
from django.core.paginator import Paginator
from .utils import require_login



from django.core.cache import cache
# from django.core.cache import cache

def index(request):
    logger = logging.getLogger("django")
    logger.warning("首页开始运行了……")
    articles = utils.getAllArticle().order_by('-publishTime')
    # 第一种分页的实现，我们自己手写实现
    pageSize = int(request.GET.get("pageSize", settings.PAGE_SIZE))
    pageNow = int(request.GET.get("pageNow", 1))

    paginator = Paginator(articles, pageSize)
    page = paginator.page(pageNow)
    return render(request, "blog/index.html", {"page": page, "pageSize": pageSize, "pageNow":pageNow})


def add_user(request):
    logger = logging.getLogger("django")
    logger.warning("用户添加")
    users = models.Users.objects.all()
    return render(request,"blog/add_user.html",{"users":users})


def show(request,user_id):
    logger = logging.getLogger("django")
    logger.warning("用户展示")
    users = models.Users.objects.get(pk=user_id)
    return render(request, "blog/show.html", {"users": users})


def update(request,u_id):
    logger = logging.getLogger("django")
    logger.warning("更新数据")
    if request.method=="GET":
        users=models.Users.objects.filter(id=u_id).first()
        return render(request, "blog/update.html", {"users": users})
    else:
        nickname = request.POST["nickname"].strip()
        age = request.POST["age"]
        if int(age)<0:
            return render(request, "blog/update.html", {"msg": "年龄不能小于0"})
        if len(nickname)<1:
            return render(request, "blog/update.html", {"msg": "呢称不能为空"})
        user= models.Users.objects.get(pk=u_id)
        user.age=age
        user.nickname=nickname
        user.save()
        # return redirect("/blog/show/"+ str(u_id)+ "/")
        return redirect(reverse("blog:show",args=(u_id,)))


def delete_user(request,user_id):
    logger = logging.getLogger("django")
    logger.warning("删除用户")
    # users = models.Users.objects.all()
    # u_id = request.GET["id"]
    try:
        user = models.Users.objects.get(pk=user_id)

        user.delete()
        # return render(request, "blog/add_user.html", {"users": users})
        # try:
        return redirect(reverse("blog:add_user"))
    except Exception as e:
        print(e)
        return redirect(reverse("blog:add_user"))
    # except Exception as e :
    #     print(e)
    #     print("#########")
    #     users = models.Users.objects.all()
    #     return render(request, "blog/add_user.html", {"users": users})


def login(request):
    logger = logging.getLogger("django")
    logger.warning("用户登录")
    if request.method == "GET":
        request.session["s1"] = 0
        return render(request,"blog/login.html",{"msg": "请认真填写"})
    elif request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        password1 = request.POST.get("password1").strip()
        res=request.POST.get("res")
        mycode = request.POST.get("code",None)
        save_code=request.session["code"]

        try:
            if request.session["s1"] >= 3:
                if mycode == None or save_code.upper() != mycode.upper():
                    return render(request, "blog/login.html", {"msg": "验证码错误,请正确填写"})
                if password!=password1:
                    request.session["s1"] += 1
                    return render(request, "blog/login.html", {"msg": "两次密码不一致"})
                password=utils.hmac_by_md5(password)
                users=models.Users.objects.get(username=username,password=password)
                request.session["loginUser"] = users
                request.session["s1"] = 0
                if res:
                    response=redirect(reverse("blog:index"))
                    response.set_cookie("password",password)
                    return response
                else:
                    logger = logging.getLogger("django")
                    logger.warning("登录成功…")
                    return redirect(reverse("blog:index"))
            else:
                if password!=password1:
                    request.session["s1"] += 1
                    return render(request, "blog/login.html", {"msg": "两次密码不一致"})
                password = utils.hmac_by_md5(password)
                users=models.Users.objects.get(username=username,password=password)
                request.session["loginUser"] = users
                request.session["s1"] = 0
                if res:
                    response=redirect(reverse("blog:index"))
                    response.set_cookie("password",password)
                    return response
                else:
                    logger = logging.getLogger("django")
                    logger.warning("登录成功…")
                    return redirect(reverse("blog:index"))
        except Exception as e:
            print(e)
            logger = logging.getLogger("django")
            logger.warning("登录失败…")
            request.session["s1"] += 1
            return render(request, "blog/login.html", {"msg": "登陆失败"})


def logout(request):
    logger = logging.getLogger("django")
    logger.warning("退出登录")
    try:
        del request.session["loginUser"]
    finally:
        return redirect(reverse("blog:index"))


@require_login
def main(request,user_id):
    logger = logging.getLogger("django")
    logger.warning("个人主页展示…")
    users = models.Users.objects.get(pk=user_id)
    article=utils.getMyArticle(user_id).order_by('-publishTime')
    # simplejson.loads(serializers.serialize('json', [user])[1:-1])

    pageSize = int(request.GET.get("pageSize", settings.PAGE_SIZE))
    pageNow = int(request.GET.get("pageNow", 1))

    paginator = Paginator(article, pageSize)
    page = paginator.page(pageNow)
    return render(request, "blog/main.html", {"article": page, "pageSize": pageSize, "pageNow": pageNow,"users": users,})

    # return render(request,"blog/main.html",{"users": users,"article":article})


def register(request):
    logger = logging.getLogger("django")
    logger.warning("用户注册…")
    if request.method=="GET":
        return render(request,"blog/register.html",{"msg": "请认真填写"})
    elif request.method=="POST":
        try:
            users = models.Users.objects.all()
            username=request.POST.get("username").strip()
            password = request.POST.get("password").strip()
            password1 = request.POST.get("password1").strip()
            nickname = request.POST.get("nickname").strip()

            mycode = request.POST.get("code", None)
            save_code = request.session["code"]

            if mycode == None or save_code.upper() != mycode.upper():
                del request.session['code']
                return render(request, "blog/login.html", {"msg": "验证码错误,请正确填写"})

            for u in users:
                if username == u.username:
                    return render(request, "blog/register.html", {"msg": "账号不能重复"})
            if len(username)<1:
                return render(request, "blog/register.html", {"msg": "账号不能为空"})
            if len(password)<6:
                return render(request, "blog/register.html", {"msg": "密码长度不能小于六位"})
            if password!=password1:
                return render(request, "blog/register.html", {"msg": "两次密码不一致"})
            password = utils.hmac_by_md5(password)
            user=models.Users(username=username,password=password,nickname=nickname)
            user.save()
            del request.session['code']
            logger = logging.getLogger("django")
            logger.warning("注册成功…")
            return render(request, "blog/register.html", {"msg": "注册成功,请返回登陆"})
        except Exception as e:
            print(e)
            logger = logging.getLogger("django")
            logger.warning("注册失败…")
            return render(request,"blog/register.html",{"msg":"对不起，用户名不能为空"})




def author_info_editor(request,a_id):
    logger = logging.getLogger("django")
    logger.warning("修改个人信息…")
    user = models.Users.objects.get(pk=a_id)
    if request.method == "GET":
        return render(request,"blog/author_info_editor.html",{"users": user})
    else:
        header_img = request.FILES.get("header_img",None)
        # path = 'static/upload/' +uuid.uuid4().hex+ header_img.name
        # try:
        #     with open(path, "wb") as file:
        #         for f in header_img.chunks():
        #             file.write(f)
        #
        # except Exception as e:
        #     print(e)
        #     return redirect(reverse("blog:index"))

        user.header = header_img
        user.save()
        # return redirect(reverse("blog:article_info", kwargs={"a_id": a_id}))
        return redirect(reverse("blog:author_info", kwargs={"a_id": a_id}))



def author_info_passwd(request):
    logger = logging.getLogger("django")
    logger.warning("修改登录密码…")
    if request.method=="GET":
        return render(request, "blog/author_info_passwd.html", {"msg": "请认真填写"})
    else:
        password = request.POST["password"].strip()
        username = request.POST["username"].strip()
        password1 = request.POST["password1"].strip()
        password2 = request.POST["password2"].strip()
        try:
            if password1!=password2:
                return render(request, "blog/author_info_passwd.html", {"msg": "两次输入的密码不一致"})
            password = utils.hmac_by_md5(password)
            users = models.Users.objects.get(username=username, password=password)
            password1 = utils.hmac_by_md5(password1)
            users.password=password1
            users.save()
            logger = logging.getLogger("django")
            logger.warning("修改登录密码成功…")
            return render(request, "blog/author_info_passwd.html", {"msg": "修改密码成功，请重新登录"})
        except Exception as e:
            print(e)
            logger = logging.getLogger("django")
            logger.warning("修改登录密码失败…")
            return render(request, "blog/author_info_passwd.html", {"msg": "修改密码失败"})



def author_info(request,a_id):
    logger = logging.getLogger("django")
    logger.warning("展示个人信息…")
    user = models.Users.objects.get(pk=a_id)
    return render(request,"blog/author_info.html",{"users": user})



def article_single(request,a_id):
    logger = logging.getLogger("django")
    logger.warning("展示单篇文章…")
    at = models.Article.objects.get(pk=a_id)
    return render(request, "blog/article_single.html", {"article": at})


@require_login
def article_delete(request,a_id):
    logger = logging.getLogger("django")
    logger.warning("文章删除…")
    at=models.Article.objects.get(pk=a_id)
    user_id = request.session["loginUser"].id
    at.delete()
    # return redirect(reverse("blog:index"))
    return redirect(reverse("blog:main", kwargs={"user_id": user_id}))



@require_login
def article_update(request,a_id):
    logger = logging.getLogger("django")
    logger.warning("更新文章…")
    at = models.Article.objects.get(pk=a_id)
    if request.method == "GET":
        return render(request, "blog/article_update.html", {"article": at})
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        remark = utils.clear_html_re(content)[:50] + "..."
        at.title=title
        at.content=content
        at.remark=remark
        at.save()
        logger = logging.getLogger("django")
        logger.warning("修改文章成功…")
        return redirect(reverse("blog:article_single",kwargs={"a_id":a_id}))



def article_publish(request):
    logger = logging.getLogger("django")
    logger.warning("发表文章…")
    if request.method == "GET":
        #######################################################################
        return render(request,"blog/article_publish3.html",{})
    else:
        title=request.POST["title"]
        content = request.POST["content"]
        author=request.session["loginUser"]
        user_id=request.session["loginUser"].id
        remark = utils.clear_html_re(content)[:50] + "..."


        article = models.Article(title=title,content=content,author=author,remark=remark)
        article.save()
        utils.getAllArticle(isChenge=True)
        utils.getMyArticle(user_id,isChenge=True)
        # return redirect(reverse("blog:article_single", kwargs={"a_id": article.id}))
        logger = logging.getLogger("django")
        logger.warning("发表文章成功…")
        return JsonResponse({"msg": "文章添加成功", "success": True})


@require_login
def code(request):
    logger = logging.getLogger("django")
    logger.warning("验证码")
    img,mycode=utils.create_code()

    request.session["code"]=mycode

    bio = BytesIO()
    img.save(bio,'PNG')
    return HttpResponse(bio.getvalue(), 'image/png')



def checkusername(request, u_name):
    logger = logging.getLogger("django")
    logger.warning("用户是否登录验证…")
    qs = models.Users.objects.filter(username=u_name)
    if len(qs) > 0:
        return JsonResponse({"msg": "该用户名已经存在，请重新数据输入！！", "success": False})
    else:
        return JsonResponse({"msg": "恭喜您，用户名可用", "success": True})

