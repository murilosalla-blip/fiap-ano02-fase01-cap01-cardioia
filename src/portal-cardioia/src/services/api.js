export function buildPatientsUrl(baseUrl = import.meta.env.BASE_URL) {
  return `${baseUrl}data/patients.json`;
}

export async function fetchPatients() {
  const response = await fetch(buildPatientsUrl());
  if (!response.ok) throw new Error("Não foi possível carregar os pacientes.");
  return response.json();
}
