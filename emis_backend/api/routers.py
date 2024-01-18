from rest_framework.routers import SimpleRouter

from .views import (
    HistoryViewSet,
    EquipmentViewSet,
    PersonnelViewSet,
    EntityViewSet,
    ReportCardViewSet,
    StatusCardViewSet,
    HistoryTabelViewSet,
    CodeViewSet,
    DepartmentViewSet,
    AdditionalIdentityV1ViewSet,
    TypeControlViewSet,
    IdentityViewSetV1,
    AttachmentViewSet
)
from modules.profiles.api import UserViewSet

router = SimpleRouter()
router.register(r'entity', EntityViewSet)
router.register(r'report_card', ReportCardViewSet)
router.register(r'status_card', StatusCardViewSet)
router.register(r'identity', IdentityViewSetV1)
router.register(r'additional_identity', AdditionalIdentityV1ViewSet)
router.register(r'history', HistoryViewSet)
router.register(r'history_tabel', HistoryTabelViewSet)
router.register(r'code', CodeViewSet)
router.register(r'personnel', PersonnelViewSet)
router.register(r'equipment', EquipmentViewSet)
router.register(r'attachment', AttachmentViewSet)
router.register(r'department', DepartmentViewSet)
router.register(r'users', UserViewSet)
router.register(r'type_control', TypeControlViewSet)
