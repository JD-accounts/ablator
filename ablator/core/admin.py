from django.contrib import admin

from core.models import Release
from .models import ClientUser, FunctionalityGroup, Functionality, Availability, App


@admin.register(ClientUser)
class ClientUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('human_readable_name', 'name', 'created_at',)


class FunctionalityInline(admin.TabularInline):
    model = Functionality


@admin.register(FunctionalityGroup)
class FunctionalityGroupAdmin(admin.ModelAdmin):
    list_display = ('human_readable_name', 'name', 'app', 'created_at', 'rollout_strategy')
    inlines = [FunctionalityInline]


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
        'functionality_group',
        'start_at',
        'end_at',
    )


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'functionality', 'is_enabled', 'created_at',)