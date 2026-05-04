# Mini Enterprise Collaboration Workflow

A role-based enterprise collaboration system for managing users, tasks, Kanban workflow, approval requests, document uploads, dashboards, and audit logs.

The application is built with a layered backend architecture and a React frontend. The backend separates API routing, service/business logic, repository/database access, models, and schemas.

---

## 1. Technology Stack

### Backend

- **Python**
- **FastAPI** - REST API framework
- **SQLAlchemy ORM** - database models and queries
- **Pydantic** - request and response validation
- **Alembic** - database migrations
- **MySQL** - relational database
- **PyMySQL** - MySQL database driver
- **JWT authentication** - token-based login
- **Passlib** - password hashing
- **python-jose** - JWT encoding/decoding
- **Uvicorn** - ASGI server
- **FastAPI CORS Middleware** - frontend-backend communication

### Frontend

- **React**
- **Vite**
- **Tailwind CSS**
- **Axios**
- **React Router DOM**
- **LocalStorage** for storing logged-in user and access token

### Database / DevOps

- **MySQL running in Docker**
- **Alembic migrations** for table creation and schema changes

---

## 2. Main Features

- User registration and login
- JWT-based authentication
- Role-based access for Admin, Manager, and Employee
- Admin user management
- Task creation, assignment, update, delete, and status tracking
- Kanban board for task workflow
- Priority and due date handling
- Approval workflow with approve, reject, hold, and transfer to admin
- Leave request support with leave date, full day or half day, and session details
- Document upload, listing, preview/download, delete, and version tracking
- Dashboard summary
- Audit log viewing for admin

---

## 3. Project Structure

The current uploaded code contains the following structure.

```text
backend/
└── app/
    ├── main.py
    ├── api/
    │   ├── deps.py
    │   └── v1/
    │       ├── api.py
    │       └── endpoints/
    │           ├── auth.py
    │           ├── users.py
    │           ├── tasks.py
    │           ├── approvals.py
    │           ├── documents.py
    │           ├── dashboard.py
    │           └── audit_logs.py
    ├── core/
    │   ├── config.py
    │   ├── database.py
    │   ├── roles.py
    │   └── security.py
    ├── models/
    │   ├── __init__.py
    │   ├── user.py
    │   ├── task.py
    │   ├── approval.py
    │   ├── document.py
    │   ├── audit_log.py
    │   ├── department.py
    │   └── workspace.py
    ├── repositories/
    │   ├── __init__.py
    │   ├── user_repository.py
    │   ├── task_repository.py
    │   ├── approval_repository.py
    │   ├── document_repository.py
    │   └── audit_repository.py
    ├── schemas/
    │   ├── auth.py
    │   ├── user.py
    │   ├── task.py
    │   ├── approval.py
    │   ├── document.py
    │   └── dashboard.py
    ├── services/
    │   ├── auth_service.py
    │   ├── user_service.py
    │   ├── task_service.py
    │   ├── approval_service.py
    │   ├── document_service.py
    │   ├── dashboard_service.py
    │   └── audit_service.py
    └── utils/
        └── file_storage.py

frontend/
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── App.css
    ├── index.css
    ├── api/
    │   ├── client.js
    │   ├── axios.js
    │   ├── authApi.js
    │   ├── adminApi.js
    │   ├── taskApi.js
    │   ├── approvalApi.js
    │   ├── documentApi.js
    │   ├── dashboardApi.js
    │   ├── workspaceApi.js
    │   └── context/
    │       └── AuthContext.jsx
    ├── app/
    │   └── router.jsx
    ├── hooks/
    │   └── useAuth.js
    ├── components/
    │   ├── layout/
    │   │   ├── AppLayout.jsx
    │   │   ├── Header.jsx
    │   │   └── Sidebar.jsx
    │   └── tasks/
    │       ├── KanbanBoard.jsx
    │       ├── TaskCard.jsx
    │       └── TaskList.jsx
    ├── pages/
    │   ├── LoginPage.jsx
    │   ├── RegisterPage.jsx
    │   ├── DashboardPage.jsx
    │   ├── TasksPage.jsx
    │   ├── KanbanPage.jsx
    │   ├── ApprovalsPage.jsx
    │   ├── DocumentsPage.jsx
    │   └── AdminUsersPage.jsx
    └── assets/
        ├── hero.png
        ├── react.svg
        └── vite.svg
```

