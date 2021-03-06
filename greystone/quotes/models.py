from django.db import models
from django.db.models import Avg, Count, Min, Sum
from django.core.validators import MaxValueValidator, MinValueValidator


"""
This database consists of five models: Address, Expense, Caprate, 
Rent and Result.

The models reflect the workflow that I had envisioned 
as users move through the UI, e.g.:
1. User clicks 'create new quote',
2. User enters address, then expense, then caprate and finally the rent roll.
3. User clicks 'finish' which takes them to the home page. 
4. Lastly, user clicks on 'current quotes' to see list of quotes and details.

All models have a one-to-one relationship with the Address model, 
except for the Result model, which has a many-to-one relationship 
with Address.

Also, propertymetrics.com was helpful in understanding the calculations - 
https://www.propertymetrics.com/blog/2014/01/03/how-commercial-real-estate-loan-underwriting-works/

Shaun Cox 8/14/18
"""


class Address(models.Model):
    """
    Address of the commercial property
    """
    street = models.CharField(
        "street",
        max_length=100,
    )
    city = models.CharField(
        "city",
        max_length=75,
    )
    state = models.CharField(
        "state",
        max_length=2,
    )
    zip_code = models.CharField(
        "zip Code",
        max_length=5,
    )

    class Meta:
        unique_together = [
            "street", 
            "city", 
            "state", 
            "zip_code"
        ]

    def __str__(self):
        return self.street


class Expense(models.Model):
    """
    Annual expenses for the commercial property
    """
    expense_id = models.PositiveIntegerField(
        primary_key=True, 
        unique=True,
        default=1,
        editable=False,
    )
    address = models.OneToOneField(
        Address,
        unique=True,
        on_delete=models.CASCADE,
    )
    marketing = models.PositiveIntegerField(
        "marketing (annualized)",
    )
    taxes = models.PositiveIntegerField(
        "taxes (annualized)",
    )
    insurance = models.PositiveIntegerField(
        "insurance (annualized)",
    )
    repairs = models.PositiveIntegerField(
        "repairs (annualized)",
    )
    administration = models.PositiveIntegerField(
        "administration (annualized)",
    )
    annual_expense = models.PositiveIntegerField(
        "annual Expense",
        default=0,
    )

    @property
    def get_annual_expense(self):
        return self.marketing + self.taxes + self.insurance + self.repairs + self.administration

    def save(self, *args, **kwargs):
        self.expense_id = self.address.id
        self.annual_expense = self.get_annual_expense 
        super(Expense, self).save(*args, **kwargs)


class CapRate(models.Model):
    """
    Cap rate for the commercial property
    """
    cap_rate_id = models.PositiveIntegerField(
        primary_key=True, 
        unique=True,
        default=1,
        editable=False,
    )
    address = models.OneToOneField(
        Address,
        default=1,
        unique=True,
        on_delete=models.CASCADE,
    )
    cap_rate = models.DecimalField(
        "capitalization Rate",
        decimal_places=2,
        max_digits=5,
    )

    def save(self, *args, **kwargs):
        self.cap_rate_id = self.address.id
        super(CapRate, self).save(*args, **kwargs)


class Rent(models.Model):
    """
    Rent for each unit of the commercial property
    """
    address = models.ForeignKey(
        Address, 
        on_delete=models.CASCADE,
    )
    monthly_rent = models.PositiveIntegerField(
        "monthly Rent",
    )
    unit_number = models.CharField(
        "unit Number",
        max_length=10,
    )
    vacancy = models.PositiveIntegerField(
        "vacancy Rate (in whole numbers)",
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ],
    )
    bedrooms = models.PositiveIntegerField(
        "bedrooms",
        validators=[
            MaxValueValidator(50),
            MinValueValidator(1)
        ],
    )
    bathrooms = models.PositiveIntegerField(
        "bathrooms",
        validators=[
            MaxValueValidator(50),
            MinValueValidator(1)
        ],
    )
    annual_unit_rent = models.PositiveIntegerField(
        "annual Unit Rent", 
        default=0,
    )

    class Meta:
        unique_together = [
            "address",
            "unit_number", 
        ]

    @property
    def get_annual_unit_rent(self):
        return self.monthly_rent * 12

    def save(self, *args, **kwargs):
        self.annual_unit_rent = self.get_annual_unit_rent 
        super(Rent, self).save(*args, **kwargs)


class Result(models.Model):
    """
    Quotes for the commercial property entered
    """
    address = models.OneToOneField(
        Address, 
        unique=True,
        on_delete=models.CASCADE,
    )
    annual_property_rent = models.PositiveIntegerField(
        "annual Rent of Property",
        default=0,
    )
    loan_amount = models.IntegerField(
        "loan Amount",
        default=0,
    )
    dscr_loan_amount = models.IntegerField(
        "Loan (DSCR approach)",
        default=0,
    )
    debt_rate = models.DecimalField(
        "debt Rate",
        decimal_places=2,
        max_digits=6,
        default=0,
    )
    noi = models.IntegerField(
        "net Operating Income",
        default=0,
    )
    debt_payment = models.IntegerField(
        "annual Debt Payment (NOI / 1.25)",
        default=0,
    )
    property_value = models.IntegerField(
        "property Value",
        default=0,
    )

    @property
    def get_annual_property_rent(self):
        annual_property_rent = Rent.objects. \
            filter(address=self.address). \
            aggregate(Sum('annual_unit_rent'))['annual_unit_rent__sum']
        return annual_property_rent

    @property
    def get_annual_property_expense(self):
        annual_property_expense = Expense.objects. \
            values_list('annual_expense', flat=True). \
            get(address=self.address)
        return annual_property_expense

    @property
    def get_cap_rate(self):
        cap_rate = CapRate.objects. \
            values_list('cap_rate', flat=True). \
            get(address=self.address)
        return cap_rate

    @property
    def get_dscr_loan_amount(self):
        loan = ((self.debt_payment / 12) * \
            (1 - (1 / (1 + ((self.debt_rate / 100) / 12)) ** (10 * 12)))) / \
            ((self.debt_rate / 100) / 12)
        return loan

    @property
    def get_loan_amount(self):
        if self.property_value < self.dscr_loan_amount:
            return self.property_value
        else:
            return self.dscr_loan_amount

    def save(self, *args, **kwargs):
        self.annual_property_rent = self.get_annual_property_rent
        annual_property_expense = self.get_annual_property_expense
        cap_rate = self.get_cap_rate
        self.debt_rate = 2.98 + 2.00
        self.noi = self.annual_property_rent - annual_property_expense
        self.debt_payment = (self.noi * 100) / 125
        self.property_value = self.noi / (cap_rate / 100)
        self.dscr_loan_amount = self.get_dscr_loan_amount
        self.loan_amount = self.get_loan_amount
        super(Result, self).save(*args, **kwargs)


