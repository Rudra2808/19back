from django.test import TestCase
from .models import UserIdentity, Property, Rental

class UserIdentityTestCase(TestCase):
    def setUp(self):
        self.user = UserIdentity.objects.create(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            mobile_number="1234567890",
            password="SecureP@ss123"
        )

    def test_user_created(self):
        self.assertEqual(self.user.username, "john_doe")

class PropertyTestCase(TestCase):
    def setUp(self):
        self.user = UserIdentity.objects.create(
            username="seller",
            first_name="Seller",
            last_name="Example",
            email="seller@example.com",
            mobile_number="9999999999",
            password="SellerP@ss"
        )
        self.property = Property.objects.create(
            title="Sea View Apartment",
            description="Luxury flat near beach.",
            price=12000000.00,
            property_type='AP',
            address="123 Beach Street",
            city="Goa",
            state="Goa",
            zip_code="403001",
            listed_by=self.user,
            is_available=True,
            is_rental=True
        )

    def test_property_listing(self):
        self.assertEqual(self.property.city, "Goa")

class RentalTestCase(TestCase):
    def setUp(self):
        self.user = UserIdentity.objects.create(
            username="renter",
            first_name="Renter",
            last_name="Test",
            email="renter@example.com",
            mobile_number="8888888888",
            password="RenterP@ss"
        )
        self.property = Property.objects.create(
            title="Rental House",
            description="A house for rent.",
            price=15000.00,
            property_type='HS',
            address="456 Local Lane",
            city="Pune",
            state="Maharashtra",
            zip_code="411001",
            listed_by=self.user,
            is_available=True,
            is_rental=True
        )
        self.rental = Rental.objects.create(
            property=self.property,
            rent_per_month=15000.00,
            security_deposit=30000.00,
            lease_duration_months=12,
            is_rented=False
        )

    def test_rental_created(self):
        self.assertEqual(self.rental.lease_duration_months, 12)
