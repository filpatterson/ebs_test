from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from apps.products.models import Product, PriceInterval


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        """function of a serializer to create object and set it right into the database
        :param validated_data: product data that was verified to be valid
        """
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.sku = validated_data.get('sku', instance.sku)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance


class PriceIntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceInterval
        fields = '__all__'

    def create(self, validated_data):
        """function of a serializer to create object and set it right into the database
        :param validated_data: product data that was verified to be valid
        """
        return PriceInterval.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.product = Product.objects.get(validated_data.get('product', instance.product))
        instance.price = validated_data.get('price', instance.name)
        instance.start_date = validated_data.get('start_date', instance.sku)
        instance.end_date = validated_data.get('end_date', instance.description)

        instance.save()
        return instance


class ProductStatsSerializer(serializers.Serializer):
    product = PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
