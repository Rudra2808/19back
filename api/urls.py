from django.urls import path
from .views import (
    RegisterUserView, PropertyListCreateView, RentalDetailView,
    TransactionListView, MessageListCreateView,UserListView, LoginUserView,
    add_to_wishlist,get_wishlist,PropertyDetailView,predict_price,predict_rent,
    seller_properties,CallbackCreateView
)
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('properties/', PropertyListCreateView.as_view(), name='property-list'),
    path('rental/<int:pk>/', RentalDetailView.as_view(), name='rental-detail'),
    path('transactions/', TransactionListView.as_view(), name='transactions'),
    path('messages/', MessageListCreateView.as_view(), name='messages'),
    path('users/', UserListView.as_view(), name='user-list'),  # 👈 Add this line
    path('properties/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('wishlist/', get_wishlist),
    path('predict-price/', predict_price, name='predict-price'),
    path('predict-rent/', predict_rent, name='predict-rent'),
    path("wishlist/add/", add_to_wishlist, name="add_to_wishlist"),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('properties/seller/<str:username>/', seller_properties),
    path('callback/', CallbackCreateView.as_view(), name='callback-create'),
    path('callbacks/seller/<str:username>/', views.get_all_callbacks),
    path('properties/<int:pk>/remove/', views.remove_property, name='remove-property'),
    path('callbacks/<int:pk>/mark-called/', views.mark_callback_called, name='mark-callback-called'),
    path("wishlist/remove/<int:pk>/", views.remove_from_wishlist, name="remove-from-wishlist"),
    path("properties/<int:pk>/mark-as-rented/", views.mark_as_rented, name="mark-as-rented"),
    path("rentals/seller/<str:username>/", views.seller_rentals, name="seller-rentals"),
    # urls.py
path("rentals/<int:pk>/remove/", views.remove_rental, name="remove-rental"),

    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
