from django.contrib import admin

from .models import *

# 注册ArticlePost到admin中
admin.site.register(ArticlePost)
admin.site.register(ArticleColumn)
admin.site.register(Comment)
admin.site.register(Contact)