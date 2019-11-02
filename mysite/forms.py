# 引入表单类
from django import forms
# 引入文章模型
from .models import *


# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = ArticlePost
        # 定义表单包含的字段
        fields = ('title',  'column', 'body', 'summary', 'avatar')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
