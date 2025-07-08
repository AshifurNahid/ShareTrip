from django.contrib import admin  # type: ignore

from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "creator",
        "destination",
        "start_date",
        "price_per_person",
    ]
    list_filter = ["start_date", "destination"]
    search_fields = ["title", "destination"]
