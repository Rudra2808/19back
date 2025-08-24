from django.urls import path
from .views import (
    RegisterUserView, PropertyListCreateView, RentalDetailView,UserListView, LoginUserView,
    add_to_wishlist,get_wishlist,PropertyDetailView,predict_price,predict_rent,
    seller_properties,CallbackCreateView, UserProfileView, ChangePasswordView
)
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('properties/', PropertyListCreateView.as_view(), name='property-list'),
    path('rental/<int:pk>/', RentalDetailView.as_view(), name='rental-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
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
    path("rentals/<int:pk>/remove/", views.remove_rental, name="remove-rental"),
    path('users/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('users/<str:username>/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('users/<str:username>/forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('agreements/create/', views.create_agreement, name='agreement-create'),
    path('agreements/<int:agreement_id>/upload-pdf/', views.upload_agreement_pdf, name='agreement-upload-pdf'),
    path('agreements/user/<str:username>/', views.list_user_agreements, name='user-agreements'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
