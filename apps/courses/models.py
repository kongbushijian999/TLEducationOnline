# _*_ encoding:utf-8 _*_
from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField
from organization.models import CourseOrg, Teacher
# Create your models here.


class Course(models.Model):
    # Course -> Lesson -> Video
    # 课程基本信息 -> 章节信息 -> 章节下视频信息
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, verbose_name='教师', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = UEditorField(verbose_name=u"课程详情",width=600, height=600, imagePath="courses/ueditor/",
                                         filePath="courses/ueditor/", default='')
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2, verbose_name='难度')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟数）')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name='封面图', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.CharField(default='后端开发', max_length=20, verbose_name='课程类别')
    tag = models.CharField(default='', max_length=10, verbose_name='课程标签')
    youneed_know = models.CharField(default='', max_length=300, verbose_name='课程前提')
    teacher_tell = models.CharField(default='', max_length=300, verbose_name='老师告诉你')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()
    # 在xadmin中显示的内容，不设置则显示‘get_zj_nums’
    get_zj_nums.short_description = "章节数"

    # 插入HTML代码，使用后需要在list_display[]中添加‘go_to’，这样就能在xadmin前端显示了
    # def go_to(self):
    #     from django.utils.safestring import mark_safe
    #     return mark_safe("<a href='https://www.baidu.com/'>跳转</a>")
    # go_to.short_description = "跳转到百度"

    def get_learn_users(self):
        # 获取学习了该课程的用户数据
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        # 获取课程所有章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        # 必须这样设置，不然就会多生成一张表
        proxy = True

    def __str__(self):
        return self.name


class Lesson(models.Model):
    # 章节信息
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        # 获取章节视频
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    # 章节下视频信息
    lesson = models.ForeignKey(Lesson, verbose_name='章节', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='视频名')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟数）')
    url = models.CharField(max_length=200, default='', verbose_name='访问地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='名称')
    download = models.FileField(upload_to='courses/resource/%Y/%m', verbose_name='资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name