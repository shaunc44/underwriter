from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import (
    ListView, DetailView, CreateView, 
    DeleteView, UpdateView, TemplateView
)
from django.urls.base import reverse_lazy
from django.db.models.query import QuerySet
from django.db import IntegrityError

from django import forms

from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.decorators import (
    api_view, list_route, detail_route
)
from rest_framework.reverse import reverse

from quotes.serializers import (
    AddressSerializer, RentSerializer,
    ExpenseSerializer, CapRateSerializer, ResultSerializer
)
from quotes.models import (
    Address, Rent, Expense, CapRate, Result
)


class AddressesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Addresses to be viewed or edited.
    """
    queryset = Address.objects.all().order_by('street')
    serializer_class = AddressSerializer


class AddressListView(ListView):
    model = Address
    queryset = Address.objects.all().order_by('street')
    template_name = 'quotes/address_list.html'


class AddressDetailView(DetailView):
    model = Address
    template_name = 'quotes/address_detail.html'


class AddressCreateView(CreateView):
    model = Address
    template_name = 'quotes/address_create_form.html'
    fields = [
        'street', 
        'city', 
        'state', 
        'zip_code'
    ]

    def get_success_url(self):
        success_url = reverse_lazy(
            'expense_create', 
            kwargs={'pk': self.object.pk}
        )
        return success_url


class AddressUpdateView(UpdateView):
    model = Address
    template_name = 'quotes/address_update_form.html'
    fields = [
        'street', 
        'city', 
        'state', 
        'zip_code'
    ]

    def get_success_url(self):
        success_url = reverse_lazy(
            'expense_update', 
            kwargs={'pk': self.object.pk}
        )
        return success_url


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Expenses to be viewed or edited.
    """
    queryset = Expense.objects.all().order_by('address')
    serializer_class = ExpenseSerializer


class ExpenseCreateView(CreateView):
    model = Expense
    template_name = 'quotes/expense_create_form.html'
    fields = [
        'marketing', 
        'taxes', 
        'insurance',
        'repairs',
        'administration',
    ]

    def get_success_url(self):
        success_url = reverse_lazy(
            'cap_rate_create', 
            kwargs={'pk': self.object.address.id}
        )
        return success_url

    def form_valid(self, form):
        form.instance.address_id = self.kwargs['pk']
        return super(ExpenseCreateView, self).form_valid(form)


class ExpenseUpdateView(UpdateView):
    model = Expense
    template_name = 'quotes/expense_update_form.html'
    fields = [
        'marketing', 
        'taxes', 
        'insurance',
        'repairs',
        'administration',
    ]

    def get_success_url(self):
        success_url = reverse_lazy(
            'cap_rate_update', 
            kwargs={'pk': self.object.address.id}
        )
        obj, created = Result.objects.update_or_create(
            address_id=self.object.address.id
        )
        return success_url

    def form_valid(self, form):
        form.instance.address_id = self.kwargs['pk']
        return super(ExpenseUpdateView, self).form_valid(form)


class CapRateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CapRates to be viewed or edited.
    """
    queryset = CapRate.objects.all().order_by('address')
    serializer_class = CapRateSerializer


class CapRateCreateView(CreateView):
    model = CapRate
    template_name = 'quotes/caprate_create_form.html'
    fields = ['cap_rate']

    def get_success_url(self):
        success_url = reverse_lazy(
            'rent_create', 
            kwargs={'pk': self.object.address.id}
        )
        return success_url

    def form_valid(self, form):
        form.instance.address_id = self.kwargs['pk']
        return super(CapRateCreateView, self).form_valid(form)


class CapRateUpdateView(UpdateView):
    model = CapRate
    template_name = 'quotes/caprate_update_form.html'
    fields = ['cap_rate']

    def get_success_url(self):
        rent_ids = Rent.objects.filter(address_id=self.object.address.id)
        rent_ids_list = rent_ids.values_list('id', flat=True)

        if len(rent_ids_list) > 0:
            success_url = reverse_lazy(
                'rent_update', 
                kwargs={'pk': rent_ids_list[0]}
            )
        else:
            success_url = reverse_lazy(
                'rent_create',
                kwargs={'pk': self.object.address.id}
            )
        obj, created = Result.objects.update_or_create(
            address_id=self.object.address.id
        )
        return success_url


class RentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Rents to be viewed or edited.
    """
    queryset = Rent.objects.all().order_by('address')
    serializer_class = RentSerializer
    template_name = 'quotes/rent.html'


