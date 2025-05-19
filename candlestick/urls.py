from django.urls import path

from .views import (
    UploadStockDataView,
    candlestickpatterns_view,
    home_view,
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
]
