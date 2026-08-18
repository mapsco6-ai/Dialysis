from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.pharmacy.models import Prescription

from .models import MedicationAdministrationRecord


@receiver(post_save, sender=Prescription)
def create_mar_task_for_new_prescription(sender, instance, created, **kwargs):
    """A newly written active prescription immediately becomes a task on
    the nurse's MAR list - this is the automatic half of the nurse's
    hybrid workflow (task list + always-available manual chart access)."""
    if created and instance.status == Prescription.Status.ACTIVE:
        MedicationAdministrationRecord.objects.create(
            prescription=instance,
            patient=instance.patient,
            scheduled_time=timezone.now(),
        )
