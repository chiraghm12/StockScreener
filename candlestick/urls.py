"""
Defines URL routing for the stock analysis application.

Each path is associated with a view that either handles stock data upload,
displays candlestick pattern detections, or manages Upstox authentication.

Paths:
- Home
- Upload OHLC stock data
- Display detected candlestick patterns (e.g., Hammer, Doji, Kicker, Engulfing)
- Upstox authentication flow (start + success redirect)
"""

from django.urls import path

from .views import (
    UploadStockDataView,
    bearish_engulfing_view,
    bearish_kicker_view,
    bullish_engulfing_view,
    bullish_kicker_view,
    candlestickpatterns_view,
    doji_view,
    hammer_view,
    home_view,
    inverted_hammer_view,
    pro_gap_positive_view,
    spinning_top_bottom_view,
    upstox_authentication_success,
    upstox_authentication_view,
)

urlpatterns = [
    path("", home_view, name="Home"),
    path("upload_stock_data", UploadStockDataView.as_view(), name="Upload Stock Data"),
    path("candlestick", candlestickpatterns_view, name="CandleStick"),
    path(
        "upstox-authentication",
        upstox_authentication_view,
        name="upstox_authentication",
    ),
    path(
        "success", upstox_authentication_success, name="upstox_authentication_success"
    ),
    path("hammer", hammer_view, name="Hammer-Page"),
    path("inverted-hammer", inverted_hammer_view, name="Inverted-Hammer-Page"),
    path("doji", doji_view, name="Doji-Page"),
    path(
        "spinning-top-bottom", spinning_top_bottom_view, name="Spinning-Top-Bottom-Page"
    ),
    path("pro-gap-positive", pro_gap_positive_view, name="Pro-Gap-Page"),
    path("bullish-engulfing", bullish_engulfing_view, name="Bullish-Engulfing-Page"),
    path("bearish-engulfing", bearish_engulfing_view, name="Bearish-Engulfing-Page"),
    path("bullish-kicker", bullish_kicker_view, name="Bullish-Kicker-Page"),
    path("bearish-kicker", bearish_kicker_view, name="Bearish-Kicker-Page"),
]
