from django.urls import re_path
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import *
import uuid
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from modules.crm.models import *
from .forms import UploadForm


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = '__all__'
        # extra_fields = ['pk']


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    filterset_fields = ['entity']

    def create(self, request, *args, **kwargs):
        response = super(AttachmentViewSet, self).create(request, *args, **kwargs)
        model = request.GET.get('model')
        pk = request.GET.get('pk')
        model = eval(model.title())
        item = model.objects.get(pk=pk)
        form = UploadForm(self.request.POST, self.request.FILES)
        # here may be placed additional operations for
        # extracting id of the object and using reverse()
        if 'html' in request.GET:
            name = request.POST.get('name')
            if self.request.FILES:
                i = 1
                for f in self.request.FILES.getlist('attachments'):
                    obj = Attachment.objects.create(name=f'{name}_{i}', attachments=f)
                    i += 1
                    item.files.add(obj)

            context = {
                'pk': request.GET['html']
            }
            return render(request, f'crm/{request.GET.get("model")}_files.html', context)
