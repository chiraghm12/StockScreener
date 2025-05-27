from django.contrib import admin

from .models import (
    BearishEngulfing,
    BearishKicker,
    BullishEngulfing,
    BullishKicker,
    Doji,
    Hammer,
    InvertedHammer,
    OHLCData,
    ProGapPositive,
    SpinningTopBottom,
    Stock,
    UpatoxAccessToken,
)


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
    search_fields = ["stock__symbol"]


@admin.register(UpatoxAccessToken)
class UpatoxAccessTokenAdmin(admin.ModelAdmin):
    list_display = ["token"]


@admin.register(Hammer)
class HammerAdmin(admin.ModelAdmin):
    list_display = ["data_date", "stock"]


@admin.register(InvertedHammer)
class InvertedHammerAdmin(admin.ModelAdmin):
    list_display = ["data_date", "stock"]


@admin.register(Doji)
class DojiAdmin(admin.ModelAdmin):
    list_display = ["data_date", "stock"]


@admin.register(SpinningTopBottom)
class SpinningTopBottomAdmin(admin.ModelAdmin):
    list_display = ["data_date", "stock"]


@admin.register(ProGapPositive)
class ProGapPositiveAdmin(admin.ModelAdmin):
    list_display = ["data_date", "stock"]


@admin.register(BullishEngulfing)
class BullishEngulfingAdmin(admin.ModelAdmin):
    list_display = ["data_date", "stock"]


@admin.register(BearishEngulfing)
class BearishEngulfingAdmin(admin.ModelAdmin):
    list_display = ["data_date", "stock"]


@admin.register(BullishKicker)
class BullishKickerAdmin(admin.ModelAdmin):
    list_display = ["data_date", "stock"]


@admin.register(BearishKicker)
class BearishKickerAdmin(admin.ModelAdmin):
    list_display = ["data_date", "stock"]
