from django.db.models import Model, Q
from django.urls import reverse
from django.utils.translation import gettext as _

import graphene as graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from guardian.shortcuts import get_objects_for_user

from aleksis.apps.plank.forms import (
    CategoryForm,
    CheckOutProcessForm,
    InventoryForm,
    ItemForm,
    ItemTypeForm,
    LocationForm,
    ManufacturerForm,
)
from aleksis.apps.plank.models import (
    Category,
    CheckedOutItem,
    CheckOutCondition,
    CheckOutProcess,
    Inventory,
    Item,
    ItemType,
    Location,
    Manufacturer,
)
from aleksis.core.models import Group, Person
from aleksis.core.schema import PersonType
from aleksis.core.util.model_helpers import ICONS


class DeleteMutation(graphene.Mutation):
    """Mutation to delete an object."""

    klass: Model = None
    permission_required: str = ""
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()  # noqa

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = cls.klass.objects.get(pk=kwargs["id"])
        if info.context.user.has_perm(cls.permission_required, obj):
            obj.delete()
            return cls(ok=True)
        else:
            raise Exception("Permission denied")


class PermissionMutationMixin:
    """Mixin for mutations that require a permission check."""

    permission_edit = ""
    permission_create = ""

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        is_edit = bool(kwargs.get("id"))
        if is_edit:
            if not cls.permission_edit:
                raise Exception("Permission denied")
            instance = cls._meta.model._default_manager.get(pk=kwargs.get("id"))
            if not info.context.user.has_perm(cls.permission_edit, instance):
                raise Exception("Permission denied")
        else:
            if not cls.permission_create:
                raise Exception("Permission denied")
            if kwargs.get("inventory"):
                inventory = Inventory.objects.get(pk=kwargs["inventory"])
                if not info.context.user.has_perm(cls.permission_create, inventory):
                    raise Exception("Permission denied")
            elif not info.context.user.has_perm(cls.permission_create):
                raise Exception("Permission denied")
        return super().mutate_and_get_payload(root, info, **kwargs)


class PermissionsForTypeMixin:
    """Mixin for adding permissions to a Graphene type."""

    can_edit = graphene.Boolean()
    can_delete = graphene.Boolean()

    def resolve_can_edit(root: Model, info, **kwargs):
        perm = f"{root._meta.app_label}.edit_{root._meta.model_name}_rule"
        return info.context.user.has_perm(perm, root)

    def resolve_can_delete(root: Model, info, **kwargs):
        perm = f"{root._meta.app_label}.delete_{root._meta.model_name}_rule"
        return info.context.user.has_perm(perm, root)


class InventoryStatusType(graphene.ObjectType):
    """Graphene type for inventory status."""

    count_items = graphene.Int()
    count_available_items = graphene.Int()
    count_checked_out_items = graphene.Int()
    count_not_in_time = graphene.Int()


class InventoryGroupType(DjangoObjectType):
    class Meta:
        model = Group
        skip_registry = True
        fields = ("id", "name", "short_name")


class CheckOutConditionType(DjangoObjectType):
    class Meta:
        model = CheckOutCondition
        fields = ("inventory", "default", "text", "id")


class InventoryType(PermissionsForTypeMixin, DjangoObjectType):
    permission_edit = "plank.edit_inventory_rule"
    permission_delete = "plank.delete_inventory_rule"

    status = graphene.Field(InventoryStatusType)

    check_out_conditions = graphene.List(CheckOutConditionType)
    check_out_persons = graphene.List(PersonType)
    check_out_groups = graphene.List(InventoryGroupType)
    check_out_create_group = graphene.Field(InventoryGroupType, required=False)

    def resolve_check_out_conditions(root: Inventory, info, **kwargs):
        return root.check_out_conditions.all()

    def resolve_check_out_persons(root: Inventory, info, **kwargs):
        if not info.context.user.has_perm("plank.check_out_rule", root):
            return []
        groups = root.check_out_groups.all()
        persons = Person.objects.filter(member_of__in=groups)
        return persons

    def resolve_check_out_groups(root: Inventory, info, **kwargs):
        if not info.context.user.has_perm("plank.view_inventory_rule", root):
            return []
        return root.check_out_groups.all()

    def resolve_check_out_create_group(root: Inventory, info, **kwargs):
        if not info.context.user.has_perm(
            "plank.view_inventory_rule", root
        ) and not info.context.user.has_perm("plank.check_out_rule", root):
            return None
        return root.check_out_create_group

    class Meta:
        model = Inventory
        fields = ("name", "id", "check_out_groups", "check_out_create_group")


