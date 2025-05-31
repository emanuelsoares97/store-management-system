# Planeamento de Endpoints para Swagger / OpenAPI

Este documento lista, em formato Markdown, quais endpoints devem estar obrigatoriamente documentados (e implementados no estilo Namespace/Resource) **antes** do frontend ser desenvolvido, e quais rotas podem ficar para uma iteração posterior.

---

## 🚀 Endpoints Obrigatórios (MVP)

Estes são os endpoints mínimos que o frontend vai consumir diretamente para o fluxo principal de autenticação, cadastro de cliente, listagem de produto e criação/listagem de vendas. Eles devem aparecer no Swagger/OpenAPI e estar funcionando antes de avançar com o frontend.

### 1. Autenticação

- **POST `/auth/login`**  
  - Descrição: Gera o token JWT (ou outro esquema de token) para o usuário fazer login.  
  - Payload (exemplo):
    ```json
    {
      "email": "usuario@exemplo.com",
      "password": "senha123"
    }
    ```
  - Response (exemplo):
    ```json
    {
      "access_token": "<jwt_token>",
      "refresh_token": "<refresh_token_opcional>"
    }
    ```

- **(Opcional / se usar Refresh Tokens) POST `/auth/refresh`**  
  - Descrição: Recebe um _refresh_token_ e retorna um novo _access_token_.  
  - Payload (exemplo):
    ```json
    {
      "refresh_token": "<refresh_token>"
    }
    ```
  - Response (exemplo):
    ```json
    {
      "access_token": "<novo_jwt_token>"
    }
    ```

> **Por que documentar primeiro?**  
> - Sem o endpoint de login, o frontend não consegue obter credenciais para chamar nenhuma rota protegida.  
> - Se vocês planejam usar _refresh tokens_, é recomendável incluir esse endpoint desde o início.

---

### 2. Customer (Cliente)

- **POST `/customer/new`**  
  - Descrição: Cria um novo cliente.  
  - Proteção:  
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin", "gerente")
    ```
  - Payload (exemplo):
    ```json
    {
      "name": "João Silva",
      "email": "joao.silva@exemplo.com",
      "phone": "+351912345678"
    }
    ```
  - Response (201 Created):
    ```json
    {
      "id": 42,
      "name": "João Silva",
      "email": "joao.silva@exemplo.com",
      "phone": "+351912345678",
      "active": true
    }
    ```

- **GET `/customer/actives`**  
  - Descrição: Retorna lista de clientes ativos.  
  - Proteção:
    ```python
    @AuthService.token_required
    ```
  - Response (200 OK):
    ```json
    [
      {
        "id": 42,
        "name": "João Silva",
        "email": "joao.silva@exemplo.com",
        "phone": "+351912345678",
        "active": true
      },
      {
        "id": 43,
        "name": "Maria Santos",
        "email": "maria.santos@exemplo.com",
        "phone": "+351987654321",
        "active": true
      }
    ]
    ```

> **Por que documentar?**  
> - O frontend precisa obter o dropdown ou lista de clientes para criar uma venda.  
> - O cadastro de cliente via interface também depende deste endpoint.

---

### 3. Product (Produto)

- **GET `/product/actives`**  
  - Descrição: Retorna lista de produtos ativos (e já disponíveis para venda).  
  - Proteção:
    ```python
    @AuthService.token_required
    ```
  - Response (200 OK):
    ```json
    [
      {
        "id": 100,
        "name": "Teclado Mecânico",
        "price": 79.90,
        "stock": 15,
        "active": true
      },
      {
        "id": 101,
        "name": "Rato Wireless",
        "price": 29.50,
        "stock": 30,
        "active": true
      }
      // ...
    ]
    ```

- **(Opcional / se necessário) GET `/product/<int:product_id>`**  
  - Descrição: Retorna detalhes de um produto específico (ex.: preço, stock, descrição).  
  - Proteção:
    ```python
    @AuthService.token_required
    ```
  - Path parameter:
    - `product_id`: ID do produto a ser consultado.  
  - Response (200 OK):
    ```json
    {
      "id": 100,
      "name": "Teclado Mecânico",
      "description": "Teclado mecânico retroiluminado, switches azuis.",
      "price": 79.90,
      "stock": 15,
      "active": true,
      "category_id": 5
    }
    ```

> **Por que documentar `/product/actives` primeiro?**  
> - O frontend precisa dos produtos disponíveis para preencher o carrinho/itens de venda.  
> - Caso o MVP não exija detalhes individuais, basta atender apenas esta rota.

---

### 4. Sale (Venda)

- **POST `/sale/new`**  
  - Descrição: Registra uma nova venda, associando-a a um cliente e a um ou mais itens de produto.  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin", "gerente")
    ```
  - Payload (exemplo):
    ```json
    {
      "customer_id": 42,
      "items": [
        { "product_id": 100, "quantity": 2 },
        { "product_id": 101, "quantity": 1 }
      ],
      "total": 189.30,
      "payment_method": "cartão"
    }
    ```
  - Response (201 Created):
    ```json
    {
      "sale_id": 2025,
      "customer_id": 42,
      "items": [
        { "product_id": 100, "quantity": 2, "unit_price": 79.90 },
        { "product_id": 101, "quantity": 1, "unit_price": 29.50 }
      ],
      "total": 189.30,
      "payment_method": "cartão",
      "date": "2025-05-31T14:23:00Z"
    }
    ```

