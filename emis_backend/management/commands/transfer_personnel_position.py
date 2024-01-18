from django.core.management.base import BaseCommand
from modules.crm.models import Personnel, HistoryTabel


class Command(BaseCommand):
    help = 'Пересохраняет текущие профессии персонала в новое поле таблицы'

    def handle(self, *args, **options):
        personnel_with_positions = Personnel.objects.exclude(position__isnull=True).exclude(position__exact='')

        for personnel in personnel_with_positions:
            history_entries = HistoryTabel.objects.filter(personnel=personnel)

            for entry in history_entries:
                entry.position = personnel.position
                entry.save()

        personnel_with_positions = Personnel.objects.exclude(code__name__isnull=True).exclude(code__name__exact='')

        for personnel in personnel_with_positions:
            history_entries = HistoryTabel.objects.filter(personnel=personnel)

            for entry in history_entries:
                entry.code = personnel.code.name
                entry.save()
