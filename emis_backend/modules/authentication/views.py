from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic.base import View
from .forms import MyAuthenticationForm, SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str as force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from ..profiles.models import CustomUser
from django.conf import settings
# Декоратор проверки авторизации на странице
def check_auth(function_check_auth, request=None, *args, **kwargs):
    def wrap_check_auth(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function_check_auth(request, *args, **kwargs)
        else:
            return redirect('/login/')
    return wrap_check_auth


# Декоратор проверки принадлежности группе
def check_group(function_check_group, group_name, *args, **kwargs):
    def wrap_check_group(request, *args, **kwargs):
        groups = request.user.groups.all().values_list('name', flat=True)
        if group_name in groups:
            return function_check_group(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrap_check_group


class LoginFormView(FormView):

    form_class = MyAuthenticationForm
    template_name = "login.html"
    success_url = '/manager/'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')

# class RegistryUserCrm(TemplateView):
#     template_name = "registry.html"


def registry(request):
    return render(request, 'registry.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            # user.email = form.cleaned_data.get["email"]
            user.save()
            # from_email='crm@red-eye.su'
            current_site = get_current_site(request)
            mail_subject = 'Запрос на проверку почты - CRM REDEYE'
            message = render_to_string('acc_active_email.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, from_email='crm@red-eye.su', to=[to_email]
            )
            email.content_subtype = "html"
            email.send()
            return redirect('/activate_text/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def reset_password(request):
    _email = request.POST.get("email")
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(email=_email)
        except CustomUser.DoesNotExist:
            context = {
                'title': 'Восстановление пароля',
                'msg': f'Пользователь с электронной почтой {_email} не найден'
            }
            return render(request, 'profiles/profile_msg.html', context)
        current_site = settings.DOMAIN
        mail_subject = 'Создан новый пользователь в системе EMIS, требуется активация'
        message = render_to_string('acc_active_email.html', {
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, from_email=settings.EMAIL_HOST_USER, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()
        context = {
            'title': 'Восстановление пароля',
            'msg': f'Ссылка на восстановление пароля отправлена на электронную почту {_email}'
        }
        return render(request, 'profiles/profile_msg.html', context)
    return render(request, 'profiles/reset_password.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/password/')
    else:
        return redirect('/activate_text/')


def activate_text(request):
    return render(request, 'activate.html')


def activate_message(request):
    return render(request, 'message_activate_user.html')
