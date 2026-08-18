import uuid

from django.db import models


class UUIDModel(models.Model):
    """Abstract base using a UUID primary key instead of a sequential id."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """Abstract base adding created_at/updated_at timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimeStampedModel):
    """Convenience base combining UUID primary key + timestamps, used by
    every clinical/operational model in the system."""

    class Meta:
        abstract = True
