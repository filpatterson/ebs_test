from drf_util.views import BaseViewSet, BaseCreateModelMixin, BaseListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.decorators import api_view

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
            article_saved = serializer.save()
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

    # TODO create interval here
