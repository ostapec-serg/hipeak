from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, DetailView, FormView

from tours.forms import RatingForm, TourRatingsForm
from tours import models


class MainPageView(TemplateView):
    template_name = 'main/hipeak_start_page.html'
    extra_context = {'title': 'hipeak.portal'}


class DetailViewWithComment(DetailView, FormView):
    comment_model = None  # model where the comment is stored
    rating_form = None
    bookmark_form = None
    in_bookmark = False

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        if request.user.is_authenticated:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            messages.error(self.request, 'Форма заповнене не вірно!')
            return self.form_invalid(form)
        messages.error(self.request, 'Щоб залишати коментарі потрібно авторизуватись')
        return HttpResponseRedirect(reverse('news:detail', kwargs={'slug': self.get_object().slug}))

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        author = self.request.user
        comment_text = self.request.POST['comment_text']
        name = self.get_object()
        comment = self.comment_model(article_name=name, author=author, comment_text=comment_text)
        comment.save()
        messages.success(self.request, 'Коментар додано!')
        return super().form_valid(form)

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return reverse_lazy(self.success_url, kwargs={'slug': self.get_object().slug})

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = super().get_context_data()
        if self.object:
            context[self.context_object_name] = self.object
            if self.rating_form:
                context["rating_form"] = self.rating_form
            if self.bookmark_form:
                context["bookmark_form"] = self.bookmark_form
            if self.in_bookmark:
                user = self.request.user.id
                in_user_bookmark = self.object.in_user_bookmarks(username=user)
                if in_user_bookmark:
                    context["in_bookmark"] = in_user_bookmark
        context.update(kwargs)
        return context


class BaseRatingBookmarkView(DetailView, FormView):
    _article_model = None  # model where the rating or bookmarks is stored
    _article = None  # tour or organisation : str
    _slug = None

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        setting = self.set_settings()
        form = self.get_form()  # OrganisationBookmarkForm or TourBookmarkForm
        if not request.user.is_authenticated:
            messages.error(self.request, 'Щоб поставити оцінку або додати до закладок'
                                         'потрібно авторизуватись')
            return self.form_invalid(form)
        if form.is_valid():
            if setting:
                self.form_valid(form)
                return super().form_valid(form)
        else:
            messages.error(self.request, 'Форма заповнене не вірно!')
            return self.form_invalid(form)

    def set_settings(self):
        if 'organisation' in self.request.POST:
            self.model = models.Organisations
            self._article_model = models.Ratings
            self._article = 'organisation'
            self.success_url = 'tours:organisation_detail'
            self.template_name = 'tours/organisation_page_detail.html'
        elif 'tour' in self.request.POST:
            self.model = models.Tours
            self._article_model = models.TourRatings
            self._article = 'tour'
            self.success_url = 'tours:detail'
            self.template_name = 'tours/tour_detail.html'
        else:
            return False
        article_object = get_object_or_404(self.model,
                                           slug=self.request.POST[self._article])
        self._slug = article_object.slug
        return article_object

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        instance = get_object_or_404(self.model, slug=self._slug)
        article_exist = self.exist_article(instance)
        if article_exist:
            # article_exist.delete()
            messages.success(self.request, 'Ваш голос вже враховано!')
            return article_exist
        save_article = self.article_save(form, instance)
        messages.success(self.request, 'Дякуємо за Вашу оцінку')
        return save_article

    def exist_article(self, tour_instance):
        exists_rating = self._article_model.objects.filter(user_id=self.request.user,
                                                           rate_article=tour_instance)
        return exists_rating

    def article_save(self, form, article_object):
        user = self.request.user
        self._article = article_object
        rating = self.request.POST['rating']
        article_object = self._article_model(rate_article=self._article,
                                             user=user, rating=rating)
        return article_object.save()

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return reverse_lazy(self.success_url, kwargs={'slug': self._slug})
