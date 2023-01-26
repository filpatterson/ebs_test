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
    

