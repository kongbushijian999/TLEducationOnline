# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from operation.models import UserFavorite, CourseComments, CourseScores, UserCourse, UserProfile
from .models import Course, CourseResource, Video
from utils.mixin_utils import LoginRequiredMixin
import numpy as np
# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 课程搜索
        search_keywords = request.GET.get('keywords', '') # 通过地址传递
        # 如果有这个keywords
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)
                                             |Q(detail__icontains=search_keywords)|Q(category__icontains=search_keywords)
                                             |Q(tag__icontains=search_keywords)|Q(youneed_know__icontains=search_keywords)
                                             |Q(teacher_tell__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 9, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses
        })


class CourseDetailView(View):
    # 课程详情页
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False
        # 判断用户是否登录
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            # ~Q(id=course.id)排除掉推荐的是同一门课程的情况
            relate_courses = Course.objects.filter(Q(tag=tag)&~Q(id=course.id))[:1]
        else:
            relate_courses = []

        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    # 课程章节信息
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        course.students += 1
        course.save()

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        # 学习该课程的所有用户
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids) # __in是因为传进去的是一个list
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': all_resources,
            'relate_courses': relate_courses
        })


class CommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course).order_by('-add_time')

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()


        # 该用户评分的所有课程的关联
        all_currentuser_courses = CourseScores.objects.filter(user=request.user)
        # 用户已评分课程的id
        all_currentuser_courses_ids = [all_currentuser_course.course.id for all_currentuser_course in all_currentuser_courses]
        # 所有课程
        all_courses = Course.objects.all()
        # 所有课程的id
        all_courses_ids = [all_course.id for all_course in all_courses]
        # 该用户没有评分的课程的id，差集
        all_currentuser_notcourses_ids = list(set(all_courses_ids).difference(set(all_currentuser_courses_ids)))

        # 建立一个双重列表
        xx = max(all_currentuser_courses_ids) + 1
        yy = max(all_currentuser_notcourses_ids) + 1
        # 计算 R(ij)
        R = []
        # 统计同时对i和j评分的用户数量
        N = []
        for x in range(xx):
            RY = []
            NY = []
            for y in range(yy):
                RY.append(0)
                NY.append(0)
            R.append(RY)
            N.append(NY)

        for i in all_currentuser_courses_ids:
            for j in all_currentuser_notcourses_ids:
                # i是已评分，j是没评分
                # 对i评分过的用户
                scores_is = CourseScores.objects.filter(course_id=i)
                # 这些用户的id
                scores_i_ids = [scores_i.user.id for scores_i in scores_is]
                # 对j评分过的用户
                scores_js = CourseScores.objects.filter(course_id=j)
                # 这些用户的id
                scores_j_ids = [scores_j.user.id for scores_j in scores_js]
                # 两者的交集就是同时给i和j评分的用户的id
                scores_ij_ids = list(set(scores_i_ids).intersection(set(scores_j_ids)))

                # 统计这些用户的数量，得到分母
                count_scores_ij = len(scores_ij_ids)
                N[i][j] = count_scores_ij

                # 计算分子
                count = 0
                # 遍历对i和j都评分过的用户
                for id in scores_ij_ids:
                    # 用户对i的评分
                    rui = CourseScores.objects.get(user_id=id, course_id=i).scores
                    # 用户对j的评分
                    ruj = CourseScores.objects.get(user_id=id, course_id=j).scores
                    # 得到分子
                    count = count + (rui - ruj)

                # 相除得到 R(ij)
                if count_scores_ij != 0:
                    R[i][j] = count/count_scores_ij
                else:
                    R[i][j] = count

        # 计算预测评分 P(ij)
        P = []
        for y in range(yy):
            P.append(0)
        # 此时的用户是request.user，要对每个j进行预测评分
        for j in all_currentuser_notcourses_ids:
            # 分母是累加得到的
            count_all_users = 0
            # 分子同样是累加得到的
            count_all_users_scores = 0
            for i in all_currentuser_courses_ids:
                # 累加得到分母
                count_all_users = count_all_users + N[i][j]

                # 计算分子
                # 先取得 ri
                ri = CourseScores.objects.get(user=request.user, course_id=i).scores
                count_all_users_scores = count_all_users_scores + N[i][j] * (ri - R[i][j])

            # 通过累加后的分子除以累加后的分母，得到关于j的预测评分
            if count_all_users != 0:
                P[j] = count_all_users_scores/count_all_users
            else:
                P[j] = count_all_users_scores

        P_arr = np.array(P)
        P_Big = np.argsort(-P_arr)[:5]  # 逆序输出前5位
        relate_courses = Course.objects.filter(id__in=P_Big)


        # user_courses = UserCourse.objects.filter(course=course)
        # # 学习该课程的所有用户id
        # user_ids = [user_course.user.id for user_course in user_courses]
        # # 通过所有的用户id，取出这些id相关联的所有课程，此时每个课程都包含了一堆信息，例如：课程名，添加时间等等
        # all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # _id是通过user这个外键取id，__in是因为传进去的是一个list
        # # 取出所有课程的id
        # course_ids = [user_course.course.id for user_course in all_user_courses]
        # # 排序取出点击数排在前5的课程
        # relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': all_resources,
            'all_comments': all_comments,
            'relate_courses': relate_courses
        })


class AddCommentsView(LoginRequiredMixin, View):
    # 用户添加课程评论
    def post(self, request):
        # 判断用户是否登录
        if not request.user.is_authenticated:  # 未登录时
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course = Course.objects.get(id=int(course_id))
            course_comments = CourseComments()
            course_comments.course = course # 赋值
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


class AddScoreView(LoginRequiredMixin, View):
    # 用户添加课程评分
    def post(self, request):
        # 判断用户是否登录
        if not request.user.is_authenticated:  # 未登录时
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        scores = request.POST.get('scores', '5')
        if int(course_id) > 0 and scores:
            course = Course.objects.get(id=int(course_id))
            user = request.user
            course_scores = CourseScores.objects.filter(course=course, user=user)
            if course_scores.exists():
                for course_score in course_scores:
                    course_score.scores = int(scores) # 赋值
                    course_score.save()
            else:
                course_score = CourseScores()
                course_score.course = course  # 赋值
                course_score.scores = int(scores)
                course_score.user = user
                course_score.save()
                return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


class VideoPlayView(LoginRequiredMixin, View):
    # 视频播放页面
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        # 学习该课程的所有用户
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # __in是因为传进去的是一个list
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'course_resources': all_resources,
            'relate_courses': relate_courses,
            'video': video
        })