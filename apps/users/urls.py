#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path, re_path
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, \
    MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

urlpatterns = [
    # 用户信息
    path('info/', UserInfoView.as_view(), name='user_info'),

    # 用户头像上传
    path('image/upload', UploadImageView.as_view(), name='image_upload'),

    # 用户个人中心修改密码
    path('update/pwd', UpdatePwdView.as_view(), name='update_pwd'),

    # 发送邮箱验证码
    path('sendemail_code/', SendEmailCodeView.as_view(), name='sendemail_code'),

    # 修改邮箱，验证收到的验证码
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),

    # 我的课程
    path('mycourse/', MyCourseView.as_view(), name='mycourse'),

    # 我收藏的课程机构
    path('myfav/org/', MyFavOrgView.as_view(), name='myfav_org'),
    # 我收藏的授课讲师
    path('myfav/teacher/', MyFavTeacherView.as_view(), name='myfav_teacher'),
    # 我收藏的课程
    path('myfav/course/', MyFavCourseView.as_view(), name='myfav_course'),

    # 我的消息
    path('mymessage/', MyMessageView.as_view(), name='mymessage'),
]
