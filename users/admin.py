from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from users.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "is_staff",)
    list_filter = ("email", "is_staff",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
