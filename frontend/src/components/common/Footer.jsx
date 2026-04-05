import styles from './Footer.module.css';

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        <p>&copy; {new Date().getFullYear()} Glinqx – Share. Discover. Connect.</p>
      </div>
    </footer>
  );
}