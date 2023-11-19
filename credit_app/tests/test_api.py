from rest_framework import status
from rest_framework.test import APITestCase, APIClient


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