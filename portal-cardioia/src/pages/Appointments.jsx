import { useReducer, useState } from "react";
import styles from "../styles/Portal.module.css";

const initialForm = { patient: "", date: "", specialty: "Cardiologia" };

function formReducer(state, action) {
  if (action.type === "change") return { ...state, [action.field]: action.value };
  if (action.type === "reset") return initialForm;
  return state;
}

export default function Appointments() {
  const [form, dispatch] = useReducer(formReducer, initialForm);
  const [appointments, setAppointments] = useState(() =>
    JSON.parse(localStorage.getItem("cardioia_appointments") || "[]"),
  );
  const [message, setMessage] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    if (!form.patient.trim() || !form.date) {
      setMessage("Preencha paciente e data.");
      return;
    }
    const next = [...appointments, { ...form, id: crypto.randomUUID() }];
    setAppointments(next);
    localStorage.setItem("cardioia_appointments", JSON.stringify(next));
    dispatch({ type: "reset" });
    setMessage("Consulta simulada agendada.");
  }

  function removeAppointment(id) {
    const next = appointments.filter((item) => item.id !== id);
    setAppointments(next);
    localStorage.setItem("cardioia_appointments", JSON.stringify(next));
    setMessage("Consulta simulada removida.");
  }

  return (
    <>
      <header className={styles.pageHeader}>
        <div><span>Agenda local</span><h2>Agendamentos</h2></div>
        <p>Formulário controlado com useState e useReducer.</p>
      </header>
      <div className={styles.twoColumns}>
        <section className={styles.contentCard}>
          <h3>Nova consulta</h3>
          <form onSubmit={handleSubmit}>
            <label>
              Paciente
              <input
                value={form.patient}
                onChange={(event) => dispatch({ type: "change", field: "patient", value: event.target.value })}
                placeholder="Nome fictício"
              />
            </label>
            <label>
              Data
              <input
                type="date"
                value={form.date}
                onChange={(event) => dispatch({ type: "change", field: "date", value: event.target.value })}
              />
            </label>
            <label>
              Especialidade
              <select
                value={form.specialty}
                onChange={(event) => dispatch({ type: "change", field: "specialty", value: event.target.value })}
              >
                <option>Cardiologia</option>
                <option>Clínica geral</option>
                <option>Exames cardiológicos</option>
              </select>
            </label>
            <button className={styles.primaryButton} type="submit">Agendar consulta</button>
            {message && <p role="status">{message}</p>}
          </form>
        </section>
        <section className={styles.contentCard}>
          <h3>Consultas agendadas ({appointments.length})</h3>
          {appointments.length === 0 ? (
            <p>Nenhuma consulta simulada.</p>
          ) : (
            <ul className={styles.appointmentList}>
              {appointments.map((item) => (
                <li key={item.id}>
                  <div><strong>{item.patient}</strong>
                  <span>{item.specialty} • {item.date}</span></div>
                  <button type="button" className={styles.removeButton}
                    aria-label={`Remover consulta de ${item.patient}`}
                    onClick={() => removeAppointment(item.id)}>Remover</button>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </>
  );
}
