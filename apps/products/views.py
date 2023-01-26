from drf_util.views import BaseViewSet, BaseCreateModelMixin, BaseListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404

from apps.products.models import Product, PriceInterval, ProductStats
from apps.products.serializers import ProductSerializer, PriceIntervalSerializer, ProductStatsSerializer


class ProductViewSet(BaseListModelMixin, BaseCreateModelMixin, BaseViewSet):
    permission_classes = AllowAny,
    authentication_classes = ()
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    #   address via POST request to localhost/products
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
            return Response(data={"id": product_saved.id}, status=status.HTTP_201_CREATED)

    #   address via GET request to localhost/products
    @action(detail=True, methods=['get'])
    def get(self):
        """GET handler, gives all products in a list form
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"products": serializer.data})

    #   works via PUT request to localhost/products/<pk_to_change>/put
    @action(detail=True, methods=['put'])
    def put(self, request, pk):
        saved_product = get_object_or_404(Product.objects.all(), pk=pk)
        name = request.data.get('name')
        sku = request.data.get('sku')
        description = request.data.get('description')
        product = {"name": name,
                   "sku": sku,
                   "description": description}

        serializer = ProductSerializer(instance=saved_product, data=product, partial=True)
        if serializer.is_valid():
            final_result = serializer.save()
            return Response(status.HTTP_200_OK)

    #   works via DELETE request to localhost/products/<pk_to_change>/delete
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
            return Response(data={"id": price_saved.id}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def get(self):
        """GET handler, gives all products in a list form
        """
        prices = PriceInterval.objects.all()
        serializer = ProductSerializer(prices, many=True)
        return Response({"price_intervals": serializer.data})

    @action(detail=True, methods=['put'])
    def put(self, request, pk):
        saved_price_interval = get_object_or_404(PriceInterval.objects.all(), pk=pk)
        product = request.data.get('product')
        price = request.data.get('price')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        data = {"product": product,
                "price": price,
                "start_date": start_date,
                "end_date": end_date}
        serializer = ProductSerializer(instance=saved_price_interval, data=data, partial=True)
        if serializer.is_valid():
            saved_price_interval = serializer.save()
            return Response({"id": saved_price_interval.id},
                             status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk):
        price_interval = get_object_or_404(Product.objects.all(), pk=pk)
        price_interval.delete()
        return Response(status.HTTP_200_OK)


class ProductStatsViewSet(BaseListModelMixin, BaseCreateModelMixin, BaseViewSet):
    permission_classes = AllowAny,
    authentication_classes = ()
    serializer_class = ProductStatsSerializer
    queryset = ProductStats.objects.all()

    @action(detail=True, methods=['create'])
    def post(self, request):
        """POST handler, requests average price per specified time period
        """
        stats = request.data

        #   serializer is able to check if given request data is valid or not
        serializer = ProductStatsSerializer(data=stats)

        if serializer.is_valid():
            stats = serializer.save()
            return Response({"days": stats.days_count, "price": stats.average_price},
                            status=status.HTTP_200_OK)

    @action(detail=True, methods=['list'])
    def get(self):
        """GET handler, gives all products in a list form
        """
        prices = ProductStats.objects.all()
        serializer = ProductStatsSerializer(prices, many=True)
        return Response({"product_stats": serializer.data})

    # @action(detail=True, methods=['update'])
    # def update(self, request, pk):
    #     saved_product = get_object_or_404(ProductStats.objects.all(), pk=pk)
    #     product = request.data.get('product')
    #     start_date = request.data.get('start_date')
    #     end_date = request.data.get('end_date')
    #     price = request.data.get('price')
    #     days = request.data.get('days')
    #     product = {"product": product,
    #                "start_date": start_date,
    #                "end_date": end_date,
    #                "price": price,
    #                "days": days}
    #
    #     serializer = ProductSerializer(instance=saved_product, data=product, partial=True)
    #     if serializer.is_valid():
    #         final_result = serializer.save()
    #         return Response(status.HTTP_200_OK)
    #
    # @action(detail=True, methods=['delete'])
    # def delete(self, request, pk):
    #     product_stats = get_object_or_404(ProductStats.objects.all(), pk=pk)
    #     product_stats.delete()
    #     return Response(status.HTTP_200_OK)
