from django.db import models
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
    def annual_total(self):
        return self.monthly * 12


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



