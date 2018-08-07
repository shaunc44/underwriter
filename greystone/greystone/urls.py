"""greystone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.urls import include

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from quotes import views


router = routers.DefaultRouter()
router.register(r'addresses', views.AddressesViewSet)
router.register(r'rent', views.RentViewSet)
router.register(r'expense', views.ExpenseViewSet)
router.register(r'caprate', views.CapRateViewSet)
# router.register(r'result', views.ResultViewSet))


urlpatterns = [
    # path('', 
    #     include('quotes.urls')
    # ),
    path('admin/', 
        admin.site.urls),
    path('', 
        include(router.urls)
    ),
    path('api-auth/', 
        include('rest_framework.urls')
    ),
    path(
        'address-list/', 
        views.AddressListView.as_view(),
        name='address_list'
    ),
    re_path(
        r'^address/(?P<pk>[0-9]+)/$', 
        views.AddressDetailView.as_view(),
        name='address_detail'
    ),
    path(
        'address-create/', 
        views.AddressCreateView.as_view(),
        name='address_create'
    ),
    path(
        'expense-create/<int:pk>/', 
        views.ExpenseCreateView.as_view(),
        name='expense_create'
    ),
    path(
        'cap-rate-create/<int:pk>/', 
        views.CapRateCreateView.as_view(),
        name='cap_rate_create'
    ),
    # re_path(
    #     r'rent-create/(?P<pk>[0-9]+)/$', 
    #     views.RentCreateView.as_view(),
    #     name='rent_create'
    # ),
    path(
        'rent-create/<int:pk>/', 
        views.RentCreateView.as_view(),
        name='rent_create'
    ),
    # path(
    #     'result/', 
    #     views.ResultDetailView.as_view(),
    #     name='result_detail'
    # ),
    path(
        'result-list/', 
        views.ResultListView.as_view(),
        name='result_list'
    ),
    path(
        'result/<int:pk>/', 
        views.ResultDetailView.as_view(),
        name='result_detail'
    ),
    # re_path(
    #     r'^result/(?P<pk>[0-9]+)/$', 
    #     views.ResultDetailView.as_view(),
    #     name='result_detail'
    # ),
    # path(
    #     'results/', 
    #     views.ResultListView.as_view(),
    #     name='results-list',
    # ),
    # re_path(
    #     r'^results/(?P<pk>[0-9]+)/$', 
    #     views.ResultDetail.as_view()
    # ),
]

# urlpatterns = format_suffix_patterns(urlpatterns)



