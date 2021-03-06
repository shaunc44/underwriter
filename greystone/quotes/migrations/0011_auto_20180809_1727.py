# Generated by Django 2.0.5 on 2018-08-09 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0010_auto_20180809_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='annual_expense',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='annual Expense'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='annual_unit_rent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='annual Unit Rent'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='monthly_rent',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='monthly Rent'),
        ),
        migrations.AlterField(
            model_name='result',
            name='annual_property_rent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='annual Rent of Property'),
        ),
        migrations.AlterField(
            model_name='result',
            name='debt_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='debt Rate'),
        ),
        migrations.AlterField(
            model_name='result',
            name='dscr_loan_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Loan (DSCR approach)'),
        ),
        migrations.AlterField(
            model_name='result',
            name='loan_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='loan Amount'),
        ),
    ]
