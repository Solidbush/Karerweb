from django.contrib import admin

from core.mixins import OwnQuerysetMixin

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Unit)
class UnitAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(OwnQuerysetMixin, admin.ModelAdmin):
    pass
