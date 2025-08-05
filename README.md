# Workout API

Uma API robusta para gerenciamento de academias, atletas, categorias e centros de treinamento, desenvolvida com FastAPI e SQLAlchemy como parte do bootcamp de backend Python da Santander.

## ✨ Funcionalidades

- **CRUD Completo**: Operações de Criar, Ler, Atualizar e Deletar para os principais recursos da aplicação:
  - Atletas
  - Categorias
  - Centros de Treinamento
- **Validação de Dados**: Uso intensivo do Pydantic para garantir a integridade e o formato correto dos dados de entrada e saída.
- **Banco de Dados Assíncrono**: Conexão de alta performance com PostgreSQL utilizando `asyncpg` e `SQLAlchemy 2.0`.
- **Migrações de Banco de Dados**: Gerenciamento seguro e versionado do schema do banco de dados com Alembic.
- **Paginação**: Suporte para paginação `limit/offset` em todos os endpoints de listagem para lidar com grandes volumes de dados.
- **Filtros Dinâmicos**: Possibilidade de filtrar a listagem de atletas por nome e CPF através de *query parameters*.
- **Documentação Automática**: Geração automática de documentação interativa da API com Swagger UI e ReDoc.

## 🛠️ Tecnologias Utilizadas

- **Python 3.12+**
- **FastAPI**: Para a construção da API.
- **Pydantic**: Para validação de dados e gerenciamento de configurações.
- **SQLAlchemy**: Para o ORM e interação com o banco de dados.
- **Alembic**: Para migrações de banco de dados.
- **PostgreSQL**: Como sistema de gerenciamento de banco de dados.
- **Uvicorn**: Como servidor ASGI.
- **Poetry**: Para gerenciamento de dependências.
- **fastapi-pagination**: Para a implementação da paginação.

## 🚀 Configuração e Instalação

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

- Python 3.12 ou superior
- Poetry instalado
- Uma instância do PostgreSQL rodando

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd curso-santander
    ```

2.  **Crie e configure o arquivo de ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto e preencha com as suas credenciais do banco de dados.

    ```dotenv
    # /home/davidsc/projetos-python/curso-santander/.env

    DB_USER=seu_usuario
    DB_PASSWORD=sua_senha
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=workout_db
    ```

3.  **Instale as dependências:**
    Utilize o Poetry para instalar todas as dependências listadas no `pyproject.toml`.
    ```bash
    poetry install
    ```

4.  **Ative o ambiente virtual:**
    ```bash
    poetry shell
    ```

5.  **Execute as migrações do banco de dados:**
    Este comando criará todas as tabelas necessárias no banco de dados.
    ```bash
    alembic upgrade head
    ```

6.  **Inicie a aplicação:**
    ```bash
    uvicorn main:app --host=0.0.0.0 --port=8000 --reload
    ```

7.  **Acesse a documentação:**
    Com o servidor rodando, acesse a documentação interativa em seu navegador:
    - **Swagger UI:** http://localhost:8000/docs
    - **ReDoc:** http://localhost:8000/redoc