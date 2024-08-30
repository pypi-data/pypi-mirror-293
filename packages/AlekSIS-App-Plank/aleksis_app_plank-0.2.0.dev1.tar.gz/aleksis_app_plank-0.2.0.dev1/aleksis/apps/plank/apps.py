from aleksis.core.util.apps import AppConfig


class PlankConfig(AppConfig):
    name = "aleksis.apps.plank"
    verbose_name = "AlekSIS — Plank (Inventory Toolkit)"

    urls = {
        "Repository": "https://edugit.org/AlekSIS/onboarding/AlekSIS-App-Plank/",
    }
    licence = "EUPL-1.2+"
    copyright_info = (
        ([2019, 2020, 2021, 2022, 2023, 2024], "Jonathan Weth", "dev@jonathanweth.de"),
    )
