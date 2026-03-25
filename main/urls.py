from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('', views.home, name='home'),
    path('form/', views.form_view, name='form'),
]
