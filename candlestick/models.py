from django.db import models


# Create your models here.
class StockList(models.Model):
    company_name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