class InventoryMutation(PermissionMutationMixin, DjangoModelFormMutation):
    permission_edit = "plank.edit_inventory_rule"
    permission_create = "plank.create_inventory_rule"
    inventory = graphene.Field(InventoryType)

    class Meta:
        form_class = InventoryForm


class DeleteInventoryMutation(DeleteMutation):
    klass = Inventory
    permission_required = "plank.delete_inventory_rule"


class CategoryType(PermissionsForTypeMixin, DjangoObjectType):
    permission_edit = "plank.edit_category_rule"
    permission_delete = "plank.delete_category_rule"
    items_count = graphene.Int()
    item_types_count = graphene.Int()

    class Meta:
        model = Category
        fields = ("name", "notes", "colour", "icon", "id")
        convert_choices_to_enum = False


class CategoryMutation(PermissionMutationMixin, DjangoModelFormMutation):
    permission_edit = "plank.edit_category_rule"
    permission_create = "plank.create_category_rule"
    category = graphene.Field(CategoryType)

    class Meta:
        form_class = CategoryForm


class DeleteCategoryMutation(DeleteMutation):
    klass = Category
    permission_required = "plank.delete_category_rule"


class ManufacturerType(PermissionsForTypeMixin, DjangoObjectType):
    permission_edit = "plank.edit_manufacturer_rule"
    permission_delete = "plank.delete_manufacturer_rule"
    items_count = graphene.Int()
    item_types_count = graphene.Int()

    class Meta:
        model = Manufacturer
        fields = ("name", "notes", "id")


class ManufacturerMutation(PermissionMutationMixin, DjangoModelFormMutation):
    permission_edit = "plank.edit_manufacturer_rule"
    permission_create = "plank.create_manufacturer_rule"
    manufacturer = graphene.Field(ManufacturerType)

    class Meta:
        form_class = ManufacturerForm


class DeleteManufacturerMutation(DeleteMutation):
    klass = Manufacturer
    permission_required = "plank.delete_manufacturer_rule"


class CheckedOutItemType(DjangoObjectType):
    class Meta:
        model = CheckedOutItem
        fields = ("item", "id", "process", "checked_in", "checked_in_at", "checked_in_by")


class ItemGrapheneType(PermissionsForTypeMixin, DjangoObjectType):
    permission_edit = "plank.edit_item_rule"
    permission_delete = "plank.delete_item_rule"

    is_available = graphene.Boolean()

    current_checked_out_item = graphene.Field(CheckedOutItemType)
    checked_out_items = graphene.List(CheckedOutItemType)

    def resolve_current_checked_out_item(root, info, **kwargs):
        if info.context.user.has_perm("plank.view_checkoutitem_rule"):
            return root.current_checked_out_item
        return None

    def resolve_checked_out_items(root, info, **kwargs):
        if not info.context.user.has_perm("plank.view_checkoutprocess"):
            return root.checked_out_items.filter(
                Q(
                    process__inventory__in=get_objects_for_user(
                        info.context.user, "plank.view_checkoutprocess_for_inventory", Inventory
                    )
                )
                | Q(
                    process__pk__in=get_objects_for_user(
                        info.context.user, "plank.view_checkoutprocess", CheckOutProcess
                    )
                )
            )
        return root.checked_out_items.all()

    class Meta:
        model = Item
        fields = (
            "barcode",
            "name",
            "serial_number",
            "category",
            "item_type",
            "notes",
            "location",
            "last_time_seen_at",
            "inventory",
            "is_location",
            "id",
        )


