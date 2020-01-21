# -*- coding: utf-8 -*-
import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
# Create your views here.


class CustomBackend(ModelBackend):
    # 用户认证方法的重写，因为默认的认证方法只支持用户名为username的查询，不支持通过邮箱登录
    # 之后要在settings.py里配置 AUTHENTICATION_BACKENDS = ('users.views.CustomBackend',)
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):  # 因为存在Django后台中的密码是密文，所以不能直接判断相等
                return user
        except Exception as e:
            return None


class LogoutView(View):
    # 用户登出
    def get(self, request):
        logout(request)
        # 重定向到首页
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    # 点击登录按钮后先是GET方法传进来，进入login.html登录页面
    def get(self, request):
        return render(request, 'login.html', {})

    # 点击‘立即登录’按钮后，是POST方法把数据传进来
    def post(self, request):
        # 先做表单验证，把具体的信息单独封装起来，减少后台逻辑，Django会帮我们自动返回验证信息，我们只需要配置就能完成这些功能
        # 这个key值一定要与html中对应的name属性完全一致
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '') #这个key值一定要与html中对应的name属性完全一致
            pass_word = request.POST.get('password', '')
            # 认证方法，查询数据库判断用户名和密码是否正确，
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:  # 如果登录成功，跳转到首页
                # 判断用户是否激活
                if user.is_active:
                    # 用户登录，是个默认函数
                    # 根据用户的信息生成了一个session_id，保存在数据库中，因为在用户登录之后，它需要去查询这个session，取出用户的基本信息
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:  # 如果登录失败，仍跳转到登录页面，加上错误提示后重新登录
            return render(request, 'login.html', {'login_form': login_form})

# def uesr_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('username', '')
#         pass_word = request.POST.get('password', '')
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None: # 如果登录成功，跳转到首页
#             login(request, user)
#             return render(request, 'index.html')
#         else: # 如果登录失败，仍跳转到登录页面，加上错误提示后重新登录
#             return render(request, 'login.html', {'msg':'用户名或密码错误'})
#     elif request.method == 'GET':
#         return render(request, 'login.html', {})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            # 注册之前先检查用户是否已经存在，若已经存在，则提示'用户已经存在'
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form':register_form, 'msg': '用户已经存在'})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word) # password加密
            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册TL在线教育'
            user_message.save()

            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form':register_form})


class ActiveUserView(View): # 激活
    # 参数active_code要与urls.py中配置的一样，这样就能把该参数传递进来
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code) # 通过code查找记录
        if all_records: # 如果不为空
            for record in all_records:
                email = record.email # 发送邮件之前就已经记录了发送的邮箱了
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View): # 重置密码
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code) # 通过code查找记录
        if all_records: # 如果不为空
            for record in all_records:
                email = record.email # 发送邮件之前就已经记录了发送的邮箱了
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    # 修改用户密码
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '') #这个key值一定要与html中对应的name属性完全一致
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg':'密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)  # password加密
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


class UserInfoView(LoginRequiredMixin, View):
    # 用户个人信息
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    # 用户修改头像
    def post(self, request):
        # 方法一
        # image_form = UploadImageForm(request.POST, request.FILES)
        # if image_form.is_valid():
        #     image = image_form.cleaned_data['image']
        #     request.user.image = image
        #     request.user.save()
        # 方法二
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    # 在个人中心修改用户密码
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '') #这个key值一定要与html中对应的name属性完全一致
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg": "密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)  # password加密
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    # 发送邮箱验证码
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已存在"}', content_type='application/json')

        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    # 修改个人邮箱，验证收到的验证码
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '') #这个key值一定要与html中对应的name属性完全一致

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email": "验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    # 我的课程
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses
        })


class MyFavOrgView(LoginRequiredMixin, View):
    # 我收藏的课程机构
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    # 我收藏的授课教师
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list
        })


class MyFavCourseView(LoginRequiredMixin, View):
    # 我收藏的课程
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list
        })


class MyMessageView(LoginRequiredMixin, View):
    # 我的消息
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'messages': messages
        })


class IndexView(View):
    # TL在线教育首页
    def get(self, request):
        # 取出轮播图
        # print(1/0)
        all_banners = Banner.objects.all().order_by('-index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs
        })


def page_not_found(request, **kwargs):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response