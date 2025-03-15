# Estudo Flask - Backend Completo

Este repositório foi criado para estudo e prática do **Flask** e desenvolvimento de **APIs** do zero. O objetivo principal é aprofundar o conhecimento em **backend**, incluindo **autenticação JWT**, **integração com SQL** e boas práticas na organização de projetos.

---

## Início do Projeto
**Data de início:** 10 de março de 2025  

Este projeto acompanha a evolução no **Flask**, aplicando conceitos avançados de **arquitetura de APIs**, **segurança**, **persistência de dados** e **logs**.

---

## Tecnologias Utilizadas
- Python (Flask)  
- JSON para armazenamento temporário de dados  
- Organização modular (`models/`, `services/`, `data/`)  
- Logs detalhados (`DEBUG`, `INFO`, `ERROR`, `WARNING`)  
- Autenticação JWT  
- Banco de Dados SQL *(em desenvolvimento)*  

---

## Estrutura do Projeto
```
/estudo-flask
  ├─ data/            # Manipulação de arquivos JSON (dados temporários)
  ├─ db/              # Banco de dados SQLite (armazenamento persistente)
  ├─ logs/            # Armazena logs da aplicação
  ├─ models/          # Modelos de dados (Ex: Produto, Utilizador)
  ├─ services/        # Lógica de negócio (manipulação de dados)
  ├─ util/            # Ferramentas auxiliares (ex: autenticação, logs)
  ├─ venv/            # Ambiente virtual (dependências)
  ├─ app.py           # Ponto de entrada da aplicação Flask
  ├─ config.py        # Configurações globais do projeto
  ├─ database.py      # Conexão com banco de dados e ORM
  ├─ routes/          # Definição das rotas da API
  ├─ requirements.txt # Lista de dependências do projeto
  ├─ README.md        # Documentação do projeto
```

---

## Como Executar o Projeto

1. Clone o repositório:
   ```sh
   git clone https://github.com/teu-repo/flask-estudo.git
   ```

2. Acesse a pasta do projeto:
   ```sh
   cd flask-estudo
   ```

3. Crie e ative um ambiente virtual:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```

4. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

5. Execute a aplicação Flask:
   ```sh
   python app.py
   ```

A API estará disponível em **http://127.0.0.1:5000/**.

---

## Próximos Passos
- [x] Implementar autenticação com **JWT**  
- [ ] Integrar **SQLAlchemy** para persistência de dados  
- [ ] Criar testes automatizados  

---

## Licença
Este projeto é de estudo e não possui licença específica. Sinta-se livre para explorar e adaptar conforme necessário.

