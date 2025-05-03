from django.db import models


# Create your models here.
class StockList(models.Model):
    company_name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    symbol_for_use = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.symbol_for_use = f"{self.symbol}.NS"
        return super().save(*args, **kwargs)