class ItemMutation(PermissionMutationMixin, DjangoModelFormMutation):
    permission_edit = "plank.edit_item_rule"
    permission_create = "plank.create_item_rule"
    item = graphene.Field(ItemGrapheneType)

    class Meta:
        form_class = ItemForm


class DeleteItemMutation(DeleteMutation):
    klass = Item
    permission_required = "plank.delete_item_rule"


class ItemTypeType(PermissionsForTypeMixin, DjangoObjectType):
    permission_edit = "plank.edit_itemtype_rule"
    permission_delete = "plank.delete_itemtype_rule"

    items = graphene.List(ItemGrapheneType)
    items_count = graphene.Int()

    def resolve_items(self, info, **kwargs):
        if not info.context.user.has_perm("plank.view_item"):
            return self.items.filter(
                Q(
                    inventory__in=get_objects_for_user(
                        info.context.user, "plank.view_item_for_inventory", Inventory
                    )
                )
                | Q(
                    pk__in=get_objects_for_user(
                        info.context.user, "plank.view_item", self.items.all()
                    )
                )
            )
        return self.items.all()

    class Meta:
        model = ItemType
        fields = ("name", "manufacturer", "description", "image", "category", "part_number", "id")


class ItemTypeMutation(PermissionMutationMixin, DjangoModelFormMutation):
    permission_edit = "plank.edit_itemtype_rule"
    permission_create = "plank.create_itemtype_rule"
    item_type = graphene.Field(ItemTypeType)

    class Meta:
        form_class = ItemTypeForm
        return_field_name = "item_type"


class DeleteItemTypeMutation(DeleteMutation):
    klass = ItemType
    permission_required = "plank.delete_itemtype_rule"


class CheckOutProcessType(PermissionsForTypeMixin, DjangoObjectType):
    permission_edit = "plank.edit_checkoutprocess_rule"

    check_out_form = graphene.String()
    check_in_form = graphene.String()
    is_everything_checked_in = graphene.Boolean()
    is_in_time = graphene.Boolean()
    items_count = graphene.Int()
    checked_out_items = graphene.List(CheckedOutItemType)

    def resolve_check_out_form(root: CheckOutProcess, info, **kwargs):
        return info.context.build_absolute_uri(reverse("plank_check_out_form", args=[root.pk]))

    def resolve_check_in_form(root: CheckOutProcess, info, **kwargs):
        return info.context.build_absolute_uri(reverse("plank_check_in_form", args=[root.pk]))

    def resolve_checked_out_items(root, info, **kwargs):
        return root.checked_out_items.all()

    class Meta:
        model = CheckOutProcess
        fields = (
            "inventory",
            "borrowing_person",
            "lending_person",
            "checked_out_at",
            "is_check_out_in_process",
            "condition",
            "check_in_until",
            "id",
        )


class CheckOutProcessMutation(PermissionMutationMixin, DjangoModelFormMutation):
    permission_edit = "plank.edit_checkoutprocess_rule"

    class Meta:
        form_class = CheckOutProcessForm


class LocationType(PermissionsForTypeMixin, DjangoObjectType):
    permission_edit = "plank.edit_location_rule"
    permission_delete = "plank.delete_location_rule"

    items = graphene.List(ItemGrapheneType)
    items_count = graphene.Int()

    breadcrumbs = graphene.List(graphene.String)

    def resolve_items(self, info, **kwargs):
        if not info.context.user.has_perm("plank.view_item"):
            return self.items.filter(
                Q(
                    inventory__in=get_objects_for_user(
                        info.context.user, "plank.view_item_for_inventory", Inventory
                    )
                )
                | Q(
                    pk__in=get_objects_for_user(
                        info.context.user, "plank.view_item", self.items.all()
                    )
                )
            )
        return self.items.all()

    class Meta:
        model = Location
        fields = ("name", "notes", "parent", "item", "id")


