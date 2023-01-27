import datetime

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
        all_objects = PriceInterval.objects.all()
        product_related_intervals = []
        ids_to_drop = []

        new_rec_product = validated_data.get('product')
        new_rec_start_date = validated_data.get('start_date')
        new_rec_end_date = validated_data.get('end_date')

        #   consider only product related price intervals
        for price_interval in all_objects:
            if price_interval.product == new_rec_product:
                product_related_intervals.append(price_interval)

        #   make sure that there are any records with this product
        if len(product_related_intervals) != 0:
            for price_interval in product_related_intervals:
                if new_rec_end_date is None:
                    if price_interval.end_date is None:
                        if price_interval.start_date < new_rec_start_date:
                            price_interval.end_date = new_rec_start_date - datetime.timedelta(days=1)
                            price_interval.save()
                        else:
                            new_rec_end_date = price_interval.start_date - datetime.timedelta(days=1)
                            price_interval.save()
                    else:
                        if price_interval.start_date < new_rec_start_date < price_interval.end_date:
                            price_interval.end_date = new_rec_start_date - datetime.timedelta(days=1)
                            price_interval.save()
                elif price_interval.end_date is None:
                    if new_rec_start_date <= price_interval.start_date:
                        price_interval.start_date = new_rec_end_date + datetime.timedelta(days=1)
                        price_interval.save()
                    elif price_interval.start_date < new_rec_start_date:
                        price_interval.end_date = new_rec_start_date - datetime.timedelta(days=1)
                        price_interval.save()
                if price_interval.end_date is not None and new_rec_end_date is not None:

                    #   if previous record is entirely inside of the new period - drop it
                    if new_rec_start_date <= price_interval.start_date <= price_interval.end_date <= new_rec_end_date:
                        ids_to_drop.append(price_interval)

                    #   if previous record end date is inside of the new interval - change end date to be till
                    # given new record start date
                    if new_rec_start_date < price_interval.end_date < new_rec_end_date:
                        price_interval.end_date = new_rec_start_date - datetime.timedelta(days=1)
                        price_interval.save()

                    #   if previous record start date is inside of the new interval - change start date to be from given
                    # new record end date
                    if new_rec_start_date < price_interval.start_date < new_rec_end_date:
                        price_interval.start_date = new_rec_end_date + datetime.timedelta(days=1)
                        price_interval.save()

        #   remove redundant price intervals
        for drop_object in ids_to_drop:
            drop_object.delete()

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

        for price_interval in found_price_intervals:
            if price_interval.end_date is not None:
                if price_interval.start_date <= start_time <= end_time <= price_interval.end_date:
                    validated_data['days'] = (end_time - start_time).days + 1
                    validated_data['price'] = price_interval.price
                    return ProductStats.objects.create(**validated_data)
            else:
                if price_interval.start_date <= start_time:
                    validated_data['days'] = (end_time - start_time).days + 1
                    validated_data['price'] = price_interval.price
                    return ProductStats.objects.create(**validated_data)
                else:
                    validated_data['days'] = (end_time - price_interval.start_date).days + 1
                    validated_data['price'] = price_interval.price
                    return ProductStats.objects.create(**validated_data)

        for price_interval in found_price_intervals:
            if start_time <= price_interval.start_date:
                if price_interval.end_date is None:
                    intervals_prices.append(price_interval.price)
                    intervals_days.append(price_interval.get_days(end_date=end_time))
                    break
                if end_time <= price_interval.end_date:
                    intervals_prices.append(price_interval.price)
                    intervals_days.append(price_interval.get_days(end_date=end_time))
                else:
                    intervals_prices.append(price_interval.price)
                    intervals_days.append(price_interval.get_days())
            if price_interval.start_date <= start_time <= price_interval.end_date:
                intervals_prices.append(price_interval.price)
                intervals_days.append(price_interval.get_days(start_date=start_time))

        if found_price_intervals[-1].end_date < end_time:
            intervals_days[-1] += (end_time - found_price_intervals[-1].end_date).days

        time_weighted_price = 0
        for index in range(len(intervals_prices)):
            time_weighted_price += intervals_prices[index] * intervals_days[index]

        for price_interval in found_price_intervals:
            print(price_interval)

        validated_data['days'] = sum(intervals_days)
        validated_data['price'] = time_weighted_price / sum(intervals_days)

        return ProductStats.objects.create(**validated_data)
