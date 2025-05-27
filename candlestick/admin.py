"""
Admin configuration for stock-related models and candlestick pattern detection models.

This module registers the models with Django's admin interface and defines custom
display settings, filters, and search fields to enhance the admin user experience.

Models registered:
- Stock
- OHLCData
- UpatoxAccessToken
- Various candlestick pattern models (e.g., Hammer, Doji, BullishEngulfing, etc.)
"""

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
    """
    Admin interface for the Stock model.

    Displays basic stock metadata including company name, symbol, and sector.
    """

    list_display = ["id", "company_name", "symbol", "sector", "isin_code"]
    list_filter = ["sector"]
    search_fields = ["company_name", "symbol", "sector"]


@admin.register(OHLCData)
class OHLCDataAdmin(admin.ModelAdmin):
    """
    Admin interface for OHLCData model.

    Used for displaying historical price data for stocks.
    """

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
    """
    Admin interface for UpatoxAccessToken model.

    Displays the current stored access token used for Upstox API integration.
    """

    list_display = ["token"]


@admin.register(Hammer)
class HammerAdmin(admin.ModelAdmin):
    """
    Admin interface for Hammer candlestick pattern model.

    Used to review pattern detection records for Hammer pattern.
    """

    list_display = ["data_date", "stock"]


@admin.register(InvertedHammer)
class InvertedHammerAdmin(admin.ModelAdmin):
    """
    Admin interface for Inverted Hammer candlestick pattern model.
    """

    list_display = ["data_date", "stock"]


@admin.register(Doji)
class DojiAdmin(admin.ModelAdmin):
    """
    Admin interface for Doji candlestick pattern model.
    """

    list_display = ["data_date", "stock"]


@admin.register(SpinningTopBottom)
class SpinningTopBottomAdmin(admin.ModelAdmin):
    """
    Admin interface for Spinning Top Bottom candlestick pattern model.
    """

    list_display = ["data_date", "stock"]


@admin.register(ProGapPositive)
class ProGapPositiveAdmin(admin.ModelAdmin):
    """
    Admin interface for Pro Gap Positive candlestick pattern model.
    """

    list_display = ["data_date", "stock"]


@admin.register(BullishEngulfing)
class BullishEngulfingAdmin(admin.ModelAdmin):
    """
    Admin interface for Bullish Engulfing candlestick pattern model.
    """

    list_display = ["data_date", "stock"]


@admin.register(BearishEngulfing)
class BearishEngulfingAdmin(admin.ModelAdmin):
    """
    Admin interface for Bearish Engulfing candlestick pattern model.
    """

    list_display = ["data_date", "stock"]


@admin.register(BullishKicker)
class BullishKickerAdmin(admin.ModelAdmin):
    """
    Admin interface for Bullish Kicker candlestick pattern model.
    """

    list_display = ["data_date", "stock"]


@admin.register(BearishKicker)
class BearishKickerAdmin(admin.ModelAdmin):
    """
    Admin interface for Bearish Kicker candlestick pattern model.
    """

    list_display = ["data_date", "stock"]