class LocationChildrenType(LocationType):
    children = graphene.List(LocationType)

    def resolve_children(self, info, **kwargs):
        if not info.context.user.has_perm("plank.view_location"):
            return self.children.filter(
                pk__in=get_objects_for_user(
                    info.context.user, "plank.view_location", self.children.all()
                )
            )
        return self.children.all()

    class Meta:
        model = Location
        fields = ("name", "notes", "parent", "item", "id")


class LocationMutation(PermissionMutationMixin, DjangoModelFormMutation):
    permission_edit = "plank.edit_location_rule"
    permission_create = "plank.create_location_rule"
    location = graphene.Field(LocationChildrenType)

    class Meta:
        form_class = LocationForm


class DeleteLocationMutation(DeleteMutation):
    klass = Location
    permission_required = "plank.delete_location_rule"


class SortOrCheckMutation(graphene.Mutation):
    class Arguments:
        id_or_barcode = graphene.ID(required=True)
        location_id = graphene.ID(required=True)
        check_in = graphene.Boolean(required=False)

    item = graphene.Field(ItemGrapheneType)
    status = graphene.String()

    @staticmethod
    def mutate(root, info, id_or_barcode, location_id, check_in=False, **kwargs):
        location = Location.objects.get(pk=location_id)
        item = Item.get_by_id_or_barcode(id_or_barcode)
        if not item:
            raise Exception(_("Item not found"))

        status = location.sort_or_check(item)
        if status == "checked_out" and check_in:
            item.check_in(person=info.context.user.person)
            status = location.sort_or_check(item)
        item.refresh_from_db()
        return SortOrCheckMutation(item=item, status=status)


class CheckOutInputType(graphene.InputObjectType):
    inventory = graphene.ID(required=True)
    borrowing_person = graphene.ID(required=True)
    items = graphene.List(graphene.ID, required=True)
    check_out_condition = graphene.ID(required=False)
    check_in_until = graphene.Date(required=False)


class CheckOutMutation(graphene.Mutation):
    class Arguments:
        input = CheckOutInputType(required=True)  # noqa

    process = graphene.Field(CheckOutProcessType)

    @staticmethod
    def mutate(root, info, input, **kwargs):  # noqa
        # FIXME PERMISSION CHECK

        print("START MUTATE")
        inventory = Inventory.objects.get(pk=input.inventory)
        print(inventory)
        borrowing_person = Person.objects.get(pk=input.borrowing_person)
        print(borrowing_person)
        check_out_condition = None
        if input.check_out_condition:
            check_out_condition = CheckOutCondition.objects.get(pk=input.check_out_condition)
        print(check_out_condition)
        items = Item.objects.filter(pk__in=input.items)
        print(items)
        process = CheckOutProcess.objects.create(
            inventory=inventory,
            lending_person=info.context.user.person,
            borrowing_person=borrowing_person,
            condition=check_out_condition,
            check_in_until=input.check_in_until,
            is_check_out_in_process=False,
        )
        print(process)
        checked_out_items = []
        for item in items:
            if not item.is_available:
                continue
            checked_out_item = CheckedOutItem(process=process, item=item)
            checked_out_items.append(checked_out_item)
        CheckedOutItem.objects.bulk_create(checked_out_items)
        return CheckOutMutation(process=process)


