from django.contrib import admin

from apps.products.models import Product, PriceInterval, ProductStats

admin.site.register(Product)
admin.site.register(PriceInterval)
admin.site.register(ProductStats)
