from django.urls import path
from .views import (
    RegisterUserView, PropertyListCreateView, RentalDetailView,
    TransactionListView, MessageListCreateView,UserListView, LoginUserView
)
from django.conf import settings
from django.conf.urls.static import static
from .views import PropertyDetailView
# from .views import WishlistListCreateView, WishlistDeleteView
from django.urls import path
# from .views import WishlistListCreateView, WishlistDeleteView
from .views import add_to_wishlist,get_wishlist
from . import views
from .views import predict_price,predict_rent
from .views import seller_properties
from .views import CallbackCreateView


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
    # path('wishlist/<int:pk>/', WishlistDeleteView.as_view(), name='wishlist-delete'),
     path("wishlist/add/", add_to_wishlist, name="add_to_wishlist"),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('properties/seller/<str:username>/', seller_properties),
    path('callback/', CallbackCreateView.as_view(), name='callback-create'),
    path('callbacks/seller/<str:username>/', views.get_all_callbacks),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
