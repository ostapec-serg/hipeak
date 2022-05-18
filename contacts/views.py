from django.shortcuts import render, redirect
from django.core.mail import send_mass_mail
from django.contrib import messages

from contacts.form import FeedbackCaptchaV2Form


def send_feedback(request):
    if request.method == "POST":
        form = FeedbackCaptchaV2Form(request.POST)
        if form.is_valid():
            massage_content = f"Імʼя - {form.cleaned_data['name']}\n"\
                               f"Email для відповіді - {form.cleaned_data['email']}\n"\
                               f"Тема - {form.cleaned_data['subject']}\n"\
                               f"Текст\n"\
                               f"{form.cleaned_data['content']}"
            if form.cleaned_data['send_me_copy']:
                mail = (form.cleaned_data['subject'], massage_content, 'hipeak@ukr.net',
                        ['hipeak.portal@gmail.com', form.cleaned_data['email']])
                send_massage_result = send_mass_mail((mail,), fail_silently=True)
            else:
                mail = (form.cleaned_data['subject'], massage_content,
                        'hipeak@ukr.net', ['hipeak.portal@gmail.com'])
                send_massage_result = send_mass_mail((mail,), fail_silently=True)
            if send_massage_result:
                messages.success(request, 'Лист відправлено!')
                return redirect('feedback_page')
            else:
                messages.error(request, "Ой... Щось пішло не так! Помилка віправки! Спробуйте ще!")
        else:
            messages.error(request, 'Не вірно заповнені поля!')
    else:
        form = FeedbackCaptchaV2Form
        return render(request, 'contacts/feedback_page.html', {'form': form})


def contacts_page(request):
    return render(request, "contacts/contacts_page.html",
                  {'title': 'Contact_page', 'all_news': 'all_stores'})


def about_page(request):
    return render(request, "contacts/about_page.html",
                  {'title': 'About_page', 'all_news': 'about_page'})
