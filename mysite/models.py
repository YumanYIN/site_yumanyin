from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone
# reserve 反向列表元素
from django.urls import reverse
# Django-taggit 标签
from taggit.managers import TaggableManager
# 处理图片
from PIL import Image
# 引入imagekit
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
# django-ckeditor
from ckeditor.fields import RichTextField
# django-mptt
from mptt.models import MPTTModel, TreeForeignKey


class ArticleColumn(models.Model):
    """
    文章栏目的 Model
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)

    # 创建时间
    c_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# 博客文章数据模型
class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式: CASCADE: 级联删除，即删除User时也删除author
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题图
    avatar = ProcessedImageField(
        upload_to='article/avatar/%Y%m%d',
        processors=[ResizeToFit(width=400)],
        format='JPEG',
        options={'quality': 100},
    )

    # 文章栏目的 “一对多” 外键
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    # 文章标签
    # 采用 Django-taggit 库
    # tags = TaggableManager(blank=True)

    # 文章标题
    # models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    # CharField 有一个必填参数 max_length，它规定字符的最大长度
    title = models.CharField(max_length=100)

    # 文章正文。保存大量文本使用 TextField
    body = models.TextField()

    # 文章概括
    summary = models.TextField()

    # 文章浏览量
    total_views = models.PositiveIntegerField(default=0)

    # 点赞数
    likes = models.PositiveIntegerField(default=0)

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    c_time = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    u_time = models.DateTimeField(auto_now=True)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-c_time',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title

    # 获取文章地址
    # 通过reverse()方法返回文章详情页面的url，实现了路由重定向。
    def get_absolute_url(self):
        return reverse('blog/article', args=[self.id])

    # 保存时处理图片
    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article

    def was_created_recently(self):
        # 若文章是 1 分钟内发表的，则返回 True
        diff = timezone.now() - self.c_time

        # if diff.days <= 0 and diff.seconds < 60:
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            return True
        else:
            return False


# 博文的评论
class Comment(MPTTModel):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    # mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    # 之前: body = model.TextField()
    body = RichTextField()
    c_time = models.DateTimeField(auto_now_add=True)

    # 替换 Meta 为 MPTTMeta
    # class Meta:
    #   ordering = ('c_time',)
    class MPTTMeta:
        order_insertion_by = ['c_time']

    def __str__(self):
        return self.body[:20]


class Contact(models.Model):
    # name of contact
    name = models.CharField(max_length=100, null=False, blank=False)

    # email of contact
    email = models.EmailField(default="", null=False, blank=False)

    # message textarea
    message = models.TextField(blank=True, null=True)
