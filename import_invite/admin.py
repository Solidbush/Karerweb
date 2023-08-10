from adminsortable2.admin import SortableAdminBase
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionMixin
from simple_history.admin import SimpleHistoryAdmin

from core.mixins import OwnQuerysetMixin, ReadOnlyAdminModelMixin

from . import mixins, models, resources, tabulars


@admin.register(models.OrgImport)
class OrgOrderAdmin(mixins.ManualInviteModeMixin,
                    mixins.RecoverInviteModeMixin,
                    OwnQuerysetMixin, ExportActionMixin,
                    SortableAdminBase, admin.ModelAdmin):
    resource_class = resources.OrgInviteResource
    list_display = ['id', 'create_at', 'finish_at']
    exclude = ['finish_at', 'create_at']
    list_filter = ['organization']
    inlines = [tabulars.OrgInviteTabular]
    manual_model = models.OrgImportInvite
    recover_model = models.OrgImportInvite

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj) if not obj else ['karer', 'desc', 'organization']

    def export_admin_action(self, request, queryset):
        queryset = models.OrgImportInvite.objects.filter(order__in=queryset)
        return super(OrgOrderAdmin, self).export_admin_action(request, queryset)

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.update(
            export_admin_action=(
                OrgOrderAdmin.export_admin_action,
                "export_admin_action",
                _("Export selected %(verbose_name_plural)s"),
            )
        )
        return actions


@admin.register(models.OrgImportInvite)
class OrgInviteAdmin(OwnQuerysetMixin, ReadOnlyAdminModelMixin, SimpleHistoryAdmin):
    exclude = ["id", "position"]
    history_list_display = ["status"]
    history_exclude = ('history_reason',)
