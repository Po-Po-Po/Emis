from datetime import datetime, timedelta
import os
import json
import logging
import coreapi
import coreschema
from django.apps import apps
from itertools import chain

from django.shortcuts import get_object_or_404
from num2words import num2words
from rest_framework import viewsets, views, status
from rest_framework.schemas import AutoSchema
from .serializers import (
    ChoiceSetSerializer,
    ChoiceSet,
    HistorySerializer,
    PersonnelSerializer,
    EntitySerializer,
    ReportCardSerializer,
    FundSerializer,
    StatusSerializer,
    HistoryTabelSerializer,
    CodeSerializer,
    ControlSerializer,
    CardTableSerializer,
    DepartmentSerializer,
    AdditionalIdentitySerializer,
    TypeControlSerializer,
    IdentitySerializerV1,
    AttachmentSerializer
)
from modules.crm.models import Equipment, History, Entity, Personnel, \
    ReportCard, Status, HistoryTabel, Code, Department, AdditionalIdentity, Identity, TypeControl, Attachment
from django.db import models
from django.db.models import Q
from rest_framework import filters, parsers
from rest_framework.views import Response
from rest_framework.permissions import DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
import django_filters
from api.serializers import EquipmentSerializer
from api.pagination import StandardResultsSetPagination, EquipmentPagination, ControlPagination, PersonnelPagination
from modules.print_manager.fund_table import FundPrint
from modules.print_manager.contract import Contract, docx_render
from modules.print_manager.views import get_response_print
from modules.profiles.models import CustomUser
from common.request import current_request
from common.utils import convert_full_name

logger = logging.getLogger(__name__)


def get_current_user():
    request = current_request()
    try:
        user_id = request.auth.payload.get('user_id')
        return user_id
    except AttributeError:
        return None


def get_user_filter(filter_name, filter_entity=None, filter_department=None):
    user_id = get_current_user()
    _filters = {}
    if user_id:
        user = CustomUser.objects.get(id=user_id)
        groups = user.groups.filter(name='Администратор')
        department = user.department.all()
        entity = user.entity.all()

        if groups:
            return {}
        if filter_name:
            return {filter_name: user.pk}

        if filter_entity:
            _filters.update({f'{filter_entity}__in': entity})

        if filter_department:
            _filters.update({f'{filter_department}__in': department})

    return _filters


class CustomModelViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    field_user_filter = None
    field_entity_filter = None
    field_department_filter = None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('pk'):
            return queryset

        return queryset.filter(
            **get_user_filter(
                self.field_user_filter,
                filter_entity=self.field_entity_filter,
                filter_department=self.field_department_filter
            )
        )


class ChoiceViewSet(views.APIView):
    data = ()

    def get(self, request):
        data = [ChoiceSet(item) for item in self.data]
        return Response(ChoiceSetSerializer(data, many=True).data)


class CardTableViewSet(views.APIView):
    data = ()
    DICT_OF_FILTERS = {
        'contract_number': 'contract_number',
        '-contract_number': '-contract_number',
        'personnel_name': 'personnel__name',
        '-personnel_name': '-personnel__name',
        'personnel_birthday': 'personnel__birthday',
        '-personnel_birthday': '-personnel__birthday',
        'start_date': 'start_date',
        '-start_date': '-start_date',
        'end_date': 'end_date',
        '-end_date': '-end_date',
        'sum': 'accrued',
        '-sum': '-accrued',
        'comment': 'personnel__position',
        '-comment': '-personnel__position',
        'code': 'personnel__code__name',
        '-code': '-personnel__code__name',
        'entity_name': 'report_card__entity__directorate',
        '-entity_name': '-report_card__entity__directorate',
        'customer_name': 'report_card__customer__name',
        '-customer_name': '-report_card__customer__name'
    }

    def get(self, request):
        report_card_id = request.query_params.get('report_card')
        ordering_queryset = request.query_params.get('ordering', None)

        history_table = HistoryTabel.objects.filter(report_card_id=report_card_id).order_by('personnel__name')
        if ordering_queryset:
            history_table = history_table.order_by(self.DICT_OF_FILTERS.get(ordering_queryset))

        return Response(CardTableSerializer(history_table, many=True).data)


