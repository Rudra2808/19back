from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import UserIdentity, Property, Rental, Transaction, Message, Wishlist,PropertyImage
# from .serializers import PropertyImageSerializer
class UserIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIdentity
        fields = '__all__'

    def validate(self, data):
        password = data.get('password', '').lower()
        username = data.get('username', '').lower()
        first_name = data.get('first_name', '').lower()
        last_name = data.get('last_name', '').lower()

        if username in password or first_name in password or last_name in password:
            raise serializers.ValidationError(
                "Password should not contain personal details like username, first name, or last name."
            )
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']

class PropertySerializer(serializers.ModelSerializer):
    seller_contact = serializers.CharField(source='listed_by.mobile_number', read_only=True)
    seller_first_name = serializers.CharField(source='listed_by.first_name', read_only=True)
    seller_last_name = serializers.CharField(source='listed_by.last_name', read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = '__all__'  # Or list fields explicitly
        extra_fields = ['first_image']

    def get_first_image(self, obj):
        first_img = obj.images.first()
        if first_img and first_img.image:
            return self.context['request'].build_absolute_uri(first_img.image.url)
        return None
    listed_by = serializers.SlugRelatedField(
        slug_field='username',
        queryset=UserIdentity.objects.all()
    )

    class Meta:
        model = Property
        fields = '__all__'
        extra_fields = ['seller_first_name', 'seller_last_name', 'seller_contact']


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source="property.title", read_only=True)
    property_city = serializers.CharField(source="property.city", read_only=True)
    property_price = serializers.DecimalField(
        source="property.price", max_digits=12, decimal_places=2, read_only=True
    )
    property_image = serializers.ImageField(source="property.image", read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "property_title", "property_city", "property_price", "property_image", "added_on"]



from .models import Callback

class CallbackSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source='property.title', read_only=True)

    class Meta:
        model = Callback
        fields = '__all__'
