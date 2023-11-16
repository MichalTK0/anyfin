from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Policy(models.Model):
    policy_name = models.CharField(max_length=255)
    max_income = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True,
                                     validators=[MinValueValidator(0)]
                                     )
    min_income = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    max_debt_ratio = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    max_payment_remarks = models.IntegerField(validators=[MinValueValidator(0)])
    max_payment_remarks_12m = models.IntegerField(validators=[MinValueValidator(0)])
    min_age = models.IntegerField(default=18, validators=[MinValueValidator(0), MaxValueValidator(101)])
    max_age = models.IntegerField(default=101, validators=[MinValueValidator(0), MaxValueValidator(101)])

    def __str__(self):
        return f"Policy {self.id}: {self.policy_name}"


class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_income = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    customer_debt = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    payment_remarks_12m = models.IntegerField(validators=[MinValueValidator(0)])
    payment_remarks = models.IntegerField(validators=[MinValueValidator(0)])
    customer_age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(101)])

    def __str__(self):
        return f"Customer {self.id}: {self.customer_name}"


class CustomerPolicy(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        errors = []

        # Apply policy constraints
        if self.policy:
            if float(self.customer.customer_income) < float(self.policy.min_income):
                errors.append('LOW_INCOME')

            if self.policy.max_income is not None \
                    and float(self.customer.customer_income) > float(self.policy.max_income):
                errors.append('HIGH_INCOME')

            if float(self.customer.customer_debt) \
                    > float(self.policy.max_debt_ratio) * float(self.customer.customer_income):
                errors.append('HIGH_DEBT_FOR_INCOME')

            if self.customer.payment_remarks_12m > self.policy.max_payment_remarks_12m:
                errors.append('PAYMENT_REMARKS_12M')

            if self.customer.payment_remarks > self.policy.max_payment_remarks:
                errors.append('PAYMENT_REMARKS')

            if self.customer.customer_age < self.policy.min_age:
                errors.append('UNDERAGE')

            if self.customer.customer_age > self.policy.max_age:
                errors.append('ABOVE_MAX_AGE')

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"Policy {self.policy.policy_name} for {self.customer.customer_name}"
