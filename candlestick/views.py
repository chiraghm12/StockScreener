"""
Module: views.py

Handles stock-related views including uploading stock data, refreshing OHLC candlestick data, and
managing Upstox authentication for a Django-based stock screener application.
"""

import csv
import io
import logging
import time
from datetime import datetime

import requests
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from rest_framework import parsers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from stock_screener.settings import (
    ACCESS_TOKEN_URL,
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRCT_URL,
)

from .models import OHLCData, Stock, UpatoxAccessToken


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
                    logger.info(
                        f"Data for {stock.symbol} fetched"
                    )  # pylint: disable=W1203
            # sleep half second in between
            time.sleep(0.5)
        logger.info("OHLC Data fetched Successfully")
        return "Success"
    except Exception as e:  # pylint: disable=W0718
        logger.error(f"Error : {e}", exc_info=True)  # pylint: disable=W1203
        return "Error"


def home_view(request):
    """
    Renders the homepage.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered home.html page.
    """
    return render(request=request, template_name="home.html")


@csrf_protect
def candlestickpatterns_view(request):
    """
    Handles GET and POST requests for the candlestick patterns page.
    On POST, triggers data fetching from Upstox API and displays status messages via session.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered patterns.html page with patterns and result message.
    """
    patterns = [
        "Hammer",
        "Inverted Hammer",
        "Doji",
        "Spinning Top Bottom",
        "Pro Gap Positive",
        "Bullish Kicker",
        "Bullish Engulfing",
        "Bearish Kicker",
        "Bearish Engulfing",
    ]
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if start_date and end_date:
            if start_date.strip() and end_date.strip():
                result = refresh_candlestick_data(
                    start_date=start_date, end_date=end_date
                )
                # Store result in session temporarily
                request.session["result"] = result
                return redirect(reverse("CandleStick"))

    # This is the GET section — safely renders the page
    result = request.session.pop("result", None)
    message = None
    if result:
        message = (
            "Data Fetched Successfully!!"
            if result == "Success"
            else "Something went wrong!!"
        )

    return render(
        request=request,
        template_name="patterns.html",
        context={"pattern": patterns, "result": result, "message": message},
    )


def upstox_authentication_view(request):
    """
    Redirects the user to Upstox authentication URL to authorize the app.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirect to Upstox login page.
    """
    url = f"https://api.upstox.com/v2/login/authorization/dialog?client_id={CLIENT_ID}&redirect_uri={REDIRCT_URL}"
    return HttpResponseRedirect(url)


class UploadStockDataView(APIView):
    """
    API View to handle uploading and storing stock data (Nifty 500) via a CSV file.
    """

    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request):
        """
        Handles POST request to upload stock data from a CSV file.
        Clears existing stock data and replaces it with the uploaded data.

        Args:
            request (HttpRequest): The HTTP request object with the CSV file.

        Returns:
            Response: JSON response with upload status and created objects.
        """
        logger = logging.getLogger("upload_data_logger")
        try:
            with transaction.atomic():
                csv_file = request.FILES.get("file")

                if not csv_file:
                    return Response(
                        {"Status": "Failure", "Message": "CSV file not provided"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not csv_file.name.endswith(".csv"):
                    return Response(
                        {"Status": "Failure", "Message": "File is not a CSV"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                decoded_file = csv_file.read().decode("utf-8")
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)

                # Delete all old data
                Stock.objects.all().delete()

                created_objects = []
                for row in reader:
                    stock = Stock(
                        company_name=row.get("Company Name").strip(),
                        symbol=row.get("Symbol").strip(),
                        sector=row.get("Industry").strip(),
                        isin_code=f"NSE_EQ|{row.get("ISIN Code").strip()}",
                    )
                    stock.save()
                    created_objects.append(
                        {
                            "Company_name": stock.company_name,
                            "Symbol": stock.symbol,
                            "Sector": stock.sector,
                            "ISIN_Code": stock.isin_code,
                        }
                    )
                logger.info("Stock(Nifty 500) Data Uploded Successfully")
                return Response(
                    {
                        "Status": "Success",
                        "Created_count": len(created_objects),
                        "Created_objects": created_objects,
                    },
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:  # pylint: disable=W0718
            logger.error(e, exc_info=True)
            response_data = {"Status": "Failure", "Error": str(e)}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def upstox_authentication_success(request):
    """
    Handles redirect from Upstox after successful authentication,
    exchanges authorization code for access token and saves it.

    Args:
        request (HttpRequest): The HTTP request containing the authorization code.

    Returns:
        HttpResponse: Rendered success.html page.
    """
    code = request.GET.get("code", "")

    payload = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRCT_URL,
        "grant_type": "authorization_code",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    response = requests.post(
        ACCESS_TOKEN_URL, headers=headers, data=payload, timeout=120
    )
    access_token = response.json().get("access_token")

    UpatoxAccessToken.objects.create(token=access_token)
    return render(request=request, template_name="success.html")
