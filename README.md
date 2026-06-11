# Fit API

Sistema web para gerenciamento de academia, desenvolvido em Django. O projeto organiza as principais rotinas de uma academia: usuários, perfis de acesso, planos, modalidades, turmas, frequências, treinos e pagamentos.

## Funcionalidades

- Login e logout de usuários.
- Dashboards por perfil: administrador, funcionário e aluno.
- Cadastro, listagem, edição e exclusão de usuários.
- Gestão de planos de assinatura.
- Gestão de modalidades, turmas, inscrições e frequências.
- Gestão de treinos e sugestão por grupo muscular.
- Controle de pagamentos.
- Endpoints JSON para integração.
- Documentação OpenAPI/Swagger.

## Stack

- Python
- Django
- Django REST Framework
- SimpleJWT
- drf-spectacular
- PostgreSQL

## Como o sistema se comunica

A aplicação segue um fluxo direto entre navegador, backend e banco de dados:

1. O usuário acessa uma página web.
2. O Django renderiza o template HTML correspondente.
3. O `script.js` observa os formulários com `data-api-url`.
4. Quando existe `data-method`, o JavaScript faz `fetch()` para a rota REST correta.
5. A requisição entra em `config/urls.py` e segue para o `urls.py` do app.
6. A view valida permissão, autentica o usuário e prepara a resposta.
7. O serializer valida e converte os dados de entrada.
8. O model grava, atualiza ou consulta os dados no banco.
9. O banco retorna o resultado e a view responde em JSON ou redireciona para outra página.

No login, o Django cria a sessão e também grava o JWT em cookie. Assim, a interface web consegue usar as mesmas rotas REST sem exigir que o usuário envie o token manualmente a cada ação.

Resumo:

- Navegador: exibe a interface e dispara as ações.
- Templates: montam a página HTML.
- JavaScript: converte submits em chamadas REST.
- Views: coordenam a regra de negócio.
- Serializers: validam e formatam os dados.
- Models: representam as entidades.
- Banco de dados: persiste tudo o que o sistema gerencia.

## Estrutura do projeto

```text
config/       Configurações globais do Django e rotas principais
academia/     Usuários, autenticação, dashboards e permissões
planos/       Planos de assinatura
modalidades/  Modalidades, turmas, inscrições e frequências
treinos/      Treinos e sugestões
pagamentos/   Pagamentos dos alunos
```

## Requisitos

- Python 3.12 ou versão compatível.
- PostgreSQL instalado e rodando.
- Banco de dados criado.

## Configuração

### 1. Criar e ativar ambiente virtual

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto, no mesmo nível do `manage.py`.

Modelo:

```env
SECRET_KEY=coloque-sua-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=django.db.backends.postgresql
DB_NAME=erp_academia
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

### 4. Aplicar migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Criar superusuário

```bash
python manage.py createsuperuser
```

## Como executar

```bash
python manage.py runserver
```

Acesse:

- Sistema web: `http://127.0.0.1:8000/`
- Admin Django: `http://127.0.0.1:8000/admin/`
- Swagger: `http://127.0.0.1:8000/api/docs/`
- Schema OpenAPI: `http://127.0.0.1:8000/api/schema/`

## Autenticação JWT

Obter tokens:

```http
POST /api/auth/login/
```

Payload:

```json
{
  "email": "usuario@email.com",
  "password": "senha"
}
```

Atualizar access token:

```http
POST /api/auth/refresh/
```

Payload:

```json
{
  "refresh": "refresh_token"
}
```

Para rotas protegidas, envie:

```http
Authorization: Bearer <access_token>
```

## Rotas principais

As rotas abaixo existem na área web sob o prefixo `/api/academia/` e também como endpoints JSON quando marcadas como "Endpoints JSON".

### Sistema

- `/api/academia/` - login
- `/api/academia/dashboard/` - dashboard geral
- `/api/academia/dashboard/admin/` - dashboard do administrador
- `/api/academia/dashboard/funcionario/` - dashboard do funcionário
- `/api/academia/dashboard/aluno/` - dashboard do aluno
- `/api/academia/usuarios/` - listar usuários
- `/api/academia/usuarios/criar/` - criar usuário
- `/api/academia/usuarios/editar/<id>/` - editar usuário
- `/api/academia/usuarios/excluir/<id>/` - excluir usuário

Endpoints JSON:

- `/api/academia/alunos/`
- `/api/academia/funcionarios/`
- `/api/academia/administradores/`
- `/api/academia/usuarios/<id>/`

### Planos

- `/planos/` - listar planos
- `/planos/criar/` - criar plano
- `/planos/editar/<id_plano>/` - editar plano
- `/planos/excluir/<id_plano>/` - excluir plano
- `/planos/meu/` - visualizar plano do aluno

Endpoints JSON:

- `/api/planos/`
- `/api/planos/<id_plano>/`

### Modalidades

- `/modalidades/` - listar modalidades
- `/modalidades/turmas/lista/` - listar turmas
- `/modalidades/criar/` - criar modalidade
- `/modalidades/editar/<id>/` - editar modalidade
- `/modalidades/excluir/<id>/` - excluir modalidade
- `/modalidades/registrar/<id>/` - registrar aluno em modalidade
- `/modalidades/cancelar/<id>/` - cancelar registro em modalidade
- `/modalidades/frequencias/` - listar frequências
- `/modalidades/frequencias/criar/` - criar frequência

Endpoints JSON:

- `/api/modalidades/`
- `/api/modalidades/<id>/`
- `/api/modalidades/turmas/`
- `/api/modalidades/turmas/<turma_id>/inscricoes/`
- `/api/modalidades/turmas/inscricoes/<id>/`
- `/api/modalidades/inscricoes/`
- `/api/modalidades/inscricoes/<id>/cancelar/`
- `/api/modalidades/frequencias/<id>/`

### Treinos

- `/treinos/` - listar treinos
- `/treinos/criar/` - criar treino
- `/treinos/editar/<id_treino>/` - editar treino
- `/treinos/excluir/<id_treino>/` - excluir treino
- `/treinos/sugestoes/` - sugestão de treino por grupo muscular

Endpoints JSON:

- `/api/treinos/`
- `/api/treinos/<id_treino>/`
- `/api/treinos/sugestoes/?grupo=Peito`

### Pagamentos

- `/pagamentos/` - listar pagamentos
- `/pagamentos/criar/` - criar pagamento
- `/pagamentos/editar/<id>/` - editar pagamento
- `/pagamentos/excluir/<id>/` - excluir pagamento

Endpoints JSON:

- `/api/pagamentos/`
- `/api/pagamentos/<id>/`

## Observações de segurança

- Use `DEBUG=False` em produção.
- Configure `ALLOWED_HOSTS` com domínios reais.
- Não versione o arquivo `.env`.
- Troque credenciais expostas antes de publicar o projeto.
