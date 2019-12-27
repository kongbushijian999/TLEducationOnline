#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset, Main, Side, Row
from django.utils.translation import ugettext as _

from .models import EmailVerifyRecord, Banner, UserProfile


# class UserProfileAdmin(UserAdmin):
#     def get_form_layout(self):
#         if self.org_obj:
#             self.form_layout = (
#                 Main(
#                     Fieldset('',
#                              'username', 'password',
#                              css_class='unsort no_title'
#                              ),
#                     Fieldset(_('Personal info'),
#                              Row('first_name', 'last_name'),
#                              'email'
#                              ),
#                     Fieldset(_('Permissions'),
#                              'groups', 'user_permissions'
#                              ),
#                     Fieldset(_('Important dates'),
#                              'last_login', 'date_joined'
#                              ),
#                 ),
#                 Side(
#                     Fieldset(_('Status'),
#                              'is_active', 'is_staff', 'is_superuser',
#                              ),
#                 )
#             )
#         return super(UserAdmin, self).get_form_layout()


class BaseSetting(object): # 在最上方添加一个‘主题’下拉框
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '幕学后台管理系统' # 左上角logo文字处
    site_footer = '幕学在线网'      # 底部中间的文字
    menu_style = 'accordion'        # 将左侧的表单收起来


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time'] # 在前段显示的数据
    search_fields = ['code', 'email', 'send_type']             # 查询功能
    list_filter = ['code', 'email', 'send_type', 'send_time']  # 过滤筛选功能
    # model_icon = 'fa fa-address-book-o'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']  # 在前段显示的数据
    search_fields = ['title', 'image', 'url', 'index']  # 查询功能
    list_filter = ['title', 'image', 'url', 'index', 'add_time']  # 过滤筛选功能


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)