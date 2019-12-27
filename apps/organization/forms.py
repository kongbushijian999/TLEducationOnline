#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from django import forms
from operation.models import UserAsk


# 使用Django中的model来定义这个表，解决代码重复的问题
class UserAskForm(forms.ModelForm):
    # my_field = forms.CharField()  可以新增字段
    class Meta:
        model = UserAsk # 指明使用哪个model来进行转换
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):  # 必须以clean开头
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')