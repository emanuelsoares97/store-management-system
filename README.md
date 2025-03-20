# Store Management System

Este repositório foi criado para estudar e aprofundar conhecimentos no desenvolvimento de **APIs REST** utilizando o **Flask**. O objetivo é aplicar boas práticas no backend, incluindo organização modular, autenticação **JWT**, integração com **SQL** e manipulação de logs. Serão implementadas funcionalidades essenciais para uma API profissional.

---

## Tecnologias Utilizadas

- **Python (Flask)** – Framework web para construção da API
- **SQLAlchemy** – ORM para gerenciamento de banco de dados
- **JWT (JSON Web Token)** – Autenticação segura para utilizadores
- **SQLite** – Banco de dados relacional para armazenamento dos dados
- **Werkzeug Security** – Hash de senhas para segurança
- **Logging** – Registro de eventos da aplicação

---

## Estrutura do Projeto

```
/store-management-system
  ├─ .vscode/          # Configurações do Visual Studio Code
  ├─ __pycache__/      # Arquivos de cache do Python
  ├─ data/             # Dados utilizados pela aplicação
  ├─ db/               # Banco de dados SQLite (armazenamento persistente)
  ├─ logs/             # Armazena logs da aplicação
  ├─ models/           # Modelos de dados (Produto, Utilizador, Venda)
  ├─ routes/           # Definição das rotas da API
  ├─ services/         # Lógica de negócio (CRUD e validações)
  ├─ templates/        # Templates HTML para renderização
  ├─ tests/            # Testes automatizados
  ├─ util/             # Ferramentas auxiliares (ex: autenticação, logs)
  ├─ .gitattributes    # Atributos do Git
  ├─ .gitignore        # Arquivos e pastas ignorados pelo Git
  ├─ LICENSE           # Licença MIT do projeto
  ├─ README.md         # Documentação do projeto
  ├─ app.py            # Ponto de entrada da aplicação Flask
  ├─ base.py           # Configurações base da aplicação
  ├─ config.py         # Configurações globais do projeto
  ├─ database.py       # Conexão com banco de dados e ORM
  ├─ reiniciar_db.py   # Script para reiniciar o banco de dados
  └─ requirements.txt  # Lista de dependências do projeto
```

---

## Como Executar o Projeto

1. **Clone o repositório**

   ```sh
   git clone https://github.com/emanuelsoares97/store-management-system.git
   ```

2. **Acesse a pasta do projeto**

   ```sh
   cd store-management-system
   ```

3. **Crie e ative um ambiente virtual**

   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

4. **Instale as dependências**

   ```sh
   pip install -r requirements.txt
   ```

5. **Execute a aplicação Flask**

   ```sh
   python app.py
   ```

A API estará disponível em **http://127.0.0.1:5000/**.

---

## Principais Funcionalidades

- **CRUD de Produtos** – Criar, listar, atualizar e remover produtos
- **CRUD de Utilizadores** – Gerenciar utilizadores e permissões (Admin, Gerente, Estoquista, Cliente)
- **Autenticação JWT** – Geração e validação de tokens
- **Sistema de Permissões** – Controle de acesso baseado em funções (RBAC)
- **Banco de Dados SQLAlchemy** – Persistência de dados com ORM
- **Registro de Logs** – Monitoramento e depuração da aplicação
- **Rotas Protegidas** – Apenas utilizadores autenticados podem acessar certos endpoints

---

## Próximos Passos

- [x] Implementar autenticação com **JWT**
- [x] Criar **CRUD de utilizadores** com permissões
- [x] Criar **CRUD de produtos**
- [ ] Criar **CRUD de vendas** (com relacionamento entre produto e utilizador)
- [x] Melhorar sistema de **logs e tratamento de erros**
- [ ] Criar **testes automatizados**

---

## Licença

Este projeto está licenciado sob a **MIT License**. Consulte o arquivo `LICENSE` para mais detalhes.

