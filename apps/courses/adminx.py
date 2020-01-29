#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db.models import Sum

import xadmin
from .models import Course, Lesson, Video, CourseResource, BannerCourse


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    # 在前端显示的数据，不仅可以显示变量，也可以显示函数的调用值，例如'get_zj_nums'
    list_display = ['name', 'desc', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums',
                    'get_zj_nums', 'course_org', 'teacher', 'add_time']
    search_fields = ['name', 'desc', 'degree', 'students', 'fav_nums', 'click_nums', 'course_org', 'teacher']  # 查询功能
    list_filter = ['name', 'desc', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums',
                   'course_org', 'teacher', 'add_time']  # 过滤筛选功能
    model_icon = 'fa fa-book'
    ordering = ['-click_nums']          # xadmin默认排序后显示
    # readonly_fields = ['click_nums']    # 将click_nums字段设为只读
    # exclude = ['fav_nums']              # 隐藏字段，与只读readonly_fields是相互冲突的，不能既只读又隐藏
    # 将多个表拼到一起（有外键），在course下直接添加lesson，resource，但不能双层嵌套，即此时不能再在lesson中添加video
    inlines = [LessonInline, CourseResourceInline]
    list_editable = ['degree', 'desc', 'course_org', 'teacher']  # 在列表页直接修改
    refresh_times = [3, 5]                # 定时刷新页面，单位是秒，此时可以选择列表里的3s或5s刷新一次页面
    style_fields = {"detail": "ueditor"}  # 指明了detail页面使用ueditor样式
    import_excel = True                   # 导入功能

    # 统计数量
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)

    # 在保存课程的时候的操作--save_models()函数
    # 此时定义的是--在保存课程的时候统计课程机构的课程数
    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


# 一张表使用两个管理器，将所有课程分成轮播与课程两个管理器
class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'course_org', 'teacher']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students', 'course_org', 'teacher']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'course_org', 'teacher']
    model_icon = 'fa fa-recycle'
    ordering = ['-click_nums']
    # readonly_fields = ['click_nums']
    # exclude = ['fav_nums']
    list_editable = ['course_org', 'teacher']  # 在列表页直接修改
    inlines = [LessonInline, CourseResourceInline]

    # 统计数量
    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs

    # 在保存课程的时候的操作--save_models()函数
    # 此时定义的是--在保存课程的时候统计课程机构的课程数
    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']  # 在前段显示的数据
    search_fields = ['course', 'name']  # 查询功能
    list_filter = ['course__name', 'name', 'add_time'] # 过滤筛选功能
    model_icon = 'fa fa-sitemap'


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']  # 在前段显示的数据
    search_fields = ['lesson', 'name']  # 查询功能
    list_filter = ['lesson', 'name', 'add_time']  # 过滤筛选功能
    model_icon = 'fa fa-video-camera'

    # 在保存课程的时候的操作--save_models()函数
    # 此时定义的是--在保存视频的时候统计课程的总学习时长
    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.lesson.course is not None:
            # 取出视频对应的课程
            course = obj.lesson.course
            # 取出该课程下所有章节
            all_lessons = course.lesson_set.all()
            # 根据章节遍历出所有章节的id
            lesson_ids = [lesson.id for lesson in all_lessons]
            # 根据章节id取出所有的视频
            all_videos = Video.objects.filter(lesson_id__in=lesson_ids)
            # 根据视频遍历出所有的学习时长
            video_learn_times = [video.learn_times for video in all_videos]
            # 将所有的学习时长加起来存入课程的学习时长里面
            course.learn_times = sum(video_learn_times)
            # 保存课程
            course.save()


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']  # 在前段显示的数据
    search_fields = ['course', 'name', 'download']  # 查询功能
    list_filter = ['course', 'name', 'download', 'add_time']  # 过滤筛选功能
    model_icon = 'fa fa-folder'


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
