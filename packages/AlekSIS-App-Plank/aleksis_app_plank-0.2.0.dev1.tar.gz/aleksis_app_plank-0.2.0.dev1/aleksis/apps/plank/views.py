import json
from typing import Any, Dict

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils.translation import gettext as _
from django.views.generic.detail import DetailView, SingleObjectMixin

from guardian.shortcuts import get_objects_for_user

from aleksis.core.util.pdf import render_pdf
from aleksis.core.views import RenderPDFView

from .models import CheckOutProcess, Inventory, Item, Location


class LocationCompletenessReportView(PermissionRequiredMixin, SingleObjectMixin, RenderPDFView):
    model = Location
    template_name = "plank/reports/completeness.html"
    permission_required = "plank.view_location_rule"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        item_statuses = self.request.GET.get("item_statuses", "[]")
        item_statuses = json.loads(item_statuses)
        if not item_statuses:
            raise PermissionDenied(_("No item statuses given"))
        item_statuses = {int(key): value for key, value in item_statuses.items()}
        items = Item.objects.filter(location=self.object)
        if not self.request.user.has_perm("plank.view_item"):
            items = items.filter(
                Q(
                    category__inventory__in=get_objects_for_user(
                        self.request.user, "plank.view_item_for_inventory", Inventory
                    )
                )
                | Q(
                    pk__in=get_objects_for_user(
                        self.request.user, "plank.view_item", Item.objects.all()
                    )
                )
            )
        item_statuses = {
            key: value
            for key, value in item_statuses.items()
            if key in items.values_list("pk", flat=True)
        }
        items_with_status = []
        for item in items:
            items_with_status.append(
                {
                    "item": item,
                    "status": item_statuses.get(item.pk, "missing"),
                }
            )

        context["items_with_status"] = items_with_status
        context["items_count"] = items.count()
        context["missing_items"] = items.count() - len(list(item_statuses.keys()))
        context["moved_items"] = len([i for i in item_statuses.values() if i == "moved"])
        return context


class CheckOutFormView(PermissionRequiredMixin, DetailView):
    permission_required = "plank.view_checkoutprocess_rule"
    model = CheckOutProcess
    template_name = "plank/reports/check-out.html"

    def get(self, request, *args, **kwargs):
        context = {}
        process = self.get_object()
        context["process"] = process
        return render_pdf(request, self.template_name, context)


class CheckInFormView(PermissionRequiredMixin, DetailView):
    permission_required = "plank.view_checkoutprocess_rule"
    model = CheckOutProcess
    template_name = "plank/reports/check-in.html"

    def get(self, request, *args, **kwargs):
        context = {}
        process = self.get_object()
        context["process"] = process
        context["checked_out_items"] = process.checked_out_items.all().filter(checked_in=True)
        return render_pdf(request, self.template_name, context)
