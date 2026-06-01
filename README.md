# ERP Academia - API

API para gerenciamento de academia com autenticação JWT, controle de usuários e módulos de planos, modalidades, treinos e pagamentos.

## Funcionalidades

- Autenticação de API com JWT (`access` e `refresh token`)
- CRUD de usuários:
  - Usuários
  - Administradores
  - Funcionários
  - Alunos
- CRUD de planos
- CRUD de modalidades
- CRUD de inscrições em modalidades
- CRUD de frequências
- CRUD de treinos
- CRUD de pagamentos
- Documentação OpenAPI/Swagger

## Stack

- Python
- Django
- Django REST Framework
- SimpleJWT
- drf-spectacular (schema e Swagger UI)
- PostgreSQL

## Requisitos

- Python 3.12+ (ou compatível com seu ambiente)
- PostgreSQL rodando
- Banco criado (ex.: `erp_academia`)

## Configuração do ambiente

### 1) Clone e acesse o projeto

```bash
git clone <url-do-seu-repositorio>
cd "tde POO"
```

### 2) Crie e ative o ambiente virtual

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3) Instale as dependências

```bash
pip install -r requirements.txt
```

### 4) Configure variáveis de ambiente

Crie o arquivo `.env` na raiz do projeto (mesmo nível do `manage.py`).

Use este modelo:

```env
SECRET_KEY=coloque_uma_chave_segura_aqui
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=django.db.backends.postgresql
DB_NAME=erp_academia
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

## Banco de dados

### 1) Gerar/aplicar migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2) Criar superusuário (opcional, recomendado)

```bash
python manage.py createsuperuser
```

## Como rodar

```bash
python manage.py runserver
```

Servidor local padrão:

- `http://127.0.0.1:8000/`

## Autenticação da API (JWT)

### Login (obter tokens)

`POST /api/auth/login/`

Payload:

```json
{
  "email": "seu_email",
  "password": "sua_senha"
}
```

Resposta:

```json
{
  "refresh": "...",
  "access": "..."
}
```

### Refresh do access token

`POST /api/auth/refresh/`

Payload:

```json
{
  "refresh": "seu_refresh_token"
}
```

### Uso do token nas rotas protegidas

Enviar header:

```http
Authorization: Bearer <access_token>
```

## Documentação da API

- Schema OpenAPI: `GET /api/schema/`
- Swagger UI: `GET /api/docs/`

## Endpoints da API

Base URL local: `http://127.0.0.1:8000`

### Academia

- `GET/POST /api/academia/usuarios/`
- `GET/PUT/PATCH/DELETE /api/academia/usuarios/{id}/`
- `GET/POST /api/academia/administradores/`
- `GET/PUT/PATCH/DELETE /api/academia/administradores/{id}/`
- `GET/POST /api/academia/funcionarios/`
- `GET/PUT/PATCH/DELETE /api/academia/funcionarios/{id}/`
- `GET/POST /api/academia/alunos/`
- `GET/PUT/PATCH/DELETE /api/academia/alunos/{id}/`

### Planos

- `GET/POST /api/planos/`
- `GET/PUT/PATCH/DELETE /api/planos/{id_plano}/`

### Modalidades

- `GET/POST /api/modalidades/`
- `GET/PUT/PATCH/DELETE /api/modalidades/{id}/`
- `GET/POST /api/modalidades/inscricoes/`
- `GET/PUT/PATCH/DELETE /api/modalidades/inscricoes/{id}/`
- `GET/POST /api/modalidades/frequencias/`
- `GET/PUT/PATCH/DELETE /api/modalidades/frequencias/{id}/`

### Treinos

- `GET/POST /api/treinos/`
- `GET/PUT/PATCH/DELETE /api/treinos/{id_treino}/`

### Pagamentos

- `GET/POST /api/pagamentos/`
- `GET/PUT/PATCH/DELETE /api/pagamentos/{id}/`

## Interface administrativa do Django

- `GET /admin/`

Requer usuário com permissões de staff/superuser.

## Estrutura resumida

- `config/` -> configurações globais do Django e rotas principais
- `academia/` -> usuários e perfis
- `planos/` -> planos de assinatura
- `modalidades/` -> modalidades, inscrições e frequências
- `treinos/` -> gestão de treinos
- `pagamentos/` -> gestão financeira de mensalidades

## Observações de segurança (produção)

- Defina `DEBUG=False`
- Configure `ALLOWED_HOSTS` com domínios reais
- Não versione `.env`
- Rotacione credenciais sensíveis se já foram expostas anteriormente
