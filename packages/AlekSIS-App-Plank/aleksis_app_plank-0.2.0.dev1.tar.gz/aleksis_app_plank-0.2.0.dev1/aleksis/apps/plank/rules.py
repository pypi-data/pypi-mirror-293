from rules import add_perm

from aleksis.apps.plank.models import (
    Category,
    CheckOutProcess,
    Inventory,
    Item,
    ItemType,
    Location,
    Manufacturer,
)
from aleksis.apps.plank.util.predicates import (
    has_any_object_via_inventory,
    has_object_perm_for_inventory,
)
from aleksis.core.util.predicates import (
    has_any_object,
    has_global_perm,
    has_object_perm,
    has_person,
)

view_inventories_predicate = has_person & (
    has_global_perm("plank.view_inventory") | has_any_object("plank.view_inventory", Inventory)
)
add_perm("plank.view_inventories_rule", view_inventories_predicate)

view_inventory_predicate = has_person & (
    has_global_perm("plank.view_inventory") | has_object_perm("plank.view_inventory")
)
add_perm("plank.view_inventory_rule", view_inventory_predicate)

create_inventory_predicate = has_person & has_global_perm("plank.add_inventory")
add_perm("plank.create_inventory_rule", create_inventory_predicate)

edit_inventory_predicate = view_inventory_predicate & (
    has_global_perm("plank.change_inventory") | has_object_perm("plank.change_inventory")
)
add_perm("plank.edit_inventory_rule", edit_inventory_predicate)

delete_inventory_predicate = view_inventory_predicate & (
    has_global_perm("plank.delete_inventory") | has_object_perm("plank.delete_inventory")
)
add_perm("plank.delete_inventory_rule", delete_inventory_predicate)

view_categories_predicate = has_person & (
    has_global_perm("plank.view_category")
    | has_any_object("plank.view_category", Category)
    | has_object_perm("plank.view_category_for_inventory")
)
add_perm("plank.view_categories_rule", view_categories_predicate)

view_category_predicate = has_person & (
    has_global_perm("plank.view_category")
    | has_object_perm("plank.view_category")
    | has_object_perm_for_inventory("plank.view_category_for_inventory")
)
add_perm("plank.view_category_rule", view_category_predicate)

create_category_predicate = has_person & (
    has_global_perm("plank.add_category") | has_object_perm("plank.add_category_for_inventory")
)
add_perm("plank.create_category_rule", create_category_predicate)

edit_category_predicate = view_category_predicate & (
    has_global_perm("plank.change_category")
    | has_object_perm("plank.change_category")
    | has_object_perm_for_inventory("plank.change_category_for_inventory")
)
add_perm("plank.edit_category_rule", edit_category_predicate)

delete_category_predicate = view_category_predicate & (
    has_global_perm("plank.delete_category")
    | has_object_perm("plank.delete_category")
    | has_object_perm_for_inventory("plank.delete_category_for_inventory")
)
add_perm("plank.delete_category_rule", delete_category_predicate)

view_manufacturers_predicate = has_person & (
    has_global_perm("plank.view_manufacturer")
    | has_any_object("plank.view_manufacturer", Manufacturer)
    | has_object_perm("plank.view_manufacturer_for_inventory")
)
add_perm("plank.view_manufacturers_rule", view_manufacturers_predicate)

view_manufacturer_predicate = has_person & (
    has_global_perm("plank.view_manufacturer")
    | has_object_perm("plank.view_manufacturer")
    | has_object_perm_for_inventory("plank.view_manufacturer_for_inventory")
)
add_perm("plank.view_manufacturer_rule", view_manufacturer_predicate)

create_manufacturer_predicate = has_person & (
    has_global_perm("plank.add_manufacturer")
    | has_object_perm("plank.add_manufacturer_for_inventory")
)
add_perm("plank.create_manufacturer_rule", create_manufacturer_predicate)

edit_manufacturer_predicate = view_manufacturer_predicate & (
    has_global_perm("plank.change_manufacturer")
    | has_object_perm("plank.change_manufacturer")
    | has_object_perm_for_inventory("plank.change_manufacturer_for_inventory")
)
add_perm("plank.edit_manufacturer_rule", edit_manufacturer_predicate)

delete_manufacturer_predicate = view_manufacturer_predicate & (
    has_global_perm("plank.delete_manufacturer")
    | has_object_perm("plank.delete_manufacturer")
    | has_object_perm_for_inventory("plank.delete_manufacturer_for_inventory")
)
add_perm("plank.delete_manufacturer_rule", delete_manufacturer_predicate)

view_locations_predicate = has_person & (
    has_global_perm("plank.view_location")
    | has_any_object("plank.view_location", Location)
    | has_object_perm("plank.view_location_for_inventory")
)
add_perm("plank.view_locations_rule", view_locations_predicate)

view_location_predicate = has_person & (
    has_global_perm("plank.view_location")
    | has_object_perm("plank.view_location")
    | has_object_perm_for_inventory("plank.view_location_for_inventory")
)
add_perm("plank.view_location_rule", view_location_predicate)

create_location_predicate = has_person & (
    has_global_perm("plank.add_location") | has_object_perm("plank.add_location_for_inventory")
)
add_perm("plank.create_location_rule", create_location_predicate)

edit_location_predicate = view_location_predicate & (
    has_global_perm("plank.change_location")
    | has_object_perm("plank.change_location")
    | has_object_perm_for_inventory("plank.change_location_for_inventory")
)
add_perm("plank.edit_location_rule", edit_location_predicate)

