#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time', 'get_zj_nums']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students', 'fav_nums', 'click_nums']  # 查询功能
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time']  # 过滤筛选功能
    model_icon = 'fa fa-book'
    ordering = ['-click_nums']          # xadmin默认排序后显示
    # readonly_fields = ['click_nums']    # 将click_nums字段设为只读
    # exclude = ['fav_nums']              # 隐藏字段，与只读readonly_fields是相互冲突的，不能既只读又隐藏
    # 将多个表拼到一起（有外键），在course下直接添加lesson，resource，但不能双层嵌套，即此时不能再在lesson中添加video
    inlines = [LessonInline, CourseResourceInline]
    list_editable = ['degree', 'desc']  # 在列表页直接修改
    refresh_times = [3, 5]              # 定时刷新页面，单位是秒，此时可以选择列表里的3s或5s刷新一次页面
    style_fields = {"detail": "ueditor"}# 指明了detail页面使用ueditor样式
    import_excel = True                 # 导入功能

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
    # def save_models(self):
    #     obj = self.new_obj
    #     obj.save()
    #     if obj.course_org is not None:
    #         course_org = obj.course_org
    #         course_org.course_nums = Course.objects.filter(course_org=course_org).count()
    #         course_org.save()


# 一张表使用两个管理器，将所有课程分成轮播与课程两个管理器
class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    model_icon = 'fa fa-recycle'
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]

    # 统计数量
    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


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
