#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


# 对表单做些验证
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    # EmailField是会在后台自动做验证的
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile # 指明使用哪个model来进行转换
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile # 指明使用哪个model来进行转换
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']