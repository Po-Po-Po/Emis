from rest_framework import serializers

import serpy
from modules.crm.models import (
    Equipment,
    History,
    Entity,
    Personnel,
    ReportCard,
    Status,
    HistoryTabel,
    Code,
    Department,
    AdditionalIdentity,
    Identity,
    TypeControl,
    Attachment
)
from common.utils import convert_full_name


class ChoiceSet:
    name = None
    id = None

    def __init__(self, item):
        self.id = item[0]
        self.name = item[1]


class ChoiceSetSerializer(serpy.Serializer):
    name = serpy.Field()
    id = serpy.Field()


class CardTableSerializer(serpy.Serializer):
    id = serpy.MethodField()
    number = serpy.MethodField()
    contract_number = serpy.MethodField()
    personnel_name = serpy.MethodField()
    personnel_birthday = serpy.MethodField()
    start_date = serpy.MethodField()
    end_date = serpy.MethodField()
    sum = serpy.MethodField()
    position = serpy.MethodField()
    code = serpy.MethodField()
    entity_name = serpy.MethodField()
    customer_name = serpy.MethodField()
    description = serpy.MethodField()

    def get_id(self, obj):
        return obj.id

    def get_number(self, obj):
        return obj.number

    def get_contract_number(self, obj):
        return obj.contract_number

    def get_personnel_name(self, obj):
        return obj.personnel.name if obj.personnel else None

    def get_personnel_birthday(self, obj):
        return obj.personnel.birthday if obj.personnel else None

    def get_start_date(self, obj):
        return obj.start_date

    def get_end_date(self, obj):
        return obj.end_date

    def get_sum(self, obj):
        return obj.accrued

    def get_position(self, obj):
        return obj.position

    def get_code(self, obj):
        return obj.code

    def get_entity_name(self, obj):
        return obj.report_card.entity.directorate if obj.report_card.entity else None

    def get_customer_name(self, obj):
        return convert_full_name(obj.report_card.customer.name)

    def get_description(self, obj):
        if obj.description:
            return obj.description
        else:
            return obj.report_card.description


class EntityForEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ['id', 'name']


class EquipmentSerializer(serializers.ModelSerializer):
    type_name = serializers.StringRelatedField(read_only=True)
    entity = EntityForEquipmentSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Equipment
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)
    equipment_name = serializers.SerializerMethodField(read_only=True)
    entity_name = serializers.SerializerMethodField(read_only=True)
    type_name = serializers.SerializerMethodField(read_only=True)
    file = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = History
        fields = [
            'id',
            'created_on',
            'type',
            'type_name',
            'comment',
            'equipment',
            'equipment_name',
            'entity',
            'entity_name',
            'file',
            'user_name',
        ]

    def get_user_name(self, obj):
        return obj.user_name

    def get_equipment_name(self, obj):
        return f'{obj.equipment.name} ({obj.equipment.factory_number})'

    def get_entity_name(self, obj):
        if obj.entity:
            return obj.entity.name
        return None

    def get_type_name(self, obj):
        return obj.type_name

    def get_file(self, obj):
        return obj.file


class HistoryTabelSerializer(serializers.ModelSerializer):
    personnel_name = serializers.SerializerMethodField()
    personnel_birthday = serializers.SerializerMethodField()
    work_day = serializers.SerializerMethodField()

    class Meta:
        model = HistoryTabel
        fields = '__all__'

    def get_personnel_name(self, obj):
        return obj.personnel.name if obj.personnel else None

    def get_personnel_birthday(self, obj):
        return obj.personnel.birthday if obj.personnel else None

    def get_work_day(self, obj):
        return obj.work_day


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = '__all__'


class EntitySerializer(serializers.ModelSerializer):
    type_name = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Entity
        fields = '__all__'


class ReportCardSerializer(serializers.ModelSerializer):
    responsible_name = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    status_name = serializers.SerializerMethodField()
    entity_name = serializers.SerializerMethodField()

    class Meta:
        model = ReportCard
        fields = '__all__'

    def get_status_name(self, obj):
        if obj.status:
            return obj.status.name
        return None

    def get_customer_name(self, obj):
        if obj.customer:
            arr_name = obj.customer.name.split(' ')
            if len(arr_name) == 3:
                name = f'{arr_name[0]} {arr_name[1][:1]}. {arr_name[2][:1]}.'
                return name
        return None

    def get_responsible_name(self, obj):
        if obj.responsible:
            return obj.responsible.name
        return None

    def get_entity_name(self, obj):
        return obj.entity.directorate if obj.entity else None


