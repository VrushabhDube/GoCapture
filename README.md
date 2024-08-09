# GoCapture

## Installation

1. Download the repo file.
2. Extract it.
3. Open this folder in cmd.
4. Activate the environment using the command: `.venv/Scripts/activate`.
5. Execute the `main.py` file by typing: `python main.py`.

## API Documentation

**Base URL:** /

### User Resource

- **GET** `/users`: Get all users.
- **GET** `/users/<user_id>`: Get user by ID.
- **POST** `/users`: Create a new user.
- **PUT** `/users/<user_id>`: Update a user.
- **DELETE** `/users/<user_id>`: Delete a user.

### Task Resource

- **GET** `/tasks`: Get tasks by user ID.
- **GET** `/tasks/<task_id>`: Get task by ID.
- **POST** `/tasks`: Create a new task.
- **PUT** `/tasks/<task_id>`: Update a task.
- **DELETE** `/tasks/<task_id>`: Delete a task.

### Authentication

- **POST** `/login`: Login and get JWT token.
- **POST** `/logout`: Logout and blacklist JWT token.
- **POST** `/refresh`: Refresh JWT token.

## Brief Write-up on Approach and Assumptions

### Approach

- **Model Design:** Utilizes `User` and `Task` models with a one-to-many relationship.
- **API Structure:** RESTful endpoints for CRUD operations on `User` and `Task`.
- **Authentication:** JWT for secure access; tokens are issued on login and blacklisted on logout.
- **Session Management:** SQLAlchemy handles database transactions with sessions managed via `get_db()`.
- **Token Blacklisting:** Tokens are blacklisted in-memory upon logout.

### Assumptions

- **Database:** Uses MySQL; schema setup via SQLAlchemy.
- **Authentication:** Relies on JWT for authentication; assumes token integrity.
- **Security:** Passwords hashed with `bcrypt`; JWT secret is securely managed.
- **Deployment:** In-memory blacklisting suitable for development; production may require a more robust solution.
