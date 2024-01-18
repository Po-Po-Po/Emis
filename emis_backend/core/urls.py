"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve 
from filebrowser.sites import site
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework import routers
import debug_toolbar
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
urlpatterns = [
    path('admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
    path('', include('modules.crm.urls')), 
    path('', include('modules.authentication.urls')),
    path('', include('modules.profiles.urls')), 
    path('', include('modules.files_manager.urls')),
    path('', include('modules.print_manager.urls')),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^api\/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^api/', include(router.urls)),
    path('api/', include('api.urls')),
    path('api_schema', get_schema_view(
        title="EMIS api",
        description="Api documentation...",
        version="0.0.1"
    ), name='openapi-schema'),
    path('docs/', include_docs_urls(title='Docs for API')),

    path('debug/', include(debug_toolbar.urls)),

    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]


# add_app(f'{BASE_DIR}/modules', urlpatterns=urlpatterns)
# print(urlpatterns)