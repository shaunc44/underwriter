from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404
from django.http import HttpResponse
from django.views.generic import (
    ListView, DetailView, CreateView, DeleteView, UpdateView
)
from django.urls.base import reverse_lazy
from django.db.models.query import QuerySet

from rest_framework import viewsets
# from rest_framework.renderers import JSONRenderer
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
# from rest_framework.decorators import action

from quotes.serializers import (
    AddressSerializer, RentSerializer,
    ExpenseSerializer, CapRateSerializer, ResultSerializer
)
from quotes.models import (
    Address, Rent, Expense, CapRate, Result
)


"""
Address Views for API and HTML
"""
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
        # success_url = reverse_lazy('rent_create', pk)
        success_url = reverse_lazy(
            'expense_create', 
            kwargs={'pk': self.object.pk}
        )
        return success_url


class AddressUpdateView(UpdateView):
    model = Address
    # template_name_suffix = '_update_form'
    template_name = 'quotes/address_update_form.html'
    fields = [
        'street', 
        'city', 
        'state', 
        'zip_code'
    ]

    def get_success_url(self):
        # success_url = reverse_lazy('rent_create', pk)
        success_url = reverse_lazy(
            'expense_update', 
            kwargs={'pk': self.object.pk}
        )
        return success_url


"""
Expense Views both API and HTML
"""
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
    # success_url = reverse_lazy('rent_create')
    def get_success_url(self):
        # success_url = reverse_lazy('rent_create', pk)
        success_url = reverse_lazy(
            'cap_rate_create', 
            kwargs={'pk': self.object.address.id}
        )
        return success_url

    def form_valid(self, form):
        # form.instance.owner = self.request.user
        form.instance.address_id = self.kwargs['pk']
        return super(ExpenseCreateView, self).form_valid(form)


class ExpenseUpdateView(UpdateView):
    model = Expense
    # template_name_suffix = '_update_form'
    template_name = 'quotes/expense_update_form.html'
    fields = [
        'marketing', 
        'taxes', 
        'insurance',
        'repairs',
        'administration',
    ]

    def get_success_url(self):
        # success_url = reverse_lazy('rent_create', pk)
        success_url = reverse_lazy(
            'cap_rate_update', 
            kwargs={'pk': self.object.address.id}
        )
        return success_url

    def form_valid(self, form):
        # form.instance.owner = self.request.user
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
    # template_name_suffix = '_update_form'
    template_name = 'quotes/caprate_update_form.html'
    fields = ['cap_rate']

    def get_success_url(self):
        # success_url = reverse_lazy('rent_create', pk)
        success_url = reverse_lazy(
            'rent_update', 
            kwargs={'pk': self.object.address.id}
        )
        return success_url

    def form_valid(self, form):
        form.instance.address_id = self.kwargs['pk']
        return super(CapRateUpdateView, self).form_valid(form)


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
        # r.save()
        return success_url

    def form_valid(self, form):
        # form.instance.owner = self.request.user
        form.instance.address_id = self.kwargs['pk']
        return super(RentCreateView, self).form_valid(form)

    # def form_valid(self, form):
    #     # form.instance.owner = self.request.user
    #     form.instance.address_id = self.kwargs['pk']
    #     return super(RentCreateView, self).form_valid(form)

    # def get_success_url(self):
    #     success_url = reverse_lazy(
    #         'address_list', 
    #     )
    #     r = Result(address_id=self.object.address.id)
    #     r.save()
    #     return success_url

        # if form.is_valid():
            # form.save()
            # if 'list' in request.POST:
            #     return returnedirect('list_url')
            # else:
            #     return redirect('detail_url')

    # if form.is_valid():
    #     form.save()
    #     if 'list' in request.POST:
    #         return returnedirect('list_url')
    #     else:
            # return redirect('detail_url')

    # r = Result(address_id=pk)
    # r.save()

    # form.fields['field'].widget.attrs['readonly'] = True


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
            success_url = reverse_lazy(
                'rent_update', 
                kwargs={'pk': self.object.address.id}
            )
        elif 'delete_rent_unit' in self.request.POST:
            success_url = reverse_lazy(
                'rent_update', 
                kwargs={'pk': self.object.address.id}
            )
        else:
            success_url = reverse_lazy(
                'rent_create', 
                kwargs={'pk': self.object.address.id}
            )

        # r = Result(address_id=self.object.address.id)
        # r.save()
        return success_url

    def form_valid(self, form):
        form.instance.address_id = self.kwargs['pk']
        return super(RentUpdateView, self).form_valid(form)

#     def form_valid(self, form):
#         # form.instance.owner = self.request.user
#         form.instance.address_id = self.kwargs['pk']
#         return super(RentCreateView, self).form_valid(form)

class RentDeleteView(DeleteView):
    model = Rent

    def get_success_url(self):
        success_url = reverse_lazy(
            'rent_update'
        )
        address = Address.objects.get(id=self.object.address.id)
        address.delete()
        return success_url


class ResultListView(ListView):
    model = Result
    queryset = Result.objects.all()
    template_name = 'quotes/result_list.html'


class ResultDetailView(DetailView):
    model = Result
    template_name = 'quotes/result_detail.html'


