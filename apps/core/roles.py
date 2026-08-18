"""Central definition of the system's role names.

These map 1:1 to Django Group names created by `accounts`' `seed_roles`
management command, and are referenced by every app's permission classes
so the role list has a single source of truth.
"""


class Roles:
    ADMIN = "Admin"
    DOCTOR = "Doctor"
    NURSE = "Nurse"
    PHARMACIST = "Pharmacist"
    WAREHOUSE_KEEPER = "WarehouseKeeper"
    LAB_TECH = "LabTech"
    RECEPTIONIST = "Receptionist"

    ALL = (
        ADMIN,
        DOCTOR,
        NURSE,
        PHARMACIST,
        WAREHOUSE_KEEPER,
        LAB_TECH,
        RECEPTIONIST,
    )
