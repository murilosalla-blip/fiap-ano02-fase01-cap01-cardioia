import "@testing-library/jest-dom/vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import App from "./App";
import { AuthProvider } from "./contexts/AuthContext";

function renderPortal(route = "/") {
  return render(
    <MemoryRouter initialEntries={[route]}>
      <AuthProvider>
        <App />
      </AuthProvider>
    </MemoryRouter>,
  );
}

describe("CardioIA Portal", () => {
  beforeEach(() => {
    localStorage.clear();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => [
          { id: 1, name: "Paciente Teste", age: 50, status: "Estável", lastVisit: "01/09/2026" },
        ],
      }),
    );
  });

  it("protege as rotas e permite login com credenciais simuladas", async () => {
    renderPortal("/");
    expect(await screen.findByText("Entrar no CardioIA")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Entrar" }));

    expect(await screen.findByRole("heading", { name: "Dashboard" })).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText("1")).toBeInTheDocument());
    expect(localStorage.getItem("cardioia_fake_jwt")).toBeTruthy();
  });

  it("rejeita credenciais diferentes das credenciais demonstrativas", async () => {
    renderPortal("/login");
    fireEvent.change(screen.getByLabelText("E-mail"), {
      target: { value: "invalido@exemplo.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Entrar" }));
    expect(await screen.findByRole("alert")).toHaveTextContent(
      "E-mail ou senha de demonstração inválidos.",
    );
  });

  it("busca pacientes simulados e apresenta falha da API", async () => {
    localStorage.setItem("cardioia_fake_jwt", "token");
    const view = renderPortal("/pacientes");
    expect(await screen.findByText("Paciente Teste")).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Buscar paciente"), { target: { value: "ausente" } });
    expect(screen.queryByText("Paciente Teste")).not.toBeInTheDocument();
    view.unmount();
    fetch.mockResolvedValueOnce({ ok: false });
    renderPortal("/pacientes");
    expect(await screen.findByRole("alert")).toHaveTextContent("Não foi possível carregar os pacientes.");
  });

  it("valida, cria, persiste e remove agendamentos", async () => {
    localStorage.setItem("cardioia_fake_jwt", "token");
    renderPortal("/agendamentos");
    fireEvent.click(screen.getByRole("button", { name: "Agendar consulta" }));
    expect(await screen.findByRole("status")).toHaveTextContent("Preencha paciente e data.");
    fireEvent.change(screen.getByLabelText("Paciente"), { target: { value: "Pessoa Fictícia" } });
    fireEvent.change(screen.getByLabelText("Data"), { target: { value: "2026-10-10" } });
    fireEvent.click(screen.getByRole("button", { name: "Agendar consulta" }));
    expect(await screen.findByText("Pessoa Fictícia")).toBeInTheDocument();
    expect(JSON.parse(localStorage.getItem("cardioia_appointments"))).toHaveLength(1);
    fireEvent.click(screen.getByRole("button", { name: "Remover consulta de Pessoa Fictícia" }));
    expect(screen.queryByText("Pessoa Fictícia")).not.toBeInTheDocument();
    expect(JSON.parse(localStorage.getItem("cardioia_appointments"))).toHaveLength(0);
  });

  it("encerra a sessão e volta ao login", async () => {
    localStorage.setItem("cardioia_fake_jwt", "token");
    renderPortal("/");
    fireEvent.click(await screen.findByRole("button", { name: "Sair" }));
    expect(await screen.findByText("Entrar no CardioIA")).toBeInTheDocument();
    expect(localStorage.getItem("cardioia_fake_jwt")).toBeNull();
  });
});
