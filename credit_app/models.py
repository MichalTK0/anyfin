from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Policy(models.Model):
    """
    Model representing available policies.

    Fields:
    policy_name: The name of the policy.
    max_income: The maximum income allowed for the policy.
    min_income: The minimum income required for the policy.
    max_debt_ratio: The maximum allowed debt-to-income ratio for the policy.
    max_payment_remarks: The maximum allowed payment remarks.
    max_payment_remarks_12m: The maximum allowed payment remarks in the last 12 months.
    min_age: The minimum age requirement for the policy.
    max_age: The maximum age allowed for the policy.
    """
    policy_name = models.CharField(max_length=255)
    max_income = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True,
                                     validators=[MinValueValidator(0)]
                                     )
    min_income = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    max_debt_ratio = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    max_payment_remarks = models.IntegerField(validators=[MinValueValidator(0)])
    max_payment_remarks_12m = models.IntegerField(validators=[MinValueValidator(0)])
    min_age = models.IntegerField(default=18, validators=[MinValueValidator(0), MaxValueValidator(125)])
    max_age = models.IntegerField(default=101, validators=[MinValueValidator(0), MaxValueValidator(125)])

    class Meta:
        verbose_name = "Policy"
        verbose_name_plural = "Policies"

    def __str__(self):
        return f"Policy {self.id}: {self.policy_name}"


class Customer(models.Model):
    """
    Model representing customers.

    Fields:
    customer_name: The name of the customer.
    customer_income: The income of the customer.
    customer_debt: The debt amount of the customer.
    payment_remarks_12m: The number of payment remarks in the last 12 months.
    payment_remarks: The total number of payment remarks.
    customer_age: The age of the customer.
    """
    customer_name = models.CharField(max_length=255)
    customer_income = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    customer_debt = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    payment_remarks_12m = models.IntegerField(validators=[MinValueValidator(0)])
    payment_remarks = models.IntegerField(validators=[MinValueValidator(0)])
    customer_age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(125)])

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"Customer {self.id}: {self.customer_name}"


class CustomerPolicy(models.Model):
    """
    Model representing customer policies.

    Fields:
    customer: The customer associated with the policy.
    policy: The policy associated with the customer.
    accepted: Indicates whether the policy is accepted.
    rejection_reason: The reason for policy rejection.

    Meta:
    unique_together: Ensures uniqueness of customer-policy pairs.

    Methods:
    save(): Overrides the save method to perform full cleaning before saving.
    clean(): Custom cleaning method to apply policy constraints and determine acceptance/rejection. The rejection
    reasons are saved to the model's rejection_reason fields for reference later.

    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    rejection_reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ['customer', 'policy']
        verbose_name = "Customer Policy"
        verbose_name_plural = "Customer Policies"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        rejections = []

        # Apply policy constraints
        if self.policy:
            if float(self.customer.customer_income) < float(self.policy.min_income):
                rejections.append("LOW_INCOME")

            if self.policy.max_income is not None \
                    and float(self.customer.customer_income) > float(self.policy.max_income):
                rejections.append("HIGH_INCOME")

            if float(self.customer.customer_debt) \
                    > float(self.policy.max_debt_ratio) * float(self.customer.customer_income):
                rejections.append("HIGH_DEBT_FOR_INCOME")

            if self.customer.payment_remarks_12m > self.policy.max_payment_remarks_12m:
                rejections.append("PAYMENT_REMARKS_12M")

            if self.customer.payment_remarks > self.policy.max_payment_remarks:
                rejections.append("PAYMENT_REMARKS")

            if self.customer.customer_age < self.policy.min_age:
                rejections.append("UNDERAGE")

            if self.customer.customer_age > self.policy.max_age:
                rejections.append("ABOVE_MAX_AGE")

        if rejections:
            self.rejection_reason = ", ".join(rejections)
        else:
            self.accepted = True

    def __str__(self):
        if self.accepted:
            return f"{self.customer} - {self.policy} - Accepted"
        else:
            return f"{self.customer} - {self.policy} - Rejected: {self.rejection_reason}"
