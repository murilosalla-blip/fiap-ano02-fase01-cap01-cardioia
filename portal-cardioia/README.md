# CardioIA Portal — Grupo Aura

Portal responsivo desenvolvido em React + Vite para o **Ir Além 1** da Fase 2 do CardioIA.

> Todos os pacientes e agendamentos são fictícios. O projeto é exclusivamente educacional e não realiza diagnóstico.

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

## Credenciais de demonstração

As credenciais são inteiramente fictícias e aparecem na própria tela de login
para facilitar a demonstração acadêmica. Não reutilize credenciais reais neste
protótipo.

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

## Publicação

O portal está publicado em [Julia-carvalho96/fiap-cardioia-portal](https://github.com/Julia-carvalho96/fiap-cardioia-portal).

Pendências finais:

- adicionar a lista de integrantes e RMs após autorização explícita;
- adicionar o link do vídeo não listado de até quatro minutos.
