from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from credit_app.models import Customer, Policy


class CustomerAPITests(APITestCase):
    """
    Customer API Endpoint Tests Cases

    Tests:
    test_create_customer_accept: submits a valid customer, expects a 201 status with ACCEPT message.
    test_create_customer_reject: submits an invalid customer, expects a 400 status, REJECT message, errors on a missing
    customer_name field and wrong data type for customer_income field.
    """

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
    """
    Policy API Endpoint Tests Cases

    Tests:
    test_create_policy_accept: submits a valid policy, expects a 201 status with ACCEPT message.
    test_create_policy_reject: submits an invalid policy, expects a 400 status, REJECT message, errors on a missing
    policy_name field and wrong data type for max_income field.
    """

    def setUp(self):
        self.factory = APIClient()
        self.policy_endpoint = '/api/policies/'

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
    """
    CustomerPolicy API Endpoint Tests Cases
    For each test a valid customer is created along with two policies, one which will accept the customer and one which
    will reject the customer.

    Tests:
    test_create_customer_policy_accept: submits a valid customer policy, expects a 201 status with ACCEPT message,
    accept boolean set to true, and no rejection reasons.

    test_create_customer_policy_reject: submits a valid customer policy, with a customer which will fail its constraints
    expects a 201 status, REJECT message, accept boolean set to false, and rejection reasons relating to age and income.

    test_customer_can_have_multiple_policies: submits two different customer policies for the same customer.
    Expects a 201 for both.

    test_customer_cant_have_same_policy: submits the same customer policy twice. Expects a 201 for the first request,
    a 400 for the second.
    """
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
