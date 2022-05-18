from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from news_blog.forms import CommentsForm
from tours.models import Organisations


class OrganisationsView(ListView):
    model = Organisations
    queryset = Organisations.objects.select_related().all()
    ordering = 'date_added'
    template_name = 'tours/tours_page.html'
    paginate_by = 3
    extra_context = {'title': 'Tours'}


class ToursView(ListView):
    queryset = Organisations.objects.select_related().all()
    ordering = 'date_added'
    template_name = 'tours/tours_page.html'
    paginate_by = 3
    extra_context = {'title': 'Tours'}


class OrganisationsDetail(DetailView):
    model = Organisations
    form_class = CommentsForm
    template_name = 'tours/organisation_page_detail.html'
    context_object_name = 'organisation_context'

    def get_success_url(self):
        return reverse_lazy('organisation_detail', kwargs={'slug': self.get_object().slug})


def tour_detail(request):
    pass
