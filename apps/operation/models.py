# _*_ encoding:utf-8 _*_
from django.db import models
from datetime import datetime
from users.models import UserProfile
from courses.models import Course
# Create your models here.


class UserAsk(models.Model):
    # 用户咨询（我要学习）
    name = models.CharField(max_length=20, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    course_name = models.CharField(max_length=50, verbose_name='课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseComments(models.Model):
    # 课程评论
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    comments = models.CharField(max_length=200, verbose_name='评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserFavorite(models.Model):
    # 用户收藏
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    fav_id = models.IntegerField(default=0, verbose_name='数据id')
    fav_type = models.IntegerField(choices=((1, '课程'), (2, '课程结构'), (3, '教师')), default=1, verbose_name='收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='收藏时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserMessage(models.Model):
    # 用户消息
    user = models.IntegerField(default=0, verbose_name='接收用户')
    # 不用外键因为消息有两种，一种是定向发送给某个用户的，另一种则是系统发送给所有用户的
    # 因此用int类型，默认是0代表发给所有用户，另一种则代表用户的id
    # 这样我们在读取消息时就能读取出两种消息来，一种是user=0的，另一种就是user=登录用户id的
    message = models.CharField(max_length=500, verbose_name='消息内容')
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserCourse(models.Model):
    # 用户课程
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='学习时间')

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