delete_location_predicate = view_location_predicate & (
    has_global_perm("plank.delete_location")
    | has_object_perm("plank.delete_location")
    | has_object_perm_for_inventory("plank.delete_location_for_inventory")
)
add_perm("plank.delete_location_rule", delete_location_predicate)

view_item_types_predicate = has_person & (
    has_global_perm("plank.view_itemtype")
    | has_any_object("plank.view_itemtype", ItemType)
    | has_object_perm("plank.view_itemtype_for_inventory")
)
add_perm("plank.view_itemtypes_rule", view_item_types_predicate)

view_item_type_predicate = has_person & (
    has_global_perm("plank.view_itemtype")
    | has_object_perm("plank.view_itemtype")
    | has_object_perm_for_inventory("plank.view_itemtype_for_inventory")
)
add_perm("plank.view_itemtype_rule", view_item_type_predicate)

create_item_type_predicate = has_person & (
    has_global_perm("plank.add_itemtype") | has_object_perm("plank.add_itemtype_for_inventory")
)
add_perm("plank.create_itemtype_rule", create_item_type_predicate)

edit_item_type_predicate = view_item_type_predicate & (
    has_global_perm("plank.change_itemtype")
    | has_object_perm("plank.change_itemtype")
    | has_object_perm_for_inventory("plank.change_itemtype_for_inventory")
)
add_perm("plank.edit_itemtype_rule", edit_item_type_predicate)

delete_item_type_predicate = view_item_type_predicate & (
    has_global_perm("plank.delete_itemtype")
    | has_object_perm("plank.delete_itemtype")
    | has_object_perm_for_inventory("plank.delete_itemtype_for_inventory")
)
add_perm("plank.delete_itemtype_rule", delete_item_type_predicate)

view_items_predicate = has_person & (
    has_global_perm("plank.view_item")
    | has_any_object("plank.view_item", Item)
    | has_any_object_via_inventory("plank.view_item_for_inventory", Item)
    | has_object_perm("plank.view_item_for_inventory")
)
add_perm("plank.view_items_rule", view_items_predicate)

view_item_predicate = has_person & (
    has_global_perm("plank.view_item")
    | has_object_perm("plank.view_item")
    | has_object_perm_for_inventory("plank.view_item_for_inventory")
)
add_perm("plank.view_item_rule", view_item_predicate)

create_item_predicate = has_person & (
    has_global_perm("plank.add_item") | has_object_perm("plank.add_item_for_inventory")
)
add_perm("plank.create_item_rule", create_item_predicate)

edit_item_predicate = view_item_predicate & (
    has_global_perm("plank.change_item")
    | has_object_perm("plank.change_item")
    | has_object_perm_for_inventory("plank.change_item_for_inventory")
)
add_perm("plank.edit_item_rule", edit_item_predicate)

delete_item_predicate = view_item_predicate & (
    has_global_perm("plank.delete_item")
    | has_object_perm("plank.delete_item")
    | has_object_perm_for_inventory("plank.delete_item_for_inventory")
)
add_perm("plank.delete_item_rule", delete_item_predicate)

check_out_predicate = has_person & (
    has_global_perm("plank.check_out")
    | has_object_perm_for_inventory("plank.check_out_for_inventory")
)
add_perm("plank.check_out_rule", check_out_predicate)

check_in_item_predicate = has_person & (
    has_global_perm("plank.check_in")
    | has_object_perm_for_inventory("plank.check_in_for_inventory")
)
add_perm("plank.check_in_item_rule", check_in_item_predicate)

check_in_predicate = has_person & (
    has_global_perm("plank.check_in") | has_any_object("plank.check_in_for_inventory", Inventory)
)
add_perm("plank.check_in_rule", check_in_predicate)

view_check_out_processes_predicate = has_person & (
    has_global_perm("plank.view_checkoutprocess")
    | has_any_object("plank.view_checkoutprocess", CheckOutProcess)
    | has_any_object_via_inventory("plank.view_checkoutprocess_for_inventory", CheckOutProcess)
    | has_object_perm("plank.view_checkoutprocess_for_inventory")
)
add_perm("plank.view_checkoutprocesses_rule", view_check_out_processes_predicate)

view_check_out_process_predicate = has_person & (
    has_global_perm("plank.view_checkoutprocess")
    | has_object_perm("plank.view_checkoutprocess")
    | has_object_perm_for_inventory("plank.view_checkoutprocess_for_inventory")
)
add_perm("plank.view_checkoutprocess_rule", view_check_out_process_predicate)

edit_check_out_process_predicate = view_check_out_process_predicate & (
    has_global_perm("plank.change_checkoutprocess")
    | has_object_perm("plank.change_checkoutprocess")
    | has_object_perm_for_inventory("plank.change_checkoutprocess_for_inventory")
)
add_perm("plank.edit_checkoutprocess_rule", edit_check_out_process_predicate)

view_menu_predicate = (
    view_inventories_predicate
    | view_categories_predicate
    | view_manufacturers_predicate
    | view_locations_predicate
    | view_item_types_predicate
    | view_items_predicate
    | create_item_predicate
    | check_out_predicate
    | check_in_predicate
    | view_check_out_processes_predicate
)
add_perm("plank.view_menu_rule", view_menu_predicate)
