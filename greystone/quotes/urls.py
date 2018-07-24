from django.urls import path

from quotes import views


urlpatterns = [
    path('', views.display_quotes, name='quotes'),
]