class ControlViewSet(views.APIView):
    pagination_class = ControlPagination
    data = ()
    dict_of_filters = {
        'type': 'contract_number',
        '-type': '-contract_number',
        'info': 'personnel__name',
        '-info': '-personnel__name',
        'number': 'personnel__birthday',
        '-number': '-personnel__birthday',
        'entity': 'start_date',
        '-entity': '-start_date',
        'end_date': 'end_date',
        '-end_date': '-end_date',
        'department': 'accrued',
        '-department': '-accrued',
    }
    def get_type(self, obj):
        if isinstance(obj, Equipment):
            return obj.type_name
        elif isinstance(obj, AdditionalIdentity):
            return obj.name
        elif isinstance(obj, TypeControl):
            return obj.row1

    def get_info(self, obj):
        if isinstance(obj, Equipment):
            return obj.name
        elif isinstance(obj, AdditionalIdentity):
            return obj.personnel.name
        elif isinstance(obj, TypeControl):
            return obj.identity_set.first().personnel.name

    def get_number(self, obj):
        if isinstance(obj, Equipment):
            return obj.factory_number
        elif isinstance(obj, AdditionalIdentity):
            return obj.number
        elif isinstance(obj, TypeControl):
            return obj.identity_set.first().number

    def get_entity_name(self, obj):
        if isinstance(obj, Equipment):
            return obj.entity_set.first().name if obj.entity_set.first() else 'Объект у оборудования отсутствует'
        elif isinstance(obj, AdditionalIdentity):
            return obj.personnel.entity.name if obj.personnel.entity else 'Объект у персонала отсутствует'
        elif isinstance(obj, TypeControl):
            return  obj.identity_set.first().personnel.entity.name if obj.identity_set.first().personnel.entity else 'Объект у персонала отсутствует'


    def get_department(self, obj):
        if isinstance(obj, Equipment):
            return obj.department.name if obj.department else 'Отдел у объекта отсутствует'
        elif isinstance(obj, AdditionalIdentity):
            return obj.personnel.department.name if obj.personnel.department else 'Отдел у персонала отсутствует'
        elif isinstance(obj, TypeControl):
            return  obj.identity_set.first().personnel.department.name if obj.identity_set.first().personnel.department else 'Отдел у персонала отсутствует'

    def get_end_date(self, obj):
        if isinstance(obj, Equipment):
            return obj.validity
        elif isinstance(obj, AdditionalIdentity):
            return obj.date2
        elif isinstance(obj, TypeControl):
            return obj.row2

    def sort(self, ordering, combined_data):
        reverse_order = ordering.startswith('-')
        if ordering.endswith('type'):
            combined_data = sorted(
                combined_data,
                key=lambda x: self.get_type(x),
                reverse=reverse_order
            )
        if ordering.endswith('info'):
            combined_data = sorted(
                combined_data,
                key=lambda x: self.get_info(x),
                reverse=reverse_order
            )
        if ordering.endswith('number'):
            combined_data = sorted(
                combined_data,
                key=lambda x: self.get_number(x),
                reverse=reverse_order
            )
        if ordering.endswith('entity'):
            combined_data = sorted(
                combined_data,
                key=lambda x: self.get_entity_name(x),
                reverse=reverse_order
            )
        if ordering.endswith('department'):
            combined_data = sorted(
                combined_data,
                key=lambda x: self.get_department(x),
                reverse=reverse_order
            )
        if ordering.endswith('end_date'):
            combined_data = sorted(
                combined_data,
                key=lambda x: self.get_end_date(x),
                reverse=reverse_order
            )
        return combined_data


    def get(self, request):
        search = request.query_params.get('search_info', '')
        search_number = request.query_params.get('search_number', '')
        entity = request.query_params.get('entity', None)
        department = request.query_params.get('department', None)
        section = request.query_params.get('section', '')
        ordering = request.query_params.get('ordering', '')

        user_entity = request.user.entity.all()
        current_date = datetime.now().date()
        one_month_later = current_date + timedelta(days=30)
        personnel = Personnel.objects.filter(~Q(status='У') & Q(name__icontains=search) & Q(entity__in=user_entity))
        if entity:
            personnel = personnel.filter(entity__pk=int(entity))
        if department:
            personnel = personnel.filter(department__pk=int(department))
        identities = Identity.objects.filter(Q(personnel__in=personnel) & Q(number__icontains=search_number)).prefetch_related('control').order_by('-date_of_issue')
        type_control = []
        for identity in identities:
            identity_control = (identity.control.filter(Q(row2__isnull=False))
                                .exclude(row2__contains='-'))
            for control in identity_control:
                for format in ['%d.%m.%Y', '%Y-%m-%d']:
                    try:
                        control.row2 = datetime.strptime(control.row2, format).date()
                        if control.row2 < one_month_later:
                            type_control.append(control)
                        break
                    except:
                        continue

        additional_identities = AdditionalIdentity.objects.filter(Q(date2__lte=one_month_later) & Q(number__icontains=search_number),
                                                                  personnel__in=personnel).order_by('-date2')
        equipment_data = (Equipment.objects.filter(Q(validity__lte=one_month_later) & Q(factory_number__icontains=search_number) & Q(entity__in=user_entity) &
                                                   (Q(name__icontains=search) | Q(factory_number__icontains=search)))
                          .exclude(Q(validity__isnull=True) | Q(status__in=['К', 'С']))
                          .order_by('-validity'))
        if entity:
            equipment_data = equipment_data.filter(entity__pk=int(entity))
        if department:
            equipment_data = equipment_data.filter(department__pk=int(department))

        if section == 'Персонал':
            combined_data = list(chain(type_control, additional_identities))
        elif section == 'Оборудование':
            combined_data = list(equipment_data)
        else:
            combined_data = list(chain(type_control, additional_identities, equipment_data))

        combined_data = sorted(
            combined_data,
            key=lambda x: x.row2 if hasattr(x, 'row2') else x.date2 if hasattr(x, 'date2') else x.validity
        )
        if ordering:
            combined_data = self.sort(ordering, combined_data)

        paginator = ControlPagination()
        result_page = paginator.paginate_queryset(combined_data, request)
        serializer = ControlSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class FundViewSet(views.APIView):
    pagination_class = StandardResultsSetPagination
    data = ()
    DICT_OF_FILTERS = {
        'contract_number': 'contract_number',
        '-contract_number': '-contract_number',
        'name': 'personnel__name',
        '-name': '-personnel__name',
        'birthday': 'personnel__birthday',
        '-birthday': '-personnel__birthday',
        'start_date': 'start_date',
        '-start_date': '-start_date',
        'end_date': 'end_date',
        '-end_date': '-end_date',
        'sum': 'accrued',
        '-sum': '-accrued',
        'service_provide': 'personnel__position',
        '-service_provide': '-personnel__position',
        'code_name': 'personnel__code__name',
        '-code_name': '-personnel__code__name',
        'entity_name': 'report_card__entity__directorate',
        '-entity_name': '-report_card__entity__directorate',
        'customer_name': 'report_card__customer__name',
        '-customer_name': '-report_card__customer__name',
        'description': 'description',
        '-description': '-description',
    }

    def get(self, request):
        entity = request.query_params.get('entity', None)
        code = request.query_params.get('code', None)
        customer = request.query_params.get('customer', None)
        period = request.query_params.get('period', None)
        search = request.query_params.get('search', None)
        ordering_queryset = request.query_params.get('ordering', None)
        print_queryset = request.query_params.get('print', None)
        fund_queryset = HistoryTabel.objects.filter(**get_user_filter('report_card__user'))
        if search:
            fund_queryset = fund_queryset.filter(Q(personnel__name__icontains=search))
        if code:
            fund_queryset = fund_queryset.filter(personnel__code__id=code)
        if entity:
            fund_queryset = fund_queryset.filter(report_card__entity_id=entity)
        if customer:
            fund_queryset = fund_queryset.filter(report_card__customer__id=customer)
        if period:
            fund_queryset = fund_queryset.filter(report_card__period=period)
        if ordering_queryset:
            fund_queryset = fund_queryset.order_by(self.DICT_OF_FILTERS.get(ordering_queryset))

        if print_queryset:
            print_fund = FundPrint(fund_queryset)
            file_local = print_fund.build()
            response = get_response_print(file_local, 'fund_table.xlsx')
            os.remove(file_local)
            return response

        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(fund_queryset, request)
        serializer = FundSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



