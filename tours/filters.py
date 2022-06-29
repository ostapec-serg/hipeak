import django_filtersfrom tours.models import Toursclass ToursFilter(django_filters.FilterSet):    CHOICES = (        ('нові', 'Нові'),        ('старі', 'Старі')    )    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Назва туру')    ordering = django_filters.ChoiceFilter(label='Порядок', choices=CHOICES, method='filter_by_order')    start_date = django_filters.DateFilter(field_name='start_date', lookup_expr='gte', label='Старт: (дд.мм.рр)')    finish_date = django_filters.DateFilter(field_name='finish_date', lookup_expr='lte', label='Фініш: (дд.мм.рр)')    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Максимальний бюджет')    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Мінімальний бюджет')    flying = django_filters.BooleanFilter(field_name='flying', label='Переліт')    transfer = django_filters.BooleanFilter(field_name='transfer', label='Трансфер')    class Meta:        model = Tours        fields = (            'organisation',            'food',            'residence',            'category',        )    def filter_by_order(self, queryset, name, value):        expression = '-pub_date' if value == 'нові' else '-pub_date'        return queryset.order_by(expression)