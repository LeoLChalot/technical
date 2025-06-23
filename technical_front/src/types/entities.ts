export interface Project {
  id: number;
  name: string;
  is_active: boolean;
  created_at: string; // Les dates arrivent en format string (ISO) depuis l'API
  updated_at: string;
}

export interface Indicator {
  id: number;
  identifier: string;
  label: string;
  label_short: string;
  timeslots: number;
  position: number;
  asset: string | null;
}