- **GET `/sale/all`**  
  - Descrição: Retorna lista de todas as vendas (para relatórios ou histórico).  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin", "gerente")
    ```
  - Response (200 OK):
    ```json
    [
      {
        "sale_id": 2024,
        "customer_id": 40,
        "total": 59.90,
        "payment_method": "dinheiro",
        "date": "2025-05-30T11:05:00Z"
      },
      {
        "sale_id": 2025,
        "customer_id": 42,
        "total": 189.30,
        "payment_method": "cartão",
        "date": "2025-05-31T14:23:00Z"
      }
      // ...
    ]
    ```

> **Por que documentar?**  
> - O frontend de vendas precisa chamar `/sale/new` para finalizar a compra.  
> - Se houver um painel administrativo com histórico de vendas, ele consome `/sale/all`.

---

## 🕒 Endpoints para Deixar “Para Depois”

Estes endpoints continuam existentes (ou podem ser mantidos em Blueprints puros), mas **não precisam** estar documentados no Swagger antes de entregar o MVP do frontend. A migração para Namespaces/Resources e a inclusão na documentação podem acontecer na próxima fase.

### 1. Customer (Cliente) – Rotas Adicionais

- **GET `/customer/all`**  
  - Descrição: Lista todos os clientes (incluindo inativos).  
  - Apenas se for necessário no futuro, para funções de “admin” ver histórico completo.

- **PUT `/customer/<int:customer_id>/update`**  
  - Descrição: Atualiza dados de um cliente existente.  
  - Proteção:  
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin", "gerente")
    ```

- **PATCH `/customer/<int:customer_id>/deactivate`**  
  - Descrição: Desativa (remove logicamente) um cliente.  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin")
    ```

- **PATCH `/customer/<int:customer_id>/reactivate`**  
  - Descrição: Reativa um cliente desativado.  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin")
    ```

---

### 2. Product (Produto) – Rotas de CRUD Completo

- **POST `/product/new`**  
  - Descrição: Cria um novo produto.  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin", "gerente")
    ```

- **PUT `/product/<int:product_id>/update`**  
  - Descrição: Atualiza dados de um produto existente.  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin", "gerente")
    ```

- **PATCH `/product/<int:product_id>/deactivate`**  
  - Descrição: Marca um produto como inativo.  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin")
    ```

- **PATCH `/product/<int:product_id>/reactivate`**  
  - Descrição: Reativa um produto inativo.  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin")
    ```

