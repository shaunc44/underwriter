from quotes.models import Address, Rent, Expense, CapRate
from rest_framework import viewsets
from quotes.serializers import AddressSerializer, RentSerializer
from quotes.serializers import ExpenseSerializer, CapRateSerializer

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from quotes.models import Address, Rent, Expense, CapRate


class AddressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Addresss to be viewed or edited.
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class RentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Rents to be viewed or edited.
    """
    queryset = Rent.objects.all()
    serializer_class = RentSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Expenses to be viewed or edited.
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class CapRateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CapRates to be viewed or edited.
    """
    queryset = CapRate.objects.all()
    serializer_class = CapRateSerializer


"""
I need to work on the classes below. Ideally I would like to 
return the outputs from these views 
(maybe calculations should occur in the models => fat models, skinny views)
"""
class LoanAmountView(APIView):
    """
    A view that returns the loan amount in JSON.
    """
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        noi = Rent.objects.filter(annual_total) - Expense.objects.filter()
        value = noi / CapRate.objects.filter()
        debt_rate = 0.0295 + 0.02
        debt_pmt = debt_rate * loan_proceeds # ???
        present_value = payoff / (1+debt_rate)**num_pmts
        content = {'loan_amount': loan_amount}
        return Response(content)


class LoanAmountView(APIView):
    pass
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
