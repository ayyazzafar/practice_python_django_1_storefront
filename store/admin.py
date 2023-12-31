from django.contrib import admin, messages
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


# Register your models here.

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    exclude = ['promotions']
    # readonly_fields = ['title']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title', 'last_update']
    list_editable = ['unit_price']
    list_per_page = 10
    list_filter = ['last_update', 'collection', InventoryFilter]
    list_select_related = ['collection']
    search_fields = ['title']
    actions = ['clear_inventory']

    @admin.display(ordering='collection')
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        else:
            return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products were successfully updated', level='success'),
        messages.success(request, f'{updated_count} products were successfully updated')


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    list_filter = ['membership']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
#     sort by first name and last name
    ordering = ['first_name']
#     all other options

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (reverse('admin:store_order_changelist')
               +
               '?'
               + urlencode({'customer__id': str(customer.id)})
               )
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )

        #     text representation of the object




@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['id', 'placed_at', 'customer_name']
    list_per_page = 10
    list_filter = ['placed_at']
    list_select_related = ['customer']
    search_fields = ['id']
    ordering = ['id']

    @admin.display(ordering='customer')
    def customer_name(self, order):
        return order.customer.first_name + ' ' + order.customer.last_name



@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']
    list_per_page = 10

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
               +
               '?'
               + urlencode({'collection__id': str(collection.id)})
               )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


admin.site.register(models.Promotion)

