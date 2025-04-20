from django.contrib import admin
from account.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "date_joined")
    list_filter = ("date_joined", "is_staff", "gender")
    search_fields = ("date_joined", "is_staff")
    prepopulated_fields = {"slug":("first_name", )}

