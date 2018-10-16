from django.conf.urls import url

from . import views
app_name = "blog"

urlpatterns = [
    url(r'^index/$',views.index, name="index"),
    url(r'^add_user/$',views.add_user, name="add_user"),
    # url(r'^delete_user/$',views.delete_user, name="delete_user"),
    # url(r'^(\d+)/delete_user/$',views.delete_user, name="delete_user"),
    # url(r'^delete_user/(\d+)/$',views.delete_user, name="delete_user"),
    url(r'^delete_user/(?P<user_id>\d+)/$',views.delete_user, name="delete_user"),
    url(r'^show/(?P<user_id>\d+)/$',views.show, name="show"),
    url(r'^update/(\d+)/$',views.update, name="update"),


    url(r'^login/$',views.login, name="login"),
    url(r'^logout/$',views.logout, name="logout"),
    url(r'^main/(?P<user_id>\d+)/$',views.main, name="main"),
    url(r'^register/$',views.register, name="register"),
    url(r'^(?P<a_id>\d+)/author_info_editor/$',views.author_info_editor, name="author_info_editor"),
    url(r'^(?P<a_id>\d+)/author_info/$',views.author_info, name="author_info"),
    url(r'^author_info_passwd/$',views.author_info_passwd, name="author_info_passwd"),


    url(r'^(?P<a_id>\d+)/article_single/$',views.article_single, name="article_single"),
    url(r'^(?P<a_id>\d+)/article_delete/$',views.article_delete, name="article_delete"),
    url(r"^(\w+)/checkusername/$", views.checkusername, name="checkusername"),


    url(r'^(?P<a_id>\d+)article_update/$',views.article_update, name="article_update"),

    url(r'^article_publish/$',views.article_publish, name="article_publish"),
    url(r'^code/$',views.code, name="code"),
]