---

## 4. Backend Architecture

The backend follows this layered flow:

```text
Router / Endpoint → Service Layer → Repository Layer → SQLAlchemy Model → MySQL Database
```

### Layer Purpose

| Layer              | Purpose                                                                                               |
| ------------------ | ----------------------------------------------------------------------------------------------------- |
| `api/v1/endpoints` | Handles HTTP routes, dependency injection, request body, and response return                          |
| `services`         | Holds business logic such as role rules, task assignment rules, approval flow, document version logic |
| `repositories`     | Handles database read/write operations using SQLAlchemy                                               |
| `models`           | SQLAlchemy database table definitions                                                                 |
| `schemas`          | Pydantic request/response validation                                                                  |
| `core`             | Configuration, database connection, roles, and security helpers                                       |
| `utils`            | Utility logic such as file storage                                                                    |

---

## 5. Environment Configuration

Create a `.env` file in the backend root directory.

```env
APP_NAME=Mini Enterprise Collaboration Flow
API_V1_PREFIX=/api/v1

DATABASE_URL=mysql+pymysql://root:root@127.0.0.1:3306/ec

JWT_SECRET_KEY=change_me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

CORS_ORIGIN=http://localhost:5173,http://127.0.0.1:5173

SEED_ADMIN=True
ADMIN_EMAIL=admin@gmail.com
ADMIN_PASSWORD=admin1234

UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE_BYTES=5242880

RATE_LIMIT_LOGIN=5/minute
RATE_LIMIT_TICKET_CREATE=10/hour
```

Frontend `.env` file:

```env
VITE_API_BASE=http://127.0.0.1:8000/api/v1
```

---

## 6. API Endpoints and Purpose

Base URL:

```text
http://127.0.0.1:8000/api/v1
```

### Authentication APIs

| Method | Endpoint         | Purpose                                                                                     | Auth Required |
| ------ | ---------------- | ------------------------------------------------------------------------------------------- | ------------- |
| `POST` | `/auth/register` | Register a new user with name, email, password, and role                                    | No            |
| `POST` | `/auth/login`    | Login using email and password through OAuth2 form data and return JWT token plus user data | No            |

---

### User Management APIs

| Method   | Endpoint           | Purpose                                                                          | Access         |
| -------- | ------------------ | -------------------------------------------------------------------------------- | -------------- |
| `GET`    | `/users/`          | List users for admin and manager, used for user management and assignee dropdown | Admin, Manager |
| `POST`   | `/users/`          | Create new user                                                                  | Admin          |
| `PUT`    | `/users/{user_id}` | Update existing user details                                                     | Admin          |
| `DELETE` | `/users/{user_id}` | Delete a user                                                                    | Admin          |

---

### Task APIs

| Method   | Endpoint           | Purpose                                                             | Access                                |
| -------- | ------------------ | ------------------------------------------------------------------- | ------------------------------------- |
| `GET`    | `/tasks`           | List tasks based on logged-in user role                             | Logged-in users                       |
| `GET`    | `/tasks/{task_id}` | View single task details                                            | Logged-in users                       |
| `POST`   | `/tasks`           | Create task with title, priority, due date, and assignee            | Admin, Manager based on service rules |
| `PUT`    | `/tasks/{task_id}` | Update task fields such as status, assignee, due date, and priority | Based on role rules                   |
| `DELETE` | `/tasks/{task_id}` | Delete task                                                         | Based on role rules                   |

Task status values used by the UI:

```text
todo
in_progress
review
done
```

Task priority values:

```text
low
medium
high
```

---

### Approval Workflow APIs

| Method | Endpoint                  | Purpose                                                                    | Access                            |
| ------ | ------------------------- | -------------------------------------------------------------------------- | --------------------------------- |
| `POST` | `/approvals`              | Submit approval request such as leave, expense, purchase, or other request | Logged-in users                   |
| `GET`  | `/approvals`              | List approval requests based on role                                       | Logged-in users                   |
| `POST` | `/approvals/{id}/action`  | Approve, reject, hold, or transfer approval request                        | Manager/Admin based on workflow   |
| `GET`  | `/approvals/{id}/history` | View full action history of an approval request                            | Available through approval module |

