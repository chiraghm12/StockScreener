"""
Utility module for candlestock app
"""

import logging
import time
from datetime import datetime

import requests

from .models import (
    BearishEngulfing,
    BearishKicker,
    BullishEngulfing,
    BullishKicker,
    Doji,
    Hammer,
    InvertedHammer,
    OHLCData,
    ProGapPositive,
    SpinningTopBottom,
    Stock,
    UpatoxAccessToken,
)


def is_hammer(open_price, high_price, low_price, close_price):
    """
    Method for check if candle is hammer or not.

    Args:
        open_price (float): candle's open price
        high_price (float): candle's high price
        low_price (float): candle's low price
        close_price (float): candle's close price

    Returns:
        bool: True or False
    """
    if open_price == 0 and close_price == 0 and low_price == 0 and high_price == 0:
        return False

    if open_price == close_price == high_price == low_price:
        return False

    body = float(abs(close_price - open_price))  # Real body
    lower_shadow = 0
    upper_shadow = 0
    if close_price > open_price:
        upper_shadow = float(high_price - close_price)
        lower_shadow = float(open_price - low_price)
    else:
        upper_shadow = float(high_price - open_price)
        lower_shadow = float(close_price - low_price)

    if (lower_shadow >= (body * 2)) and (upper_shadow <= (body * 0.5)):
        return True
    return False


def is_inverted_hammer(open_price, high_price, low_price, close_price):
    """
    Method for check if candle is inverted hammer or not.

    Args:
        open_price (float): candle's open price
        high_price (float): candle's high price
        low_price (float): candle's low price
        close_price (float): candle's close price

    Returns:
        bool: True or False
    """
    if open_price == 0 and close_price == 0 and low_price == 0 and high_price == 0:
        return False

    if open_price == close_price == high_price == low_price:
        return False

    body = float(abs(close_price - open_price))  # Real body
    lower_shadow = 0
    upper_shadow = 0
    if close_price > open_price:
        upper_shadow = float(high_price - close_price)
        lower_shadow = float(open_price - low_price)
    else:
        upper_shadow = float(high_price - open_price)
        lower_shadow = float(close_price - low_price)

    if (upper_shadow >= (body * 2)) and (lower_shadow <= (body * 0.5)):
        return True
    return False


def is_spinning_top_bottom(open_price, high_price, low_price, close_price):
    """
    Method for check if candle is spinning top-bottom or not.

    Args:
        open_price (float): candle's open price
        high_price (float): candle's high price
        low_price (float): candle's low price
        close_price (float): candle's close price

    Returns:
        bool: True or False
    """
    if open_price == 0 and close_price == 0 and low_price == 0 and high_price == 0:
        return False

    if open_price == close_price == high_price == low_price:
        return False

    body = float(abs(close_price - open_price))  # Real body
    lower_shadow = 0
    upper_shadow = 0

    if close_price > open_price:
        upper_shadow = float(high_price - close_price)
        lower_shadow = float(open_price - low_price)
    else:
        upper_shadow = float(high_price - open_price)
        lower_shadow = float(close_price - low_price)

    if (lower_shadow >= body * 1.5) and (upper_shadow >= body * 1.5):
        return True

    return False


def is_doji(open_price, high_price, low_price, close_price):
    """
    Method for check if candle is doji or not.

    Args:
        open_price (float): candle's open price
        high_price (float): candle's high price
        low_price (float): candle's low price
        close_price (float): candle's close price

    Returns:
        bool: True or False
    """
    if open_price == close_price == high_price == low_price:
        return False

    if open_price == close_price:
        return True

    return False


def is_bullish_engulfing(first_candle, second_candle):
    """
    Method for bullish engulfing candle stick pattern.
    """

    # first_high = first_candle.get("high_price")
    # first_low = first_candle.get("low_price")
    first_open = first_candle.get("open_price")
    first_close = first_candle.get("close_price")

    # second_high = second_candle.get("high_price")
    # second_low = second_candle.get("low_price")
    second_open = second_candle.get("open_price")
    second_close = second_candle.get("close_price")

    # Check if the first candle is bearish
    is_first_bearish = first_close < first_open

    # Check if the second candle is bullish
    is_second_bullish = second_close > second_open

    # Check if the second candle engulfs the first candle
    is_engulfing = (second_open <= first_close) and (second_close >= first_open)

    # Return True if all conditions are met
    return is_first_bearish and is_second_bullish and is_engulfing


def is_bearish_engulfing(first_candle, second_candle):
    """
    Method for bearish engulfing candle stick pattern.
    """

    # first_high = first_candle.get("high_price")
    # first_low = first_candle.get("low_price")
    first_open = first_candle.get("open_price")
    first_close = first_candle.get("close_price")

    # second_high = second_candle.get("high_price")
    # second_low = second_candle.get("low_price")
    second_open = second_candle.get("open_price")
    second_close = second_candle.get("close_price")

    # Check if the first candle is bullish
    is_first_bullish = first_close > first_open

    # Check if the second candle is bearish
    is_second_bearish = second_close < second_open

    # Check if the second candle engulfs the first candle
    is_engulfing = (second_open >= first_close) and (second_close <= first_open)

    # Return True if all conditions are met
    return is_first_bullish and is_second_bearish and is_engulfing


