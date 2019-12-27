#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xadmin
from .models import CourseOrg, CityDict, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']  # 在前段显示的数据
    search_fields = ['name', 'desc']  # 查询功能
    list_filter = ['name', 'desc', 'add_time']  # 过滤筛选功能


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city', 'add_time']  # 在前段显示的数据
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city']  # 查询功能
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city', 'add_time']  # 过滤筛选功能


class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']  # 在前段显示的数据
    search_fields = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']  # 查询功能
    list_filter = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']  # 过滤筛选功能


xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
