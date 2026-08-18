// Mirrors apps/core/roles.py on the backend - the 7 staff role Groups.
export const Roles = {
  ADMIN: "Admin",
  DOCTOR: "Doctor",
  NURSE: "Nurse",
  PHARMACIST: "Pharmacist",
  WAREHOUSE_KEEPER: "WarehouseKeeper",
  LAB_TECH: "LabTech",
  RECEPTIONIST: "Receptionist",
} as const;

export type Role = (typeof Roles)[keyof typeof Roles];

export const ROLE_LABELS_AR: Record<Role, string> = {
  [Roles.ADMIN]: "مدير النظام",
  [Roles.DOCTOR]: "طبيب",
  [Roles.NURSE]: "ممرض",
  [Roles.PHARMACIST]: "صيدلي",
  [Roles.WAREHOUSE_KEEPER]: "مسؤول مخزن",
  [Roles.LAB_TECH]: "فني مختبر",
  [Roles.RECEPTIONIST]: "استقبال",
};
