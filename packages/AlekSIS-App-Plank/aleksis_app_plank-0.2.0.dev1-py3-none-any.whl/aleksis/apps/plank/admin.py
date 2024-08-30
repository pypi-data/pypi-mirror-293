from django.contrib import admin, messages
from django.utils.translation import gettext as _

from .models import (
    Category,
    CheckedOutItem,
    CheckOutCondition,
    CheckOutProcess,
    Item,
    ItemType,
    Location,
)


class ItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Item._meta.fields if field.name != "id"]


admin.site.register(Category)
admin.site.register(Location)
admin.site.register(ItemType)
admin.site.register(Item, ItemAdmin)
admin.site.register(CheckOutProcess)
admin.site.register(CheckedOutItem)


class CheckOutConditionAdmin(admin.ModelAdmin):
    actions = ["make_default"]

    def make_default(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(
                request,
                _("There can be only one condition as default."),
                level=messages.ERROR,
            )
            return
        cond = queryset[0]
        cond.default = True
        cond.save()

    make_default.short_description = _("Set as default")
    list_display = ("text", "default")


admin.site.register(CheckOutCondition, CheckOutConditionAdmin)
