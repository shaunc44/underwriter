from django.db import models
from django.db.models import Avg, Count, Min, Sum
from django.core.validators import MaxValueValidator, MinValueValidator


class Address(models.Model):
    """
    Address of the commercial property
    """
    street = models.CharField(
        "street Address",
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

    def __str__(self):
        return self.street


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

    @property
    def annual_rent(self):
        return self.monthly_rent * 12

    def calc_bldg_rent(self):
        monthly_bldg_rent = Rent.objects.filter(address=address).aggregate(Sum('monthly_rent'))
        annual_bldg_rent = monthly_bldg_rent * 12
        return annual_bldg_rent


class Expense(models.Model):
    """
    Expenses for the commercial property
    """
    address = models.OneToOneField(
        Address,
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

    @property
    def annual_expense(self):
        return self.marketing + self.taxes + self.insurance + self.repairs + self.administration


class CapRate(models.Model):
    """
    Cap rate for the commercial property
    """
    address = models.OneToOneField(
        Address,
        default=1,
        on_delete=models.CASCADE,
    )
    cap_rate = models.DecimalField(
        "capitalization Rate",
        decimal_places=2,
        max_digits=5,
    )


class Estimate(models.Model):
    """
    Cap rate for the commercial property
    """
    address = models.OneToOneField(
        Address,
        default=1,
        on_delete=models.CASCADE,
    )
    loan_amount = models.PositiveIntegerField(
        "loan Amount",
    )
    debt_rate = models.PositiveIntegerField(
        "debt Rate",
    )

    get noi(self):



