import importlib.util
import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        seed_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "seed.py",
        )
        spec = importlib.util.spec_from_file_location("seed", seed_path)
        seed = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(seed)
        seed.run()
        self.stdout.write(self.style.SUCCESS("Demo data seeded."))
