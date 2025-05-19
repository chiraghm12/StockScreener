import csv
import io
import logging

import requests
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import parsers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from stock_screener.settings import (
    ACCESS_TOKEN_URL,
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRCT_URL,
)

from .models import Stock, UpatoxAccessToken


def home_view(request):
    return render(request=request, template_name="home.html")


def candlestickpatterns_view(request):
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
    return render(
        request=request, template_name="patterns.html", context={"pattern": patterns}
    )


def upstox_authentication_view(request):
    url = f"https://api.upstox.com/v2/login/authorization/dialog?client_id={CLIENT_ID}&redirect_uri={REDIRCT_URL}"
    return HttpResponseRedirect(url)


class UploadStockDataView(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request):
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
                    )
                    stock.save()
                    created_objects.append(
                        {
                            "company_name": stock.company_name,
                            "symbol": stock.symbol,
                            "sector": stock.sector,
                        }
                    )
                logger.info("Stock Data Uploded Successfully")
                return Response(
                    {
                        "Status": "Success",
                        "created_count": len(created_objects),
                        "created_objects": created_objects,
                    },
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:
            logger.error(e, exc_info=True)
            response_data = {"Status": "Failure", "Error": str(e.__str__())}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def upstox_authentication_success(request):
    print(request)
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
