from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, FormView
from django.contrib import messages


from news_blog.forms import CommentsForm
from tours.models import Organisations, Ratings


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


@login_required(login_url='/login')
def organisation_rating(request):
    if request.method == 'POST':
        if 1 <= int(request.POST['rating']) <= 5:
            organisation_instance = get_object_or_404(Organisations, slug=request.POST['organisation'])
            exists_rating = Ratings.objects.filter(user_id=request.user, organisation=organisation_instance,)
            if exists_rating:
                exists_rating.delete()
                messages.success(request, 'Ваш голос вже враховано!')
                return HttpResponseRedirect(reverse('organisation_detail', args=[(str(organisation_instance.slug))]))
            else:
                create_rating_instance = Ratings(organisation=organisation_instance,
                                                 user=request.user, rating=request.POST['rating'])
                create_rating_instance.save()
                messages.success(request, 'Дякуємо за Вашу оцінку')
                return HttpResponseRedirect(reverse('organisation_detail', args=[(str(organisation_instance.slug))]))
        else:
            messages.error(request, 'Невірна оцінка. Спробуйте ще!  Оцінка повинна бути від 1 до 5')
            return HttpResponseRedirect(reverse('organisation_detail', kwargs={'slug': request.POST['organisation']}))
    else:
        messages.error(request, 'Невірний запит. Спробуйте ще!')
        return HttpResponseRedirect(reverse('organisation_detail', kwargs={'slug': request.POST['organisation']}))
