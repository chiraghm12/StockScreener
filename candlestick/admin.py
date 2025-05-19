from django.contrib import admin

from .models import Hammer, InvertedHammer, OHLCData, Stock, UpatoxAccessToken


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ["id", "company_name", "symbol", "sector", "isin_code"]
    list_filter = ["sector"]
    search_fields = ["company_name", "symbol", "sector"]


@admin.register(OHLCData)
class OHLCDataAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "data_date",
        "stock",
        "open_price",
        "close_price",
        "high_price",
        "low_price",
    ]
    list_filter = ["data_date", "stock"]
    search_fields = ["stock"]


@admin.register(UpatoxAccessToken)
class UpatoxAccessTokenAdmin(admin.ModelAdmin):
    list_display = ["token"]


@admin.register(Hammer)
class HammerAdmin(admin.ModelAdmin):
    list_display = ["data_date"]


@admin.register(InvertedHammer)
class InvertedHammerAdmin(admin.ModelAdmin):
    list_display = ["data_date"]
