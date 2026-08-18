import { useQuery } from "@tanstack/react-query";
import { apiClient } from "./client";
import type { DialysisSession, Machine, Paginated, Patient } from "./types";

export function usePatients() {
  return useQuery({
    queryKey: ["patients"],
    queryFn: async () => (await apiClient.get<Paginated<Patient>>("/patients/")).data,
  });
}

export function useMachines() {
  return useQuery({
    queryKey: ["machines"],
    queryFn: async () => (await apiClient.get<Paginated<Machine>>("/machines/")).data,
  });
}

export function useDialysisSessions() {
  return useQuery({
    queryKey: ["dialysis-sessions"],
    queryFn: async () =>
      (await apiClient.get<Paginated<DialysisSession>>("/dialysis-sessions/")).data,
  });
}
