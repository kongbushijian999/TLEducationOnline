# _*_ encoding:utf-8 _*_
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    # 数据表中的verbose_name也是显示在xadmin后台管理系统页面上的，不加上verbose_name，则直接显示英文字段名
    # 例如：nick_name加上verbose_name后显示‘昵称’，不加则显示‘nick_name’
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(max_length=7, choices=(('male', '男'), ('female', '女')), default='female')
    address = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', max_length=100)

    # meta信息就是在adminx.py文件里注册后，显示在xadmin后台管理系统页面上的信息
    # 这里如果改成‘用户信息abc’，则xadmin后台管理系统上显示的也是‘用户信息abc’
    class Meta:
        verbose_name = '用户信息'
        # 这里如果不加这一句，在xadmin后台管理系统上则会自动帮我们加上字母‘s’，显示为‘用户信息s’
        verbose_name_plural = verbose_name

    # 如果不重载该方法，在print UserProfile的实例的时候，就不能打印我们自定义的字符串
    def __str__(self):
        return self.username

    def get_unread_nums(self):
        # 获取用户未读消息的数量
        from operation.models import UserMessage
        # 不能放在开头，不然会形成循环的调用
        # 此时是在调用时import
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(choices=(('register', '注册'), ('forget', '找回密码'), ('update_email', '修改邮箱')), max_length=20, verbose_name='验证码类型')
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')
    # 要去掉now()后的括号，不然就会根据model编译的时间来生成默认时间，不是我们想要的，去掉后则是class实例化的时间

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    # 重载该方法，这样就能在xadmin后台管理系统页面上显示具体的信息，而非‘邮箱验证码’
    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name='轮播图', max_length=100)
    url = models.URLField(max_length=200, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name='顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name