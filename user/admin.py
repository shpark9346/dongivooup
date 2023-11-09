
from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User

#admin.site.register(User, UserAdmin)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    #Define admin model for custom User model with no username field.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'nickname', 'phone', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'nickname', 'phone', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)


#admin.site.register(get_user_model(), CustomUserAdmin)
