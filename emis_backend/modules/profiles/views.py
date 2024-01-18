from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CustomSetPasswordForm, CustomUserForm
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from ..authentication.views import check_auth, check_group
from functools import partial


def send_email(head_message, message):
    mail_subject = head_message
    message = message
    email = EmailMessage(
        mail_subject, message, from_email=settings.EMAIL_HOST_USER, to=[
            settings.EMAIL_ADMIN_CRM]
    )
    email.content_subtype = "html"
    email.send()



@check_auth
@partial(check_group, group_name="Администратор")
def profiles_list(request, *args, **kwargs):
    users = CustomUser.objects.all()
    context = {
        'users_list': users,
    }
    return render(request, 'profiles.html', context)


@check_auth
def change_password(request):
    if request.method == 'POST':
        form = CustomSetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomSetPasswordForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


@check_auth
def user_change_info(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(
                request, ('Your profile was successfully updated!'))
            email_message = render_to_string('send_email_active_to_admin.html', {
                'name': request.user.first_name,
                'lastname': request.user.last_name,
                'phone': request.user.phone,
            })
            send_email('Запрос на активацию акканута', email_message)
            request.user.is_active = False
            # group = Group.objects.get(name="Менеджер")
            # request.user.groups.add(group)
            request.user.save()
            return redirect('/activate_message/')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = CustomUserForm(instance=request.user)
    return render(request, 'userchange.html', {
        'form': user_form,
    })


@check_auth
def user_change_admin(request, user_pk=''):
    if request.method == 'GET':
        users = CustomUser.objects.get(pk=user_pk)
        user_form = ChangeUsersProfiles(instance=users)
        content = {
            'form': user_form,
        }
        return render(request, 'userchange.html', content)

    if request.method == 'POST':
        users = CustomUser.objects.get(pk=user_pk)
        user_form = ChangeUsersProfiles(request.POST, instance=users)
        if user_form.is_valid:
            user_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            content = {
                'redirect': True,
                'redirect_url': '/profiles/',
                'message': 'Данные пользователя обновленны'
            }
            return render(request, 'message.html', content)
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = ChangeUsersProfiles(instance=users)
    return render(request, 'userchange.html', {
        'form': user_form,
    })


def test_page(request, *args, **kwargs):
    if 'q' in request.GET.keys():
        q = request.GET['q']
        if q:
            return HttpResponse('Протестированная страница: ' + q)
    return HttpResponse('Тестовая страница')


@check_auth
@partial(check_group, group_name="Администратор")
def user(request):
    if 'delete' in request.GET.keys():
        delete = request.GET['delete']
        if delete != '':
            try:
                user_del = CustomUser.objects.get(pk=delete)
                user_del.groups.clear()
                user_del.delete()
                return redirect('/profiles/')
            except:
                pass
    if 'add' in request.GET.keys():
        add = request.GET['add']
        if add == 'newuser':
            if request.method == 'POST':
                form_add_user = CustomAddUser(request.POST)
                if form_add_user.is_valid():
                    form_add_user.save()
                    get_pk = CustomUser.objects.get(
                        email=request.POST['email'])
                    url = '/user/?change_password=' + str(get_pk.pk)
                    return redirect(url)
                else:
                    return render(request, 'userchange.html', {
                        'form': form_add_user
                    })
            if request.method == 'GET':
                form_add_user = CustomAddUser(request.POST)
                return render(request, 'userchange.html', {
                    'form': form_add_user
                })
    if 'change_password' in request.GET.keys():
        change_password = request.GET['change_password']
        if change_password != '':
            user_change = CustomUser.objects.get(pk=change_password)
            if request.method == 'POST':
                form = CustomSetPasswordForm(user_change, request.POST)
                if form.is_valid():
                    user_change = form.save()
                    messages.success(
                        request, 'Your password was successfully updated!')
                    # Redirect из iframe
                    content = {
                        'redirect': True,
                        'redirect_url': '/profiles/',
                        'message': 'Пароль изменен'
                    }
                    return render(request, 'message.html', content)
                else:
                    return render(request, 'change_password.html', {
                        'form': form
                    })
            else:
                form = CustomSetPasswordForm(user_change)

            return render(request, 'change_password.html', {
                'form': form
            })

    return render(request, 'message.html')
