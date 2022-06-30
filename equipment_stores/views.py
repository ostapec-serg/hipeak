from rest_framework import generics, mixins
from rest_framework.viewsets import GenericViewSet
from main.permissions import IsSuperUserOrReadOnly

from django.views.generic import ListView, DetailView

from equipment_stores.models import EquipmentStores
from equipment_stores.serializers import EquipmentStoresSerializer


class EquipmentStoresView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          GenericViewSet
                          ):
    queryset = EquipmentStores.objects.all()
    serializer_class = EquipmentStoresSerializer
    permission_classes = (IsSuperUserOrReadOnly,)


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

