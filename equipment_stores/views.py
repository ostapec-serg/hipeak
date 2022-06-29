from rest_framework import generics

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from equipment_stores.models import EquipmentStores
from equipment_stores.serializers import EquipmentStoresSerializer


class EquipmentStoresView(generics.ListAPIView):
    queryset = EquipmentStores.objects.all()
    serializer_class = EquipmentStoresSerializer


class EquipmentStoresListView(ListView):
    model = EquipmentStores
    queryset = EquipmentStores.objects.all()
    ordering = '-name'
    template_name = 'equipment_stores/stores.html'
    paginate_by = 2
    extra_context = {'title': 'Equipments Stores'}


class StoreDetail(DetailView):
    model = EquipmentStores
    template_name = 'equipment_stores/store_detail.html'
    context_object_name = 'store_context'
    extra_context = {'title': 'Store Details'}

