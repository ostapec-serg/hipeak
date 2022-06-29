from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from my_profile import views
from registration_authorisation.views import Registration, Authorisation, EmailRegisterView

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('news-blog/', include('news_blog.urls')),
    path('equipments/', include('equipment_stores.urls')),
    path('tours/', include('tours.urls')),
    path('contacts/', include('contacts.urls')),
    path('my-profile/', include('my_profile.urls')),
    path('google-oauth/', include('social_django.urls', namespace='social')),
    path('search/', include('search.urls')),
    path('login/', Authorisation.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('registration/', Registration.as_view(), name='registration'),
    path('registration/confirm/<slug>/', EmailRegisterView.as_view(), name='registration_confirm'),
    path('password_change/', views.ChangingUserPasswordView.as_view(), name='password_change'),
    path('reset_password_sent/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
