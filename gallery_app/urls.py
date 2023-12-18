from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import *
from django.contrib import admin

urlpatterns = [
    path('gallery', PostListView.as_view(), name='posts'),
    path('gallery/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('gallery/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('gallery/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)