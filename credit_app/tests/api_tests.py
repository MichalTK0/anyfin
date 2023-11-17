from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CustomerViewSetTests(APITestCase):

    def test_create_customer_accept(self):
        url = reverse("customer-list")
        data = {
            "customer_income": 1000,
            "customer_debt": 500,
            "payment_remarks_12m": 0,
            "payment_remarks": 1,
            "customer_age": 20
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"message": "ACCEPT"})

    def test_create_customer_reject(self):
        url = reverse("customer-list")
        data = {
            "customer_income": 100,
            "customer_debt": 500,
            "payment_remarks_12m": 0,
            "payment_remarks": 1,
            "customer_age": 12
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            "message": "REJECT",
            "reason": {
                "customer_income": ["LOW_INCOME"],
                "customer_age": ["UNDERAGE"]
            }
        })
