from django import forms
from django.forms import ModelForm
from .models import Attachment

class UploadForm(ModelForm):

    class Meta:
        model = Attachment
        fields = ['name', 'attachments']

    def __init__(self, *args, **kargs):
        super(UploadForm, self).__init__(*args, **kargs)
        self.fields['attachments'].widget.attrs['multiple'] = True
        self.fields['name'].widget.attrs['placeholder'] = 'Введите названия файла'
        self.fields['name'].widget.attrs['data-upload'] = 'name'