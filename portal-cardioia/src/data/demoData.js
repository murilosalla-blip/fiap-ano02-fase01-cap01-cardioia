export const DEFAULT_APPOINTMENTS = [
  { id: "demo-1", patient: "Carlos Souza", date: "2026-09-17", time: "09:00", specialty: "Cardiologia", professional: "Dra. Camila Torres", status: "Confirmada" },
  { id: "demo-2", patient: "Paulo Costa", date: "2026-09-18", time: "11:30", specialty: "Exames cardiológicos", professional: "Equipe de diagnóstico", status: "Confirmada" },
  { id: "demo-3", patient: "Lúcia Ferreira", date: "2026-09-21", time: "14:00", specialty: "Cardiologia", professional: "Dr. André Vieira", status: "A confirmar" },
  { id: "demo-4", patient: "Ana Martins", date: "2026-09-23", time: "10:30", specialty: "Retorno", professional: "Dra. Camila Torres", status: "Confirmada" },
  { id: "demo-5", patient: "João Ribeiro", date: "2026-09-28", time: "15:30", specialty: "Cardiologia", professional: "Dr. André Vieira", status: "A confirmar" },
  { id: "demo-6", patient: "Helena Rocha", date: "2026-10-01", time: "08:30", specialty: "Clínica geral", professional: "Dra. Larissa Melo", status: "Confirmada" }
];

export function loadAppointments() {
  const saved = localStorage.getItem("cardioia_appointments");
  return saved ? JSON.parse(saved) : DEFAULT_APPOINTMENTS;
}
