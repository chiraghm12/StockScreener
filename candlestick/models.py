"""
Defines database models for stock information, OHLC data, and candlestick pattern detection.

Models:
- Stock: Basic metadata about companies and their stocks.
- OHLCData: Daily open-high-low-close data for each stock.
- Multiple candlestick pattern models: Used to record the detection of specific patterns on certain dates.
- UpatoxAccessToken: Stores the latest Upstox access token for API authentication.
"""

from django.db import models


# Create your models here.
class Stock(models.Model):
    """
    Represents a stock/company listed on the exchange.

    Fields:
        company_name (str): Full name of the company.
        symbol (str): Ticker symbol of the stock.
        sector (str): Industry sector of the company.
        isin_code (str, optional): International Securities Identification Number.
    """

    company_name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    isin_code = models.CharField(max_length=255, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        """
        String representation of the Stock, using the symbol.
        """
        return str(self.symbol)


class OHLCData(models.Model):
    """
    Stores daily OHLC (Open, High, Low, Close) price data for a stock.

    Fields:
        data_date (date): The date for which the data is recorded.
        open_price (decimal): Opening price.
        close_price (decimal): Closing price.
        high_price (decimal): Highest price.
        low_price (decimal): Lowest price.
        stock (ForeignKey): Reference to the related Stock.
    """

    data_date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="ohlc_data")

    objects = models.Manager()


class Hammer(models.Model):
    """
    Records the detection of a Hammer candlestick pattern for a given stock on a specific date.
    """

    data_date = models.DateField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="hammer")

    objects = models.Manager()


class InvertedHammer(models.Model):
    """
    Records the detection of an Inverted Hammer candlestick pattern.
    """

    data_date = models.DateField()
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="inverted_hammer"
    )

    objects = models.Manager()


class Doji(models.Model):
    """
    Records the detection of a Doji candlestick pattern.
    """

    data_date = models.DateField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="doji")

    objects = models.Manager()


class SpinningTopBottom(models.Model):
    """
    Records the detection of a Spinning Top Bottom candlestick pattern.
    """

    data_date = models.DateField()
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="spinning_top_bottom"
    )

    objects = models.Manager()


class ProGapPositive(models.Model):
    """
    Records the detection of a Pro Gap Positive pattern (gap-up with momentum).
    """

    data_date = models.DateField()
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="pro_gap_positive"
    )

    objects = models.Manager()


class BullishEngulfing(models.Model):
    """
    Records the detection of a Bullish Engulfing candlestick pattern.
    """

    data_date = models.DateField()
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="bullish_engulfing"
    )

    objects = models.Manager()


class BearishEngulfing(models.Model):
    """
    Records the detection of a Bearish Engulfing candlestick pattern.
    """

    data_date = models.DateField()
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="bearish_engulfing"
    )

    objects = models.Manager()


class BullishKicker(models.Model):
    """
    Records the detection of a Bullish Kicker candlestick pattern.
    """

    data_date = models.DateField()
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="bullish_kicker"
    )

    objects = models.Manager()


class BearishKicker(models.Model):
    """
    Records the detection of a Bearish Kicker candlestick pattern.
    """

    data_date = models.DateField()
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="bearish_kicker"
    )

    objects = models.Manager()


class UpatoxAccessToken(models.Model):
    """
    Stores the current access token required for authenticating with the Upstox API.
    """

    token = models.TextField()

    objects = models.Manager()
