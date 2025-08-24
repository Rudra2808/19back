from django.contrib import admin
from .models import UserIdentity, Property, Rental,PropertyImage,Wishlist,Callback, Agreement

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
    list_display = ("id", "property", "rented_on")

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('username', 'property')


@admin.register(Callback)
class CallbackAdmin(admin.ModelAdmin):
    list_display = ('buyer_name', 'email_id', 'phone_no', 'property', 'seller', 'created_at')
    search_fields = ('buyer_name', 'email_id', 'phone_no', 'property__title', 'seller__username')
    list_filter = ('seller', 'created_at')


@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'created_at', 'pdf_file')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)