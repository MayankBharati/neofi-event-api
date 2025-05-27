# NeoFi Collaborative Event Management API

A RESTful backend API for managing events with role-based access control, history tracking, and collaborative editing features.

## 🛠 Features Implemented

✅ **JWT Authentication**  
- `/api/auth/register`, `/api/token/`, `/api/auth/logout`, `/api/token/refresh/`

✅ **CRUD Operations for Events**  
- Full CRUD for event management including recurring events via `rrule` patterns

✅ **Batch Create Events**  
- `/api/events/batch` endpoint for creating multiple events in one request

✅ **Role-Based Access Control (RBAC)**  
- Three roles: `Owner`, `Editor`, `Viewer`  
- Fine-grained permissions per event

✅ **Share Events with Granular Roles**  
- `/api/events/{id}/share` allows sharing events with custom roles

✅ **Track Changes with Version History**  
- Every create/update/delete is tracked with user attribution and JSON snapshots

✅ **View Changelog & Diff Between Versions**  
- `/api/events/{id}/changelog` lists all changes  
- `/api/events/{id}/diff/{version1}/{version2}` returns field-level differences using deep comparison

✅ **Rollback to Previous Versions**  
- `/api/events/{id}/rollback/{version_id}` reverts an event to a prior state

✅ **Interactive API Documentation via Swagger UI**  
- Auto-generated OpenAPI docs at http://localhost:8000/docs/

✅ **Security Measures**  
- JWT authentication  
- Token blacklisting for logout  
- UUIDs instead of sequential IDs  
- Input validation  
- Role-based permissions enforced at view level

✅ **History Tracking Design**  
- Every change to an event is stored in `EventHistory` model  
- Includes old and new data as JSON  
- Supports rollback and diff operations

✅ **Diff Visualization Strategy**  
- Field-by-field comparison between two versions  
- Returns structured JSON showing "from" and "to" values  
- Based on deep comparison logic

---

## 🧩 Technologies Used

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Language |
| Django 5.2 | Web framework |
| Django REST Framework | REST API support |
| PostgreSQL | Database |
| JWT Auth (`rest_framework_simplejwt`) | Token-based authentication |
| drf-spectacular | OpenAPI/Swagger documentation |
| UUIDs | Secure, non-sequential IDs |
| JSONField | Store flexible data like recurrence patterns and history diffs

---

## 🔐 Security Considerations

- JWT tokens used for secure authentication
- Token blacklisting supports logout functionality
- UUIDs prevent ID guessing attacks
- Proper permission classes restrict unauthorized access
- Input validation prevents malformed requests

---

## 📌 Endpoints Overview

### 🔐 Authentication
| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/auth/register` | POST | Register a new user |
| `/api/token/` | POST | Login and receive JWT token |
| `/api/token/refresh/` | POST | Refresh expired JWT token |
| `/api/auth/logout` | POST | Invalidate refresh token

### 📅 Event Management
| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/events/` | GET / POST | List or create events |
| `/api/events/{id}` | GET / PUT / PATCH / DELETE | Retrieve, update or delete an event |
| `/api/events/batch` | POST | Create multiple events in one request |

### 🤝 Collaboration
| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/events/{event_id}/share/` | POST | Share event with users |
| `/api/events/{event_id}/permissions/` | GET | List all users with access |
| `/api/events/{event_id}/permissions/{user_id}/` | PUT / DELETE | Update or remove user permission |

### 🔄 Versioning & Diff
| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/events/{event_id}/changelog/` | GET | Get change history for an event |
| `/api/events/{event_id}/diff/{version1}/{version2}/` | GET | Compare two versions of an event |
| `/api/events/{event_id}/rollback/{version_id}/` | POST | Revert to a previous version |
| `/api/events/{event_id}/version/{version_id}/` | GET | Get specific version of an event |

---

## 🚀 Setup Instructions

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver