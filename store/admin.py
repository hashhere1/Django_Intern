from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from . models import Collection, Product, Customer, Order
from . import models




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ["clear_inventory"]
    autocomplete_fields = ["collection"]
    search_fields = ["title"]
    prepopulated_fields = {"slug":["title"]}
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_select_related = ["collection"]
    list_filter = ["collection", "last_update"]
    
    def collection_title(self, product):
        return product.collection.title
    

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"
    
    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated.",
            messages.ERROR

        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["user__first_name", "user__last_name", "membership", "orders"]
    list_editable = ["membership"]
    list_select_related = ['user'] 
    search_fields = ["user__first_name__istartswith", "user__last_name__istartswith"]

    @admin.display(ordering="orders")
    def orders(self, customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        return format_html('<a href="{}">{}</a>', url, customer.order_set)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user").annotate(
            product_count=Count("order__orderitem__product")
        )
        


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "product_count"]
    search_fields = ["title"]

    @admin.display(ordering="product_count")
    def product_count(self, collection):
        url = (reverse('admin:store_product_changelist') + "?" + urlencode({
            "collection__id": str(collection.id)
        }))
        return format_html('<a href= "{}">{}</a>', url, collection.product_count)
        
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count("product")
        )

class OrderItemInLine(admin.StackedInline):
    autocomplete_fields = ["product"]
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "placed_at"]
    inlines = [OrderItemInLine]
    autocomplete_fields = ["customer"]