from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for every staff account in the system.

    Patients are NOT users - they are represented by the separate
    `patients.Patient` model and never log in.
    """

    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    national_id = models.CharField(max_length=32, blank=True)
    employee_id = models.CharField(max_length=32, blank=True, unique=False)
    hire_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.full_name or self.username
