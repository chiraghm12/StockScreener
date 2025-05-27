"""
Module: views.py

Handles stock-related views including uploading stock data, refreshing OHLC candlestick data, and
managing Upstox authentication for a Django-based stock screener application.
"""

import csv
import io
import logging

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

from .models import (
    BearishEngulfing,
    BearishKicker,
    BullishEngulfing,
    BullishKicker,
    Doji,
    Hammer,
    InvertedHammer,
    ProGapPositive,
    SpinningTopBottom,
    Stock,
    UpatoxAccessToken,
)
from .utils import refresh_candlestick_data


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
        {"name": "Hammer", "uri": "Hammer-Page"},
        {"name": "Inverted Hammer", "uri": "Inverted-Hammer-Page"},
        {"name": "Doji", "uri": "Doji-Page"},
        {"name": "Spinning Top Bottom", "uri": "Spinning-Top-Bottom-Page"},
        {"name": "Pro Gap Positive", "uri": "Pro-Gap-Page"},
        {"name": "Bullish Kicker", "uri": "Bullish-Kicker-Page"},
        {"name": "Bullish Engulfing", "uri": "Bullish-Engulfing-Page"},
        {"name": "Bearish Kicker", "uri": "Bearish-Kicker-Page"},
        {"name": "Bearish Engulfing", "uri": "Bearish-Engulfing-Page"},
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
        context={"patterns": patterns, "result": result, "message": message},
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


def hammer_view(request):
    """
    View to display all Hammer candlestick patterns.

    Retrieves all Hammer instances from the database and renders them
    using the 'hammers.html' template. Passes the patterns and a result flag to the template.
    """
    hammers = Hammer.objects.all()

    return render(
        request=request,
        template_name="hammers.html",
        context={"hammers": hammers, "result": len(hammers) > 0},
    )


def inverted_hammer_view(request):
    """
    View to display all Inverted Hammer candlestick patterns.

    Retrieves all InvertedHammer instances from the database and renders them
    using the 'invertedhammers.html' template.
    """
    hammers = InvertedHammer.objects.all()

    return render(
        request=request,
        template_name="invertedhammers.html",
        context={"hammers": hammers, "result": len(hammers) > 0},
    )


def doji_view(request):
    """
    View to display all Doji candlestick patterns.

    Retrieves all Doji instances and renders them in the 'doji.html' template.
    """
    dojis = Doji.objects.all()

    return render(
        request=request,
        template_name="doji.html",
        context={"dojis": dojis, "result": len(dojis) > 0},
    )


def spinning_top_bottom_view(request):
    """
    View to display all Spinning Top and Bottom candlestick patterns.

    Fetches all SpinningTopBottom instances and renders them using the 'spinningtopbottom.html' template.
    """
    spinning_top_bottoms = SpinningTopBottom.objects.all()

    return render(
        request=request,
        template_name="spinningtopbottom.html",
        context={
            "spinning_top_bottoms": spinning_top_bottoms,
            "result": len(spinning_top_bottoms) > 0,
        },
    )


def pro_gap_positive_view(request):
    """
    View to display all Pro Gap Positive patterns.

    Fetches all ProGapPositive instances and renders them using the 'progaps.html' template.
    """
    pro_gaps = ProGapPositive.objects.all()

    return render(
        request=request,
        template_name="progaps.html",
        context={"pro_gaps": pro_gaps, "result": len(pro_gaps) > 0},
    )


def bullish_engulfing_view(request):
    """
    View to display all Bullish Engulfing candlestick patterns.

    Retrieves all BullishEngulfing instances and displays them via the 'bullishengulfing.html' template.
    """
    bullish_engulfings = BullishEngulfing.objects.all()

    return render(
        request=request,
        template_name="bullishengulfing.html",
        context={
            "bullish_engulfings": bullish_engulfings,
            "result": len(bullish_engulfings) > 0,
        },
    )


def bearish_engulfing_view(request):
    """
    View to display all Bearish Engulfing candlestick patterns.

    Retrieves all BearishEngulfing instances and renders them using the 'bearishengulfing.html' template.
    """
    bearish_engulfings = BearishEngulfing.objects.all()

    return render(
        request=request,
        template_name="bearishengulfing.html",
        context={
            "bearish_engulfings": bearish_engulfings,
            "result": len(bearish_engulfings) > 0,
        },
    )


def bullish_kicker_view(request):
    """
    View to display all Bullish Kicker candlestick patterns.

    Fetches all BullishKicker instances and renders them with the 'bullishkicker.html' template.
    """
    bullish_kickers = BullishKicker.objects.all()

    return render(
        request=request,
        template_name="bullishkicker.html",
        context={
            "bullish_kickers": bullish_kickers,
            "result": len(bullish_kickers) > 0,
        },
    )


def bearish_kicker_view(request):
    """
    View to display all Bearish Kicker candlestick patterns.

    Fetches all BearishKicker instances and renders them with the 'bearishkicker.html' template.
    """
    bearish_kickers = BearishKicker.objects.all()

    return render(
        request=request,
        template_name="bearishkicker.html",
        context={
            "bearish_kickers": bearish_kickers,
            "result": len(bearish_kickers) > 0,
        },
    )
