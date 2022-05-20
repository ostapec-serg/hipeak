from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, FormView
from django.contrib import messages

from news_blog.forms import CommentsForm
from news_blog.models import News, Likes, Comments


class NewsListView(ListView):
    model = News
    queryset = News.objects.all()
    ordering = '-publication_datetime'
    template_name = 'news_blog/news_main_page.html'
    paginate_by = 5
    extra_context = {'title': 'News blog'}


class NewsDetail(DetailView, FormView):
    model = News
    form_class = CommentsForm
    template_name = 'news_blog/news_page_detail.html'
    context_object_name = 'news_context'

    def get_success_url(self):
        return reverse_lazy('blog post detail', kwargs={'slug': self.get_object().slug})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                messages.error(self.request, 'Форма заповнене не вірно!')
                return self.form_invalid(form)
        else:
            messages.error(self.request, 'Щоб залишати коментарі потрібно авторизуватись')
            return HttpResponseRedirect(reverse('blog post detail', kwargs={'slug': self.get_object().slug}))

    def form_valid(self, form):
        comment = Comments()
        comment.comment_text = self.request.POST['comment_text']
        comment.author = self.request.user
        comment.news_name = self.get_object()
        comment.save()
        messages.success(self.request, 'Коментар додано!')
        return super().form_valid(form)


@login_required(login_url='/login')
def like_post(request):
    if request.method == 'POST':
        news_instance = get_object_or_404(News, id=request.POST['post_id'])
        create_new_like = Likes(news=news_instance, user=request.user)
        exists_like = Likes.objects.filter(user_id=request.user, news=news_instance)
        if exists_like:
            exists_like.delete()
            return HttpResponseRedirect(reverse('blog post detail', args=[(str(news_instance.slug))]))
        else:
            create_new_like.save()
            return HttpResponseRedirect(reverse('blog post detail', args=[(str(news_instance.slug))]))
    else:
        return redirect('blog post detail')
