from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mass_mail
from rest_framework.viewsets import GenericViewSet

from hipeak_portal.local_settings import EMAIL_HOST_USER
from my_profile.models import Profile
from news_blog.forms import CommentsForm, AddNewsForm, EditNewsForm
from news_blog.models import News, Likes, Comments
from main.views import DetailViewWithComment
from news_blog.serializers import NewsSerializer

from rest_framework import mixins
from main.permissions import IsSuperUserOrReadOnly


class NewsAPIView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  GenericViewSet
                  ):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (IsSuperUserOrReadOnly, )


class NewsListView(ListView):
    """Render main news page."""
    model = News
    queryset = News.objects.all()
    ordering = '-pub_date'
    template_name = 'news_blog/news_main_page.html'
    paginate_by = 5
    extra_context = {'title': 'News'}


class NewsDetail(DetailViewWithComment):
    """Render detail news page."""
    comment_model = Comments
    model = News
    form_class = CommentsForm
    template_name = 'news_blog/news_page_detail.html'
    context_object_name = 'news_context'
    success_url = 'news:detail'
    extra_context = {'title': 'News Detail'}


class AddNewsView(CreateView):
    """Render 'add news page' with AddNews Form."""
    form_class = AddNewsForm
    template_name = 'news_blog/add_news.html'
    success_url = 'news:main_page'

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        if self.request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return redirect('main')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if self.request.user.is_superuser:
            if form.is_valid():
                return self.form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return reverse_lazy(self.success_url)


class EditNewsView(UpdateView):
    """Render 'edit news page' with EditNews Form."""
    template_name = 'news_blog/edit_news.html'
    form_class = EditNewsForm
    queryset = News.objects.all()
    success_url = 'news:main_page'

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        if self.request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return redirect('login')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if self.request.user.is_superuser:
            if form.is_valid():
                return self.form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return reverse_lazy(self.success_url)


@login_required(login_url='/login')
def like_post(request, slug):
    """add like to news"""
    if request.method == 'POST':
        news_instance = get_object_or_404(News, slug=slug)
        exists_like = Likes.objects.filter(user_id=request.user, news=news_instance)
        if exists_like:
            exists_like.delete()
            return redirect(news_instance.get_absolute_url())
        create_new_like = Likes(news=news_instance, user=request.user)
        create_new_like.save()
        return redirect(news_instance.get_absolute_url())
    return redirect('news:main_page')


def email_mailing(news_instance):
    """
    Email distribution to users who have
    subscribed to the newsletter
    """
    users = Profile.objects.select_related('user').filter(email_subscribe=True)
    users_emails = users.values_list('user__email', flat=True)
    #  re-write host url
    host_url = 'https://hipeak-portal.herokuapp.com'
    message = f"{news_instance.name}\n" \
              f"{news_instance.description}"\
              f"{host_url}{news_instance.get_absolute_url()}"
    mail = ('Нова стаття', message, EMAIL_HOST_USER, users_emails)
    send_mass_mail((mail,), fail_silently=True)
