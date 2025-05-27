from django.urls import path

from .views import (
    UploadStockDataView,
    candlestickpatterns_view,
    doji_view,
    hammer_view,
    home_view,
    inverted_hammer_view,
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
]
