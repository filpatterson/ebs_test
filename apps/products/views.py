from drf_util.views import BaseViewSet, BaseCreateModelMixin, BaseListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.decorators import api_view

import datetime

from django.shortcuts import get_object_or_404

from apps.products.models import Product, PriceInterval
from apps.products.serializers import ProductSerializer, PriceIntervalSerializer

from collections import namedtuple


# nt = namedtuple("object", ['model', 'serializers'])
# pattern = {
#     "product": nt(Product, ProductSerializer),
#     "price_interval": nt(PriceInterval, PriceIntervalSerializer)
# }

# @api_view(['GET', 'POST'])
# def ListView(request, api_name):
#     object = pattern.get(api_name, None)
#     if object == None:
#         #   if no object found then throw not found response to user
#         return Response(
#             data = 'invalid URL',
#             status = status.HTTP_404_NOT_FOUND
#         )

#     if request.method == "GET":
#         object_list = object.model.objects.all()
#         serializers = object.serializers(object_list, many=True)
#         return Response(serializers.data)
#     if request.method == "POST":
#         data = request.data
#         serializers = object.serializers(data=data)

#         if not serializers.is_valid():
#             #   throw error if given POST request has incorrect data
#             return Response(
#                 data = serializers.error,
#                 status = status.HTTP_404_NOT_FOUND
#             )
#         serializers.save()
#         return Response(
#             data = serializers.error,
#             status = status.HTTP_201_CREATED
#         )

class ProductViewSet(BaseListModelMixin, BaseCreateModelMixin, BaseViewSet):
    permission_classes = AllowAny,
    authentication_classes = ()
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    @action(detail=True, methods=['post'])
    def post(self, request):
        """POST handler, creates new product using given data
        :param request: request to be handled
        """
        product = request.data.get('product')

        #   serializer is able to check if given request data is valid or not
        serializer = ProductSerializer(data=product)
        if serializer.is_valid():
            product_saved = serializer.save()
            return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def get(self):
        """GET handler, gives all products in a list form
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"articles": serializer.data})

    @action(detail=True, methods=['put'])
    def put(self, request, pk):
        saved_product = get_object_or_404(Product.objects.all(), pk=pk)
        data = request.data.get('product')
        serializer = ProductSerializer(instance=saved_product, data=data, partial=True)
        if serializer.is_valid():
            saved_product = serializer.save()
        return Response(status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk):
        product = get_object_or_404(Product.objects.all(), pk=pk)
        product.delete()
        return Response(status.HTTP_200_OK)


class ProductPriceViewSet(BaseListModelMixin, BaseCreateModelMixin, BaseViewSet):
    permission_classes = AllowAny,
    authentication_classes = ()
    serializer_class = PriceIntervalSerializer
    queryset = PriceInterval.objects.all()

    @action(detail=True, methods=['post'])
    def post(self, request):
        """POST handler, creates new product using given data
        :param request: request to be handled
        """
        price = request.data.get('product_price')

        #   serializer is able to check if given request data is valid or not
        serializer = ProductSerializer(data=price)
        if serializer.is_valid():
            price_saved = serializer.save()
            return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def get_average_price(self, request, pk):
        # product = request.data.get("product")
        product = int(pk)
        start_time = datetime.datetime.strptime(request.data.get("start_date"), "%Y-%M-%d").date()
        end_time = datetime.datetime.strptime(request.data.get("end_date"), "%Y-%M-%d").date()

        all_price_intervals = PriceInterval.objects.all()
        found_price_intervals = []
        intervals_days = []
        intervals_prices = []
        for price_interval in all_price_intervals:
            if price_interval.product.id == product:
                found_price_intervals.append(price_interval)

        found_price_intervals = sorted(found_price_intervals, key=lambda interval: interval.start_date)

        is_start_found = False
        if start_time <= found_price_intervals[0].start_date:
            is_start_found = True

        for price_interval in found_price_intervals:
            if is_start_found:
                if price_interval.is_in_between(end_time):
                    intervals_prices.append(price_interval.price)
                    intervals_days.append(price_interval.get_days(end_date=end_time))
                    break
                else:
                    intervals_prices.append(price_interval.price)
                    intervals_days.append(price_interval.get_days())
            if not is_start_found:
                if price_interval.is_in_between(start_time):
                    is_start_found = True
                    if price_interval.is_in_between(end_time):
                        intervals_prices.append(price_interval.price)
                        intervals_days.append(price_interval.get_days(start_time, end_time))
                        break
                    else:
                        intervals_prices.append(price_interval.price)
                        intervals_days.append(price_interval.get_days(start_date=start_time))

        time_weighted_price = 0
        for index in range(len(intervals_prices)):
            time_weighted_price += intervals_prices[index] * intervals_days[index]

        print(time_weighted_price / sum(intervals_days))




    @action(detail=True, methods=['get'])
    def get(self):
        """GET handler, gives all products in a list form
        """
        prices = PriceInterval.objects.all()
        serializer = ProductSerializer(prices, many=True)
        return Response({"articles": serializer.data})

    @action(detail=True, methods=['put'])
    def put(self, request, pk):
        saved_price_interval = get_object_or_404(PriceInterval.objects.all(), pk=pk)
        data = request.data.get('product')
        serializer = ProductSerializer(instance=saved_price_interval, data=data, partial=True)
        if serializer.is_valid():
            saved_price_interval = serializer.save()
        return Response(status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk):
        price_interval = get_object_or_404(Product.objects.all(), pk=pk)
        price_interval.delete()
        return Response(status.HTTP_200_OK)

