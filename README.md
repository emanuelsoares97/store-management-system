# Store Management System

Este repositório foi criado para estudar e aprofundar conhecimentos no desenvolvimento de APIs REST utilizando o Flask. O objetivo é aplicar boas práticas no backend, incluindo organização modular, autenticação JWT, integração com SQL, logging e testes automatizados. As funcionalidades implementadas são pensadas para simular um sistema real de gestão de loja.

---

## Tecnologias Utilizadas

- Python (Flask) – Framework web para construção da API
- SQLAlchemy – ORM para gerenciamento de banco de dados
- JWT (JSON Web Token) – Autenticação segura para utilizadores
- SQLite – Banco de dados relacional para armazenamento dos dados
- Pytest – Testes automatizados
- Werkzeug Security – Hash de senhas para segurança
- Logging – Registro de eventos da aplicação
- Python-Dotenv – Gerenciamento de variáveis de ambiente com arquivos `.env`

---

## Estrutura do Projeto

```
/store-management-system
├─ app/                         # Código principal da aplicação
│  ├─ models/                   # Modelos do SQLAlchemy
│  ├─ routes/                   # Rotas da API (modularizadas por recurso)
│  │  └─ api/                   # Subpastas com rotas protegidas
│  ├─ services/                 # Camada de lógica de negócio
│  ├─ util/                     # Funções utilitárias (logger, validações, etc.)
│  ├─ templates/                # Templates HTML (caso necessário)
│  ├─ __init__.py               # Inicializa e configura a app Flask
│  └─ database.py               # Classe para lidar com a conexão ao banco
├─ tests/                       # Testes automatizados com Pytest
├─ db/                          # Banco de dados SQLite (persistência)
├─ logs/                        # Logs da aplicação
├─ .env.example                 # Exemplo de variáveis de ambiente
├─ .gitignore                   # Arquivos e pastas ignorados pelo Git
├─ config.py                    # Configurações globais da aplicação via variáveis de ambiente
├─ requirements.txt             # Dependências do projeto
├─ run.py                       # Arquivo para executar a aplicação
├─ README.md                    # Documentação do projeto
└─ LICENSE                      # Licença MIT
```

---

## Como Executar o Projeto

1. Clone o repositório

```bash
git clone https://github.com/emanuelsoares97/store-management-system.git
```

2. Acesse a pasta do projeto

```bash
cd store-management-system
```

3. Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

4. Copie o arquivo `.env.example` para `.env` e defina os valores:

```bash
cp .env.example .env  # ou crie manualmente
```

Exemplo de `.env`:
```
SECRET_KEY=supersecreta123
DATABASE_URL=sqlite:///db/database.db
DEBUG=True
```

5. Instale as dependências

```bash
pip install -r requirements.txt
```

6. Execute a aplicação Flask

```bash
python run.py
```

A API estará disponível em http://127.0.0.1:5000/

---

## Principais Funcionalidades

- CRUD de Produtos
- CRUD de Utilizadores com níveis de permissão (Admin, Gerente, Estoquista, Cliente)
- CRUD de Categorias e Vendas
- Autenticação e Autorização com JWT
- Sistema de permissões (RBAC)
- Registro de logs
- Testes automatizados com Pytest
- Retorno de erros padronizado

---

## Testes Automatizados

Para executar os testes e ver a cobertura de código:

```bash
pytest --cov=app tests/
```

Os testes estão organizados por rota/recurso e simulam interações com a API, garantindo a estabilidade e confiabilidade do sistema.

---

## Próximos Passos

- [x] Implementar autenticação com JWT
- [x] Criar CRUD de utilizadores com permissões
- [x] Criar CRUD de produtos
- [x] Criar testes automatizados
- [x] Melhorar sistema de logs e tratamento de erros
- [x] Criar CRUD de vendas com relacionamento entre produto e utilizador
- [ ] Implementar documentação com Swagger

---

## Licença

Este projeto está licenciado sob a MIT License. Consulte o arquivo `LICENSE` para mais detalhes.

