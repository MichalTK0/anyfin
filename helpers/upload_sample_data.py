import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/"

HEADERS = {"Content-Type": "application/json"}

sample_customer_data = [
    # Name, Income, Debt, Remarks 12m, Remarks, Age
    ("John Doe", 5000, 2500, 0, 0, 18),
    ("Jane Doe", 60000, 0, 1, 0, 28),
]

sample_policy_data = [
    # Name, max income, min income, max debt ratio, max remarks, max remarks 12m, min age, max age
    ("Default Policy", None, 500, 0.5, 1, 0, 18, 101),
    ("Young Adults", 20000, 250, 0.2, 0, 0, 18, 24)
]

customer_ids = []
policy_ids = []

# Upload Customers
for name, income, debt, remarks_12m, remarks, age in sample_customer_data:
    customer_data = {
        "customer_name": name,
        "customer_income": income,
        "customer_debt": debt,
        "payment_remarks_12m": remarks_12m,
        "payment_remarks": remarks,
        "customer_age": age
    }

    resp = requests.post(url=BASE_URL + 'customers/', data=json.dumps(customer_data), headers=HEADERS).json()
    print(resp)
    customer_ids.append(resp['detail']['id'])

# Upload Policies
for name, max_income, min_income, max_debt, max_remarks, max_remarks_12m, min_age, max_age in sample_policy_data:
    policy_data = {
        "policy_name": name,
        "max_income": max_income,
        "min_income": min_income,
        "max_debt_ratio": max_debt,
        "max_payment_remarks": max_remarks,
        "max_payment_remarks_12m": max_remarks_12m,
        "min_age": min_age,
        "max_age": max_age
    }

    resp = requests.post(url=BASE_URL + 'policies/', data=json.dumps(policy_data), headers=HEADERS).json()
    print(resp)
    policy_ids.append(resp['detail']['id'])

# Try assigning every customer to every policy
for c_id in customer_ids:

    for p_id in policy_ids:

        data = {
            "customer": c_id,
            "policy": p_id
        }

        resp = requests.post(url=BASE_URL + 'customer_policies/', data=json.dumps(data), headers=HEADERS).json()
        print(resp)
