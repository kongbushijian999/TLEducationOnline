#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path, re_path
from .views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView, AddScoreView, VideoPlayView

urlpatterns = [
    # 课程列表页
    path('list/', CourseListView.as_view(), name='course_list'),
    # 课程详情页
    re_path(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),

    re_path(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    # 课程评论
    re_path(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name='course_comments'),

    # 添加课程评论
    path('add_comment/', AddCommentsView.as_view(), name='add_comment'),
    # 添加课程评分
    path('add_score/', AddScoreView.as_view(), name='add_score'),
    # 视频
    re_path(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),

]
