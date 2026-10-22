# TaskFlow API

API REST para gerenciamento de tarefas, desenvolvida com Python e FastAPI.

Criei este projeto durante meus estudos de desenvolvimento backend para colocar em prática autenticação, operações com banco de dados, testes automatizados e Docker. A ideia é simples: cada usuário pode organizar suas próprias tarefas e acompanhar o andamento delas.

## Funcionalidades

- Cadastro, consulta, atualização e exclusão de usuários
- Login com JWT e proteção das rotas que exigem autenticação
- Criação, listagem, edição e exclusão de tarefas
- Tarefas vinculadas ao usuário autenticado
- Estados das tarefas: `draft`, `todo`, `doing`, `done` e `trash`
- Filtros por título, descrição e estado, com paginação
- Documentação interativa gerada pelo FastAPI

## Tecnologias

- **Python e FastAPI** — desenvolvimento da API
- **SQLAlchemy (assíncrono) e PostgreSQL** — persistência de dados
- **Alembic** — migrações do banco
- **Pydantic** — validação dos dados e configurações
- **JWT e pwdlib** — autenticação e hash de senhas
- **Poetry** — gerenciamento de dependências
- **Docker Compose** — ambiente local com API e banco de dados
- **Pytest, Ruff e GitHub Actions** — testes, lint e integração contínua

## Como executar

O jeito mais simples de rodar o projeto é com Docker e Docker Compose instalados.

**1. Clone o repositório:**

```bash
git clone https://github.com/FelipeMNV/TaskFlow-API.git
cd TaskFlow-API
```

**2. Crie um arquivo `.env` na raiz do projeto** com estas variáveis:

```env
SECRET_KEY=substitua-por-uma-chave-secreta-forte
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

O `compose.yaml` já configura a conexão com o PostgreSQL para a execução via Docker. Não publique seu arquivo `.env`.

**3. Suba os containers:**

```bash
docker compose up --build
```

O script de inicialização aplica as migrações com Alembic antes de subir a API.

Com a aplicação rodando, acesse:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Principais rotas

| Método | Rota | O que faz |
| --- | --- | --- |
| `POST` | `/users/` | Cadastra um usuário |
| `GET` | `/users/` | Lista usuários (requer autenticação) |
| `GET` | `/users/{user_id}` | Consulta um usuário |
| `PUT` | `/users/{user_id}` | Atualiza a própria conta |
| `DELETE` | `/users/{user_id}` | Exclui a própria conta |
| `POST` | `/auth/token` | Faz login e retorna um token JWT |
| `POST` | `/auth/refresh_token` | Emite um novo token a partir de um token válido |
| `POST` | `/todos/` | Cria uma tarefa |
| `GET` | `/todos/` | Lista e filtra as próprias tarefas |
| `PATCH` | `/todos/{todo_id}` | Atualiza uma tarefa |
| `DELETE` | `/todos/{todo_id}` | Exclui uma tarefa |

Para testar as rotas protegidas pelo Swagger, cadastre um usuário em `POST /users/` e depois use **Authorize** para fazer login com o e-mail e a senha cadastrados.

## Testes

Com as dependências instaladas pelo Poetry, execute:

```bash
poetry run task test
```

Esse comando também executa a verificação de lint antes dos testes. O repositório possui um workflow do GitHub Actions para rodar essas verificações em pushes e pull requests.

## Sobre o projeto

Este é um projeto de estudo, meu objetivo foi entender melhor o desenvolvimento de uma API do início ao fim, incluindo banco de dados, autenticação, testes e execução em containers.