- **DELETE `/product/<int:product_id>/delete`**  
  - Descrição: Remove um produto permanentemente (se for o caso).  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin")
    ```

---

### 3. Category (Categoria)

- **GET `/category/actives`**  
  - Descrição: Lista categorias ativas (caso o frontend precise filtrar).  
  - Proteção:
    ```python
    @AuthService.token_required
    ```

- **GET `/category/all`**  
  - Descrição: Lista todas as categorias, incluindo inativas.  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin")
    ```

- **POST `/category/new`**  
  - Descrição: Cria uma nova categoria.  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin", "gerente")
    ```

- **PUT `/category/<int:category_id>/update`**  
  - Descrição: Atualiza dados de categoria existente.  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin", "gerente")
    ```

- **PATCH `/category/<int:category_id>/deactivate`**  
  - Descrição: Desativa uma categoria.  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin")
    ```

- **PATCH `/category/<int:category_id>/reactivate`**  
  - Descrição: Reativa uma categoria.  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin")
    ```

---

### 4. User (Usuário)

> **Observação:** Neste momento, apenas o **admin** pode criar novos usuários diretamente pelo backend. Se não houver a necessidade de um painel de administração via frontend para usuários, estas rotas podem ficar documentadas apenas posteriormente (ou até mesmo serem omitidas se não forem usadas externamente).

- **POST `/user/new`**  
  - Descrição: Cria um novo usuário (por exemplo, para equipe interna/admin).  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin")
    ```

- **GET `/user/actives`**  
  - Descrição: Lista usuários ativos (funcionários, admins, gerentes).  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin", "gerente")
    ```

- **GET `/user/all`**  
  - Descrição: Lista todos os usuários (incluindo inativos).  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin")
    ```

- **PUT `/user/<int:user_id>/update`**  
  - Descrição: Atualiza dados de um usuário.  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin", "gerente")
    ```

- **PATCH `/user/<int:user_id>/desactivate`**  
  - Descrição: Desativa um usuário (remover acesso logado).  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin")
    ```

- **PATCH `/user/<int:user_id>/reactivate`**  
  - Descrição: Reativa um usuário desativado.  
  - Proteção:
    ```python
    @AuthService.token_required
    @AuthService.role_required("admin")
    ```

---

## 🎯 Resumo das Prioridades

1. **MVP (Frontend precisa obrigatoriamente)**  
   - Autenticação:  
     - `POST /auth/login`  
     - (Opcional) `POST /auth/refresh`  
   - Customer:  
     - `POST /customer/new`  
     - `GET /customer/actives`  
   - Product:  
     - `GET /product/actives`  
   - Sale:  
     - `POST /sale/new`  
     - `GET /sale/all`

2. **Para Documentar / Refatorar Depois (opcional no MVP)**  
   - Customer (rotas de CRUD completo: `/customer/all`, `PUT /customer/<id>`, `PATCH /customer/<id>/deactivate|reactivate`)  
   - Product (CRUD completo: `/product/new`, `PUT /product/<id>`, `PATCH /product/<id>/deactivate|reactivate`, `DELETE /product/<id>/delete`)  
   - Category (CRUD completo e listagens)  
   - User (criação/listagem/edição/desativação/reactivação apenas para admin)

---

## 📌 Dicas para o Repositório

- Crie um arquivo `SWAGGER_PRIORIDADES.md` (ou `README_SWAGGER.md`) na raiz ou na pasta `docs/` do seu backend.  
- Cole este conteúdo em Markdown para referência futura.  
- Quando for expandir a documentação, adicione uma nova seção “**Fase 2**” e marque quais endpoints intermediários já foram migrados.  
- Atualize as anotações de rota (ex.: `@ns.doc(...)` ou `@ns.expect(...)`) conforme for refinando os modelos de dados.  

Dessa forma, você terá sempre documentado, no repositório, **o que é essencial para entregar o MVP** ao frontend e **o que pode ficar para uma fase posterior**. Boa sorte nos últimos ajustes, e sucesso nos estudos de Django!
