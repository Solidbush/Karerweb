from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HistoryView

router = DefaultRouter()
router.register("history", HistoryView, "")

urlpatterns = [
    path("", include(router.urls))
]
