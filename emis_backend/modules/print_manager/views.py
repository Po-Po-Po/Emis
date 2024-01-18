from django.contrib.auth.decorators import login_required
import os
from django.http import HttpResponse, JsonResponse
from modules.print_manager.report_card import ReportCartPrint
from modules.crm.models import ReportCard


def get_response_print(file_local, filename, content_type: str = 'application/vnd.ms-excel'):
    with open(file_local, 'rb') as f:
        file_data = f.read()

    response = HttpResponse(file_data, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response['Filename'] = filename
    return response


def print_manager(request, url=None):
    error = {}
    report_card_id = request.GET.get('report_card_id')

    if report_card_id is None:
        error = {'message': 'not param report_card_id'}

    if not error:
        queryset = ReportCard.objects.get(id=report_card_id)
        report_card = ReportCartPrint(queryset)
        file_local = report_card.build()

        response = get_response_print(file_local, 'report_card.xlsx')

        os.remove(file_local)

    else:
        response = JsonResponse(error)

    return response
