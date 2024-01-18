from django.views.generic.edit import FormView
from .forms import UploadForm
from .models import Attachment
from django.shortcuts import render, redirect
from django.views.generic.base import View
from modules.crm.models import *
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
import codecs
import json, os
class UploadView(View):
    def handle_uploaded_file(self, f, model, pk):
        filename = f'media/files/{model}/{pk}/{str(f)}'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    

    def post(self, request, url='', model="", pk=''):
        model = eval(model.title())
        item = model.objects.get(pk=pk)
        form = UploadForm(self.request.POST, self.request.FILES)
        if form.is_valid:
            self.handle_uploaded_file(self.request.FILES['attachments'], model, pk)
            attach = form.save(commit=False)
            name = request.POST.get('name')
            context = {
                'pk': pk
            }
            i = 1
            if self.request.FILES:
                for f in self.request.FILES.getlist('attachments'):
                    obj = Attachment.objects.create(name=f'{name}_{i}', attachments=f)
                    i += 1
                    item.files.add(obj)
            return render(request, 'crm/entity_files.html', context)
        else:
            return HttpResponse('Ошибка сохранения')
