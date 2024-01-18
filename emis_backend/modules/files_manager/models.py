from django.db import models
from django.utils.translation import gettext_lazy as _
from uuslug import slugify


def path_file(instance, filename):
    ext = str(filename).split('.')[-1]
    return f'files/{instance.pk}/{slugify(str(filename))}.{ext}'


class Attachment(models.Model):
    name = models.CharField(_("Название файла"),
                            max_length=100, blank=True, null=True)
    attachments = models.FileField(_("Файлы"), blank=True, upload_to=path_file)

    objects = models.Manager()

    def __str__(self):
        if self.name:
            return self.name
        return 'No name'

    @property
    def ext(self):
        filename = self.attachments.name
        if filename:
            return filename.split('.')[-1]
        return ''
