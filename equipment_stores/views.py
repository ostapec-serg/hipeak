from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from equipment_stores.models import EquipmentStores


class EquipmentStoresListView(ListView):
    model = EquipmentStores
    queryset = EquipmentStores.objects.all()
    ordering = '-name'
    template_name = 'equipment_stores/stores.html'
    paginate_by = 5
    extra_context = {'title': 'Equipments'}


class StoreDetail(DetailView):
    model = EquipmentStores
    template_name = 'equipment_stores/store_detail.html'
    context_object_name = 'store_context'

    def get_success_url(self):
        return reverse_lazy('organisation_detail', kwargs={'slug': self.get_object().slug})


# @login_required(login_url='/login')
# def add_bookmarks(request, post_id):
#     if request.method == 'POST':
#         news_instance = News.objects.get(pk=post_id)
#         create_relate = Bookmarks(news=news_instance, user=request.user)
#         create_relate.save()
#         return HttpResponseRedirect(reverse('blog post detail', args=[str(post_id)]))
#

# @login_required(login_url='/login')
# def choose_rating(request, post_id):
#     if request.method == 'POST':
#         news_instance = News.objects.get(pk=post_id)
#         create_relate = Ratings(news=news_instance, user=request.user, rating=request.POST['news_post_id'])
#         create_relate.save()
#         return HttpResponseRedirect(reverse('blog post detail', args=[str(post_id)]))
