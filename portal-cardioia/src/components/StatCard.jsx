import styles from "../styles/Portal.module.css";

export default function StatCard({ label, value, detail }) {
  return (
    <article className={styles.statCard}>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </article>
  );
}
