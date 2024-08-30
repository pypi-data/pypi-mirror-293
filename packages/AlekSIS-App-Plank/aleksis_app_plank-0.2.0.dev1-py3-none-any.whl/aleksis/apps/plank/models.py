from typing import Optional

from django.db import models
from django.db.models import Max
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField

from aleksis.core.mixins import ExtensibleModel
from aleksis.core.models import Person
from aleksis.core.util.model_helpers import ICONS


class Inventory(ExtensibleModel):
    """An inventory of items."""

    name = models.CharField(_("Name"), max_length=255)
    check_out_groups = models.ManyToManyField(
        "core.Group",
        verbose_name=_("Groups with check out permission"),
        help_text=_("To persons in this groups things can be checked out."),
        blank=True,
        null=True,
        related_name="+",
    )
    check_out_create_group = models.ForeignKey(
        "core.Group",
        on_delete=models.SET_NULL,
        verbose_name=_("Group for persons created at check out"),
        help_text=_(
            "Persons created in check outs will be put in this group. "
            "If not group is set, creating persons at check out will be disabled."
        ),
        blank=True,
        null=True,
        related_name="+",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Inventory")
        verbose_name_plural = _("Inventories")
        permissions = [
            ("view_item_for_inventory", _("Can view item for inventory")),
            ("change_item_for_inventory", _("Can change item for inventory")),
            ("delete_item_for_inventory", _("Can delete item for inventory")),
            ("create_item_for_inventory", _("Can create item for inventory")),
            ("check_out_for_inventory", _("Can check out items for inventory")),
            ("check_in_for_inventory", _("Can check out items for inventory")),
            ("view_checkoutprocess_for_inventory", _("Can view check out process for inventory")),
            (
                "change_checkoutprocess_for_inventory",
                _("Can change check out process for inventory"),
            ),
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def status(self) -> dict[str, int]:
        """Get current status and statistics of this inventory."""
        context = {}
        items = Item.objects.filter(inventory=self)
        context["count_items"] = items.count()
        available = 0
        checked_out = 0
        not_in_time = 0
        for item in items:
            if item.is_available:
                available += 1
            else:
                checked_out += 1
                checked_out_item = item.checked_out_items.filter(checked_in=False)[0]
                if not checked_out_item.process.is_in_time:
                    not_in_time += 1
        context["count_available_items"] = available
        context["count_checked_out_items"] = checked_out
        context["count_not_in_time"] = not_in_time
        return context


class Category(ExtensibleModel):
    """A category of items in an inventory (e. g. IT stuff)."""

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    notes = models.TextField(verbose_name=_("Notes"), blank=True)
    icon = models.CharField(
        max_length=50, blank=True, choices=[("", "")] + ICONS, verbose_name=_("Icon")
    )
    colour = ColorField(verbose_name=_("Colour"), format="hexa", default="#00000000")

    class Meta:
        ordering = ["name"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return self.name

    @property
    def items_count(self) -> int:
        """Get number of items in this category."""
        return self.items.count()

    @property
    def item_types_count(self) -> int:
        """Get number of item types in this category."""
        return self.item_types.count()


class Location(ExtensibleModel):
    """A location in which items can be stored."""

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    notes = models.TextField(verbose_name=_("Notes"), blank=True)
    parent = models.ForeignKey(
        "Location",
        on_delete=models.CASCADE,
        verbose_name=_("Parent location"),
        related_name="children",
        blank=True,
        null=True,
    )
    item = models.OneToOneField(
        "Item",
        on_delete=models.SET_NULL,
        verbose_name=_("Item"),
        related_name="is_location",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self) -> str:
        return self.name

    def sort_or_check(self, item: "Item") -> str:
        """Sort item in location or check that item is in location."""
        if not item.is_available:
            return "checked_out"
        item.last_time_seen_at = timezone.now()
        if item.location == self:
            item.save()
            return "in_place"
        item.location = self
        item.save()
        return "moved"

    @property
    def items_count(self) -> int:
        """Get number of items in this location."""
        return self.items.count()

    @property
    def breadcrumbs(self):
        if self.parent:
            return [*self.parent.breadcrumbs, self.name]
        return [self.name]


class Manufacturer(ExtensibleModel):
    """A manufacturer of items."""

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    notes = models.TextField(verbose_name=_("Notes"), blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Manufacturer")
        verbose_name_plural = _("Manufacturers")

    def __str__(self):
        return self.name

    @property
    def items_count(self) -> int:
        """Get number of items with this manufacturer."""
        return Item.objects.filter(item_type__in=self.item_types.all()).count()

    @property
    def item_types_count(self) -> int:
        """Get number of item types with this manufacturer."""
        return self.item_types.count()


class ItemType(ExtensibleModel):
    """A type of item in an inventory (e. g. a specific model of a laptop)."""

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.SET_NULL,
        verbose_name=_("Manufacturer"),
        blank=True,
        null=True,
        related_name="item_types",
    )
    description = models.TextField(blank=True, verbose_name=_("Description"))
    category = models.ForeignKey(
        Category,
        models.CASCADE,
        verbose_name=_("Category"),
        related_name="item_types",
    )
    image = models.ImageField(upload_to="images/item_types/", blank=True, verbose_name=_("Image"))
    part_number = models.CharField(max_length=255, blank=True, verbose_name=_("Part number"))

    class Meta:
        ordering = ["name"]
        verbose_name = _("Item type")
        verbose_name_plural = _("Item type")

    def __str__(self):
        return self.name

    @property
    def items_count(self) -> int:
        """Get number of items of this type."""
        return self.items.count()


class Item(ExtensibleModel):
    """An item in an inventory (a concrete physical thing)."""

    inventory = models.ForeignKey(to=Inventory, on_delete=models.CASCADE, related_name="items")

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    barcode = models.CharField(
        max_length=15,
        verbose_name=_("Barcode"),
        blank=True,
        help_text=_("Leave blank to automatically generate the barcode"),
        unique=True,
    )
    serial_number = models.CharField(max_length=255, blank=True, verbose_name=_("Serial number"))

    category = models.ForeignKey(
        Category,
        models.CASCADE,
        verbose_name=_("Category"),
        related_name="items",
    )
    item_type = models.ForeignKey(
        ItemType,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Item type"),
        related_name="items",
    )

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    location = models.ForeignKey(
        Location,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Location"),
        related_name="items",
    )
    last_time_seen_at = models.DateTimeField(auto_now=True, verbose_name=_("Last time seen at"))

    class Meta:
        ordering = ["name", "item_type__name"]
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

    def __str__(self) -> str:
        if self.item_type:
            return f"{self.name} ({self.item_type})"
        else:
            return self.name

    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = self.gen_barcode()

        super().save(*args, **kwargs)

    def gen_barcode(self) -> str:
        """Generate a barcode for this item."""
        pk = self.pk if self.pk else Item.get_next_item_id()
        return f"{pk:05d}"

    @staticmethod
    def get_next_item_id() -> int:
        """Guess ID of the next item to be created."""
        id_max = Item.objects.all().aggregate(Max("id"))["id__max"]
        return id_max + 1 if id_max else 1

    @property
    def is_available(self):
        """Check if item is available."""
        return not self.current_checked_out_item

    @property
    def current_checked_out_item(self) -> Optional["CheckedOutItem"]:
        """Get current check out for this item (if checked out)."""
        qs = self.checked_out_items.filter(checked_in=False)
        if qs.exists():
            return qs.first()
        return None

    @property
    def contained_items(self):
        contains = set()

        def _get_contains(item):
            if not hasattr(item, "is_location"):
                return
            contains.update(set(item.is_location.items.all()))
            for next_item in item.is_location.items.all():
                _get_contains(next_item)

        _get_contains(self)

        return contains

    @classmethod
    def get_by_id_or_barcode(cls, id_or_barcode: str) -> Optional["Item"]:
        """Get item by ID or barcode."""
        try:
            return cls.objects.get(pk=int(id_or_barcode))
        except (cls.DoesNotExist, ValueError):
            try:
                return cls.objects.get(barcode=id_or_barcode)
            except cls.DoesNotExist:
                return None

    def check_in(self, person: Person) -> "CheckedOutItem":
        """Check in item."""
        checked_out_item = self.current_checked_out_item
        if checked_out_item:
            checked_out_item.checked_in = True
            checked_out_item.checked_in_at = timezone.now()
            checked_out_item.checked_in_by = person
            checked_out_item.save()
        return checked_out_item


class CheckOutCondition(ExtensibleModel):
    """A condition to which an item is checked out."""

    inventory = models.ForeignKey(
        to=Inventory, on_delete=models.CASCADE, related_name="check_out_conditions"
    )
    default = models.BooleanField(verbose_name=_("Default"))
    text = models.TextField(verbose_name=_("Text"))

    class Meta:
        ordering = ["text"]
        verbose_name = _("Check out condition")
        verbose_name_plural = _("Check out conditions")

    def __str__(self) -> str:
        return self.text

    def save(self, *args, **kwargs):
        if self.default:
            # select all other active items
            qs = CheckOutCondition.objects.filter(default=True)
            # except self (if self already exists)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            # and deactive them
            qs.update(default=False)

        super().save(*args, **kwargs)


class CheckOutProcess(ExtensibleModel):
    """A check out process (one or multiple items are checked out to one person)."""

    inventory = models.ForeignKey(
        to=Inventory, on_delete=models.CASCADE, related_name="check_out_processes"
    )
    borrowing_person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="check_outs_as_borrowing",
        verbose_name=_("Borrowing person"),
    )
    lending_person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="check_outs_as_lending",
        verbose_name=_("Lending person"),
    )
    checked_out_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Checked out at"))
    is_check_out_in_process = models.BooleanField(
        default=True, verbose_name=_("Check out in process?")
    )
    check_in_until = models.DateField(verbose_name=_("Check in until"), blank=True, null=True)
    condition = models.ForeignKey(
        CheckOutCondition,
        on_delete=models.SET_NULL,
        verbose_name=_("Check out condition"),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-check_in_until", "-checked_out_at"]
        verbose_name = _("Check out process")
        verbose_name_plural = _("Check out processes")
        permissions = [
            ("check_out", _("Can check out items")),
            ("check_in", _("Can check in items")),
        ]

    def __str__(self) -> str:
        return f"{self.borrowing_person} ({self.checked_out_at})"

    def save(self, *args, **kwargs):
        if self.condition is None:
            self.condition = CheckOutCondition.objects.all().filter(default=True).first()

        super().save(*args, **kwargs)

    @property
    def is_everything_checked_in(self) -> bool:
        """Check if all items are checked in."""
        return getattr(
            self,
            "_is_everything_checked_in",
            not self.checked_out_items.filter(checked_in=False).exists(),
        )

    @property
    def is_in_time(self) -> bool:
        """Check if check in is in time."""
        if self.check_in_until:
            return self.check_in_until >= timezone.now().date()
        else:
            return True

    @property
    def items_count(self) -> int:
        """Get number of items."""
        return getattr(self, "_items_count", self.checked_out_items.count())


class CheckedOutItem(ExtensibleModel):
    """A checked out item (as a part of a check out process)."""

    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="checked_out_items", verbose_name=_("Item")
    )
    process = models.ForeignKey(
        CheckOutProcess,
        on_delete=models.CASCADE,
        related_name="checked_out_items",
        verbose_name=_("Check out process"),
    )
    checked_in = models.BooleanField(default=False, verbose_name=_("Checked in?"))
    checked_in_at = models.DateTimeField(verbose_name=_("Checked in at"), blank=True, null=True)
    checked_in_by = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="check_ins",
        verbose_name=_("Checked in by"),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = [
            "-process__check_in_until",
            "-process__checked_out_at",
            "item__name",
            "item__item_type__name",
        ]
        verbose_name = _("Check out item")
        verbose_name_plural = _("Check out items")

    def __str__(self) -> str:
        return f"{self.item} [{self.process}]"
