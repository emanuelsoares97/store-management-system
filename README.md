# Flask Store Backend

Este repositório foi criado para estudo e prática do **Flask** e desenvolvimento de **APIs REST**. O objetivo é construir uma API segura e eficiente para gerenciar **produtos, utilizadores, vendas e permissões de acesso** utilizando **JWT, SQLAlchemy** e boas práticas de organização de código.

---

## Início do Projeto
**Data de início:** 10 de março de 2025  

Este projeto acompanha a evolução no **Flask**, aplicando conceitos avançados de **arquitetura de APIs**, **segurança**, **persistência de dados** e **logs**.

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
/flask-store-backend
  ├─ db/              # Banco de dados SQLite (armazenamento persistente)
  ├─ logs/            # Armazena logs da aplicação
  ├─ models/          # Modelos de dados (Produto, Utilizador, Venda)
  ├─ services/        # Lógica de negócio (CRUD e validações)
  ├─ util/            # Ferramentas auxiliares (ex: autenticação, logs)
  ├─ routes/          # Definição das rotas da API
  ├─ venv/            # Ambiente virtual (dependências)
  ├─ app.py           # Ponto de entrada da aplicação Flask
  ├─ config.py        # Configurações globais do projeto
  ├─ database.py      # Conexão com banco de dados e ORM
  ├─ requirements.txt # Lista de dependências do projeto
  ├─ LICENSE          # Licença MIT do projeto
  └─ README.md        # Documentação do projeto
```

---

## Como Executar o Projeto

1⃣ **Clone o repositório**  
```sh
git clone https://github.com/teu-usuario/flask-store-backend.git
```

2⃣ **Acesse a pasta do projeto**  
```sh
cd flask-store-backend
```

3⃣ **Crie e ative um ambiente virtual**  
```sh
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

4⃣ **Instale as dependências**  
```sh
pip install -r requirements.txt
```

5⃣ **Execute a aplicação Flask**  
```sh
python app.py
```

A API estará disponível em **http://127.0.0.1:5000/**.

---

## Principais Funcionalidades  

✅ CRUD de **Produtos** – Criar, listar, atualizar e remover produtos  
✅ CRUD de **Utilizadores** – Gerenciar utilizadores e permissões (Admin, Gerente, Estoquista, Cliente)  
✅ **Autenticação JWT** – Geração e validação de tokens  
✅ **Sistema de Permissões** – Controle de acesso baseado em funções (RBAC)  
✅ **Banco de Dados SQLAlchemy** – Persistência de dados com ORM  
✅ **Registro de Logs** – Monitoramento e depuração da aplicação  
✅ **Rotas Protegidas** – Apenas utilizadores autenticados podem acessar certos endpoints  

---

##  Próximos Passos  
- [x] Implementar autenticação com **JWT**  
- [x] Criar **CRUD de utilizadores** com permissões  
- [x] Criar **CRUD de produtos**  
- [ ] Criar **CRUD de vendas** (com relacionamento entre produto e utilizador)  
- [ ] Melhorar sistema de **logs e tratamento de erros**  
- [ ] Criar **testes automatizados** 🧪  

---

## Licença  
Este projeto está licenciado sob a **MIT License**. Consulte o arquivo `LICENSE` para mais detalhes.

