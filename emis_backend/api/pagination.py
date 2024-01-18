from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class StandardResultsSetPagination(LimitOffsetPagination):
    default_limit = 150


class EquipmentPagination(LimitOffsetPagination):
    default_limit = 150


class ControlPagination(LimitOffsetPagination):
    default_limit = 150


class PersonnelPagination(LimitOffsetPagination):
    default_limit = None

