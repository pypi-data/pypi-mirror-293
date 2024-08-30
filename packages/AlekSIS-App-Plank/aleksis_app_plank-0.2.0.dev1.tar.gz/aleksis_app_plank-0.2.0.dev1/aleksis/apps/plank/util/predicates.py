from guardian.shortcuts import get_objects_for_user
from rules import predicate

from aleksis.apps.plank.models import Inventory
from aleksis.core.util.predicates import check_object_permission


@predicate
def has_object_perm_for_inventory(perm: str):
    name = f"has_object_perm_for_inventory:{perm}"

    @predicate(name)
    def fn(user, obj) -> bool:
        if not obj or not getattr(obj, "inventory", None):
            return False
        return check_object_permission(user, perm, obj.inventory)

    return fn


def has_any_object_via_inventory(perm: str, klass):
    name = f"has_any_object_via_inventory:{perm}"

    @predicate(name)
    def fn(user) -> bool:
        inventories = get_objects_for_user(user, perm, Inventory)
        return klass.objects.filter(inventory__in=inventories).exists()

    return fn
