# CardioIA Portal — Grupo Aura

Portal responsivo desenvolvido em React + Vite para o **Ir Além 1** da Fase 2 do CardioIA. A aplicação simula a rotina administrativa de uma clínica cardiológica com autenticação, carteira de pacientes, agenda e indicadores.

## Links da demonstração

- **Portal administrativo:** https://julia-carvalho96.github.io/grupo-aura-cardioia-portal/
- **Simulação dos modelos de IA:** https://cardioia-fiap.streamlit.app/
- **Repositório público do portal:** https://github.com/Julia-carvalho96/grupo-aura-cardioia-portal

O portal organiza pacientes e consultas. O Streamlit executa as modalidades independentes de IA da Fase 2: extração de sintomas, classificação textual de risco e demonstração tabular. Os dois produtos possuem navegação entre si, mas continuam em deploys separados porque o portal é um protótipo front-end sem back-end real.

> Todos os pacientes e agendamentos são fictícios. O projeto é exclusivamente educacional e não realiza diagnóstico.

## Integrantes

- Murilo Salla — RM568041
- Elias da Silva de Souza — RM568500
- Julia Duarte de Carvalho — RM567816

## Funcionalidades

- autenticação simulada via Context API;
- JWT fictício salvo no localStorage;
- proteção de rotas;
- dashboard de pacientes, consultas e prioridades;
- carteira demonstrativa com 12 pacientes totalmente fictícios;
- agenda inicial com seis consultas fictícias e diferentes especialidades;
- visão de próximos atendimentos e distribuição por status;
- listagem consumida de JSON local por uma camada de serviço;
- busca de pacientes;
- agendamento com useState e useReducer;
- inclusão, persistência e remoção de consultas simuladas;
- persistência local dos agendamentos;
- layout responsivo com CSS Modules.

## Atendimento aos critérios

| Critério | Implementação |
|---|---|
| Autenticação e proteção de rotas | `AuthContext`, JWT fictício no `localStorage` e `ProtectedRoute` |
| Consumo de dados | 12 pacientes fictícios carregados de JSON local pela camada `services` |
| Controle de estado | `useState`, `useReducer`, `useEffect` e `useContext` |
| Agendamentos | Seis consultas iniciais, criação, persistência e remoção local |
| Dashboard | Totais de pacientes e consultas, prioridades, próximos atendimentos e distribuição por status |
| Componentização | Pastas independentes para contextos, componentes, serviços e páginas |
| Responsividade | CSS Modules com adaptação para desktop, tablet e celular |

## Testes

Os sete testes executados por `npm test` cobrem rota protegida, login válido e inválido, busca e
falha no carregamento de pacientes, carga da agenda fictícia,
criação/persistência/remoção de agendamentos, vínculo com o produto de IA e
logout. `npm run build` valida a versão de produção.

## Acesso de demonstração

Informe qualquer e-mail fictício em formato válido e uma senha com pelo menos
seis caracteres. Não reutilize credenciais reais neste protótipo.

## Estrutura

```text
src/
├── components/
├── contexts/
├── pages/
├── services/
└── styles/
```

## Executar

Pré-requisito: Node.js `22.13` ou superior, ou Node.js `24`. Essas versões são compatíveis com as dependências registradas no `package-lock.json`.

```bash
npm install
npm run dev
```

## Validar a build

```bash
npm test
npm run build
```

## Vídeo da entrega

O enunciado exige um vídeo não listado no YouTube, com até quatro minutos. O link será inserido aqui depois da gravação e publicação.
