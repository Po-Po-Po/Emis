from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from openpyxl import Workbook
from modules.crm.models import Personnel

@csrf_exempt
def personnel_excel(request):
    personnel_data = Personnel.objects.all()

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Personnel Data'

    headers = ['ФИО', 'Дата рождения', 'Должность', 'Объект', 'Отдел', 'Телефон', 'Статус', 'Почта']
    worksheet.append(headers)

    for person in personnel_data:
        row = [person.name, person.birthday, person.position, person.entity.name if person.entity else 'Объект отсутствует',
               person.department.name if person.department else 'Отдел отсутствует', str(person.phone), person.status, person.email]
        worksheet.append(row)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=personnel_data.xlsx'
    workbook.save(response)
    return response
