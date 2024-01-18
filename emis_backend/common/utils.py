from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.db.models import Q
from django.utils.module_loading import import_module
import os
from rest_framework import serializers


def add_app(path_module_project, urlpatterns=None, install_app=None):
    modules = os.listdir(path_module_project)
    for module in modules:
        path_module = f'{path_module_project}/{module}'
        if os.path.isdir(path_module_project) and str(module) != '__pycache__' and  str(module) != '__init__.py':
            if urlpatterns != None:
                urls = import_module(f'modules.{module}.urls')
                for url in urls.urlpatterns:
                    urlpatterns.append(url)
            if install_app != None:
                print(f'modules.{module}')
                install_app.append(f'modules.{module}')
                
def path_file(instance, filename):
    ext = str(filename).split('.')[-1]
    return f'files/{instance.pk}/{slugify(str(filename))}.{ext}'
    
class CustomSerializer(serializers.HyperlinkedModelSerializer):

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CustomSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


def convert_full_name(name):
    if isinstance(name, str):
        arr_name = name.split(' ')
        if len(arr_name) == 3:
            name = f'{arr_name[0]} {arr_name[1][:1]}. {arr_name[2][:1]}.'
            return name
    return name
