from django.contrib import admin
from .models import Cryptocurrency, PriceHistory, SearchHistory

@admin.register(Cryptocurrency)
class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'coin_id', 'created_at']
    search_fields = ['name', 'symbol', 'coin_id']
    readonly_fields = ['created_at']

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['cryptocurrency', 'price_usd', 'market_cap', 'volume_24h', 'timestamp']
    list_filter = ['cryptocurrency', 'timestamp']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['cryptocurrency', 'user', 'searched_at']
    list_filter = ['cryptocurrency', 'searched_at']
    readonly_fields = ['searched_at']
    ordering = ['-searched_at']