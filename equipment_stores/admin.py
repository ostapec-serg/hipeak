from django.contrib import admin
from django.contrib.admin import ModelAdmin

from equipment_stores.models import EquipmentStores


@admin.register(EquipmentStores)
class EquipmentStoresAdmin(ModelAdmin):
    list_display = ('name', 'url', 'services',)
    list_display_links = ('name', 'url', 'services',)
