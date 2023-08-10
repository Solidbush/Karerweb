from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import forms, models, views

admin.site.site_title = 'Объект'
admin.site.site_header = 'Объект'
admin.site.index_title = 'Главная'
admin.site.get_urls = lambda: [
                                  path("accept-pvc/", views.accept_pvc, name='accept_pvc'),
                                  path("register/", views.register, name='accept_pvc'),
                              ] + admin.AdminSite.get_urls(admin.site)


@admin.register(models.Karer)
class KarerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['number', 'model', 'vin_number']


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone']


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['inn', 'name']
    list_display_links = ['name']

    def get_readonly_fields(self, request, obj=None):
        return ['name', 'address', 'ogrn', 'kpp'] if obj else []

    def get_form(self, request, obj=None, change=False, **kwargs):
        if not obj:
            return forms.OrganizationCreateForm
        return super().get_form(request, obj, change, **kwargs)


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(models.User)
class UserAdmin(_UserAdmin):
    readonly_fields = ['last_login', 'date_joined']
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "karer",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    ordering = ["email"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
