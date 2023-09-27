from django.contrib import admin
from .models import Product, Variations, ProductGallery
import admin_thumbnails
from .models import ReviewRating


@admin_thumbnails.thumbnail("image")
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


@admin_thumbnails.thumbnail("images")
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("productName",)}
    list_display = (
        "productName",
        "price",
        "isAvailable",
        "stock",
        "category",
        "modifiedDate",
    )
    list_editable = ("isAvailable",)
    inlines = [ProductGalleryInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = ("product", "variationCategory", "variationValue", "isAvailable")
    list_editable = ("isAvailable",)
    list_filter = ("product", "variationCategory", "variationValue")


admin.site.register(Product, ProductAdmin)
admin.site.register(Variations, VariationAdmin)
admin.site.register(ProductGallery)
admin.site.register(ReviewRating)
