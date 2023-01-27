import datetime

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from apps.products.models import Product, PriceInterval, ProductStats


def custom_checker(present_end_date: datetime.date, new_end_date) -> int:
    check_case = 0
    if present_end_date is None:
        check_case += 1
    if new_end_date is None:
        check_case += 2
    return check_case


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
        ids_to_drop = []

        new_rec_product = validated_data.get('product')
        new_rec_start_date = validated_data.get('start_date')
        new_rec_end_date = validated_data.get('end_date')

        price_intervals = PriceInterval.objects.all()

        product_related_intervals = [interval for interval in price_intervals
                                     if interval.product == new_rec_product]

        check_cases = [custom_checker(interval.end_date, new_rec_end_date)
                       for interval in price_intervals]

        size = len(product_related_intervals)

        for index in range(size):
            #   if both end dates are estimated
            if check_cases[index] == 0:
                #   if previous record interval is inside of the new interval - drop old one
                if new_rec_start_date <= product_related_intervals[index].start_date < \
                        product_related_intervals[index].end_date <= new_rec_end_date:
                    ids_to_drop.append(product_related_intervals[index])
                    continue

                #   if previous record start date is inside of the new interval - change start date to be from given
                # new record end date
                if new_rec_start_date < product_related_intervals[index].start_date < new_rec_end_date:
                    product_related_intervals[index].start_date = new_rec_end_date + datetime.timedelta(days=1)
                    continue

                #   if previous end date is inside if the new interval - change previous end date to new start date
                if new_rec_start_date < product_related_intervals[index].end_date < new_rec_end_date:
                    product_related_intervals[index].end_date = new_rec_start_date - datetime.timedelta(days=1)
                    continue

            #   if old record has no date
            if check_cases[index] == 1:
                if product_related_intervals[index].start_date < new_rec_start_date:
                    product_related_intervals[index].end_date = new_rec_start_date - datetime.timedelta(days=1)
                    continue

            #   if new date has no date
            if check_cases[index] == 2:
                if product_related_intervals[index].start_date < new_rec_start_date < product_related_intervals[index].end_date:
                    product_related_intervals[index].end_date = new_rec_start_date - datetime.timedelta(days=1)
                    continue

            #   if both records have no date
            if check_cases[index] == 3:
                if product_related_intervals[index].start_date < new_rec_start_date:
                    product_related_intervals[index].end_date = new_rec_start_date - datetime.timedelta(days=1)
                    continue
                if new_rec_start_date >= product_related_intervals[index].start_date:
                    new_rec_end_date = product_related_intervals[index].start_date - datetime.timedelta(days=1)

        for index in range(size):
            product_related_intervals[index].save()

        for index in range(len(ids_to_drop)):
            ids_to_drop[index].delete()

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
        start_time = validated_data.get("start_date")
        end_time = validated_data.get("end_date")

        intervals_days = []
        intervals_prices = []

        found_price_intervals = [interval for interval in PriceInterval.objects.all()
                                 if interval.product.id == product]
        found_price_intervals = sorted(found_price_intervals, key=lambda interval: interval.start_date)

        for price_interval in found_price_intervals:
            if price_interval.end_date is not None:
                if price_interval.start_date <= start_time <= end_time <= price_interval.end_date:
                    validated_data['days'] = (end_time - start_time).days + 1
                    validated_data['price'] = price_interval.price
                    return ProductStats.objects.create(**validated_data)
            if price_interval.end_date is None:
                if price_interval.start_date <= start_time:
                    validated_data['days'] = (end_time - start_time).days + 1
                    validated_data['price'] = price_interval.price
                    return ProductStats.objects.create(**validated_data)
                validated_data['days'] = (end_time - price_interval.start_date).days + 1
                validated_data['price'] = price_interval.price
                return ProductStats.objects.create(**validated_data)

        # for price_interval in found_price_intervals:
            if start_time <= price_interval.start_date:
                if price_interval.end_date is None:
                    intervals_prices.append(price_interval.price)
                    intervals_days.append(price_interval.get_days(end_date=end_time))
                    break
                if end_time <= price_interval.end_date:
                    intervals_prices.append(price_interval.price)
                    intervals_days.append(price_interval.get_days(end_date=end_time))
                    break
                if end_time > price_interval.end_date:
                    intervals_prices.append(price_interval.price)
                    intervals_days.append(price_interval.get_days())
            if price_interval.start_date <= start_time <= price_interval.end_date:
                intervals_prices.append(price_interval.price)
                intervals_days.append(price_interval.get_days(start_date=start_time))

        if found_price_intervals[-1].end_date < end_time:
            intervals_days[-1] += (end_time - found_price_intervals[-1].end_date).days

        multiplication_vector = [price * days for price, days in zip(intervals_prices, intervals_days)]
        days = sum(intervals_days)
        time_weighted_price = sum(multiplication_vector) / days

        validated_data['days'] = days
        validated_data['price'] = time_weighted_price

        return ProductStats.objects.create(**validated_data)
