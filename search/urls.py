from django.urls import path, includefrom search.views import *# SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]urlpatterns = [    path('', search_view, name='search'),    # path('', MySearchView.as_view(), name='search'),]