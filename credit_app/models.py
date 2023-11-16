from collections import defaultdict
from django.core.exceptions import ValidationError
from django.db import models


class Customer(models.Model):
    # TODO: improve validation. Can some of these be negative or not?
    customer_income = models.DecimalField(max_digits=9, decimal_places=2)
    customer_debt = models.DecimalField(max_digits=9, decimal_places=2)
    payment_remarks_12m = models.IntegerField()
    payment_remarks = models.IntegerField()
    customer_age = models.IntegerField()

    def clean(self):
        super().clean()
        errors = defaultdict(list)

        # Validate income
        if self.customer_income < 500:
            errors['customer_income'].append('LOW_INCOME')

        # Validate debt based on income
        if float(self.customer_debt) > 0.5 * float(self.customer_income):
            errors['customer_debt'].append('HIGH_DEBT_FOR_INCOME')

        # Validate payment_remarks_12m
        if self.payment_remarks_12m > 0:
            errors['payment_remarks_12m'].append('PAYMENT_REMARKS_12M')

        # Validate payment_remarks
        if self.payment_remarks > 1:
            errors['payment_remarks'].append('PAYMENT_REMARKS')

        # Validate age
        if self.customer_age < 18:
            errors['customer_age'].append('UNDERAGE')

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"Customer {self.id}"
