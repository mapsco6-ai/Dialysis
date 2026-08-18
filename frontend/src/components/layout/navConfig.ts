import {
  LayoutGrid,
  Users,
  CalendarClock,
  Pill,
  Package,
  ClipboardList,
  FlaskConical,
  UserCog,
} from "lucide-react";
import { Roles, type Role } from "../../auth/roles";

export interface NavItem {
  label: string;
  path: string;
  icon: typeof LayoutGrid;
  roles: Role[] | "all";
}

export const NAV_ITEMS: NavItem[] = [
  { label: "لوحة التحكم", path: "/", icon: LayoutGrid, roles: "all" },
  {
    label: "المرضى",
    path: "/patients",
    icon: Users,
    roles: [Roles.DOCTOR, Roles.NURSE, Roles.RECEPTIONIST, Roles.PHARMACIST, Roles.LAB_TECH],
  },
  {
    label: "الجدولة",
    path: "/scheduling",
    icon: CalendarClock,
    roles: [Roles.RECEPTIONIST, Roles.DOCTOR, Roles.NURSE],
  },
  {
    label: "الصيدلية",
    path: "/pharmacy",
    icon: Pill,
    roles: [Roles.PHARMACIST, Roles.DOCTOR],
  },
  {
    label: "المخزن",
    path: "/warehouse",
    icon: Package,
    roles: [Roles.WAREHOUSE_KEEPER, Roles.PHARMACIST],
  },
  {
    label: "مهام التمريض",
    path: "/nursing",
    icon: ClipboardList,
    roles: [Roles.NURSE, Roles.DOCTOR],
  },
  {
    label: "المختبر",
    path: "/lab",
    icon: FlaskConical,
    roles: [Roles.LAB_TECH, Roles.DOCTOR],
  },
  { label: "الموظفون", path: "/staff", icon: UserCog, roles: [Roles.ADMIN] },
];
