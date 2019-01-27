from django.contrib import admin

from moderation.models import Ban, BanReason, WordFilter, ImageFilter


class UserSavingAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Ban)
class BanAdmin(UserSavingAdmin):
    list_display = ('id', 'type', 'value', 'reason', 'active_until', 'created_at', 'created_by',)
    readonly_fields = ('created_at', 'created_by',)


@admin.register(BanReason)
class BanReasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')


@admin.register(WordFilter)
class WordFilterAdmin(UserSavingAdmin):
    list_display = ('id', 'expression', 'created_at', 'created_by',)
    readonly_fields = ('created_at', 'created_by',)


@admin.register(ImageFilter)
class ImageFilterAdmin(UserSavingAdmin):
    list_display = ('id', 'checksum', 'size', 'created_at', 'created_by',)
    readonly_fields = ('created_at', 'created_by',)
