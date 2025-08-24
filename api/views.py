from rest_framework import generics,status
from .models import UserIdentity, Property, Rental
from .serializers import (
    UserIdentitySerializer, PropertySerializer,
    RentalSerializer, UserProfileSerializer
)
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserIdentitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterUserView(generics.CreateAPIView):
    queryset = UserIdentity.objects.all()
    serializer_class = UserIdentitySerializer


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('listed_by')

        try:
            user = UserIdentity.objects.get(username=username)
        except UserIdentity.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        if user.role != 'seller':
            return Response({"error": "Only sellers can add properties."}, status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)


class RentalDetailView(generics.RetrieveUpdateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

class UserListView(generics.ListAPIView):
    queryset = UserIdentity.objects.all()
    serializer_class = UserIdentitySerializer

class LoginUserView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        role=request.data.get('role')
        
        try:
            user = UserIdentity.objects.get(username=username)
            if check_password(password, user.password):
                return Response({
    "message": "Login successful",
    "username": user.username,
    "first_name": user.first_name,
    "last_name": user.last_name,
    "email": user.email,
    "role": user.role 
}, status=200)
            else:
                return Response({"message": "Invalid password"}, status=400)
        except UserIdentity.DoesNotExist:
            return Response({"message": "User not found"}, status=404)


from rest_framework import generics
from .models import Property
from .serializers import PropertySerializer
from rest_framework.permissions import IsAuthenticated

class PropertyDetailView(generics.RetrieveUpdateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Wishlist, Property, UserIdentity

@api_view(['POST'])
def add_to_wishlist(request):
    username = request.data.get("username")
    property_id = request.data.get("property_id")

    if not username or not property_id:
        return Response({"error": "username and property_id required"}, status=400)

    try:
        user = UserIdentity.objects.get(username=username)
        property_obj = Property.objects.get(id=property_id)
        Wishlist.objects.create(username=user, property=property_obj)
        return Response({"message": "Added to wishlist"})
    except UserIdentity.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except Property.DoesNotExist:
        return Response({"error": "Property not found"}, status=404)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Wishlist

@api_view(['GET'])
def get_wishlist(request):
    username = request.GET.get('username')  
    if username:
        wishlist_items = Wishlist.objects.filter(username__username=username)
    else:
        wishlist_items = Wishlist.objects.all()

    data = []
    for item in wishlist_items:
        first_image = None
        if hasattr(item.property, 'images') and item.property.images.exists():
            first_img = item.property.images.first()
            if first_img and first_img.image:
                first_image = request.build_absolute_uri(first_img.image.url)
        
        data.append({
            "id": item.id,  
            "property_id": item.property.id, 
            "address": item.property.address,
            "title": item.property.title,
            "price": item.property.price,
            "image": first_image, 
            "property_type": item.property.property_type,
            "city": item.property.city,
            "state": item.property.state,
            "is_rental": item.property.is_rental
        })

    return Response(data)


from rest_framework import generics, permissions
from .models import Wishlist
from .serializers import WishlistSerializer

class WishlistListView(generics.ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        username = self.request.query_params.get('username')
        if username:
            return Wishlist.objects.filter(username=username)
        return Wishlist.objects.all()
import joblib
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response

model1 = joblib.load("price_prediction_model.pkl")




@api_view(["POST"])
def predict_price(request):
    try:
        data = request.data
        features = np.array([[
            float(data.get("area_sqft", 0) or 0),
            float(data.get("bedrooms", 0) or 0),
            float(data.get("bathrooms", 0) or 0),
            float(data.get("floors", 0) or 0),
            float(data.get("balcony_sqft", 0) or 0),
            float(data.get("year_built", 0) or 0),
            float(data.get("parking_spaces", 0) or 0),
            float(data.get("amenities_score", 0) or 0),
            float(data.get("nearby_schools_km", 0) or 0),
            float(data.get("nearby_hospital_km", 0) or 0),
            float(data.get("nearby_metro_km", 0) or 0),
            float(data.get("crime_rate", 0) or 0),
            float(data.get("air_quality_index", 0) or 0),
            float(data.get("market_trend_score", 0) or 0),
        ]])
        prediction = model1.predict(features)[0]
        return Response({"predicted_price": round(prediction, 2)})
    except Exception as e:
        return Response({"error": str(e)}, status=400)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Property, UserIdentity
from .serializers import PropertySerializer

@api_view(['GET'])
def seller_properties(request, username):
    try:
        user = UserIdentity.objects.get(username=username)
    except UserIdentity.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    properties = Property.objects.filter(listed_by=user)
    serializer = PropertySerializer(properties, many=True, context={'request': request})
    return Response(serializer.data)



import joblib
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response

model = joblib.load("rent_price_model.pkl")

@api_view(["POST"])
def predict_rent(request):
    try:
        data = request.data
        features = np.array([[
            data.get("area_sqft"),
            data.get("bedrooms"),
            data.get("bathrooms"),
            data.get("floor_number"),
            data.get("total_floors"),
            data.get("balcony_sqft"),
            data.get("parking_spaces"),
            data.get("amenities_score"),
            data.get("nearby_school_km"),
            data.get("nearby_hospital_km"),
            data.get("nearby_metro_km"),
            data.get("crime_rate"),
            data.get("air_quality_index"),
        ]], dtype=float)

        prediction = model.predict(features)[0]
        return Response({"predicted_rent": round(prediction, 2)})

    except Exception as e:
        return Response({"error": str(e)}, status=400)

from .models import PropertyImage

class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def post(self, request, *args, **kwargs):
        images = request.FILES.getlist('images') 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        property_instance = serializer.save()

        for img in images:
            PropertyImage.objects.create(property=property_instance, image=img)

        return Response(self.get_serializer(property_instance).data, status=status.HTTP_201_CREATED)


from .models import Callback
from .serializers import CallbackSerializer,serializers

class CallbackCreateView(generics.CreateAPIView):
    queryset = Callback.objects.all()
    serializer_class = CallbackSerializer

    def perform_create(self, serializer):
        property_id = self.request.data.get('property_id')
        try:
            prop = Property.objects.get(id=property_id)
            serializer.save(
                property=prop,
                seller=prop.listed_by  
            )
        except Property.DoesNotExist:
            raise serializers.ValidationError({"error": "Invalid property ID"})
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Callback
from .serializers import CallbackSerializer

@api_view(['GET'])
def get_all_callbacks(request, username):
    try:
        user = UserIdentity.objects.get(username=username)
    except UserIdentity.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    properties = Callback.objects.filter(seller=user)
    serializer = CallbackSerializer(properties, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
def remove_property(request, pk):
    try:
        property_obj = Property.objects.get(pk=pk)
        property_obj.is_available = False
        property_obj.save()
        return Response({"message": "Property marked as unavailable"})
    except Property.DoesNotExist:
        return Response({"error": "Property not found"}, status=404)


from .models import Callback

@api_view(['POST'])
def mark_callback_called(request, pk):
    try:
        cb = Callback.objects.get(pk=pk)
        cb.called = True
        cb.save()
        return Response({"message": "Callback marked as called"})
    except Callback.DoesNotExist:
        return Response({"error": "Callback not found"}, status=404)



from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['DELETE'])
def remove_from_wishlist(request, pk):
    try:
        from .models import Wishlist
        wishlist_item = Wishlist.objects.get(pk=pk)
        wishlist_item.delete()
        return Response({"message": "Removed from wishlist"}, status=status.HTTP_200_OK)
    except Wishlist.DoesNotExist:
        return Response({"error": "Item not found in wishlist"}, status=status.HTTP_404_NOT_FOUND)



from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def mark_as_rented(request, pk):
    try:
        property_obj = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return Response({"error": "Property not found"}, status=404)

    if hasattr(property_obj, "rental"):
        return Response({"error": "This property is already rented"}, status=400)

    pdf_file = request.FILES.get("agreement")
    if not pdf_file:
        return Response({"error": "PDF file required"}, status=400)

    rental = Rental.objects.create(
        property=property_obj,
        tenant_agreement=pdf_file
    )

    property_obj.is_available = False
    property_obj.save()

    return Response({
        "message": "Property marked as rented",
        "rental_id": rental.id,
        "pdf_url": rental.tenant_agreement.url
    })
from .models import Rental, UserIdentity
from .serializers import RentalSerializer

@api_view(['GET'])
def seller_rentals(request, username):
    try:
        user = UserIdentity.objects.get(username=username)
    except UserIdentity.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    rentals = Rental.objects.filter(property__listed_by=user)
    serializer = RentalSerializer(rentals, many=True, context={'request': request})
    return Response(serializer.data)



@api_view(['DELETE'])
def remove_rental(request, pk):
    try:
        rental = Rental.objects.get(pk=pk)
        property_obj = rental.property

        rental.delete()

        property_obj.is_available = True
        property_obj.save()

        return Response({"message": "Rental removed and property is available again"})
    except Rental.DoesNotExist:
        return Response({"error": "Rental not found"}, status=404)


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserIdentity.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'


class ChangePasswordView(APIView):
    def post(self, request, username):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response({"error": "old_password and new_password are required"}, status=400)

        try:
            user = UserIdentity.objects.get(username=username)
        except UserIdentity.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if not check_password(old_password, user.password):
            return Response({"error": "Old password is incorrect"}, status=400)

        lower_new = new_password.lower()
        if (
            user.username.lower() in lower_new or
            user.first_name.lower() in lower_new or
            user.last_name.lower() in lower_new
        ):
            return Response({"error": "Password should not contain personal details like username, first name, or last name."}, status=400)

        user.password = make_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully"})


class ForgotPasswordView(APIView):
    def post(self, request, username):
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        if not email or not new_password:
            return Response({"error": "email and new_password are required"}, status=400)

        try:
            user = UserIdentity.objects.get(username=username)
        except UserIdentity.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if user.email.lower() != email.lower():
            return Response({"error": "Email does not match our records"}, status=400)

        lower_new = new_password.lower()
        if (
            user.username.lower() in lower_new or
            user.first_name.lower() in lower_new or
            user.last_name.lower() in lower_new
        ):
            return Response({"error": "Password should not contain personal details like username, first name, or last name."}, status=400)

        user.password = make_password(new_password)
        user.save()
        return Response({"message": "Password reset successfully"})


from rest_framework.parsers import MultiPartParser, FormParser
from .models import Agreement
from .serializers import AgreementSerializer

@api_view(['POST'])
def create_agreement(request):
    username = request.data.get('username')
    form_data = request.data.get('form_data')
    title = request.data.get('title')
    if not username or not form_data:
        return Response({"error": "username and form_data are required"}, status=400)

    try:
        user = UserIdentity.objects.get(username=username)
    except UserIdentity.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    past_count = Agreement.objects.filter(user=user).count()
    base_price = 500.0
    discount_pct = min(past_count * 4.0, 40.0) 
    final_amount = round(base_price * (1.0 - discount_pct / 100.0), 2)

    agreement = Agreement.objects.create(user=user, form_data=form_data, amount=final_amount, title=title)
    return Response({
        "agreement_id": agreement.id,
        "base_amount": base_price,
        "discount_percent": discount_pct,
        "final_amount": final_amount,
        "title": agreement.title,
    })


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_agreement_pdf(request, agreement_id):
    try:
        agreement = Agreement.objects.get(id=agreement_id)
    except Agreement.DoesNotExist:
        return Response({"error": "Agreement not found"}, status=404)

    pdf_file = request.FILES.get('file')
    if not pdf_file:
        return Response({"error": "PDF file is required"}, status=400)

    agreement.pdf_file = pdf_file
    agreement.save()
    return Response({"message": "PDF uploaded", "pdf_url": agreement.pdf_file.url})


@api_view(['GET'])
def list_user_agreements(request, username):
    try:
        user = UserIdentity.objects.get(username=username)
    except UserIdentity.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    agreements = Agreement.objects.filter(user=user).order_by('-created_at')
    serializer = AgreementSerializer(agreements, many=True, context={'request': request})
    return Response(serializer.data)

