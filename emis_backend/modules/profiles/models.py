from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from modules.authentication.tokens import account_activation_token
from django.core.mail import EmailMessage
from modules.crm.models import Personnel, History, Department, Entity

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    personnel = models.ForeignKey(Personnel, verbose_name=_("Персонал"), on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    asterisk_number = models.CharField(_('asterisk_number'), max_length=3, blank=True)
    phone = models.CharField(_('phone'), max_length=12, blank=True)
    # phone = PhoneField(blank=True, help_text='Контактный номер')
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=False, help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    history = models.ManyToManyField(History, verbose_name=_("История"), blank=True, related_name='history_user')
    department = models.ManyToManyField(Department, verbose_name=_("Отдел"), blank=True, related_name='department_user')
    entity = models.ManyToManyField(Entity, verbose_name=_("Объект"), blank=True, related_name='entity_user')
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        from urllib.parse import quote
        return "/users/%s/" % quote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def get_phone(self):
        "Returns the short name for the user."
        return self.phone

    def get_asterisk_number(self):
        "Returns the short name for the user."
        return self.asterisk_number

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def __str__(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def save(self, *args, **kwargs):
        if not self.pk:
            self._new_user = True
        raw_password = self._password
        super(CustomUser, self).save(*args, **kwargs)
        try:
            _new_user = self._new_user
        except AttributeError as e:
            _new_user = False

        if _new_user:
            # ToDo Save temp token in DB, live time token 1h, after auth del token
            current_site = settings.DOMAIN
            mail_subject = 'Создан новый пользователь в системе EMIS, требуется активация'
            message = render_to_string('acc_active_email.html', {
                'email': self.email,
                'password': raw_password
            })
            to_email = self.email
            email = EmailMessage(
                mail_subject, message, from_email=settings.EMAIL_HOST_USER, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()
