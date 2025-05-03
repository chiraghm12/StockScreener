from rest_framework import serializers

from .models import StockList


class StockListSerializers(serializers.ModelSerializer):
    class Meta:
        model = StockList
        fields = "__all__"
