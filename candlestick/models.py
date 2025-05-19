from django.db import models


# Create your models here.
class Stock(models.Model):
    company_name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    isin_code = models.CharField(max_length=255, null=True, blank=True)


class OHLCData(models.Model):
    data_date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="ohlc_data")


class Hammer(models.Model):
    data_date = models.DateField()
    stocks = models.ManyToManyField(Stock)


class InvertedHammer(models.Model):
    data_date = models.DateField()
    stocks = models.ManyToManyField(Stock)


class UpatoxAccessToken(models.Model):
    token = models.TextField()
