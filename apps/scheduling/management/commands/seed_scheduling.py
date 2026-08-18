from datetime import time

from django.core.management.base import BaseCommand

from apps.scheduling.models import Machine, Shift

MACHINES = [f"M-{i:02d}" for i in range(1, 11)]

SHIFTS = [
    ("Morning", time(6, 0), time(10, 0)),
    ("Midday", time(10, 30), time(14, 30)),
    ("Afternoon", time(15, 0), time(19, 0)),
]


class Command(BaseCommand):
    help = "Seed default dialysis machines and shifts for a demo/dev center."

    def handle(self, *args, **options):
        for code in MACHINES:
            _, created = Machine.objects.get_or_create(code=code)
            self.stdout.write(f"Machine {code}: {'created' if created else 'exists'}")

        for name, start, end in SHIFTS:
            _, created = Shift.objects.get_or_create(
                name=name, defaults={"start_time": start, "end_time": end}
            )
            self.stdout.write(f"Shift {name}: {'created' if created else 'exists'}")

        self.stdout.write(self.style.SUCCESS("Scheduling seed data ready."))
