from django.contrib import admin
from user.models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
    ]
    search_fields = [
        "id",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
    ]
