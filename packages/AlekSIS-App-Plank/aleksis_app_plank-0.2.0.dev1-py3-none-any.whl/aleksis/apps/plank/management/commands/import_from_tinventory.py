import json
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware

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
from aleksis.core.models import Person


class Command(BaseCommand):
    """Import data from old software TInventory."""

    help = "Import data from old software TInventory"  # noqa

    def add_arguments(self, parser):
        parser.add_argument("file", type=str)
        parser.add_argument("inventory", type=int)

    def handle(self, *args, **options):
        inventory = Inventory.objects.get(pk=options["inventory"])
        if not inventory.check_out_create_group:
            raise CommandError(
                "No check out create group set. Persons can't be imported without one."
            )

        with open(options["file"], "r") as f:
            data = json.load(f)

        data_sorted = {}
        for item in data:
            data_sorted.setdefault(item["model"], [])
            data_sorted[item["model"]].append(item)

        data_map = {
            "category": {},
            "location": {},
            "check_out_condition": {},
            "item_type": {},
            "item": {},
            "person": {},
            "user": {},
            "check_out_process": {},
        }

        for category in data_sorted["api.category"]:
            self.stdout.write(str(category))
            new_category, __ = Category.objects.get_or_create(
                name=category["fields"]["name"], inventory=inventory
            )
            data_map["category"][category["pk"]] = new_category

        for location in data_sorted["api.location"]:
            self.stdout.write(str(location))
            new_location, __ = Location.objects.get_or_create(
                name=location["fields"]["name"], inventory=inventory
            )
            data_map["location"][location["pk"]] = new_location

        for check_out_condition in data_sorted["api.checkoutcondition"]:
            self.stdout.write(str(check_out_condition))
            new_check_out_condition, __ = CheckOutCondition.objects.get_or_create(
                text=check_out_condition["fields"]["text"],
                inventory=inventory,
                defaults=dict(default=check_out_condition["fields"]["default"]),
            )
            data_map["check_out_condition"][check_out_condition["pk"]] = new_check_out_condition

        for preset in data_sorted["api.preset"]:
            self.stdout.write(str(preset))
            manufacturer, __ = Manufacturer.objects.get_or_create(
                name=preset["fields"]["manufacturer"], inventory=inventory
            )
            category = data_map["category"][preset["fields"]["category"]]
            new_item_type, __ = ItemType.objects.get_or_create(
                name=preset["fields"]["name"],
                category=category,
                defaults=dict(
                    manufacturer=manufacturer, description=preset["fields"]["description"]
                ),
            )
            data_map["item_type"][preset["pk"]] = new_item_type

        for item in data_sorted["api.item"]:
            self.stdout.write(str(item))
            item_type = data_map["item_type"].get(item["fields"]["preset"], None)
            location = data_map["location"][item["fields"]["location"]]
            category = data_map["category"][item["fields"]["category"]]
            last_time_seen_at = make_aware(
                datetime.strptime(item["fields"]["last_time_seen_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            )
            new_item, __ = Item.objects.get_or_create(
                barcode=item["fields"]["barcode"],
                category=category,
                defaults=dict(
                    name=item["fields"]["name"],
                    item_type=item_type,
                    location=location,
                    last_time_seen_at=last_time_seen_at,
                    notes=item["fields"]["notes"],
                ),
            )
            data_map["item"][item["pk"]] = new_item

        for person in data_sorted["api.person"]:
            self.stdout.write(str(person))
            split_name = person["fields"]["name"].split(" ")
            first_name = " ".join(split_name[: len(split_name) - 1])
            last_name = split_name[-1]
            if Person.objects.filter(email=person["fields"]["email"]).count() == 1:
                new_person = Person.objects.get(email=person["fields"]["email"])
            elif (
                len(split_name) > 1
                and Person.objects.filter(first_name=first_name, last_name=last_name).exists()
            ):
                new_person = Person.objects.get(first_name=first_name, last_name=last_name)
            else:
                new_person = Person.objects.create(
                    first_name=first_name,
                    last_name=last_name if len(split_name) > 1 else "?",
                    email=person["fields"]["email"],
                )
                new_person.member_of.add(inventory.check_out_create_group)
            data_map["person"][person["pk"]] = new_person

        for user in data_sorted["auth.user"]:
            self.stdout.write(str(user))
            if Person.objects.filter(email=user["fields"]["email"]).count() == 1:
                new_user = Person.objects.get(email=user["fields"]["email"])
            elif Person.objects.filter(
                first_name=user["fields"]["first_name"], last_name=user["fields"]["last_name"]
            ).exists():
                new_user = Person.objects.get(
                    first_name=user["fields"]["first_name"], last_name=user["fields"]["last_name"]
                )
            else:
                new_user = Person.objects.create(
                    first_name=user["fields"]["first_name"],
                    last_name=user["fields"]["last_name"],
                    email=user["fields"]["email"],
                )
                new_user.member_of.add(inventory.check_out_create_group)
            data_map["user"][user["pk"]] = new_user

        for check_out_process in data_sorted["api.checkoutprocess"]:
            self.stdout.write(str(check_out_process))
            borrowing_person = data_map["person"][check_out_process["fields"]["borrowing_person"]]
            lending_person = data_map["user"][check_out_process["fields"]["lending_user"]]
            checked_out_at = make_aware(
                datetime.strptime(
                    check_out_process["fields"]["checked_out_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            )
            check_in_until = (
                datetime.strptime(check_out_process["fields"]["check_in_until"], "%Y-%m-%d")
                if check_out_process["fields"]["check_in_until"]
                else None
            )
            check_out_condition = (
                data_map["check_out_condition"][check_out_process["fields"]["condition"]]
                if check_out_process["fields"]["condition"]
                else None
            )
            new_check_out_process, __ = CheckOutProcess.objects.get_or_create(
                inventory=inventory,
                borrowing_person=borrowing_person,
                checked_out_at=checked_out_at,
                defaults=dict(
                    lending_person=lending_person,
                    is_check_out_in_process=check_out_process["fields"]["is_check_out_in_process"],
                    check_in_until=check_in_until,
                    condition=check_out_condition,
                ),
            )
            data_map["check_out_process"][check_out_process["pk"]] = new_check_out_process

        for check in data_sorted["api.check"]:
            self.stdout.write(str(check))
            item = data_map["item"][check["fields"]["item"]]
            check_out_process = data_map["check_out_process"][check["fields"]["check_out"]]
            checked_in_at = (
                make_aware(
                    datetime.strptime(check["fields"]["checked_in_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
                )
                if check["fields"]["checked_in_at"]
                else None
            )
            checked_in_by = (
                data_map["user"][check["fields"]["checked_in_by"]]
                if check["fields"]["checked_in_by"]
                else None
            )
            new_checked_out_item, __ = CheckedOutItem.objects.get_or_create(
                process=check_out_process,
                item=item,
                defaults=dict(
                    checked_in=check["fields"]["checked_in"],
                    checked_in_at=checked_in_at,
                    checked_in_by=checked_in_by,
                ),
            )
