from __future__ import annotations

import importlib
import inspect
import pkgutil
from pathlib import Path


class ClassCollector:
    def __init__(self, base_class: type):
        self.base_class = base_class
        self.classes: list[type] = []
        self.packages = self.get_start_folder()

    def get_start_folder(self) -> list[str]:
        current_path = Path.cwd()
        return [
            item.name
            for item in current_path.iterdir()
            if item.is_dir() and (item / "__init__.py").exists()
        ]

    def collect_classes(self):
        for pack in self.packages:
            package = __import__(pack)
            for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__):  # noqa: B007
                full_name = f"{pack}.{module_name}"
                module = __import__(full_name, fromlist=[""])
                self._visit_module(module)

    def _visit_module(self, module):
        for name, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and obj != self.base_class
                and obj not in self.classes
                and issubclass(obj, self.base_class)
                and not name.startswith("Base")
            ):
                self.classes.append(obj)

    def import_classes(self):
        imported_classes = []
        for cls in self.classes:
            module = importlib.import_module(cls.__module__)
            imported_class = getattr(module, cls.__name__)
            imported_classes.append(imported_class)
        return imported_classes
