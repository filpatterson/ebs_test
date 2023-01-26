from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from apps.products.models import Product, PriceInterval, ProductStats


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
        instance.name = validated_data.get('name')
        instance.sku = validated_data.get('sku')
        instance.description = validated_data.get('description')

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


class ProductStatsSerializer(serializers.ModelSerializer):
    product = PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

    class Meta:
        model = ProductStats
        fields = '__all__'

    def create(self, validated_data):
        product = validated_data.get("product").id
        # product_obj = validated_data.get("product")
        # start_time = datetime.datetime.strptime(validated_data.get("start_date"), "%Y-%M-%d").date()
        # end_time = datetime.datetime.strptime(validated_data.get("end_date"), "%Y-%M-%d").date()
        start_time = validated_data.get("start_date")
        end_time = validated_data.get("end_date")

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

        validated_data['days_count'] = sum(intervals_days)
        validated_data['average_price'] = time_weighted_price / sum(intervals_days)

        return ProductStats.objects.create(**validated_data)
