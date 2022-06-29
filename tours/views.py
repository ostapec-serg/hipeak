<<<<<<< HEAD
from rest_framework import generics

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView
=======
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, FormView
from django.contrib import messages


from news_blog.forms import CommentsForm
from tours.models import Organisations, Ratings
>>>>>>> 21a625e0fd39a6ed230266947b4b916e3dec324c

from tours import forms
from tours import models
from main import views
from tours.filters import ToursFilter
from tours.models import Tours
from tours.serializers import ToursSerializer


class ToursAPIView(generics.ListAPIView):
    queryset = models.Tours.objects.all()
    serializer_class = ToursSerializer


class ToursFilteredView(ListView):
    """
    Render some list of objects, set by `self.model` or `self.queryset`.
    `self.queryset` is filtered by 'filter_class'. If filters not used,
    rendering all objects in model set by `self.model`
    """
    model = models.Tours
    filter_class = ToursFilter
    queryset = models.Tours.objects.order_by('-pub_date')
    ordering = '-pub_date'
    paginate_by = 7
    template_name = 'tours/tours_main_page.html'
    extra_context = {'title': 'Tours'}
    context_object_name = 'tours_context'

    def get_context_data(self, **kwargs):
        filtered_data = self.filter_class(self.request.GET, self.queryset)
        self.queryset = filtered_data.qs
        context = super(ToursFilteredView, self).get_context_data(
            object_list=self.queryset, **kwargs
        )
        context['filter'] = filtered_data
        return context


# check
class OrganisationsView(ListView):
    """
    Render all Organisations objects, set by `self.model` or `self.queryset`.
    """
    model = models.Organisations
    queryset = models.Organisations.objects.all()
    ordering = '-pub_date'
    template_name = 'tours/tours_page.html'
    paginate_by = 3
    extra_context = {'title': 'Organisation'}


class TourDetail(views.DetailViewWithComment):
    """
    Render a "detail" view of Tour objects.
    Render form.class, rating_form, bookmark_form
    """
    comment_model = models.TourComments
    model = models.Tours
    form_class = forms.TourCommentsForm
    template_name = 'tours/tour_detail.html'
    context_object_name = 'tour_context'
    success_url = 'tours:detail'
    rating_form = forms.TourRatingsForm
    bookmark_form = forms.TourBookmarkForm
    in_bookmark = True
    extra_context = {'title': 'Tours Detail'}


class OrganisationsDetail(views.DetailViewWithComment):
    """
    Render a "detail" view of Organisations objects.
    Render form.class, rating_form, bookmark_form
    """
    comment_model = models.OrganisationsComment
    model = models.Organisations
    form_class = forms.OrganisationCommentsForm
    template_name = 'tours/organisation_page_detail.html'
    context_object_name = 'organisation_context'
    success_url = 'tours:organisation_detail'
    rating_form = forms.RatingForm
    bookmark_form = forms.OrganisationBookmarkForm
    in_bookmark = True
    extra_context = {'title': 'Organisation Detail'}


class AddTourView(CreateView):
    template_name = 'tours/add_tour.html'
    form_class = forms.AddTourForm
    queryset = models.Tours.objects.all()
    success_url = '/tours'


class EditTourView(UpdateView):
    template_name = 'tours/edit_tour.html'
    form_class = forms.EditTourForm
    queryset = models.Tours.objects.all()
    success_url = '/tours'


class OrganisationTourView(views.DetailViewWithComment):
    model = models.Organisations
    extra_context = {'title': 'Organisation Tours'}
    form_class = forms.OrganisationCommentsForm
    template_name = 'tours/organisation_page_detail.html'
    context_object_name = 'organisation_context'
    success_url = 'tours:organisation_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['organisation_tours'] = Tours.objects.filter(organisation__slug=self.object.slug)
        return context


class RatingView(views.BaseRatingBookmarkView):
    form_class = forms.RatingForm


class BookmarkView(views.BaseRatingBookmarkView):
    # article_name_1 = 'organisation'
    # article_name_2 = 'tour'

    def get(self, request, *args, **kwargs):
        setting_instance = self.set_settings()
        exist_bookmark = self.exist_article(setting_instance)
        if exist_bookmark:
            exist_bookmark.delete()
            messages.success(request, 'Видалено!')
            return HttpResponseRedirect(reverse(self.success_url,
                                                kwargs={'slug': self._slug}))
        else:
            self.bookmark_save(setting_instance)
        messages.success(request, 'Додано')
        return HttpResponseRedirect(reverse(self.success_url,
                                            kwargs={'slug': self._slug}))

    def set_settings(self):
        if 'organisation' in self.request.GET:
            self.model = models.Organisations
            self._article = self.request.GET.get('organisation', '')
            self.success_url = 'tours:organisation_detail'
            self.template_name = 'tours/organisation_page_detail.html'
            self._article_model = models.Bookmarks
        elif 'tour' in self.request.GET:
            self.model = models.Tours
            self._article = self.request.GET.get('tour', '')
            self.success_url = 'tours:detail'
            self.template_name = 'tours/tour_detail.html'
            self._article_model = models.TourBookmarks
        else:
            return False
        article_object = get_object_or_404(self.model, slug=self._article)
        self._slug = article_object.slug
        return article_object

    def exist_article(self, instance):
        if 'organisation' in self.request.GET:
            exists_rating = self._article_model.objects.filter(user_id=self.request.user,
                                                               organisation=instance)
        else:
            exists_rating = self._article_model.objects.filter(user_id=self.request.user,
                                                               tour=instance)
        return exists_rating

<<<<<<< HEAD
    def bookmark_save(self, article_object):
        user = self.request.user
        self._article = article_object
        if 'tour' in self.request.GET:
            article_object = self._article_model(tour=self._article, user=user)
        else:
            article_object = self._article_model(organisation=self._article, user=user)
        return article_object.save()
=======
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
>>>>>>> 21a625e0fd39a6ed230266947b4b916e3dec324c