def is_bullish_kicker(first_candle, second_candle):
    """
    Method for bullish kicker candle stick pattern.
    """
    first_high = first_candle.get("high_price")
    # first_low = first_candle.get("low_price")
    first_open = first_candle.get("open_price")
    first_close = first_candle.get("close_price")

    # second_high = second_candle.get("high_price")
    second_low = second_candle.get("low_price")
    second_open = second_candle.get("open_price")
    second_close = second_candle.get("close_price")

    # check if the first candle is bearish
    is_first_bearish = first_close < first_open

    # check if the second candle is bullish
    is_second_bullish = second_close > second_open

    # No overlap in prices
    no_overlap = first_high <= second_low

    return is_first_bearish and is_second_bullish and no_overlap


def is_bearish_kicker(first_candle, second_candle):
    """
    Method for bearish kicker candle stick pattern.
    """
    # first_high = first_candle.get("high_price")
    first_low = first_candle.get("low_price")
    first_open = first_candle.get("open_price")
    first_close = first_candle.get("close_price")

    second_high = second_candle.get("high_price")
    # second_low = second_candle.get("low_price")
    second_open = second_candle.get("open_price")
    second_close = second_candle.get("close_price")

    # check if the first candle is bullish
    is_first_bullish = first_close > first_open

    # check if the second candle is bearish
    is_second_bearish = second_close < second_open

    # No overlap in prices
    no_overlap = first_low >= second_high

    return is_first_bullish and is_second_bearish and no_overlap


def is_pro_gap_positive(first_candle, second_candle):
    """
    Method for bearish kicker candle stick pattern.
    """
    # first_high = first_candle.get("high_price")
    # first_low = first_candle.get("low_price")
    first_open = first_candle.get("open_price")
    first_close = first_candle.get("close_price")

    # second_high = second_candle.get("high_price")
    # second_low = second_candle.get("low_price")
    second_open = second_candle.get("open_price")
    second_close = second_candle.get("close_price")

    # check if the first candle is bearish
    is_first_bearish = first_close < first_open

    # check if the second candle is bullish
    is_second_bullish = second_close > second_open

    # condition for pro gap
    gap_positive = second_open > first_close

    return is_first_bearish and is_second_bullish and gap_positive


def identify_single_candle_pattern():
    logger = logging.getLogger("stock_screener_logger")
    ohlc_data = OHLCData.objects.filter(data_date=datetime.today())
    hammers = []
    inverted_hammers = []
    dojis = []
    spinning_top_bottoms = []

    logger.info("Single CandleStick data loading started..")

    # delete old data
    Hammer.objects.all().delete()
    InvertedHammer.objects.all().delete()
    Doji.objects.all().delete()
    SpinningTopBottom.objects.all().delete()
    logger.info("Old data deleted.")

    for ohlc in ohlc_data:
        if is_hammer(
            open_price=ohlc.open_price,
            close_price=ohlc.close_price,
            high_price=ohlc.high_price,
            low_price=ohlc.low_price,
        ):
            hammers.append(Hammer(data_date=ohlc.data_date, stock=ohlc.stock))
        if is_inverted_hammer(
            open_price=ohlc.open_price,
            close_price=ohlc.close_price,
            high_price=ohlc.high_price,
            low_price=ohlc.low_price,
        ):
            inverted_hammers.append(
                InvertedHammer(data_date=ohlc.data_date, stock=ohlc.stock)
            )
        if is_doji(
            open_price=ohlc.open_price,
            close_price=ohlc.close_price,
            high_price=ohlc.high_price,
            low_price=ohlc.low_price,
        ):
            dojis.append(Doji(data_date=ohlc.data_date, stock=ohlc.stock))
        if is_spinning_top_bottom(
            open_price=ohlc.open_price,
            close_price=ohlc.close_price,
            high_price=ohlc.high_price,
            low_price=ohlc.low_price,
        ):
            spinning_top_bottoms.append(
                SpinningTopBottom(data_date=ohlc.data_date, stock=ohlc.stock)
            )
    if hammers:
        Hammer.objects.bulk_create(hammers, batch_size=200)
    if inverted_hammers:
        InvertedHammer.objects.bulk_create(inverted_hammers, batch_size=200)
    if dojis:
        Doji.objects.bulk_create(dojis, batch_size=200)
    if spinning_top_bottoms:
        SpinningTopBottom.objects.bulk_create(spinning_top_bottoms, batch_size=1000)

    logger.info("Single CandleStick data loading finished")


