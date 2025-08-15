from django.contrib import admin
from .models import UserIdentity, Property, Rental, Transaction, Message,PropertyImage



class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1 

@admin.register(UserIdentity)
class UserIdentityAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'mobile_number')
    search_fields = ('username', 'email')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'city', 'price', 'is_rental', 'is_available')
    list_filter = ('property_type', 'city', 'is_rental')
    search_fields = ('title', 'city')
    inlines = [PropertyImageInline] 

    
@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image')


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('property', 'rent_per_month', 'is_rented', 'lease_duration_months')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'transaction_type', 'amount', 'date')
    list_filter = ('transaction_type',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp')
    search_fields = ('sender__username', 'receiver__username')



from django.contrib import admin
from .models import Wishlist

# @admin.register(Wishlist)
# class WishlistAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'property', 'added_on')
#     list_filter = ('added_on',)
#     search_fields = ('user__username', 'property__address')
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('username', 'property')



from .models import Callback  # Import the Callback model
from django.contrib import admin
from .models import Callback

@admin.register(Callback)
class CallbackAdmin(admin.ModelAdmin):
    list_display = ('buyer_name', 'email_id', 'phone_no', 'property', 'seller', 'created_at')
    search_fields = ('buyer_name', 'email_id', 'phone_no', 'property__title', 'seller__username')
    list_filter = ('seller', 'created_at')
ilter = ('seller_username', 'created_at')