class DirectorateViewSet(views.APIView):
    data = ()

    def get(self, request):
        directorate = Entity.objects.all().values_list('directorate', flat=True).annotate(n=models.Count('pk'))
        data = [ChoiceSet(item) for item in [[i, i] for i in directorate]]
        return Response(ChoiceSetSerializer(data, many=True).data)


class EquipmentTypeViewSet(ChoiceViewSet):
    data = Equipment.TYPE


class EquipmentStatusViewSet(ChoiceViewSet):
    data = Equipment.VERIFICATION_STATUS


class PersonnelStatusViewSet(ChoiceViewSet):
    data = Personnel.WORK_STATUS


class HistoryTypeViewSet(ChoiceViewSet):
    data = History.TYPE


class EntityNTDViewSet(ChoiceViewSet):
    data = Entity.NTD


class EntityRDViewSet(ChoiceViewSet):
    data = Entity.RD


class HistoryViewSet(CustomModelViewSet):
    field_entity_filter = 'entity'
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_on', 'entity__name', 'equipment__name', 'type', 'history_user']
    ordering = ['-created_on']
    search_fields = ['equipment__name', 'equipment__factory_number']
    filterset_fields = ['entity', 'equipment', 'type', 'history_user__personnel']
    pagination_class = StandardResultsSetPagination


