import datetime

from django.db import models
from drf_util.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=100, db_index=True)
    sku = models.CharField(max_length=100, db_index=True)
    description = models.CharField(max_length=100, db_index=True)

    def __str__(self) -> str:
        return self.name


class PriceInterval(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)

    def get_product(self) -> Product:
        return self.product

    def is_in_between(self, given_date: datetime.date) -> bool:
        if self.end_date is None:
            return self.start_date <= given_date
        else:
            return self.start_date <= given_date <= self.end_date

    def get_days(self, start_date: datetime.date = None, end_date: datetime.date = None):
        if start_date is None and end_date is None:
            return (self.end_date - self.start_date).days + 1
        if start_date is not None:
            return (self.end_date - start_date).days + 1
        if end_date is not None:
            return (end_date - self.start_date).days + 1
        if start_date is not None and end_date is not None:
            return (end_date - start_date).days + 1

    def __str__(self):
        return f"Product: {self.product}; price: {self.price}; start date: {self.start_date}; end date: {self.end_date}"


class ProductStats(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    average_price = models.FloatField(null=True)
    days_count = models.IntegerField(default=0)
