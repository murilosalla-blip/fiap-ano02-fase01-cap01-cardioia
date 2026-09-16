export async function fetchPatients() {
  const response = await fetch(`${import.meta.env.BASE_URL}data/patients.json`);
  if (!response.ok) throw new Error("Não foi possível carregar os pacientes.");
  return response.json();
}
