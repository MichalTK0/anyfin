from django.test import TestCase
from django.core.exceptions import ValidationError
from credit_app.models import Customer


class CustomerModelTests(TestCase):

    def test_low_income_validation(self):

        low_income_customer = Customer(
            customer_income=499,
            customer_debt=0,
            payment_remarks_12m=0,
            payment_remarks=1,
            customer_age=25,
        )

        with self.assertRaises(ValidationError) as context:
            low_income_customer.full_clean()

        errors = context.exception.message_dict
        self.assertEqual(errors["customer_income"], ["LOW_INCOME"])

    def test_high_debt_validation(self):

        high_debt_customer = Customer(
            customer_income=1000,
            customer_debt=501,
            payment_remarks_12m=0,
            payment_remarks=1,
            customer_age=25,
        )

        with self.assertRaises(ValidationError) as context:
            high_debt_customer.full_clean()

        errors = context.exception.message_dict
        self.assertEqual(errors["customer_debt"], ["HIGH_DEBT_FOR_INCOME"])

    def test_valid_customer(self):

        valid_customer = Customer(
            customer_income=1000,
            customer_debt=400,
            payment_remarks_12m=0,
            payment_remarks=1,
            customer_age=25,
        )

        valid_customer.full_clean()

    def test_underage_validation(self):

        underage_customer = Customer(
            customer_income=1000,
            customer_debt=400,
            payment_remarks_12m=0,
            payment_remarks=1,
            customer_age=17,
        )

        with self.assertRaises(ValidationError) as context:
            underage_customer.full_clean()

        errors = context.exception.message_dict
        self.assertEqual(errors["customer_age"], ["UNDERAGE"])
