from django.core.mail import send_mass_mail
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.views.generic.list import ListView

from hipeak_portal.settings import EMAIL_HOST_USER, HIPEAK_EMAIL
from contacts.form import FeedbackCaptchaV2Form
from equipment_stores.models import EquipmentStores
from tours.models import Organisations

import threading


class ContactView(TemplateView):
    """
    Simple class to render main 'contact' page
    """
    template_name = 'contacts/contacts_page.html'
    extra_context = {'title': 'Contacts'}


class AboutView(TemplateView):
    """
    Simple class to render 'about hipeak.portal' page
    """
    template_name = "contacts/about_page.html"
    extra_context = {'title': 'About page'}


class OrganisationContactView(ListView):
    """
    Render main contact page with contacts list
    of all organisations
    """
    model = Organisations
    queryset = model.objects.all()
    paginate_by = 1
    template_name = 'contacts/contacts_page.html'
    extra_context = {'title': 'Contacts'}


class EquipmentStoresContactView(ListView):
    """
    Render main contact page with contacts list
    of all equipment stores
    """
    model = EquipmentStores
    queryset = model.objects.all()
    paginate_by = 2
    template_name = 'contacts/contacts_page.html'
    extra_context = {'title': 'Contacts'}


class FeedbackView(TemplateView, FormView):
    """
    Render feedback page. Processes the feedback form
    and sends the letter in a separate thread.
    """
    form_class = FeedbackCaptchaV2Form
    template_name = 'contacts/feedback_page.html'
    success_url = 'contacts:feedback'
    extra_context = {'title': 'Feedback'}

    def form_valid(self, form):
        """If the form is valid, create and start thread for sending email
         and redirect to the supplied URL.
         """
        # create thread for sending email
        thr = threading.Thread(
            target=self.send_feedback_thread,
            args=(form,),
            name='send_feedback'
        )
        # start thread
        thr.start()
        messages.success(self.request, 'Лист відправлено!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, 'Не вірно заповнені поля!')
        return super().form_invalid(form)

    @staticmethod
    def send_feedback_thread(form):
        """Sending email in thread"""
        massage_content = \
            f"Імʼя - {form.cleaned_data['name']}\n" \
            f"Email для відповіді - {form.cleaned_data['email']}\n" \
            f"Тема - {form.cleaned_data['subject']}\n" \
            f"Текст\n" \
            f"{form.cleaned_data['content']}"

        if form.cleaned_data['send_me_copy']:
            mail = (form.cleaned_data['subject'], massage_content, EMAIL_HOST_USER,
                    [HIPEAK_EMAIL, form.cleaned_data['email']])
        else:
            mail = (form.cleaned_data['subject'], massage_content,
                    EMAIL_HOST_USER, [HIPEAK_EMAIL])
        send_mass_mail((mail,), fail_silently=True)

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            return super().get_success_url()
        return reverse_lazy(self.success_url)
