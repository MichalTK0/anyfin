import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "anyfin_project.settings")
django.setup()

from credit_app.models import Customer, Policy, CustomerPolicy


def clean_models():
    CustomerPolicy.objects.all().delete()
    Policy.objects.all().delete()
    Customer.objects.all().delete()


if __name__ == "__main__":
    print("DB Clean Running")
    clean_models()
    print("Cleaned!")
