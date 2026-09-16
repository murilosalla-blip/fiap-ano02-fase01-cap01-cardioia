import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import styles from "../styles/Portal.module.css";

export default function Layout() {
  const { logout } = useAuth();
  return (
    <div className={styles.appShell}>
      <aside className={styles.sidebar}>
        <div>
          <span className={styles.badge}>Grupo Aura</span>
          <h1>CardioIA</h1>
          <p>Portal acadêmico</p>
        </div>
        <nav aria-label="Navegação principal">
          <NavLink to="/" end>Dashboard</NavLink>
          <NavLink to="/pacientes">Pacientes</NavLink>
          <NavLink to="/agendamentos">Agendamentos</NavLink>
          <a
            href="https://cardioia-fiap.streamlit.app/"
            target="_blank"
            rel="noreferrer"
          >
            Modelos de IA ↗
          </a>
        </nav>
        <button className={styles.secondaryButton} onClick={logout}>Sair</button>
      </aside>
      <main className={styles.mainContent}>
        <div className={styles.demoNotice}>
          Dados inteiramente simulados • Uso educacional
        </div>
        <Outlet />
      </main>
    </div>
  );
}
