# Library Management System

A simple Library Management System built with Flask and SQLAlchemy.

## Features
- User registration and login (with JWT authentication)
- Add and view books
- Pagination support for listing books

## Technologies Used
- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- SQLite 

## Prerequisites

The application requires a pre-existing installation of Python 3.x

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/library-management.git
cd library-management
```

### 2. Create a virtual environment and activate it:

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000/`.

## Database Assumptions
This project uses **SQLite** as the database. SQLite is used here primarily for simplicity and ease of setup, especially for local development and testing purposes. The SQLite database is in-memory during testing and will not persist once the application is stopped. 

**Assumption:**
- The database will be initialized automatically when the app starts. There is no need for manual database setup. 
- This application is designed to run with SQLite for local development and small-scale testing. For production, you can easily switch to another relational database system by modifying the SQLAlchemy URI configuration.

## Design Choices

- **Flask**: A simple and flexible web micro-framework. required for use in the project constraints.

- **SQLAlchemy ORM**: Used to abstract SQL queries and manage database interactions via Python classes. This follows the **Active Record** pattern where each model corresponds to a database record.

- **JWT Authentication**: Implements **Token-based Authentication** for stateless, secure user sessions. The app uses **Flask-JWT-Extended** to generate and verify JWT tokens.

- **Factory Pattern**: Used in Flask to configure and initialize the app with different settings, ensuring flexibility for various environments.

- **Singleton Pattern**: Applied to the database connection to ensure only one instance of the database session is used throughout the app.

- **Flask Blueprints**: Blueprints are used to organize the app into smaller components like authentication and book management, which can be easily extended in the future.

- **Pagination**: Implemented to limit the number of books displayed on a single page, improving performance and user experience.
## API Endpoints

### 1. Healthcheck
- **GET** `/healthcheck`
- **Response:**
  ```json
  {
    "message": "Server is running"
  }
  ```

### 2. Register User
- **POST** `/register`
- **Request Body:**
  ```json
  {
    "username": "newuser",
    "password": "password123"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Member registered successfully"
  }
  ```

### 3. Login
- **POST** `/login`
- **Request Body:**
  ```json
  {
    "username": "newuser",
    "password": "password123"
  }
  ```
- **Response:**
  ```json
  {
    "access_token": "your_access_token_here"
  }
  ```

### 4. Add Book
- **POST** `/books`
- **Request Body:**
  ```json
  {
    "title": "Book Title",
    "author": "Book Author"
  }
  ```
- **Headers:**
  - `Authorization: Bearer your_access_token_here`
- **Response:**
  ```json
  {
    "message": "Book added successfully"
  }
  ```

### 5. Get Books
- **GET** `/books`
- **Query Parameters:**
  - `page`: Page number
  - `per_page`: Number of books per page
- **Headers:**
  - `Authorization: Bearer your_access_token_here`
- **Response:**
  ```json
  {
    "books": [
      {
        "id": 1,
        "title": "Book Title",
        "author": "Book Author"
      }
    ]
  }
  ```

## Running Tests

To run tests for this application, use the following command:

```bash
python -m unittest discover tests
```

This will run all the test cases in the `tests` folder.

## Assumptions & Limitations
- **Assumption**: This application uses SQLite for the development and testing environments. The database will be created in memory when the application starts.
- **Limitation**: SQLite is not recommended for heavy production use, however it has been used in this project for simplicity. For production, it is recommended to use a more robust database system like PostgreSQL or MySQL.


