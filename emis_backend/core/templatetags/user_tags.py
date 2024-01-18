from django import template
from django.forms.fields import CheckboxInput
from django.template import Context, Template
from filebrowser.sites import site
from filebrowser.base import FileListing
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
import json, re
register = template.Library()

@register.filter
def has_group(user, group_name):
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False

@register.simple_tag()
def define(val=None, val2=None):
  value = val + '.' + str(val2)
  return value

@register.filter(name='is_checkbox')
def is_checkbox(value):
    return isinstance(value, CheckboxInput)

@register.filter(name='name_template')
def name_template(value, tag):
    """
        Возвращаем имя файла шаблона
    """
    return str(value.template.template).split(tag)[-1]

@register.simple_tag()
def as_html(value, context=None):
    """
        Возвращаем значение значение поле как HTML
        с подгрузкой статики и тегов
    """
    if context:
        context = {'resource': context}
    if not value:
        value = ''
    template = Template("{% load static %}{% load user_tags %}" + value)
    return template.render(Context(context))

@register.simple_tag()
def render(value, **kwargs):
    """
        Рендарим шаблон секции и вставляем в него значения этой секции
    """
    if kwargs.get('pk'):
        pk = kwargs.get('pk')
    else:
        pk = ''
    
    if kwargs.get('csrf'):
        csrf = kwargs.get('csrf')
    else:
        csrf = None
    try:
        template_name = str(value.template.template).split('/')[-1]
        include = "{% include '" + template_name + "' %}"
    except:
        template_name = ''
        print('Not template')
    context = {
        'section': value,
        'title': kwargs.get('title'),
        'pk': str(pk),
        'resource': kwargs.get('resource'),
        'text': kwargs.get('text', None),
        'csrf': f'<input type="hidden" name="csrfmiddlewaretoken" value="{str(csrf)}" />'
    }
    template = Template(include)
    return template.render(Context(context))

   
@register.filter(name='get_key')
def get_key_json(data, key):
    """
    Возвращаем значение ключа
    """
    return dict(data).get(key)

@register.filter(name='only_number')
def only_number(value):
    """
    Убираем все знаки кроме цифр
    """
    return re.sub(r"\D+", "", value)


@register.filter(name='str')
def to_str(value):
    """
    Убираем все знаки кроме цифр
    """
    return str(value)


def checked_radiobox(val):
    if val == 1:
        checked = 'checked'
        return checked
    else:
        checked = ''
        return checked

@register.filter(name='to_dict')
def to_dict(data):
    return data.items()

@register.simple_tag()
def to_list(data):
    return data.split('||')

@register.simple_tag()
def set_val(data):
    return data

@register.simple_tag()
def get_domain(request):
    return request.META.get('HTTP_HOST').split(':')[0]


@register.simple_tag()
def get_request(request, resource):
    utm = {}
    for key, item in request.items():
        utm.update({key:item})

    resource.get = utm

@register.simple_tag()
def get(request, _key):
    data = {}
    for key, item in request.items():
        print(f'{key}:{item}')
        data.update({key:item})

    return data.get(_key)