def identify_double_candle_pattern(start_date, end_date):
    logger = logging.getLogger("stock_screener_logger")
    ohlc_data = OHLCData.objects.filter()
    pro_gap_positive = []
    bullish_engulfing = []
    bearish_engulfing = []
    bullish_kicker = []
    bearish_kicker = []

    logger.info("Double CandleStick data loading started..")

    # delete old data
    ProGapPositive.objects.all().delete()
    BullishEngulfing.objects.all().delete()
    BearishEngulfing.objects.all().delete()
    BullishKicker.objects.all().delete()
    BearishKicker.objects.all().delete()
    logger.info("Old data deleted.")

    today_data = ohlc_data.filter(data_date=end_date)
    yesterday_data = ohlc_data.filter(data_date=start_date)

    for ohlc_today in today_data:
        ohlc_yesterday = yesterday_data.filter(stock=ohlc_today.stock)
        first_candle = {
            "open_price": float(ohlc_yesterday[0].open_price),
            "close_price": float(ohlc_yesterday[0].close_price),
            "high_price": float(ohlc_yesterday[0].high_price),
            "low_price": float(ohlc_yesterday[0].low_price),
        }
        second_candle = {
            "open_price": float(ohlc_today.open_price),
            "close_price": float(ohlc_today.close_price),
            "high_price": float(ohlc_today.high_price),
            "low_price": float(ohlc_today.low_price),
        }

        if is_pro_gap_positive(first_candle=first_candle, second_candle=second_candle):
            pro_gap_positive.append(
                ProGapPositive(data_date=ohlc_today.data_date, stock=ohlc_today.stock)
            )
        if is_bullish_engulfing(first_candle=first_candle, second_candle=second_candle):
            bullish_engulfing.append(
                BullishEngulfing(data_date=ohlc_today.data_date, stock=ohlc_today.stock)
            )
        if is_bearish_engulfing(first_candle=first_candle, second_candle=second_candle):
            bearish_engulfing.append(
                BearishEngulfing(data_date=ohlc_today.data_date, stock=ohlc_today.stock)
            )
        if is_bullish_kicker(first_candle=first_candle, second_candle=second_candle):
            bullish_kicker.append(
                BullishKicker(data_date=ohlc_today.data_date, stock=ohlc_today.stock)
            )
        if is_bearish_kicker(first_candle=first_candle, second_candle=second_candle):
            bearish_kicker.append(
                BearishKicker(data_date=ohlc_today.data_date, stock=ohlc_today.stock)
            )

    if pro_gap_positive:
        ProGapPositive.objects.bulk_create(pro_gap_positive, batch_size=100)
    if bullish_engulfing:
        BullishEngulfing.objects.bulk_create(bullish_engulfing, batch_size=100)
    if bearish_engulfing:
        BearishEngulfing.objects.bulk_create(bearish_engulfing, batch_size=100)
    if bullish_kicker:
        BullishKicker.objects.bulk_create(bullish_kicker, batch_size=100)
    if bearish_kicker:
        BearishKicker.objects.bulk_create(bearish_kicker, batch_size=100)

    logger.info("Double CandleStick data loading finished")


def refresh_candlestick_data(start_date, end_date):
    """
    Fetches OHLC (Open, High, Low, Close) candlestick data for all stocks between the given dates
    using the Upstox API and stores them in the database.

    Args:
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        str: "Success" if data was fetched and stored successfully, otherwise "Error".
    """
    logger = logging.getLogger("stock_screener_logger")
    try:
        stocks = Stock.objects.all()
        access_token = UpatoxAccessToken.objects.all()[0].token

        logger.info("OHLC Data fetch Starting..")
        # Delete all old Data
        OHLCData.objects.all().delete()

        for stock in stocks:
            # fetch data from upstox
            url = f"https://api.upstox.com/v3/historical-candle/{stock.isin_code}/days/1/{end_date}/{start_date}"
            headers = {"Accept": "application/json", "Authorization": access_token}
            payload = {}
            response = requests.get(url, headers=headers, data=payload, timeout=120)
            response_data = response.json()

            if response_data.get("status") == "success":
                candle_data = response_data.get("data")
                ohlc_objects = []

                for ohlc in candle_data.get("candles"):
                    ohlc_objects.append(
                        OHLCData(
                            data_date=datetime.fromisoformat(ohlc[0]).date(),
                            open_price=ohlc[1],
                            high_price=ohlc[2],
                            low_price=ohlc[3],
                            close_price=ohlc[4],
                            stock=stock,
                        )
                    )
                if ohlc_objects:
                    # create ohlc data for two days in bulk
                    OHLCData.objects.bulk_create(ohlc_objects, batch_size=100)
                    logger.info(  # pylint: disable=W1203
                        f"Data for {stock.symbol} fetched"
                    )
            # sleep half second in between
            time.sleep(0.5)
        logger.info("OHLC Data fetched Successfully")
        # make candle stck pattern and store it.
        identify_single_candle_pattern()
        identify_double_candle_pattern(start_date=start_date, end_date=end_date)
        return "Success"
    except Exception as e:  # pylint: disable=W0718
        logger.error(f"Error : {e}", exc_info=True)  # pylint: disable=W1203
        return "Error"
