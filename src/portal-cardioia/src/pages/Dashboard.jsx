import { useEffect, useState } from "react";
import StatCard from "../components/StatCard";
import { loadAppointments } from "../data/demoData";
import { fetchPatients } from "../services/api";
import styles from "../styles/Portal.module.css";

export default function Dashboard() {
  const [patients, setPatients] = useState([]);
  const [error, setError] = useState("");
  const appointments = loadAppointments();

  useEffect(() => {
    fetchPatients().then(setPatients).catch((reason) => setError(reason.message));
  }, []);

  const priorities = patients.filter((patient) => patient.status === "Prioridade").length;
  const stable = patients.filter((patient) => patient.status === "Estável").length;
  const followUp = patients.filter((patient) => patient.status === "Acompanhamento").length;
  const upcoming = [...appointments]
    .sort((a, b) => `${a.date}${a.time}`.localeCompare(`${b.date}${b.time}`))
    .slice(0, 3);

  return (
    <>
      <header className={styles.pageHeader}>
        <div><span>Visão geral</span><h2>Dashboard</h2></div>
        <p>Indicadores simulados da rotina cardiológica.</p>
      </header>
      {error && <p className={styles.error} role="alert">{error}</p>}
      <section className={styles.statsGrid}>
        <StatCard label="Pacientes" value={patients.length} detail="Cadastros simulados" />
        <StatCard label="Consultas" value={appointments.length} detail="Agenda demonstrativa" />
        <StatCard label="Prioridades" value={priorities} detail="Marcadores demonstrativos" />
      </section>
      <section className={styles.dashboardGrid}>
        <article className={styles.contentCard}>
          <span className={styles.eyebrow}>Próximos atendimentos</span>
          <h3>Agenda da equipe</h3>
          <ul className={styles.timelineList}>
            {upcoming.map((item) => (
              <li key={item.id}>
                <div className={styles.dateBadge}>
                  <strong>{item.date.slice(8, 10)}</strong>
                  <span>{item.date.slice(5, 7)}</span>
                </div>
                <div>
                  <strong>{item.patient}</strong>
                  <p>{item.time} • {item.specialty}</p>
                  <small>{item.professional}</small>
                </div>
              </li>
            ))}
          </ul>
        </article>
        <article className={styles.contentCard}>
          <span className={styles.eyebrow}>Carteira fictícia</span>
          <h3>Status dos pacientes</h3>
          <div className={styles.statusSummary}>
            <div><strong>{stable}</strong><span>Estáveis</span></div>
            <div><strong>{followUp}</strong><span>Em acompanhamento</span></div>
            <div><strong>{priorities}</strong><span>Prioridades</span></div>
          </div>
        </article>
      </section>
      <section className={styles.contentCard}>
        <span className={styles.eyebrow}>Produto principal</span>
        <h3>Realize uma avaliação no CardioIA</h3>
        <p>
          Execute as demonstrações de dados clínicos e relatos de sintomas e consulte
          as evidências do experimento visual de ECG no ambiente unificado em Streamlit.
        </p>
        <a
          className={styles.primaryLink}
          href="https://cardioia-fiap.streamlit.app/"
          target="_blank"
          rel="noreferrer"
        >
          Abrir CardioIA — realizar avaliação
        </a>
      </section>
      <section className={styles.contentCard}>
        <h3>Sobre este protótipo administrativo</h3>
        <p>
          Este front usa somente dados fictícios e demonstra Context API, Hooks,
          rotas protegidas, consumo de JSON e controle de estado. Os modelos de IA
          são executados separadamente no produto principal.
        </p>
      </section>
    </>
  );
}
