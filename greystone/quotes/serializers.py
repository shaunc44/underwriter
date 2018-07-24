from quotes.models import Address, Rent, Expense, CapRate

from rest_framework import serializers


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = (
            'street', 
            'city', 
            'state', 
            'zip_code'
        )


class RentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rent
        fields = (
            'address',
            'monthly_rent',
            'unit_number',
            'vacancy',
            'bedrooms',
            'bathrooms',
            'annual_total'
        )

class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Expense
        fields = (
            'address',
            'marketing',
            'taxes',
            'insurance',
            'repairs',
            'administration'
        )


class CapRateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CapRate
        fields = (
            'address',
            'cap_rate'
        )



