from django.contrib import admin

from core.mixins import ReadOnlyAdminModelMixin

from .models import History


@admin.register(History)
class HistoryAdmin(ReadOnlyAdminModelMixin, admin.ModelAdmin):
    list_display = ["car", "date", "type", "mode"]
