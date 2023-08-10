from django.contrib import messages
from django.contrib.admin.utils import flatten_fieldsets
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import path, reverse


class OwnQuerysetMixin:
    def get_exclude(self, request, obj):
        exclude = super().get_exclude(request, obj) or []
        if hasattr(self.model, 'user'):
            return [*exclude, "user"]
        if request.user.is_superuser:
            return exclude
        if hasattr(self.model, 'karer'):
            return [*exclude, 'karer']
        return exclude

    def save_model(self, request, obj, form, change) -> None:
        if request.user.is_superuser:
            return super().save_model(request, obj, form, change)
        if request.user.karer:
            obj.karer = request.user.karer
        if hasattr(obj, "user"):
            obj.user = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(qs.model, 'karer') and request.user.karer:
            return qs.filter(karer=request.user.karer)
        if hasattr(qs.model, 'user'):
            return qs.filter(user=request.user)
        return qs


class ReadOnlyAdminModelMixin:

    def has_add_permission(self, request, *args, **kwargs) -> bool:
        return False

    def has_delete_permission(self, request, obj=None, *args, **kwargs) -> bool:
        return False

    def get_readonly_fields(self, request, obj=None):
        if getattr(self, "declared_fieldsets", None):
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))


class RecoverModeMixin:
    recover_model = None

    def get_urls(self):
        my_urls = [
            path('<path:object_id>/change/<path:invite_id>/recover/',
                 self.invite_recover,
                 name='%s_%s_recover' % self.get_recover_model_info()),
        ]
        return my_urls + super().get_urls()

    def get_recover_model_info(self):
        app_label = self.recover_model._meta.app_label
        return app_label, self.recover_model._meta.model_name

    def invite_recover(self, request, object_id, invite_id):
        try:
            invite = get_object_or_404(self.recover_model, id=invite_id)
            if invite.status not in ["finished", "canceled"]:
                raise ValueError(f'Заявку со статусом "{dict(invite.STATUS)[invite.status]}" нелзя восстановить')
            self.perform_invite_recover(invite)
            messages.add_message(request, messages.constants.SUCCESS, "Заявка восстановлено")
        except Exception as _exp:
            messages.add_message(request, messages.constants.ERROR, str(_exp))
        url = reverse("admin:%s_%s_change" % self.get_model_info(), kwargs={"object_id": object_id})
        return HttpResponseRedirect(url)

    def perform_invite_recover(self, invite):
        invite.status = 'waiting_pay'
        invite.save()
        print(invite)


class ManualModeMixin:
    manual_model = None

    def get_urls(self):
        my_urls = [
            path('<path:object_id>/change/<path:invite_id>/manual-mode/',
                 self.invite_manual_mode,
                 name='%s_%s_manual-mode' % self.get_manual_model_info()),
        ]
        return my_urls + super().get_urls()

    def get_manual_model_info(self):
        app_label = self.manual_model._meta.app_label
        return app_label, self.manual_model._meta.model_name

    def invite_manual_mode(self, request, object_id, invite_id):
        try:
            invite = self.manual_model.objects.get(id=invite_id)
            self.perform_invite_manual(invite)
            messages.add_message(request, messages.constants.INFO, "Заявка перешла на ручной режим")
        except Exception as _exp:
            messages.add_message(request, messages.constants.ERROR, str(_exp))
        url = reverse("admin:%s_%s_change" % self.get_model_info(), kwargs={"object_id": object_id})
        return HttpResponseRedirect(url)

    def perform_invite_manual(self, invite):
        pass