class HistoryTabelViewSet(CustomModelViewSet):
    field_user_filter = 'report_card__user'
    queryset = HistoryTabel.objects.all()
    serializer_class = HistoryTabelSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['personnel__name', 'end_date', 'start_date', 'report_card', 'contract_number']
    ordering = ['personnel__name']
    search_fields = ['report_card', 'contract_number']
    filterset_fields = ['contract_number', 'report_card']
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        personnel_id = data.get('personnel', None)

        try:
            personnel = Personnel.objects.get(pk=personnel_id)
        except Personnel.DoesNotExist:
            return Response(
                {"detail": "Объект не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        data['position'] = personnel.position
        data['code'] = personnel.code.name if personnel.code else ''

        serializer = HistoryTabelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail=True)
    def print(self, request, pk=None):
        tabel = HistoryTabel.objects.get(id=pk)

        def convert_accrued(value):
            return num2words(value, lang='ru')

        item = Contract()
        item.number = tabel.contract_number
        item.personnel_name = tabel.personnel.name
        item.start_date = tabel.start_date
        item.end_date = tabel.end_date
        item.personnel_short_name = convert_full_name(tabel.personnel.name)
        item.service = tabel.personnel.position
        item.salary = tabel.accrued
        item.salary_text = convert_accrued(tabel.accrued)

        file_local = docx_render(item)
        response = get_response_print(
            file_local,
            f'Договор {item.personnel_name}_{item.number}.docx',
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        os.remove(file_local)
        return response


class CodeViewSet(CustomModelViewSet):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    search_fields = ['name', 'id']
    filterset_fields = ['name']
    pagination_class = StandardResultsSetPagination


class EquipmentFilter(django_filters.FilterSet):
    validity = django_filters.DateFromToRangeFilter()
    date_of_verification = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Equipment
        fields = ['validity', 'entity', 'status', 'type']


class EquipmentViewSet(CustomModelViewSet):
    field_entity_filter = 'entity'
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    pagination_class = EquipmentPagination
    filterset_class = EquipmentFilter
    ordering_fields = ['type', 'name', 'status', 'factory_number', 'entity__name', 'validity']
    ordering = ['name']
    filterset_fields = ['entity', 'status', 'type']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'factory_number', 'id']

    def create(self, request, *args, **kwargs):
        entity_pk = request.data.get('entity', None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        new_equipment = serializer.instance
        if entity_pk:
            try:
                entity = Entity.objects.get(pk=entity_pk)
                entity.equipment.add(new_equipment)
            except Entity.DoesNotExist:
                return Response({'error': 'Entity not found'}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        return super(EquipmentViewSet, self).update(request, *args, **kwargs)

    @action(methods=['post'], detail=True)
    def clone(self, request, pk=None):
        equipment = Equipment.objects.get(pk=pk)
        equipment.name = request.data.get('name')
        try:
            equipment.copy()
            return Response({'pk': equipment.pk, 'message': f'{equipment.name} clone'})
        except Exception as e:
            return Response({'message': f'{e}'}, status=400)


class PersonnelViewSet(CustomModelViewSet):
    field_user_filter = None
    field_entity_filter = 'entity'
    field_department_filter = 'department'
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['position', 'name', 'directorate', 'code__name', 'email', 'entity__name', 'phone',
                       'department__name', 'status']
    ordering = ['name']
    search_fields = ['name', 'id']
    filterset_fields = ['department', 'entity', 'name']
    pagination_class = PersonnelPagination

    def create(self, request, *args, **kwargs):
        entity_pk = request.data.get('entity', None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        new_personnel = serializer.instance
        if entity_pk:
            entity = Entity.objects.get(pk=entity_pk)
            new_personnel.entity = entity
            new_personnel.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReportCardViewSet(CustomModelViewSet):
    field_user_filter = 'user'
    queryset = ReportCard.objects.all()
    serializer_class = ReportCardSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['card', 'responsible__name', 'customer__name', 'period', 'status__name', 'entity__directorate']
    ordering = ['card', 'period']
    search_fields = ['card']
    filterset_fields = ['entity', 'status', 'responsible', 'period']
    pagination_class = StandardResultsSetPagination

    @action(methods=['post'], detail=True)
    def clone(self, request, pk=None):
        report_card = ReportCard.objects.get(pk=pk)
        title = request.data.get('card')
        report_card.card = title
        try:
            report_card.copy()
            return Response({'pk': report_card.pk, 'message': f'{report_card.card} clone'})
        except Exception as e:
            return Response({'message': f'{e}'}, status=400)

    @action(methods=['post'], detail=True)
    def close_card(self, request, pk):
        report_card = ReportCard.objects.get(pk=pk)
        history_tabel_set = report_card.historytabel_set.all().order_by('personnel__name')
        try:
            report_card.is_active = False
            if report_card.is_edit_history_tabel:
                month_number = datetime.now().month
                contract_number = 1
                for history_tabel in history_tabel_set:
                    history_tabel.contract_number = str(month_number) + '.' + str(contract_number)
                    history_tabel.save()
                    contract_number += 1
                report_card.is_edit_history_tabel = False
                report_card.save()
            return Response({'pk': report_card.pk, 'message': f'{report_card.card} closed'})
        except Exception as e:
            return Response({'message': f'{e}'}, status=400)

    @action(methods=['post'], detail=True)
    def unclose_card(self, request, pk):
        report_card = ReportCard.objects.get(pk=pk)
        try:
            report_card.is_active = True
            report_card.save()
            return Response({'pk': report_card.pk, 'message': f'{report_card.card} unclosed'})
        except Exception as e:
            return Response({'message': f'{e}'}, status=400)


class EntityViewSet(CustomModelViewSet):
    field_user_filter = 'entity_user'
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['name', 'director_lnk', 'directorate']
    ordering = ['name']
    search_fields = ['name', 'directorate', 'contractor', 'id']
    filterset_fields = ['directorate', 'name']
    pagination_class = StandardResultsSetPagination


class StatusCardViewSet(CustomModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    search_fields = ['name', 'id']
    filterset_fields = []
    pagination_class = StandardResultsSetPagination


class DepartmentViewSet(CustomModelViewSet):
    field_department_filter = 'department_user__department'
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class AdditionalIdentityV1ViewSet(CustomModelViewSet):
    queryset = AdditionalIdentity.objects.all()
    serializer_class = AdditionalIdentitySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['date1', 'date2', 'cert_center', 'number', 'personnel', 'name']
    ordering = ['-date1']
    filterset_fields = ['personnel']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if self.request.FILES:
            for f in self.request.FILES.getlist('attachment'):
                instance.file = f
                instance.save()

        return super(AdditionalIdentityV1ViewSet, self).update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if self.request.FILES:
            for f in self.request.FILES.getlist('attachment'):
                serializer.instance.file = f
                serializer.instance.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class IdentityViewSetV1(CustomModelViewSet):
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "personnel_id",
            required=False,
            location="query",
            schema=coreschema.Boolean()
        )
    ])
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializerV1
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['number', 'personnel', 'date_of_issue', 'level', 'control', 'cert_center']
    ordering = ['-date_of_issue']
    filterset_fields = ['personnel']

    def retrieve(self, request, *args, **kwargs):
        """
            personnel - Indicates that personnel pk should be used instead of native id .
        """
        return super().retrieve(self, request, *args, **kwargs)

    def get_object(self):
        if 'personnel' in self.request.query_params and self.request.query_params['personnel'] == 'true':
            return get_object_or_404(self.queryset, personnel=self.kwargs.get('pk'))
        return super().get_object()

    def update(self, request, *args, **kwargs):
        # ToDo fix this row
        request.data._mutable = True

        controls = request.data.pop('control')
        instance = self.get_object()

        if self.request.FILES:
            for f in self.request.FILES.getlist('attachment'):
                instance.file = f
                instance.save()

        if controls:
            controls = json.loads(controls[0])

            for control in controls:
                control_id = None
                if 'id' in control:
                    control_id = control.pop('id')
                item, create = TypeControl.objects.update_or_create(pk=control_id, defaults=control)
                if create:
                    instance.control.add(item)
        return super(IdentityViewSetV1, self).update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # ToDo fix this row
        request.data._mutable = True

        controls = request.data.pop('control')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if self.request.FILES:
            for f in self.request.FILES.getlist('attachment'):
                serializer.instance.file = f
                serializer.instance.save()

        if controls:
            controls = json.loads(controls[0])

            for control in controls:
                item = TypeControl.objects.create(**control)
                serializer.instance.control.add(item)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TypeControlViewSet(CustomModelViewSet):

    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "identity",
            required=False,
            location="query",
            schema=coreschema.Number()
        ),
    ])

    queryset = TypeControl.objects.all()
    serializer_class = TypeControlSerializer

    def list(self, request, *args, **kwargs):
        identity_pk = request.query_params.get('identity')
        if identity_pk:
            self.queryset = TypeControl.objects.filter(identity__id=identity_pk)
        return super(TypeControlViewSet, self).list(request, *args, **kwargs)


