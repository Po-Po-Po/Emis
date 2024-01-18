from django.urls import re_path
from . import views

app_name = 'print_manager'

urlpatterns = [
    re_path(r'^(?P<url>print_manager)/$', views.print_manager, name='print_manager')
]