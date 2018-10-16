from django.contrib import admin

from . import models

@admin.register(models.Users)
class UserAdmin(admin.ModelAdmin):
    def is_delete_label(self):
        if self.is_delete_label:
            return "删除"
        else:
            return "不删除"
    #显示所需的
    list_display = ['username','nickname','age','birthday']
    #过滤
    list_filter = ("age",'nickname')
    #分页
    # list_per_page = 3

    # fields = ["nickname",'age']
    # list_editable = ["nickname",'age']
    list_display_links = ['age','nickname']
    fieldsets = [
        ("base",{"fields": ["nickname",'age']}),
        ("other",{"fields": ["username",'password']}),
    ]




# admin.site.register(models.Users)
admin.site.register(models.Article)

