from django.urls import path, includefrom news_blog.views import *from rest_framework import routersrouter = routers.DefaultRouter()router.register('news', NewsAPIView)app_name = 'news'urlpatterns = [    path('', NewsListView.as_view(), name='main_page'),    path('<str:slug>', NewsDetail.as_view(), name='detail'),    path('like/<str:slug>', like_post, name='like'),    path('add/', AddNewsView.as_view(), name='add_post'),    path('edit/<str:slug>', EditNewsView.as_view(), name='edit_post'),    path('api/v1/', include(router.urls)),]