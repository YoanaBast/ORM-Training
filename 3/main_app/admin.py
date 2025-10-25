from decimal import Decimal
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin (admin. ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_on')
    # def discount(self, product):
    #     return product.price * Decimal('0.8')
    search_fields = ('name', 'category', 'supplier')
    list_filter = ('category', 'supplier')
    fieldsets = (("General Information", {'fields': ('name', 'description', 'price', 'barcode')}),
                 ("Categorization", {'fields': ('category', 'supplier')}))
    date_hierarchy = 'created_on'