class AttachmentViewSet(CustomModelViewSet):
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "personnel",
            required=False,
            location="query",
            schema=coreschema.Number()
        ),
        coreapi.Field(
            "identity",
            required=False,
            location="query",
            schema=coreschema.Boolean()
        ),
        coreapi.Field(
            "additional_identity",
            required=False,
            location="query",
            schema=coreschema.Boolean()
        ),
        coreapi.Field(
            "equipment",
            required=False,
            location="query",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "entity",
            required=False,
            location="query",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "equipment",
            required=False,
            location="query",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "entity",
            required=False,
            location="query",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "reportcard",
            required=False,
            location="query",
            schema=coreschema.String()
        )
    ])
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

    def list(self, request, *args, **kwargs):

        filter_set = {}
        personnel_pk = request.query_params.get('personnel')
        if 'identity' in request.query_params and request.query_params['identity'] == 'true':
            filter_set = {
                'identity__personnel__pk': personnel_pk
            }
        elif 'additional_identity' in request.query_params and request.query_params['additional_identity'] == 'true':
            filter_set = {
                'additionalidentity__personnel__pk': personnel_pk
            }
        elif 'equipment' in request.query_params:
            filter_set = {
                'equipment__pk': request.query_params['equipment']
            }
        elif 'entity' in request.query_params:
            filter_set = {
                'entity__pk': request.query_params['entity']
            }
        elif 'reportcard' in request.query_params:
            filter_set = {
                'reportcard__pk': request.query_params['reportcard']
            }
        else:
            filter_set = {
                'personnel__pk': personnel_pk
            }

        if personnel_pk or filter_set:
            self.queryset = Attachment.objects.filter(**filter_set)

        return super(AttachmentViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        filename = request.data.get('filename')
        model_name = request.data.get('model')
        pk = request.data.get('id')
        model = apps.get_model('crm', model_name.title())
        item = model.objects.get(pk=pk)
        if self.request.FILES:
            i = 1
            for f in self.request.FILES.getlist('attachments'):
                obj = Attachment.objects.create(name=f'{filename}_{i}', attachments=f)
                i += 1
                item.files.add(obj)
        return Response(status=204)


class SectionViewSet(ChoiceViewSet):
    data = [
        ('Персонал', 'Персонал'),
        ('Оборудование', 'Оборудование')
    ]
