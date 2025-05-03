from django.urls import path

from .views import UploadStockDataView, home_view

urlpatterns = [
    path("", home_view, name="Home"),
    path("upload_stock_data", UploadStockDataView.as_view(), name="Upload Stock Data"),
]
