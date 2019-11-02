from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.models import User
import markdown
# 引入login装饰器
from django.contrib.auth.decorators import login_required
# 引入分页模块
from django.core.paginator import Paginator
# 引入 Q 对象
from django.db.models import Q
from django.views import View
from django.core.mail import send_mail
from site_yumanyin.settings import DEFAULT_FROM_EMAIL


def resume(request):
    return render(request, 'mysite/resume.html', locals())


def index(request):
    return render(request, 'mysite/index.html', locals())


def projects(request):
    return render(request, 'mysite/projects.html', locals())


def blog(request):
    return render(request, 'mysite/blog.html', locals())


def contact(request):
    return render(request, 'mysite/contact.html', locals())


def article_list(request):
    order = request.GET.get('order')
    column = request.GET.get('column')
    search = request.GET.get('search')

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    # 用户搜索逻辑
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    # 分页模块
    # 每页显示 3 篇文章
    paginator = Paginator(article_list, 2)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
    }
    # render函数：载入模版，并返回context对象
    return render(request, 'mysite/blog.html', context)


def article_detail(request, id):
    # 取出对应id的博客文章
    article = ArticlePost.objects.get(id=id)

    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # 将markdown语法渲染成html样式
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    # 取出文章评论
    # filter()可以取出多个满足条件的对象，而get()只能取出1个，注意区分使用
    comments = Comment.objects.filter(article=id)
    # 为评论引入表单
    comment_form = CommentForm()

    # 需要传递给模版(templates）的对象
    context = {'article': article}
    # render函数：载入模版，并返回context对象
    return render(request, 'mysite/article_detail.html', context)


# 点赞数 +1
class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')


def send_message(request):
    con = Contact()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            con.name = form.cleaned_data['name']
            con.email = form.cleaned_data['email']
            con.message = form.cleaned_data['message']
            con.save()
            context = {'name': con.name, 'email': con.email, 'message': con.message}
            if send_mail_to_admin(con) == 1:
                render(request, 'mysite/contact.html', context)
                return redirect('../?success/')
            else:
                render(request, 'mysite/contact.html', context)
                return redirect('../?success/')
        else:
            return redirect('../?error_form/')
    else:
        # method == GET
        form = ContactForm()
        return render(request, 'mysite/contact.html', locals())


def send_mail_to_admin(contact):

    get_email = contact.email
    get_name = contact.name
    get_message = contact.message

    mail_title = u'New Contact from My site'
    mail_body = u'You have gotten a new contact information from your site yinyuman.com, please check out this new message ' \
                u'and respond it as soon as possible. \n Name: %s \nEmail: %s \nMessage: %s' % (get_name, get_email, get_message)

    email = 'yinyuman96@gmail.com'
    status = send_mail(mail_title, mail_body, DEFAULT_FROM_EMAIL, [email])
    # 发送成功
    if status == 1:
        print('Send mail to yinyuman96@gmail.com')
    return status

