from netbox.api.routers import NetBoxRouter

from netbox_dns.api.views import (
    NetBoxDNSRootView,
    ViewViewSet,
    ZoneViewSet,
    NameServerViewSet,
    RecordViewSet,
    RegistrarViewSet,
    ContactViewSet,
    ZoneTemplateViewSet,
    RecordTemplateViewSet,
)

router = NetBoxRouter()
router.APIRootView = NetBoxDNSRootView

router.register("views", ViewViewSet)
router.register("zones", ZoneViewSet)
router.register("nameservers", NameServerViewSet)
router.register("records", RecordViewSet)
router.register("registrars", RegistrarViewSet)
router.register("contacts", ContactViewSet)
router.register("zonetemplates", ZoneTemplateViewSet)
router.register("recordtemplates", RecordTemplateViewSet)

urlpatterns = router.urls
