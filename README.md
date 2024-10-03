# Flask User CRUD API

Este é um projeto básico de uma API RESTful construída com Flask para gerenciar usuários, focada em aprendizagem de Docker, testes unitários, CI/CD, e deploy.

## Arquitetura

A aplicação segue a estrutura de CRUD (Create, Read, Update, Delete) para gerenciar usuários. A API utiliza MongoDB via `mongoengine` como banco de dados.

### Funcionalidades Implementadas

1. **GET /users** - Retorna a lista de todos os usuários cadastrados.
2. **GET /user/<cpf>** - Retorna os detalhes de um usuário específico pelo CPF.
3. **POST /user** - Cria um novo usuário com as informações fornecidas (CPF, email, nome, sobrenome e data de nascimento). A criação do usuário valida o CPF utilizando um algoritmo de verificação.

### Validações Implementadas

- **CPF**: A API valida a formatação e a autenticidade do CPF fornecido.
  - O CPF deve seguir o formato `xxx.xxx.xxx-xx`.
  - A verificação segue os dígitos verificadores padrão do CPF.
- **Email**: Campo obrigatório.
- **Nome e Sobrenome**: Campos obrigatórios.
- **Data de Nascimento**: Campo obrigatório.

### Exemplo de Uso

#### Criação de Usuário (POST)

```json
POST /user
{
  "cpf": "123.456.789-09",
  "email": "exemplo@dominio.com",
  "first_name": "Nome",
  "last_name": "Sobrenome",
  "birth_date": "1990-01-01"
}
```

#### Consulta de Todos os Usuários (GET)

```
GET /users
```

#### Consulta de Usuário por CPF (GET)

```
GET /user/123.456.789-09
```

---

## Modelos de Dados

A API utiliza o MongoDB para persistir os dados dos usuários, e o modelo de dados é definido utilizando `mongoengine`.

### Modelo de Usuário (UserModel)

Abaixo estão os campos do modelo `UserModel`, que representa um usuário na aplicação:

- **cpf**: `StringField` (Obrigatório, Único) — CPF do usuário, deve ser único e válido.
- **email**: `EmailField` (Obrigatório) — Endereço de email do usuário.
- **first_name**: `StringField` (Obrigatório, Máximo: 50 caracteres) — Primeiro nome do usuário.
- **last_name**: `StringField` (Obrigatório, Máximo: 50 caracteres) — Sobrenome do usuário.
- **birth_date**: `DateTimeField` (Obrigatório) — Data de nascimento do usuário.

---

Exemplo de um objeto JSON de usuário:

```json
{
  "cpf": "123.456.789-09",
  "email": "exemplo@dominio.com",
  "first_name": "Nome",
  "last_name": "Sobrenome",
  "birth_date": "1990-01-01T00:00:00"
}
```

---

## Testes Unitários

O projeto inclui testes unitários para verificar o comportamento da API e garantir que todas as operações do CRUD funcionem corretamente. Os testes são implementados utilizando `pytest`.

### Configuração dos Testes

Os testes utilizam um cliente de teste fornecido pelo Flask, permitindo que as rotas sejam testadas sem a necessidade de rodar o servidor real.

#### Fixtures

- **client**: Cria um cliente de teste com a configuração da aplicação.
- **valid_user**: Fornece um dicionário de dados de um usuário válido para os testes de criação de usuários.
- **invalid_user**: Fornece um dicionário de dados de um usuário inválido para testar os cenários de erro.

### Testes Implementados

1. **Teste de Busca de Todos os Usuários** (`test_get_users`)
   - **Método**: `GET /users`
   - **Verifica**: Se a resposta retorna status 200 (OK).

2. **Teste de Criação de Usuário** (`test_post_user`)
   - **Método**: `POST /user`
   - **Verifica**:
     - Se um usuário válido é criado com sucesso (status 200).
     - Se a criação de um usuário inválido retorna status 400 e uma mensagem de erro.

3. **Teste de Busca de Usuário por CPF** (`test_get_user`)
   - **Método**: `GET /user/<cpf>`
   - **Verifica**:
     - Se um usuário válido é retornado com as informações corretas.
     - Se a tentativa de buscar um usuário inválido retorna status 404 e uma mensagem "User not found".

### Como Rodar os Testes

1. **Instale as dependências**:
   - Certifique-se de que todas as dependências do projeto estão instaladas, incluindo `pytest`.

2. **Execute os testes**:
   - Para rodar os testes, execute o seguinte comando no terminal:
     ```bash
     pytest
     ```

---

## Docker e Docker Compose

Este projeto é containerizado usando Docker, e o ambiente é configurado utilizando `docker-compose` para facilitar o desenvolvimento e deploy da aplicação. 

- **MongoDB Service**:
  - Utiliza a imagem `mongo:5.0.8`.
  - Define as variáveis de ambiente para o nome de usuário e senha do MongoDB.
  - Reinicia automaticamente caso o serviço falhe.
  
- **API Service**:
  - Faz o build da API Flask utilizando o `Dockerfile`.
  - Mapeia a porta `5000` do container para a porta `5000` no host.
  - Define as variáveis de ambiente para conectar ao MongoDB.
  - Depende do serviço de MongoDB, garantindo que o banco de dados seja iniciado antes da API.
  - Monta o diretório `./application` como volume no container para que as mudanças no código local reflitam dentro do container.

### Como Rodar a Aplicação com Docker

1. **Construa a Imagem e Inicie os Containers**:
   - No diretório raiz do projeto, execute o seguinte comando para construir a imagem e rodar os containers:
     ```bash
     docker-compose up --build
     ```

2. **Acessar a Aplicação**:
   - A API estará disponível em `http://localhost:5000`.

3. **Parar os Containers**:
   - Para parar e remover os containers, execute:
     ```bash
     docker-compose down
     ```

---

## CI/CD com GitHub Actions

Este projeto utiliza GitHub Actions para automatizar o processo de teste e deploy da aplicação sempre que há um push para a branch `main`.

### Arquivo de Workflow

O arquivo de workflow `test.yml` define dois jobs principais: `test` e `deploy`.

### Explicação dos Jobs

- **Job de Testes (`test`)**:
  - Este job é executado sempre que um push é feito na branch `main`.
  - Utiliza o Python 3.9 para rodar os testes unitários.
  - Após a instalação das dependências via `pip`, o comando `make test` é executado para rodar os testes unitários.

- **Job de Deploy (`deploy`)**:
  - O deploy só será executado se os testes passarem (`needs: test`).
  - Usa Node.js versão 16 para configurar o ambiente.
  - Instala as dependências do projeto com `yarn`.
  - Instala a CLI do Railway para o deploy.
  - Realiza o deploy da aplicação para o serviço `Railway` usando o comando `railway up`, com o token e a URL do banco de dados passados como variáveis de ambiente via `secrets`.

### Como Configurar o CI/CD

1. **Criar Secrets no GitHub**:
   - Para configurar o deploy automático no GitHub, você precisa adicionar os secrets `RAILWAY_TOKEN` e `DATABASE_URL` no repositório:
     - No repositório GitHub, vá até *Settings* > *Secrets* > *Actions* e adicione os secrets.

2. **Executar Manualmente**:
   - Além do deploy automático em pushes para a branch `main`, você também pode iniciar o workflow manualmente via a interface do GitHub Actions clicando em "Run workflow" em *Actions*.

3. **Deploy Automático**:
   - Sempre que você fizer um push para a branch `main`, os testes serão executados automaticamente e, caso passem, o deploy será realizado no Railway.
