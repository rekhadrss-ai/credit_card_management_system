from django.contrib import admin
from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'card_holder', 'card_type', 'masked_number', 'expiry_month', 'expiry_year')
    list_filter = ('card_type',)
    search_fields = ('user__username', 'card_holder', 'last4')