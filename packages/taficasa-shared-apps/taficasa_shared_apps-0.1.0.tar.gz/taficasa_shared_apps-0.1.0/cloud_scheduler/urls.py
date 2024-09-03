from cloud_scheduler.views import CronJobStatusViewset
from core.routers import CustomAPIRouter
from django.urls import include, path

app_name = "cloud_scheduler"

router = CustomAPIRouter()
router.register(prefix="", viewset=CronJobStatusViewset)

urlpatterns = [
    path("", include(router.urls)),
]
