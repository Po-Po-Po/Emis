from django.urls import path, include
from api.routers import router
from .views import (
    ControlViewSet,
    EquipmentTypeViewSet,
    EquipmentStatusViewSet,
    PersonnelStatusViewSet,
    SectionViewSet,
    HistoryTypeViewSet,
    EntityNTDViewSet,
    EntityRDViewSet,
    DirectorateViewSet,
    CardTableViewSet,
    FundViewSet
)
from modules.profiles.api import ProfileViewSet
from utils.personnel_generate_xlsx import personnel_excel

urlpatterns = [
    path('v1/history_table/', CardTableViewSet.as_view()),
    path('v1/fund/', FundViewSet.as_view()),
    path('v1/control/', ControlViewSet.as_view()),
    path('v1/section/', SectionViewSet.as_view()),
    path('v1/equipment_type/', EquipmentTypeViewSet.as_view()),
    path('v1/equipment_status/', EquipmentStatusViewSet.as_view()),
    path('v1/personnel_status/', PersonnelStatusViewSet.as_view()),
    path('v1/personnel_print/', personnel_excel),
    path('v1/history_type/', HistoryTypeViewSet.as_view()),
    path('v1/entity_ntd/', EntityNTDViewSet.as_view()),
    path('v1/entity_rd/', EntityRDViewSet.as_view()),
    path('v1/directorate/', DirectorateViewSet.as_view()),
    path('v1/profile/', ProfileViewSet.as_view(), name='profile'),
    path('v1/', include(router.urls)),
]
