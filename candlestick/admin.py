from django.contrib import admin

from .models import StockList


@admin.register(StockList)
class StockListAdmin(admin.ModelAdmin):
    list_display = ["id", "company_name", "symbol", "sector", "symbol_for_use"]
    list_filter = ["sector"]
    search_fields = ["company_name", "symbol", "sector"]
