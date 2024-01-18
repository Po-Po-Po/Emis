import secrets
import string
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import CustomUser
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.admin import AdminPasswordChangeForm

UserModel = get_user_model()
from common.widgets import CustomSelect, MyModelChoiceField
from modules.crm.models import Personnel, Entity, Department


def generate_password() -> str:
    return secrets.token_urlsafe(8)


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.TextInput(),
        disabled=True
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.TextInput(),
        strip=False,
        disabled=True
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        _password = generate_password()
        self.fields['password1'].initial = _password
        self.fields['password2'].initial = _password

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    entity = forms.ModelMultipleChoiceField(
        queryset=Entity.objects.all(),
        label='Объект',
        widget=FilteredSelectMultiple('entity', is_stacked=False),
        required=False
    )
    department = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        label='Отдел',
        widget=FilteredSelectMultiple('department', is_stacked=False),
        required=False
    )

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        # del self.fields['username']

    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(
        label=_(""),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Новый пароль'
            }
        ),
        strip=False,
        help_text='',
    )
    new_password2 = forms.CharField(
        label=_(""),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Повторите пароль еще раз'
            }
        ),
    )


class CustomUserForm(forms.ModelForm):
    personnel = MyModelChoiceField(required=False,
                                   queryset=Personnel.objects.all(),
                                   widget=CustomSelect(attrs={
                                       'class': 'edit-select',
                                       'onchange': 'append_to_a(this, "personnel");'
                                   }))

    def __init__(self, *args, **kargs):
        super(CustomUserForm, self).__init__(*args, **kargs)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'personnel', 'is_active', 'is_superuser')

    # def save(self, commit=True):
    #     user = super(CustomUserForm, self).save(commit=False)
    #     result = super(CustomUserForm, self).save(commit=True)
    #     user.save()
    #
    #
    #     return result


class CustomAdminPasswordChangeForm(AdminPasswordChangeForm):

    def save(self, commit=True):
        raw_password = self.cleaned_data["password1"]
        user = super().save(commit=commit)

        mail_subject = 'Изменение пароля в системе EMIS'
        message = render_to_string('reset_password_email.html', {
            'email': user.email,
            'password': raw_password
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, from_email=settings.EMAIL_HOST_USER, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()
