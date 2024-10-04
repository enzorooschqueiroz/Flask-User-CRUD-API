# Flask User CRUD API

This is a basic project for a RESTful API built with Flask to manage users, focusing on learning Docker, unit tests, CI/CD, and deployment.

## Architecture

The application follows the CRUD (Create, Read, Update, Delete) structure to manage users. The API uses MongoDB via `mongoengine` as the database.

### Implemented Features

1. **GET /users** - Returns the list of all registered users.
2. **GET /user/<cpf>** - Returns the details of a specific user by CPF.
3. **POST /user** - Creates a new user with the provided information (CPF, email, first name, last name, and birth date). User creation validates the CPF using a verification algorithm.

### Implemented Validations

- **CPF**: The API validates the format and authenticity of the provided CPF.
  - The CPF must follow the format `xxx.xxx.xxx-xx`.
  - The verification follows the standard CPF check digits.
- **Email**: Required field.
- **First Name and Last Name**: Required fields.
- **Birth Date**: Required field.

### Example Usage

#### User Creation (POST)

```json
POST /user
{
  "cpf": "123.456.789-09",
  "email": "example@domain.com",
  "first_name": "FirstName",
  "last_name": "LastName",
  "birth_date": "1990-01-01"
}
```

#### Retrieve All Users (GET)

```
GET /users
```

#### Retrieve User by CPF (GET)

```
GET /user/123.456.789-09
```

### Delete User by CPF (DELETE)

```
DELETE /user/123.456.789-09
```

###  Update User by CPF (PUT)

```json
PUT /user/123.456.789-09
{
  "cpf": "123.456.789-09",
  "email": "updated@domain.com",
  "first_name": "UpdatedFirstName",
  "last_name": "UpdatedLastName",
  "birth_date": "1990-01-01"
}
```
---

## Data Models

The API uses MongoDB to persist user data, and the data model is defined using `mongoengine`.

### User Model (UserModel)

Below are the fields for the `UserModel`, representing a user in the application:

- **cpf**: `StringField` (Required, Unique) — User's CPF, must be unique and valid.
- **email**: `EmailField` (Required) — User's email address.
- **first_name**: `StringField` (Required, Max: 50 characters) — User's first name.
- **last_name**: `StringField` (Required, Max: 50 characters) — User's last name.
- **birth_date**: `DateTimeField` (Required) — User's birth date.

---

Example of a user JSON object:

```json
{
  "cpf": "123.456.789-09",
  "email": "example@domain.com",
  "first_name": "FirstName",
  "last_name": "LastName",
  "birth_date": "1990-01-01T00:00:00"
}
```

---

## Unit Tests

The project includes unit tests to verify the API's behavior and ensure that all CRUD operations work correctly. The tests are implemented using `pytest`.

### Test Configuration

The tests use a test client provided by Flask, allowing routes to be tested without running the actual server.

#### Fixtures

- **client**: Creates a test client with the application's configuration.
- **valid_user**: Provides a dictionary of valid user data for user creation tests.
- **invalid_user**: Provides a dictionary of invalid user data to test error scenarios.

### Implemented Tests

1. **Test Retrieve All Users** (`test_get_users`)
   - **Method**: `GET /users`
   - **Verifies**: The response returns status 200 (OK).

2. **Test User Creation** (`test_post_user`)
   - **Method**: `POST /user`
   - **Verifies**:
     - A valid user is successfully created (status 200).
     - The creation of an invalid user returns status 400 and an error message.

3. **Test Retrieve User by CPF** (`test_get_user`)
   - **Method**: `GET /user/<cpf>`
   - **Verifies**:
     - A valid user is returned with correct information.
     - An attempt to retrieve an invalid user returns status 404 and the message "User not found."

### How to Run the Tests

1. **Install the dependencies**:
   - Ensure that all project dependencies, including `pytest`, are installed.

2. **Run the tests**:
   - To run the tests, execute the following command in the terminal:
     ```bash
     pytest
     ```

---

## Docker and Docker Compose

This project is containerized using Docker, and the environment is configured using `docker-compose` to facilitate development and deployment.

- **MongoDB Service**:
  - Uses the `mongo:5.0.8` image.
  - Defines environment variables for MongoDB username and password.
  - Automatically restarts if the service fails.
  
- **API Service**:
  - Builds the Flask API using the `Dockerfile`.
  - Maps container port `5000` to host port `5000`.
  - Defines environment variables to connect to MongoDB.
  - Depends on the MongoDB service, ensuring that the database is started before the API.
  - Mounts the `./application` directory as a volume in the container so that local code changes reflect inside the container.

### How to Run the Application with Docker

1. **Build the Image and Start the Containers**:
   - In the root directory of the project, run the following command to build the image and run the containers:
     ```bash
     docker-compose up --build
     ```

2. **Access the Application**:
   - The API will be available at `http://localhost:5000`.

3. **Stop the Containers**:
   - To stop and remove the containers, run:
     ```bash
     docker-compose down
     ```

---

## CI/CD with GitHub Actions

This project uses GitHub Actions to automate the process of testing and deploying the application whenever there is a push to the `main` branch.

### Workflow File

The workflow file `test.yml` defines two main jobs: `test` and `deploy`.

### Explanation of the Jobs

- **Test Job (`test`)**:
  - This job runs whenever a push is made to the `main` branch.
  - Uses Python 3.9 to run unit tests.
  - After installing dependencies via `pip`, the `make test` command is executed to run the unit tests.

- **Deploy Job (`deploy`)**:
  - The deploy is only executed if the tests pass (`needs: test`).
  - Uses Node.js version 16 to set up the environment.
  - Installs project dependencies with `yarn`.
  - Installs the Railway CLI for deployment.
  - Deploys the application to the `Railway` service using the command `railway up`, with the token and database URL passed as environment variables via `secrets`.

### How to Configure CI/CD

1. **Create Secrets in GitHub**:
   - To configure automatic deployment in GitHub, you need to add the `RAILWAY_TOKEN` and `DATABASE_URL` secrets to the repository:
     - In the GitHub repository, go to *Settings* > *Secrets* > *Actions* and add the secrets.

2. **Manual Execution**:
   - Besides automatic deployment on pushes to the `main` branch, you can also manually start the workflow via the GitHub Actions interface by clicking "Run workflow" under *Actions*.

3. **Automatic Deployment**:
   - Whenever you push to the `main` branch, the tests will automatically run, and if they pass, the deployment will be performed on Railway.
