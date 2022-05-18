from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from registration_authorisation.views import Registration, Authorisation

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('news-blog/', include('news_blog.urls')),
    path('equipments/', include('equipment_stores.urls')),
    path('tours/', include('tours.urls')),
    path('login/', Authorisation.as_view(), name='authorisation_page'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('registration/', Registration.as_view(), name='registration_page'),
    path('contacts/', include('contacts.urls')),
    path('my-profile/', include('my_profile.urls')),
    path('google-oauth/', include('social_django.urls', namespace='social')),
    path('search/', include('search.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
