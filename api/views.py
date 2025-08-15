from rest_framework import generics
from .models import UserIdentity, Property, Rental, Transaction, Message
from .serializers import (
    UserIdentitySerializer, PropertySerializer,
    RentalSerializer, TransactionSerializer, MessageSerializer
)
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.response import Response    
from rest_framework import status
from .serializers import UserIdentitySerializer

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserIdentitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Registration
class RegisterUserView(generics.CreateAPIView):
    queryset = UserIdentity.objects.all()
    serializer_class = UserIdentitySerializer

# Properties: List and Create
# Properties: List and Create
# class PropertyListCreateView(generics.ListCreateAPIView):
#     queryset = Property.objects.all()
#     serializer_class = PropertySerializer
#     print('1')
#     def create(self, request, *args, **kwargs):
#         print('2')
#         username = request.data.get('listed_by')
#         try:
#             user = UserIdentity.objects.get(username=username)
#         except UserIdentity.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

#         if user.role != 'seller':
#             return Response({"error": "Only sellers can add properties."}, status=status.HTTP_403_FORBIDDEN)

#         # ✅ Convert username to ID
#         data = request.data.copy()
#         print(data)
#         data['listed_by'] = user.pk  

#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

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

        # ✅ Just pass through the request — DRF SlugRelatedField will handle username lookup
        return super().create(request, *args, **kwargs)


# Rental Details
class RentalDetailView(generics.RetrieveUpdateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

# Transactions List
class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

# Messaging
class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class UserListView(generics.ListAPIView):
    queryset = UserIdentity.objects.all()
    serializer_class = UserIdentitySerializer



class LoginUserView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        role=request.data.get('role')
        # print(role)
        # print('hello1')
        try:
            user = UserIdentity.objects.get(username=username)
            if check_password(password, user.password):
                return Response({
    "message": "Login successful",
    "username": user.username,
    "first_name": user.first_name,
    "last_name": user.last_name,
    "email": user.email,
    "role": user.role  # ✅ Include this
}, status=200)
            else:
                return Response({"message": "Invalid password"}, status=400)
        except UserIdentity.DoesNotExist:
            return Response({"message": "User not found"}, status=404)


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import UserIdentity
# import json

# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         username = data.get('username')
#         password = data.get('password')

#         try:
#             user = UserIdentity.objects.get(username=username)
#             from django.contrib.auth.hashers import check_password
#             if check_password(password, user.password):
#                 return JsonResponse({
#                     'username': user.username,
#                     'first_name': user.first_name,
#                     'last_name': user.last_name,
#                     'email': user.email
#                 })
#             else:
#                 return JsonResponse({'error': 'Invalid credentials'}, status=400)
#         except UserIdentity.DoesNotExist:
#             return JsonResponse({'error': 'User not found'}, status=400)


from rest_framework import generics
from .models import Property
from .serializers import PropertySerializer
from rest_framework.permissions import IsAuthenticated

class PropertyDetailView(generics.RetrieveAPIView):
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
    username = request.GET.get('username')  # e.g., ?username=john123
    if username:
        wishlist_items = Wishlist.objects.filter(username__username=username)
    else:
        wishlist_items = Wishlist.objects.all()

    data = []
    for item in wishlist_items:
        data.append({
            "id": item.id,
            "address": item.property.address,
            "title": item.property.title,
            "price": item.property.price,
            "image": item.property.image.url if item.property.image else None
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
# views.py
import joblib
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Load the model
model = joblib.load("price_prediction_model.pkl")

@api_view(["POST"])
def predict_price(request):
    try:
        data = request.data
        features = np.array([[
            data.get("area_sqft"),
            data.get("bedrooms"),
            data.get("bathrooms"),
            data.get("floors"),
            data.get("balcony_sqft"),
            data.get("year_built"),
            data.get("parking_spaces"),
            data.get("amenities_score"),
            data.get("nearby_schools_km"),
            data.get("nearby_hospital_km"),
            data.get("nearby_metro_km"),
            data.get("crime_rate"),
            data.get("air_quality_index"),
            data.get("market_trend_score")
        ]], dtype=float)

        prediction = model.predict(features)[0]
        return Response({"predicted_price": round(prediction, 2)})

    except Exception as e:
        return Response({"error": str(e)}, status=400)


# api/views.py
# api/views.py
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

# Load the model once when this module loads
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
        images = request.FILES.getlist('images')  # multiple files from frontend
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
                seller=prop.listed_by  # Automatically link seller from property
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