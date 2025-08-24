from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal



class UserIdentity(models.Model):
    ROLE_CHOICES = [
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    ]

    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')  # <--- New field

    id_card_type = models.CharField(max_length=10, choices=[
        ('aadhaar', 'Aadhaar Card'), ('dl', 'Driver Licence'), ('pan', 'PAN Card')
    ], blank=True, null=True)
    id_card_number = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.username


    def clean(self):
        lower_pw = self.password.lower()
        if (
            self.username.lower() in lower_pw or
            self.first_name.lower() in lower_pw or
            self.last_name.lower() in lower_pw
        ):
            raise ValidationError("Password should not be similar to your username, first name, or last name.")

    def save(self, *args, **kwargs):
        self.full_clean()
        from django.contrib.auth.hashers import make_password
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('AP', 'Apartment'),
        ('HS', 'House'),
        ('VL', 'Villa'),
        ('CM', 'Commercial'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    property_type = models.CharField(max_length=2, choices=PROPERTY_TYPE_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    listed_by = models.ForeignKey(UserIdentity, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_rental = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=500, blank=True, null=True, help_text="Google Maps embed URL")

    project_area = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    project_size = models.CharField(max_length=50, blank=True, null=True)
    launch_date = models.CharField(max_length=50, blank=True, null=True)
    avg_price = models.CharField(max_length=50, blank=True, null=True)
    possession_status = models.CharField(max_length=100, blank=True, null=True)
    configuration = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

class Rental(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name="rental")
    tenant_agreement = models.FileField(upload_to="agreements/", null=True, blank=True)
    rented_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Rental for {self.property.title} ({self.property.city})"



class Wishlist(models.Model):
    username = models.ForeignKey("UserIdentity", on_delete=models.CASCADE)
    property = models.ForeignKey("Property", on_delete=models.CASCADE)
    class Meta:
        unique_together = ('username', 'property')  
    def __str__(self):
        return f"{self.username} - {self.property.address}"


class PropertyImage(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property.title}"




class Callback(models.Model):
    buyer_name = models.CharField(max_length=150)
    email_id = models.EmailField()
    phone_no = models.CharField(max_length=20)
    called = models.BooleanField(default=False)  

    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey(UserIdentity, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer_name} - {self.property.title if self.property else 'No property'}"



class Agreement(models.Model):
    user = models.ForeignKey(UserIdentity, on_delete=models.CASCADE, related_name="agreements")
    form_data = models.JSONField()
    title = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("500.00"))
    pdf_file = models.FileField(upload_to="agreements/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Agreement #{self.id} - {self.title or self.user.username}"

