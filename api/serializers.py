from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import UserIdentity, Property, Rental, Wishlist,PropertyImage, Agreement
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
        fields = "__all__"
        depth = 1   


class WishlistSerializer(serializers.ModelSerializer):
    property_id = serializers.IntegerField(source="property.id", read_only=True)
    property_title = serializers.CharField(source="property.title", read_only=True)
    property_city = serializers.CharField(source="property.city", read_only=True)
    property_price = serializers.DecimalField(
        source="property.price", max_digits=12, decimal_places=2, read_only=True
    )
    property_image = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields = [
            "id",
            "property_id",  
            "property_title",
            "property_city",
            "property_price",
            "property_image",
            "added_on",
        ]

    def get_property_image(self, obj):
        first_img = obj.property.images.first()
        if first_img and first_img.image:
            return self.context["request"].build_absolute_uri(first_img.image.url)
        return None


from .models import Callback

class CallbackSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source='property.title', read_only=True)

    class Meta:
        model = Callback
        fields = '__all__'



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIdentity
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'mobile_number',
            'role',
            'id_card_type',
            'id_card_number',
        ]
        read_only_fields = ['username', 'role']


class AgreementSerializer(serializers.ModelSerializer):
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Agreement
        fields = '__all__'
        read_only_fields = ['created_at']

    def get_pdf_url(self, obj):
        if obj.pdf_file and hasattr(obj.pdf_file, 'url'):
            request = self.context.get('request')
            url = obj.pdf_file.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None
