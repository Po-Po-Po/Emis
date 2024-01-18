from django.urls import path, include, re_path
from . import views 
from .api import *
from core.urls import router

router.register(r'user', UserViewSet)

urlpatterns = [
    path('api/profile/', ProfileViewSet.as_view(), name='profile'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    re_path(r'^profiles/$', views.profiles_list, name='profiles'),
    re_path(r'^password/$', views.change_password, name='change_password'),
    re_path(r'^userchange/$', views.user_change_info, name='user_change_info'),
    re_path(r'^user\/(?P<user_pk>\d+)', views.user_change_admin, name='user_change_admin'),
    re_path(r'^user/$', views.user, name='user'),
    re_path(r'^test_page/$', views.test_page, name='test_page'),
]