from django.forms import ModelForm

from .models import Category, CheckOutProcess, Inventory, Item, ItemType, Location, Manufacturer


class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ("name", "check_out_create_group", "check_out_groups")


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ("name", "notes", "colour", "icon")


class ManufacturerForm(ModelForm):
    class Meta:
        model = Manufacturer
        fields = ("name", "notes")


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ("name", "notes", "parent", "item")


class ItemTypeForm(ModelForm):
    class Meta:
        model = ItemType
        fields = ("name", "category", "description", "manufacturer", "image", "part_number")


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = (
            "barcode",
            "name",
            "category",
            "item_type",
            "notes",
            "location",
            "serial_number",
            "inventory",
        )


class CheckOutProcessForm(ModelForm):
    class Meta:
        model = CheckOutProcess
        fields = ("check_in_until", "condition")