Supported approval actions:

```text
approve
reject
hold
transfer_admin
```

Approval flow:

```text
Employee submits request
↓
Status: pending_manager
↓
Manager can Approve / Reject / Hold / Transfer to Admin
↓
If transferred: Status becomes pending_admin
↓
Admin can Approve / Reject / Hold
↓
Final status: approved / rejected / on_hold
```

---

### Document APIs

| Method   | Endpoint                            | Purpose                                                            | Access                                          |
| -------- | ----------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------- |
| `POST`   | `/documents/upload`                 | Upload a file and optionally link it to a task or approval request | Logged-in users                                 |
| `GET`    | `/documents`                        | List uploaded documents                                            | Current implementation allows listing documents |
| `GET`    | `/documents/{document_id}`          | View document metadata                                             | Logged-in users                                 |
| `GET`    | `/documents/{document_id}/download` | Download or preview document using browser                         | Logged-in users                                 |
| `DELETE` | `/documents/{document_id}`          | Delete uploaded document                                           | Logged-in users                                 |

Upload request uses `multipart/form-data`:

```text
file=<selected file>
task_id=<optional task id>
approval_request_id=<optional approval request id>
```

The frontend creates preview/download URL like:

```text
http://127.0.0.1:8000/api/v1/documents/{document_id}/download
```

---

### Dashboard APIs

| Method | Endpoint             | Purpose                                                      | Access                                 |
| ------ | -------------------- | ------------------------------------------------------------ | -------------------------------------- |
| `GET`  | `/dashboard/summary` | Returns task summary counts for dashboard cards and insights | Public in current route implementation |

Dashboard summary includes:

```text
total_tasks
done_tasks
pending_tasks
todo_tasks
in_progress_tasks
review_tasks
```

---

### Audit Log APIs

| Method | Endpoint      | Purpose                                   | Access |
| ------ | ------------- | ----------------------------------------- | ------ |
| `GET`  | `/audit-logs` | View audit log entries for system actions | Admin  |

---

## 7. Installation and Execution Steps

### Prerequisites

Install:

- Python 3.12 or compatible version
- Node.js and npm
- MySQL Docker container
- Git
- Alembic

---

### Step 1: Start MySQL Docker Container

If the MySQL container already exists:

```bash
docker ps
```

If it is stopped:

```bash
docker start <mysql_container_name>
```

Enter MySQL:

```bash
docker exec -it <mysql_container_name> mysql -u root -p
```

Create database:

```sql
CREATE DATABASE IF NOT EXISTS ec;
```

---

### Step 2: Backend Setup

Go to backend folder:

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment on Windows PowerShell:

