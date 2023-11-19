from django.test import TestCase
from django.core.exceptions import ValidationError
from credit_app.models import Customer, Policy, CustomerPolicy

GTE_ZERO_ERROR = 'Ensure this value is greater than or equal to 0.'


class CustomerModelTests(TestCase):

    def test_type_validation(self):
        wrong_type_customer = Customer(
            customer_name=1234,  # Name should pass as Django is smart enough to cast to str
            customer_income="hello",
            customer_debt="test1",
            payment_remarks_12m="test2",
            payment_remarks="test3",
            customer_age="test4",
        )

        with self.assertRaises(ValidationError) as context:
            wrong_type_customer.full_clean()

        errors = context.exception.message_dict
        expected_errors = {
            "customer_income": ['“hello” value must be a decimal number.'],
            "customer_debt": ['“test1” value must be a decimal number.'],
            "payment_remarks_12m": ['“test2” value must be an integer.'],
            "payment_remarks": ['“test3” value must be an integer.'],
            "customer_age": ['“test4” value must be an integer.'],
        }

        for field, expected_error in expected_errors.items():
            self.assertEqual(errors[field], expected_error)

    def test_constraint_validation(self):
        wrong_constraint_customer = Customer(
            customer_income=-1000,
            customer_debt=-1,
            payment_remarks_12m=-21,
            payment_remarks=-7,
            customer_age=999,
        )

        with self.assertRaises(ValidationError) as context:
            wrong_constraint_customer.full_clean()

        errors = context.exception.message_dict
        expected_errors = {
            "customer_income": [GTE_ZERO_ERROR],
            "customer_debt": [GTE_ZERO_ERROR],
            "payment_remarks_12m": [GTE_ZERO_ERROR],
            "payment_remarks": [GTE_ZERO_ERROR],
            "customer_age": ['Ensure this value is less than or equal to 101.'],
        }

        for field, expected_error in expected_errors.items():
            self.assertEqual(errors[field], expected_error)

    def test_creation(self):
        valid_customer = Customer.objects.create(
            customer_name='TestMan',
            customer_income=1000,
            customer_debt=500.5,
            payment_remarks_12m=0,
            payment_remarks=2,
            customer_age=21,
        )

        valid_customer.full_clean()
        self.assertIsNotNone(valid_customer.pk)


class PolicyModelTests(TestCase):

    def test_type_validation(self):
        wrong_type_policy = Policy(
            max_income="test1",
            min_income="test2",
            max_debt_ratio="test3",
            max_payment_remarks="test4",
            max_payment_remarks_12m="test5",
            min_age="test6",
            max_age="test7"
        )

        with self.assertRaises(ValidationError) as context:
            wrong_type_policy.full_clean()

        errors = context.exception.message_dict
        expected_errors = {
            "max_income": ['“test1” value must be a decimal number.'],
            "min_income": ['“test2” value must be a decimal number.'],
            "max_debt_ratio": ['“test3” value must be a decimal number.'],
            "max_payment_remarks": ['“test4” value must be an integer.'],
            "max_payment_remarks_12m": ['“test5” value must be an integer.'],
            "min_age": ['“test6” value must be an integer.'],
            "max_age": ['“test7” value must be an integer.'],
        }

        for field, expected_error in expected_errors.items():
            self.assertEqual(errors[field], expected_error)

    def test_constraint_validation(self):
        wrong_constraint_policy = Policy(
            max_income=-1000,
            min_income=-1000,
            max_debt_ratio=-5,
            max_payment_remarks=-2,
            max_payment_remarks_12m=-5,
            min_age=-5,
            max_age=999
        )

        with self.assertRaises(ValidationError) as context:
            wrong_constraint_policy.full_clean()

        errors = context.exception.message_dict

        expected_errors = {
            "max_income": [GTE_ZERO_ERROR],
            "min_income": [GTE_ZERO_ERROR],
            "max_debt_ratio": [GTE_ZERO_ERROR],
            "max_payment_remarks": [GTE_ZERO_ERROR],
            "max_payment_remarks_12m": [GTE_ZERO_ERROR],
            "min_age": [GTE_ZERO_ERROR],
            "max_age": ['Ensure this value is less than or equal to 101.'],
        }

        for field, expected_error in expected_errors.items():
            self.assertEqual(errors[field], expected_error)

    def test_creation(self):
        valid_policy = Policy.objects.create(
            policy_name="test",
            max_income=50000,
            min_income=0,
            max_debt_ratio=0.5,
            max_payment_remarks=0,
            max_payment_remarks_12m=1,
            min_age=18,
            max_age=80
        )

        valid_policy.full_clean()
        self.assertIsNotNone(valid_policy.pk)


class CustomerPolicyModelTest(TestCase):

    def setUp(self):
        # create a customer to be used in policy tests.

        self.valid_customer = Customer.objects.create(
            customer_income=1000,
            customer_debt=499,
            payment_remarks_12m=0,
            payment_remarks=0,
            customer_age=21,
        )

        # create two policies, one which will accept, one which will reject the customer
        self.accept_policy = Policy.objects.create(
            policy_name="test",
            max_income=50000,
            min_income=0,
            max_debt_ratio=0.5,
            max_payment_remarks=0,
            max_payment_remarks_12m=1,
            min_age=18,
            max_age=80
        )

        self.reject_policy = Policy.objects.create(
            policy_name="test",
            max_income=50000,
            min_income=5000,
            max_debt_ratio=0.5,
            max_payment_remarks=0,
            max_payment_remarks_12m=1,
            min_age=30,
            max_age=80
        )

    def test_accepted_policy(self):
        valid_customer_policy = CustomerPolicy.objects.create(
            customer=self.valid_customer,
            policy=self.accept_policy
        )

        valid_customer_policy.full_clean()
        self.assertIsNotNone(valid_customer_policy.pk)

        # Check that the customer has been accepted to the policy.
        self.assertEqual(valid_customer_policy.accepted, True)
        self.assertIsNone(valid_customer_policy.rejection_reason)

    def test_rejected_policy(self):
        rejected_customer_policy = CustomerPolicy.objects.create(
            customer=self.valid_customer,
            policy=self.reject_policy
        )

        rejected_customer_policy.full_clean()

        # Check policy is not accepted
        # Expecting it to fail due to low income and customer being underage.
        self.assertEqual(rejected_customer_policy.accepted, False)
        self.assertEqual(rejected_customer_policy.rejection_reason, "LOW_INCOME, UNDERAGE")

    def test_customer_can_have_multiple_policies(self):
        valid_customer_policy = CustomerPolicy.objects.create(
            customer=self.valid_customer,
            policy=self.accept_policy
        )

        rejected_customer_policy = CustomerPolicy.objects.create(
            customer=self.valid_customer,
            policy=self.reject_policy
        )

        valid_customer_policy.full_clean()
        rejected_customer_policy.full_clean()

    def test_customer_cant_have_same_policy(self):
        valid_customer_policy = CustomerPolicy.objects.create(
            customer=self.valid_customer,
            policy=self.accept_policy
        )

        with self.assertRaises(ValidationError) as context:
            valid_customer_policy2 = CustomerPolicy.objects.create(
                customer=self.valid_customer,
                policy=self.accept_policy
            )

        self.assertEqual(context.exception.messages, ['Customer policy with this Customer and Policy already exists.'])