class ControlSerializer(serializers.ModelSerializer):
    item_id = serializers.SerializerMethodField()
    section = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()
    number = serializers.SerializerMethodField()
    entity = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = Personnel
        fields = ('item_id', 'section', 'entity', 'info', 'type', 'department', 'number', 'end_date')

    def get_section_name(self, obj):
        if obj.__class__.__name__ == 'TypeControl':
            return 'Квалификационные удостоверения'
        elif obj.__class__.__name__ == 'AdditionalIdentity':
            return 'Дополнительные удостоверения'
        else:
            return 'Оборудование'

    def get_item_id(self, obj):
        if self.get_section_name(obj) == 'Квалификационные удостоверения':
            identity = obj.identity_set.first()
            return identity.personnel.id
        elif self.get_section_name(obj) == 'Дополнительные удостоверения':
            return obj.personnel.id
        else:
            return obj.id

    def get_section(self, obj):
        return 'Персонал' if obj.__class__.__name__ in ['TypeControl', 'AdditionalIdentity'] else 'Оборудование'

    def get_type(self, obj):
        if self.get_section_name(obj) == 'Квалификационные удостоверения':
            return obj.row1
        elif self.get_section_name(obj) == 'Дополнительные удостоверения':
            return obj.name
        else:
            return obj.type_name

    def get_info(self, obj):
        if self.get_section_name(obj) == 'Квалификационные удостоверения':
            identity = obj.identity_set.first()
            return identity.personnel.name
        elif self.get_section_name(obj) == 'Дополнительные удостоверения':
            return obj.personnel.name
        else:
            return obj.name

    def get_number(self, obj):
        if self.get_section_name(obj) == 'Квалификационные удостоверения':
            identity = obj.identity_set.first()
            return identity.number
        elif self.get_section_name(obj) == 'Дополнительные удостоверения':
            return obj.number
        else:
            return obj.factory_number

    def get_entity(self, obj):
        if self.get_section_name(obj) == 'Квалификационные удостоверения':
            identity = obj.identity_set.first()
            if identity.personnel.entity:
                return identity.personnel.entity.name
            else:
                return 'Объект у персонала отсутствует'
        elif self.get_section_name(obj) == 'Дополнительные удостоверения':
            if obj.personnel.entity:
                return obj.personnel.entity.name
            else:
                return 'Объект у персонала отсутствует'
        else:
            if obj.entity:
                return obj.entity_set.first().name
            return 'Объект у оборудования отсутствует'

    def get_department(self, obj):
        if self.get_section_name(obj) == 'Квалификационные удостоверения':
            identity = obj.identity_set.first()
            if identity.personnel.department:
                return identity.personnel.department.name
            else:
                return 'Отдел у персонала отсутствует'
        elif self.get_section_name(obj) == 'Дополнительные удостоверения':
            if obj.personnel.department:
                return obj.personnel.department.name
            else:
                return 'Отдел у персонала отсутствует'
        else:
            if obj.department:
                return obj.department.name
            else:
                return 'Отдел у оборудования отсутствует'

    def get_end_date(self, obj):
        if self.get_section_name(obj) == 'Квалификационные удостоверения':
            return obj.row2
        elif self.get_section_name(obj) == 'Дополнительные удостоверения':
            return obj.date2
        else:
            return obj.validity


class FundSerializer(serializers.ModelSerializer):
    id_report_card = serializers.SerializerMethodField()
    number = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    birthday = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    sum = serializers.SerializerMethodField()
    service_provide = serializers.SerializerMethodField()
    code_name = serializers.SerializerMethodField()
    entity_name = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = HistoryTabel
        fields = '__all__'

    def get_id_report_card(self, obj: HistoryTabel):
        return obj.report_card_id

    def get_number(self, obj):
        return obj.number

    def get_name(self, obj):
        return obj.personnel.name if obj.personnel else None

    def get_birthday(self, obj):
        return obj.personnel.birthday if obj.personnel else None

    def get_start_date(self, obj):
        return obj.start_date

    def get_end_date(self, obj):
        return obj.end_date

    def get_sum(self, obj):
        return obj.accrued

    def get_service_provide(self, obj):
        return obj.position

    def get_code_name(self, obj):
        return obj.code

    def get_entity_name(self, obj):
        return obj.report_card.entity.directorate if obj.report_card.entity else None

    def get_customer_name(self, obj):
        return convert_full_name(obj.report_card.customer.name)

    def get_description(self, obj):
        if obj.description:
            return obj.description
        elif obj.report_card:
            return obj.report_card.description
        else:
            return None


class PersonnelSerializer(serializers.ModelSerializer):
    entity_name = serializers.SerializerMethodField(read_only=True)
    department_name = serializers.SerializerMethodField(read_only=True)
    code_name = serializers.SerializerMethodField()

    class Meta:
        model = Personnel
        fields = '__all__'

    def get_entity_name(self, obj):
        return obj.entity.name if obj.entity else None

    def get_department_name(self, obj):
        if obj.department:
            return obj.department.name
        return None

    def get_code_name(self, obj):
        return obj.code.name if obj.code else None


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class AdditionalIdentitySerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = AdditionalIdentity
        # fields = '__all__'
        exclude = ('_file', )

    def get_file(self, obj):
        return obj.file


class TypeControlSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeControl
        fields = '__all__'


class IdentitySerializerV1(serializers.ModelSerializer):
    control = TypeControlSerializer(many=True, read_only=True)
    file = serializers.SerializerMethodField()

    class Meta:
        model = Identity
        # fields = '__all__'
        exclude = ('_file',)

    def get_file(self, obj):
        return obj.file


class AttachmentSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = ['id', 'name', 'attachments', 'file']

    def get_file(self, obj):
        return obj.ext
