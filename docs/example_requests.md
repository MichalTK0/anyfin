# Customers
## Valid
Data: 
```
{
    "customer_name": "John Doe",
    "customer_income": 5000,
    "customer_debt": 2500,
    "payment_remarks_12m": 0,
    "payment_remarks": 0,
    "customer_age": 18
}
```
Response:
```
{
    "message": "ACCEPT",
    "detail": {
        "id": 1,
        "customer_name": "John Doe",
        "customer_income": "5000.00",
        "customer_debt": "2500.00",
        "payment_remarks_12m": 0,
        "payment_remarks": 0,
        "customer_age": 18
    }
}
```
## Invalid
Data:
```
{
    "customer_name": "John Doe",
    "customer_income": -99999,
    "customer_debt": "test",
    "payment_remarks_12m": 0,
    "payment_remarks": 0,
    "customer_age": 999
}
```
Response:
```
{
    "message": "REJECT",
    "reason": {
        "customer_income": [
            "Ensure this value is greater than or equal to 0."
        ],
        "customer_debt": [
            "A valid number is required."
        ],
        "customer_age": [
            "Ensure this value is less than or equal to 101."
        ]
    }
}
```

# Policies
## Valid
Data:
```
{
    "policy_name": "test",
    "max_income": 50000,
    "min_income": 0,
    "max_debt_ratio": 0.5,
    "max_payment_remarks": 0,
    "max_payment_remarks_12m": 1,
    "min_age": 18,
    "max_age": 80
}
```

Response:
```
{
    "message": "ACCEPT",
    "detail": {
        "id": 1,
        "policy_name": "test",
        "max_income": "50000.00",
        "min_income": "0.00",
        "max_debt_ratio": "0.50",
        "max_payment_remarks": 0,
        "max_payment_remarks_12m": 1,
        "min_age": 18,
        "max_age": 80
    }
}
```
## Invalid
Data:
```
{
    "policy_name": "test",
    "max_income": "fail",
    "min_income": -1000,
    "max_debt_ratio": 0.5,
    "max_payment_remarks": 0,
    "max_payment_remarks_12m": 1,
    "min_age": -222,
    "max_age": 999
}
```

Response:
```
{
    "message": "REJECT",
    "reason": {
        "max_income": [
            "A valid number is required."
        ],
        "min_income": [
            "Ensure this value is greater than or equal to 0."
        ],
        "min_age": [
            "Ensure this value is greater than or equal to 0."
        ],
        "max_age": [
            "Ensure this value is less than or equal to 101."
        ]
    }
}
```

# CustomerPolicies
## Valid
### Accepted Policy
Data:
```
{
    "customer": 2,
    "policy": 2
}
```

Response:
```
{
    "message": "ACCEPT",
    "detail": {
        "id": 5,
        "accepted": true,
        "rejection_reason": null,
        "customer": 2,
        "policy": 2
    }
}
```
### Rejected Policy
Data:
```
{
    "customer": 2,
    "policy": 3
}
```

Response:
```
{
    "message": "REJECT",
    "detail": {
        "id": 6,
        "accepted": false,
        "rejection_reason": "HIGH_DEBT_FOR_INCOME",
        "customer": 2,
        "policy": 3
    },
    "reason": "HIGH_DEBT_FOR_INCOME"
}
```
## Invalid
Data:
```
{
    "customer": 2,
    "policy": 3
}
```
Response:
```
{
    "message": "REJECT",
    "reason": {
        "non_field_errors": [
            "The fields customer, policy must make a unique set."
        ]
    }
}
```