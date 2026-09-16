# CardioIA Portal — Grupo Aura

Portal responsivo desenvolvido em React + Vite para o **Ir Além 1** da Fase 2 do CardioIA.

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
- listagem consumida de JSON local por uma camada de serviço;
- busca de pacientes;
- agendamento com useState e useReducer;
- inclusão, persistência e remoção de consultas simuladas;
- persistência local dos agendamentos;
- layout responsivo com CSS Modules.

## Testes

`npm test -- --run` cobre rota protegida, login válido e inválido, busca e falha no carregamento de pacientes, criação/persistência/remoção de agendamentos e logout. `npm run build` valida a versão de produção.

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
npm run build
```

## Pendências de publicação

- adicionar o link do vídeo não listado de até quatro minutos.
