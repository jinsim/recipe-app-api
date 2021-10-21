from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# 번역
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {"fields": ('email', 'password')}),
        (_("Personal Info"), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (_("Important dates"), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ("wide",),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
# 기본적인 기능만 사용할 것이므로 특별히 관리자의 기능은 필요없다.
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
