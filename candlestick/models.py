from django.db import models


# Create your models here.
class Stock(models.Model):
    company_name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    isin_code = models.CharField(max_length=255, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.symbol)


class OHLCData(models.Model):
    data_date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="ohlc_data")

    objects = models.Manager()


class Hammer(models.Model):
    data_date = models.DateField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="hammer")

    objects = models.Manager()


class InvertedHammer(models.Model):
    data_date = models.DateField()
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="inverted_hammer"
    )

    objects = models.Manager()


class Doji(models.Model):
    data_date = models.DateField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="doji")

    objects = models.Manager()


class SpinningTopBottom(models.Model):
    data_date = models.DateField()
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="spinning_top_bottom"
    )

    objects = models.Manager()


class ProGapPositive(models.Model):
    data_date = models.DateField()
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="pro_gap_positive"
    )

    objects = models.Manager()


class BullishEngulfing(models.Model):
    data_date = models.DateField()
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="bullish_engulfing"
    )

    objects = models.Manager()


class BearishEngulfing(models.Model):
    data_date = models.DateField()
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="bearish_engulfing"
    )

    objects = models.Manager()


class BullishKicker(models.Model):
    data_date = models.DateField()
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="bullish_kicker"
    )

    objects = models.Manager()


class BearishKicker(models.Model):
    data_date = models.DateField()
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="bearish_kicker"
    )

    objects = models.Manager()


class UpatoxAccessToken(models.Model):
    token = models.TextField()

    objects = models.Manager()
