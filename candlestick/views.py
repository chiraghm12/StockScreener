import csv
import io
import logging

from django.db import transaction
from django.shortcuts import render
from rest_framework import parsers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import StockList


def home_view(request):
    return render(request=request, template_name="home.html")


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
                StockList.objects.all().delete()

                created_objects = []
                for row in reader:
                    stock = StockList(
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
