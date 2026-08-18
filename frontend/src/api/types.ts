export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface Patient {
  id: string;
  mrn: string;
  full_name: string;
  gender: "M" | "F";
  phone: string;
  is_active: boolean;
}

export interface Machine {
  id: string;
  code: string;
  room: string;
  status: "available" | "in_use" | "maintenance" | "out_of_service";
}

export interface DialysisSession {
  id: string;
  patient: string;
  patient_name: string;
  machine: string | null;
  shift: string | null;
  scheduled_date: string;
  status: "scheduled" | "checked_in" | "in_progress" | "completed" | "cancelled" | "no_show";
}
