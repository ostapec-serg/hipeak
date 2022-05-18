from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = 'main/hipeak_start_page.html'
    extra_context = {'title': 'hipeak.portal'}
