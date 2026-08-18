from django.core.management.base import BaseCommand

from apps.lab.models import LabTestType

TEST_TYPES = [
    ("Serum Creatinine", "CREA", "Renal panel", "mg/dL", "0.6", "1.3", "blood"),
    ("Blood Urea Nitrogen", "BUN", "Renal panel", "mg/dL", "7", "20", "blood"),
    ("Potassium", "K", "Electrolytes", "mmol/L", "3.5", "5.1", "blood"),
    ("Sodium", "NA", "Electrolytes", "mmol/L", "135", "145", "blood"),
    ("Hemoglobin", "HGB", "CBC", "g/dL", "12", "17.5", "blood"),
    ("Calcium", "CA", "Bone/mineral", "mg/dL", "8.5", "10.5", "blood"),
    ("Phosphorus", "PHOS", "Bone/mineral", "mg/dL", "2.5", "4.5", "blood"),
    ("Hepatitis B Surface Antigen", "HBSAG", "Virology", "", None, None, "blood"),
    ("Hepatitis C Antibody", "HCVAB", "Virology", "", None, None, "blood"),
]


class Command(BaseCommand):
    help = "Seed common lab test types for a dialysis center."

    def handle(self, *args, **options):
        for name, code, category, unit, low, high, sample in TEST_TYPES:
            _, created = LabTestType.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                    "category": category,
                    "unit": unit,
                    "reference_range_low": low,
                    "reference_range_high": high,
                    "sample_type": sample,
                },
            )
            self.stdout.write(f"{code}: {'created' if created else 'exists'}")

        self.stdout.write(self.style.SUCCESS("Lab seed data ready."))
