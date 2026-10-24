import { createContext, useContext, useMemo, useState } from "react";

const AuthContext = createContext(null);
const TOKEN_KEY = "cardioia_fake_jwt";

function criarTokenFake(email) {
  const payload = { sub: email, role: "demo", exp: Date.now() + 3_600_000 };
  return btoa(JSON.stringify(payload));
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY));

  function login(email, password) {
    const emailValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
    const senhaValida = password.trim().length >= 6;
    if (!emailValido || !senhaValida) {
      return {
        success: false,
        message: "Informe um e-mail fictício válido e uma senha com pelo menos 6 caracteres.",
      };
    }
    const nextToken = criarTokenFake(email);
    localStorage.setItem(TOKEN_KEY, nextToken);
    setToken(nextToken);
    return { success: true };
  }

  function logout() {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
  }

  const value = useMemo(
    () => ({ isAuthenticated: Boolean(token), token, login, logout }),
    [token],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth deve ser usado dentro de AuthProvider.");
  return context;
}