class RentCreateView(CreateView):
    model = Rent
    template_name = 'quotes/rent_create_form.html'
    fields = [
        'monthly_rent', 
        'unit_number', 
        'vacancy', 
        'bedrooms', 
        'bathrooms',
    ]

    def get_success_url(self):
        if 'finish' in self.request.POST:
            success_url = reverse_lazy(
                'result_list'
            )
        else:
            success_url = reverse_lazy(
                'rent_create', 
                kwargs={'pk': self.object.address.id}
            )

        obj, created = Result.objects.update_or_create(
            address_id=self.object.address.id
        )
        return success_url

    def form_valid(self, form):
        try:
            form.instance.address_id = self.kwargs['pk']
            return super(RentCreateView, self).form_valid(form)
        except IntegrityError:
            form.instance.address_id = self.kwargs['pk']
            error_message = "Rent record already exists" 
            return render(
                self.request, 
                'quotes/rent_create_form.html', 
                {'error_message': error_message}
            )


class RentDuplicateView(TemplateView):
    template_name = 'quotes/rent_duplicate.html'


class RentUpdateView(UpdateView):
    model = Rent
    template_name = 'quotes/rent_update_form.html'
    fields = [
        'monthly_rent', 
        'unit_number', 
        'vacancy',
        'bedrooms',
        'bathrooms',
    ]

    def get_success_url(self):
        if 'finish' in self.request.POST:
            success_url = reverse_lazy(
                'result_list'
            )
        elif 'update_rent' in self.request.POST:
            current_rent_id = self.object.pk
            print ("\nRent ID:", current_rent_id)
            rent_roll = Rent.objects.filter(address=self.object.address)

            if len(rent_roll) > 1:
                for unit in rent_roll:
                    if unit.id > current_rent_id:
                        success_url = reverse_lazy(
                            'rent_update', 
                            kwargs={'pk': unit.id}
                        )
                        break
                    else:
                        success_url = reverse_lazy(
                            'result_list'
                        )
            else:
                success_url = reverse_lazy(
                    'result_list'
                )
        elif 'delete_rent' in self.request.POST:
            success_url = reverse_lazy(
                'rent_delete', 
                kwargs={'pk': self.object.pk}
            )
        else:
            success_url = reverse_lazy(
                'rent_create', 
                kwargs={'pk': self.object.address.id}
            )

        obj, created = Result.objects.update_or_create(
            address_id=self.object.address.id
        )
        return success_url


class RentDeleteView(DeleteView):
    model = Rent

    def get_success_url(self):
        if self.object.pk+1:
            success_url = reverse_lazy(
                'rent_update',
                kwargs={'pk': self.object.pk+1}
            )
        else:
            success_url = reverse_lazy(
                'rent_create',
                kwargs={'pk': self.object.address.id}
            )
        return success_url


class ResultListView(ListView):
    model = Result 
    queryset = Result.objects.all()
    template_name = 'quotes/result_list.html'

    def get_success_url(self):
        if 'update_quote' in self.request.POST:
            success_url = reverse_lazy(
                'address_update',
                kwargs={'pk': self.object.address.id}
            )
        else:
            success_url = reverse_lazy(
                'result_delete', 
                kwargs={'pk': self.object.pk}
            )
        return success_url


class ResultDetailView(DetailView):
    model = Result
    template_name = 'quotes/result_detail.html'


class ResultDeleteView(DeleteView):
    model = Result

    def get_success_url(self):
        success_url = reverse_lazy(
            'result_list'
        )
        address = Address.objects.get(id=self.object.address.id)
        address.delete()
        return success_url



