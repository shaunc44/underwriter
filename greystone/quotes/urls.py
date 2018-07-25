from django.urls import path

from quotes import views


urlpatterns = [
    path('quote/', views.LoanAmountView.as_view(), name='quote'),
]