class ResultDeleteView(DeleteView):
    model = Result
    # success_url = reverse_lazy(
    #     'result_list'
    # )
    def get_success_url(self):
        success_url = reverse_lazy(
            'result_list'
        )
        address = Address.objects.get(id=self.object.address.id)
        address.delete()
        return success_url



    # queryset = Result.objects.all()

    # def get_queryset(self):
    #     """Filter by address"""
    #     return self.queryset.filter(address_id=self.kwargs['pk'])

    # def form_valid(self, form):
    #     # form.instance.owner = self.request.user
    #     form.instance.address_id = self.kwargs['pk']
    #     return super(ResultDetailView, self).form_valid(form)

    # def post(self, request, format=None):
    #     serializer = ResultSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @property
    # def annual_building_rent(self):
    #     monthly_bldg_rent = Rent.objects.filter(address=address).aggregate(Sum('monthly_rent'))
    #     annual_bldg_rent = monthly_bldg_rent * 12
    #     return annual_bldg_rent



# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         # 'users': reverse('user-list', request=request, format=format),
#         'results': reverse('snippet-list', request=request, format=format)
#     })

# class ResultDetail(APIView):
#     """
#     Create, retrieve, update or delete a Result instance.
#     """
#     queryset = CapRate.objects.all()
#     serializer_class = CapRateSerializer

#     def post(self, request, format=None):
#         serializer = ResultSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get_object(self, pk):
#         try:
#             return Result.objects.get(pk=pk)
#         except Result.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         result = self.get_object(pk)
#         serializer = ResultSerializer(result)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         result = self.get_object(pk)
#         serializer = ResultSerializer(result, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         result = self.get_object(pk)
#         result.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




# class ResultViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows Quotes to be viewed or edited.
#     """
#     queryset = Result.objects.all()
#     serializer_class = ResultSerializer


# class ResultList(APIView):
#     """
#     List all results, or create a new result.
#     """
#     def get(self, request, format=None):
#         results = Result.objects.all()
#         serializer = ResultSerializer(results, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = ResultSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




"""
I need to work on the classes below. Ideally I would like to 
return the outputs from these views 
(maybe calculations should occur in the models => fat models, skinny views)
"""
# class LoanAmountView(APIView):
"""
A view that returns the loan amount in JSON.
"""
    # pass
    # renderer_classes = (JSONRenderer, )
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'quote.html'

#     def get(self, request, format=None):

#         annual_bldg_rent = Rent.calc_bldg_rent(request)

#         # noi = Rent.objects.filter(annual_rent) - Expense.objects.filter()
#         # value = noi / CapRate.objects.filter()
#         # debt_rate = 0.0295 + 0.02
#         # debt_pmt = debt_rate * loan_proceeds # ???
#         # present_value = payoff / (1+debt_rate)**num_pmts
#         # content = {'loan_amount': loan_amount}
#         # return Response(content)
#         return Response({'building_rent': annual_bldg_rent})


# class LoanAmountView(APIView):
#     pass
"""
A view that returns the debt rate in JSON.
"""
    # renderer_classes = (JSONRenderer, )

    # def get(self, request, format=None):
    #     noi = Rent.objects.filter(annual_total) - Expense.objects.filter()
    #     value = noi / CapRate.objects.filter()
    #     content = {'user_count': user_count}
    #     return Response(content)


# from django.shortcuts import render


# def display_quotes(request):
#     return render(
#         request,
#         'quotes/quotes.html'
#     )


# class AddressDetail(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     # template_name = 'address_detail.html'

#     def get(self, request, pk):
#         address = get_object_or_404(Address, pk=pk)
#         serializer = AddressSerializer(address)
#         return Response(
#             {'serializer': serializer, 'address': address},
#             template_name = 'quotes/address_detail.html'
#         )

#     def post(self, request, pk):
#         address = get_object_or_404(Address, pk=pk)
#         serializer = AddressSerializer(address, data=request.data)
#         if not serializer.is_valid():
#             return Response(
#                 {'serializer': serializer, 'address': address},
#                 template_name = 'quotes/address_detail.html'
#             )
#         serializer.save()
#         return redirect('address_list')

#     def delete(self, request, pk):
#         address = get_object_or_404(Address, pk=pk)
#         address.delete()
#         return Response(
#             status=status.HTTP_204_NO_CONTENT,
#             template_name = 'quotes/address_list.html',
#         )

# class AddressList(APIView):
#     renderer_classes = [TemplateHTMLRenderer]

#     def get(self, request):
#         queryset = Address.objects.all()
#         return Response(
#             {'address_list': queryset},
#             template_name = 'quotes/address_list.html', 
#         )


# class AddressViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows Addresses to be viewed or edited.
#     """
#     queryset = Address.objects.all().order_by('street')
#     serializer_class = AddressSerializer
#     template_name = 'quotes/address.html'

#     @list_route(renderer_classes=[TemplateHTMLRenderer])
#     def blank_form(self, request, *args, **kwargs):
#         # address = get_object_or_404(Address)
#         serializer = AddressSerializer()
#         return Response({'serializer': serializer})



