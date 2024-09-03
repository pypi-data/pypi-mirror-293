from after_effects.views import AfterEffectRunViewset
from core.routers import CustomAPIRouter
from django.urls import include, path

app_name = "after_effects"

router = CustomAPIRouter()
router.register_in_bulk(
    prefix="after_effects",
    viewsets=[AfterEffectRunViewset],
)


urlpatterns = [
    path("", include(router.urls)),
]
