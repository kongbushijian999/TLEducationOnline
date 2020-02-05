#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xadmin
from .models import UserAsk, CourseComments, CourseScores, UserFavorite, UserMessage, UserCourse


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']  # 在前段显示的数据
    search_fields = ['name', 'mobile', 'course_name']  # 查询功能
    list_filter = ['name', 'mobile', 'course_name', 'add_time']  # 过滤筛选功能
    model_icon = 'fa fa-question'


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']  # 在前段显示的数据
    search_fields = ['user', 'fav_id', 'fav_type']  # 查询功能
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']  # 过滤筛选功能
    model_icon = 'fa fa-heart'


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']  # 在前段显示的数据
    search_fields = ['user', 'message', 'has_read']  # 查询功能
    list_filter = ['user', 'message', 'has_read', 'add_time']  # 过滤筛选功能
    model_icon = 'fa fa-volume-up'


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']  # 在前段显示的数据
    search_fields = ['user', 'course']  # 查询功能
    list_filter = ['user', 'course', 'add_time']  # 过滤筛选功能
    model_icon = 'fa fa-laptop'


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']  # 在前段显示的数据
    search_fields = ['user', 'course', 'comments']  # 查询功能
    list_filter = ['user', 'course', 'comments', 'add_time']  # 过滤筛选功能
    model_icon = 'fa fa-comments'


class CourseScoresAdmin(object):
    list_display = ['user', 'course', 'scores', 'add_time']  # 在前段显示的数据
    search_fields = ['user', 'course', 'scores']  # 查询功能
    list_filter = ['user', 'course', 'scores', 'add_time']  # 过滤筛选功能
    model_icon = 'fa fa-star'


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(CourseScores, CourseScoresAdmin)