class CheckInMutation(graphene.Mutation):
    class Arguments:
        id_or_barcode = graphene.ID(required=True)

    checked_out_items = graphene.List(CheckedOutItemType)
    status = graphene.Field(graphene.String)

    @staticmethod
    def mutate(root, info, id_or_barcode, **kwargs):  # noqa
        item = Item.get_by_id_or_barcode(id_or_barcode)
        if not item:
            return CheckInMutation(status="not_found")
        if not info.context.user.has_perm("plank.check_in_item_rule", item):
            return
        if item.is_available:
            return CheckInMutation(status="not_checked_out")

        checked_out_items = [item.current_checked_out_item]
        item.check_in(person=info.context.user.person)
        for contained_item in item.contained_items:
            if not contained_item.is_available:
                checked_out_items.append(contained_item.current_checked_out_item)
                contained_item.check_in(person=info.context.user.person)

        return CheckInMutation(checked_out_items=checked_out_items, status="checked_in")


class CheckedOutItemsType(graphene.ObjectType):
    item = graphene.Field(ItemGrapheneType)
    contained_items = graphene.List(ItemGrapheneType)


class Query:
    inventories = graphene.List(InventoryType, permission=graphene.String(required=False))
    inventory_by_id = graphene.Field(InventoryType, id=graphene.ID(required=True))
    categories = graphene.List(CategoryType, permission=graphene.String(required=False))
    manufacturers = graphene.List(ManufacturerType, permission=graphene.String(required=False))
    manufacturer_by_id = graphene.Field(ManufacturerType, id=graphene.ID(required=True))
    locations = graphene.List(LocationChildrenType, permission=graphene.String(required=False))
    location_by_id = graphene.Field(LocationChildrenType, id=graphene.ID(required=True))
    item_types = graphene.List(ItemTypeType, permission=graphene.String(required=False))
    item_type_by_id = graphene.Field(ItemTypeType, id=graphene.ID(required=True))
    items = graphene.List(ItemGrapheneType)
    item_by_id = graphene.Field(ItemGrapheneType, id=graphene.ID(required=True))
    check_out_items_by_id = graphene.Field(CheckedOutItemsType, id=graphene.ID(required=True))
    check_out_conditions = graphene.List(CheckOutConditionType)
    check_out_processes = graphene.List(CheckOutProcessType)
    check_out_process_by_id = graphene.Field(CheckOutProcessType, id=graphene.ID(required=True))
    icons = graphene.List(graphene.String)
    permission = graphene.Boolean(permission=graphene.String(required=True))

    groups_for_inventory = graphene.List(InventoryGroupType)

    def resolve_check_out_processes(self, info, **kwargs):
        qs = CheckOutProcess.objects.all()
        if not info.context.user.has_perm("plank.view_checkoutprocess"):
            qs = CheckOutProcess.objects.filter(
                Q(
                    inventory__in=get_objects_for_user(
                        info.context.user, "plank.view_checkoutprocess_for_inventory", Inventory
                    )
                )
                | Q(
                    pk__in=get_objects_for_user(
                        info.context.user, "plank.view_checkoutprocess", CheckOutProcess
                    )
                )
            )
        return qs

    def resolve_check_out_process_by_id(self, info, id, **kwargs):  # noqa
        process = CheckOutProcess.objects.get(pk=id)
        if not info.context.user.has_perm("plank.view_checkoutprocess_rule", process):
            return None
        return process

    def resolve_check_out_conditions(self, info, **kwargs):
        if not info.context.user.has_perm("plank.check_out"):
            return CheckOutCondition.objects.filter(
                inventory__in=get_objects_for_user(
                    info.context.user, "plank.check_out_for_inventory", Inventory
                )
            )

        return CheckOutCondition.objects.all()

    def resolve_items(self, info, **kwargs):
        items = Item.objects.prefetch_related("is_location__items", "checked_out_items")
        if not info.context.user.has_perm("plank.view_item"):
            return items.filter(
                Q(
                    inventory__in=get_objects_for_user(
                        info.context.user, "plank.view_item_for_inventory", Inventory
                    )
                )
                | Q(pk__in=get_objects_for_user(info.context.user, "plank.view_item", Item))
            )
        return items

    def resolve_item_by_id(self, info, id, **kwargs):  # noqa
        item = Item.get_by_id_or_barcode(id)
        if not info.context.user.has_perm("plank.view_item_rule", item):
            return None
        return item

    def resolve_check_out_items_by_id(self, info, id, **kwargs):  # noqa
        item = Item.get_by_id_or_barcode(id)
        if not item or not info.context.user.has_perm("plank.view_item_rule", item):
            return None

        return CheckedOutItemsType(item=item, contained_items=item.contained_items)

    def resolve_item_types(self, info, permission=None, **kwargs):
        if not info.context.user.has_perm("plank.view_itemtype"):
            return ItemType.objects.filter(
                pk__in=get_objects_for_user(info.context.user, "plank.view_itemtype", ItemType)
            )
        return ItemType.objects.all()

    def resolve_item_type_by_id(self, info, id, **kwargs):  # noqa
        item_type = ItemType.objects.get(pk=id)
        if not info.context.user.has_perm("plank.view_itemtype_rule", item_type):
            return None
        return item_type

    def resolve_locations(self, info, **kwargs):
        if not info.context.user.has_perm("plank.view_location"):
            return Location.objects.filter(
                pk__in=get_objects_for_user(info.context.user, "plank.view_location", Location)
            )
        return Location.objects.all()

    def resolve_location_by_id(self, info, id, **kwargs):  # noqa
        location = Location.objects.get(pk=id)
        if not info.context.user.has_perm("plank.view_location_rule", location):
            return None
        return location

    def resolve_manufacturers(self, info, permission=None, **kwargs):
        if not info.context.user.has_perm("plank.view_manufacturer"):
            return Manufacturer.objects.filter(
                pk__in=get_objects_for_user(
                    info.context.user, "plank.view_manufacturer", Manufacturer
                )
            )
        return Manufacturer.objects.all()

    def resolve_manufacturer_by_id(self, info, id, **kwargs):  # noqa
        manufacturer = Manufacturer.objects.get(pk=id)
        if not info.context.user.has_perm("plank.view_manufacturer_rule", manufacturer):
            return None
        return manufacturer

    def resolve_categories(self, info, permission=None, **kwargs):
        if not info.context.user.has_perm("plank.view_category"):
            return Category.objects.filter(
                pk__in=get_objects_for_user(info.context.user, "plank.view_category", Category)
            )
        return Category.objects.all()

    def resolve_inventories(self, info, permission=None, **kwargs):
        permission = f"{permission}_for_inventory" if permission else "plank.view_inventory"
        if not info.context.user.has_perm(permission):
            return get_objects_for_user(info.context.user, permission, Inventory)
        return Inventory.objects.all()

    def resolve_inventory_by_id(self, info, id, **kwargs):  # noqa
        inventory = Inventory.objects.get(pk=id)
        if not info.context.user.has_perm("plank.view_inventory_rule", inventory):
            return None
        return inventory

    def resolve_icons(self, info, **kwargs):
        return [x[0] for x in ICONS]

    def resolve_permission(root, info, permission, **kwargs):
        return info.context.user.has_perm(permission)

    def resolve_groups_for_inventory(root, info, **kwargs):
        if not info.context.user.has_perm("plank.create_inventory_rule"):
            return []
        return Group.objects.all()


class Mutation(graphene.ObjectType):
    inventory = InventoryMutation.Field()
    delete_inventory = DeleteInventoryMutation.Field()
    category = CategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()
    manufacturer = ManufacturerMutation.Field()
    delete_manufacturer = DeleteManufacturerMutation.Field()
    location = LocationMutation.Field()
    delete_location = DeleteLocationMutation.Field()
    sort_or_check = SortOrCheckMutation.Field()
    item_type = ItemTypeMutation.Field()
    delete_item_type = DeleteItemTypeMutation.Field()
    item = ItemMutation.Field()
    delete_item = DeleteItemMutation.Field()
    check_out = CheckOutMutation.Field()
    check_in = CheckInMutation.Field()
    check_out_process = CheckOutProcessMutation.Field()
