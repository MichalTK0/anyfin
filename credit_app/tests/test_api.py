from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from credit_app.models import Customer, Policy
from django.core.exceptions import ValidationError


class CustomerAPITests(APITestCase):

    def setUp(self):
        self.factory = APIClient()
        self.customer_endpoint = '/api/customers/'

    def test_create_customer_accept(self):
        data = {
            "customer_name": "Jeff",
            "customer_income": 1000,
            "customer_debt": 500,
            "payment_remarks_12m": 0,
            "payment_remarks": 1,
            "customer_age": 20
        }

        response = self.factory.post(self.customer_endpoint, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "ACCEPT")

    def test_create_customer_reject(self):
        data = {
            "customer_income": "fail",
            "customer_debt": 500,
            "payment_remarks_12m": 0,
            "payment_remarks": 1,
            "customer_age": 20
        }

        response = self.factory.post(self.customer_endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "REJECT")

        expected_errors = {
            "customer_name": "This field is required.",
            "customer_income": "A valid number is required."

        }

        for field, expected_error in expected_errors.items():
            self.assertEqual(response.data['reason'][field][0], expected_error)


class PolicyAPITests(APITestCase):

    def setUp(self):
        self.factory = APIClient()
        self.policy_endpoint = '/api/policies/'

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

    def test_create_policy_accept(self):
        data = {
            "policy_name": "test",
            "max_income": 50000,
            "min_income": 0,
            "max_debt_ratio": 0.5,
            "max_payment_remarks": 0,
            "max_payment_remarks_12m": 1,
            "min_age": 18,
            "max_age": 80
        }

        response = self.factory.post(self.policy_endpoint, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "ACCEPT")

    def test_create_policy_reject(self):
        data = {
            "max_income": "fail",
            "min_income": 0,
            "max_debt_ratio": 0.5,
            "max_payment_remarks": 0,
            "max_payment_remarks_12m": 1,
            "min_age": 18,
            "max_age": 80
        }

        response = self.factory.post(self.policy_endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "REJECT")

        expected_errors = {
            "policy_name": "This field is required.",
            "max_income": "A valid number is required."

        }

        for field, expected_error in expected_errors.items():
            self.assertEqual(response.data['reason'][field][0], expected_error)


class CustomerPolicyAPITests(APITestCase):

    def setUp(self):
        self.factory = APIClient()
        self.policy_endpoint = '/api/customer_policies/'

        # Create a customer and two policies, one policy will accept the customer, one will reject.
        self.valid_customer = Customer.objects.create(
            customer_income=1000,
            customer_debt=499,
            payment_remarks_12m=0,
            payment_remarks=0,
            customer_age=21,
        )

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

    def test_create_customer_policy_accept(self):
        data = {
            "customer": self.valid_customer.pk,
            "policy": self.accept_policy.pk
        }

        response = self.factory.post(self.policy_endpoint, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "ACCEPT")
        self.assertEqual(response.data['detail']['accepted'], True)
        self.assertIsNone(response.data['detail']['rejection_reason'])

    def test_create_customer_policy_reject(self):
        data = {
            "customer": self.valid_customer.pk,
            "policy": self.reject_policy.pk
        }

        response = self.factory.post(self.policy_endpoint, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "REJECT")
        self.assertEqual(response.data['detail']['accepted'], False)
        self.assertEqual(response.data['detail']['rejection_reason'], 'LOW_INCOME, UNDERAGE')

    def test_customer_can_have_multiple_policies(self):
        data = {
            "customer": self.valid_customer.pk,
            "policy": self.accept_policy.pk
        }

        response = self.factory.post(self.policy_endpoint, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "customer": self.valid_customer.pk,
            "policy": self.reject_policy.pk
        }

        response = self.factory.post(self.policy_endpoint, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_customer_cant_have_same_policy(self):
        data = {
            "customer": self.valid_customer.pk,
            "policy": self.accept_policy.pk
        }

        response = self.factory.post(self.policy_endpoint, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.factory.post(self.policy_endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "REJECT")
