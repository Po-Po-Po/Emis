from django.urls import re_path
from . import views
from .api import *
from core.urls import router

app_name = 'files_manager'

router.register(r'attachments', AttachmentViewSet)
urlpatterns = [
    re_path(r'^(?P<url>upload)\/(?P<model>[a-z]+)\/(?P<pk>\d+)', views.UploadView.as_view(), name='upload'),
]