```bash
.\venv\Scripts\activate
```

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy pymysql pydantic pydantic-settings python-jose passlib[bcrypt] python-multipart email-validator alembic
```

Create `.env` file using the backend environment configuration shown above.

---

### Step 3: Run Alembic Migrations

If Alembic is already configured in your project:

```bash
alembic upgrade head
```

If you changed models and need a new migration:

```bash
alembic revision --autogenerate -m "update schema"
alembic upgrade head
```

Important current schema note:

- `approval_requests.amount` should be `FLOAT` because half-day leave uses `0.5`.

---

### Step 4: Run Backend

From the backend folder:

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

---

### Step 5: Frontend Setup

Go to frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Install required frontend packages if not already installed:

```bash
npm install axios react-router-dom
```

Create `.env`:

```env
VITE_API_BASE=http://127.0.0.1:8000/api/v1
```

Run frontend:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

## 8. Testing Flow

### Flow 1: Admin Setup

1. Open frontend.
2. Register admin:

```text
Name: Admin
Email: admin@gmail.com
Password: admin1234
Role: admin
```

3. Login as admin.
4. Open Admin page.
5. Create manager user:

```text
Name: Charles Manager
Email: charles@example.com
Password: manager1234
Role: manager
```

6. Create employee user:

```text
Name: John Employee
Email: john@example.com
Password: employee1234
Role: employee
```

Expected result:

- Admin can create users.
- Admin can edit/delete users.
- Manager and employee should not have admin user-management permissions.

---

### Flow 2: Manager Creates and Assigns Tasks

1. Login as manager.
2. Open Tasks page.
3. Create a task.
4. Select priority.
5. Select due date.
6. Select employee from assignee dropdown.
7. Submit task.

Expected result:

- Task appears in task list.
- Assignee name appears instead of only user ID.
- Priority is displayed with visual badge.

---

### Flow 3: Employee Updates Task Status

1. Login as employee.
2. Open Tasks page.
3. View assigned tasks.
4. Change status from `todo` to `in_progress`, `review`, or `done`.

Expected result:

- Employee can update assigned task status.
- Employee should not edit admin/manager-only fields if service rules block them.

---

### Flow 4: Kanban Board Testing

1. Login as manager.
2. Open Kanban page.
3. Move task from one column to another:

```text
todo → in_progress → review → done
```

4. Confirm that the task card moves immediately.
5. Refresh or revisit Kanban page.

Expected result:

- Task status remains in the updated column.
- UI should update immediately after drag/drop or status change.

---

### Flow 5: Leave Approval Request

1. Login as employee.
2. Open Approvals page.
3. Select request type as Leave.
4. Enter:

```text
Leave Date: Select date from date picker
Leave Duration: Full Day or Half Day
Session: Forenoon or Afternoon if Half Day
Title: Hospital appointment
Description: Viral fever
```

5. Submit request.

Expected result:

- Request appears with status `pending_manager`.
- Employee sees `Waiting for approval`.
- Leave card displays date, duration, session, and description.

---

### Flow 6: Manager Approval Flow

1. Login as manager.
2. Open Approvals page.
3. View employee leave request.
4. Manager should see:

```text
Approve
Reject
Hold
Transfer to Admin
```

5. Click Approve, Reject, Hold, or Transfer to Admin.

Expected result:

- Approve changes status to `approved`, unless workflow transfers to admin.
- Reject changes status to `rejected`.
- Hold changes status to `on_hold`.
- Transfer to Admin changes status to `pending_admin`.

---

### Flow 7: Admin Approval Flow

1. Login as admin.
2. Open Approvals page.
3. View requests with `pending_admin` status.
4. Admin should see approval action buttons.
5. Approve, reject, or hold request.

Expected result:

- Final decision is reflected in approval list.
- Employee can see final status.

---

### Flow 8: Document Management

1. Login as any user.
2. Open Documents page.
3. Upload a file.
4. Optionally provide task id or approval request id if UI supports it.
5. View uploaded file in document list.
6. Click Preview or Download.
7. Upload same file again to test versioning.
8. Delete document if needed.

Expected result:

- Uploaded document appears in list.
- File can be downloaded or previewed.
- Re-upload creates a new version according to backend versioning logic.

---

### Flow 9: Dashboard Testing

1. Login as any valid user.
2. Open Dashboard page.
3. Check task summary cards and distribution bars.

Expected result:

- Dashboard shows task counts.
- Counts update after creating or changing task status.

---

### Flow 10: Audit Logs

1. Login as admin.
2. Open Admin or Audit Log section if available in UI.
3. Check system actions.

Expected result:

- Admin can view audit logs.
- Non-admin users cannot access audit logs.

---

## 9. Default Local URLs

| Service  | URL                            |
| -------- | ------------------------------ |
| Backend  | `http://127.0.0.1:8000`        |
| Swagger  | `http://127.0.0.1:8000/docs`   |
| Frontend | `http://localhost:5173`        |
| API Base | `http://127.0.0.1:8000/api/v1` |

---

## 10. Project Demo Order

1. Register admin.
2. Admin creates manager and employee.
3. Manager creates and assigns task.
4. Employee updates task status.
5. Manager views Kanban board.
6. Employee submits leave request.
7. Manager approves or transfers to admin.
8. Admin finalizes transferred request.
9. Upload and download document.
10. Show dashboard and audit logs.
