from django.contrib import admin

from .models import OHLCData, Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ["id", "company_name", "symbol", "sector", "symbol_for_use"]
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
