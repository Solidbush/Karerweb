from adminsortable2.admin import SortableStackedInline
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import ClientInvite, OrgInvite


class OrgInviteTabular(SortableStackedInline):
    model = OrgInvite
    sortable_field_name = 'position'
    extra = 0
    exclude = ['finish_at']
    readonly_fields = ['status', 'open_link', 'manual_mode', "recover"]

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    @admin.display(description='Подробно')
    def open_link(self, obj: OrgInvite):
        url = f"""{reverse(
            f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change',
            kwargs={'object_id': obj.id}
        )}"""
        return format_html(f"<a href='{url}'>Открыт</a>")

    @admin.display(description='Ручной режим')
    def manual_mode(self, obj: OrgInvite):
        url = f"""{reverse(
            f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_manual-mode',
            kwargs={'object_id': obj.order.id, 'invite_id': obj.id}
        )}"""
        return format_html(f"<a href='{url}'>Перейти в ручной режим</a>")

    @admin.display(description='Восстановить заявку')
    def recover(self, obj: OrgInvite):
        url = f"""{reverse(
            f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_recover',
            kwargs={'object_id': obj.order.id, 'invite_id': obj.id}
        )}"""
        return format_html(f"<a href='{url}'>Восстановить</a>")


class ClientInviteTabular(SortableStackedInline):
    model = ClientInvite
    sortable_field_name = 'position'
    extra = 0
    exclude = ['finish_at']
    readonly_fields = ['status', 'open_link']

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    @admin.display(description='Подробно')
    def open_link(self, obj: OrgInvite):
        url = f"""{reverse(
            f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change',
            kwargs={'object_id': obj.id}
        )}"""
        return format_html(f"<a href='{url}'>Открыт</a>")

    @admin.display(description='Ручной режим')
    def manual_mode(self, obj: OrgInvite):
        url = f"""{reverse(
            f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_manual-mode',
            kwargs={'object_id': obj.order.id, 'invite_id': obj.id}
        )}"""
        return format_html(f"<a href='{url}'>Перейти в ручной режим</a>")

    @admin.display(description='Восстановить заявку')
    def recover(self, obj: OrgInvite):
        url = f"""{reverse(
            f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_recover',
            kwargs={'object_id': obj.order.id, 'invite_id': obj.id}
        )}"""
        return format_html(f"<a href='{url}'>Восстановить</a>")
