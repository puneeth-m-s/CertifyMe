# CertifyMe Backend API - Complete Test Guide

## 🚀 Quick Start

Backend running at: **http://127.0.0.1:5000**

## 📋 API Endpoints

### Authentication APIs (/auth)

#### 1. Admin Signup
```
POST /auth/signup
Content-Type: application/json

{
  "username": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}

Success Response (201):
{
  "message": "Admin created successfully"
}
```

#### 2. Admin Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123!"
}

Success Response (200):
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 3. Forgot Password
```
POST /auth/forgot-password
Content-Type: application/json

{
  "email": "john@example.com"
}

Success Response (200):
{
  "message": "Reset token generated",
  "reset_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 4. Reset Password
```
POST /auth/reset-password
Authorization: Bearer {reset_token}
Content-Type: application/json

{
  "new_password": "NewPassword456!"
}

Success Response (200):
{
  "message": "Password reset successfully"
}
```

---

### Opportunity Management APIs (/opportunities)

**Note: All opportunity endpoints require JWT authentication**

#### 1. Get All Opportunities
```
GET /opportunities
Authorization: Bearer {access_token}

Success Response (200):
[
  {
    "id": 1,
    "title": "Full Stack Web Development",
    "description": "Learn web development from scratch",
    "admin_id": 1,
    "created_at": "2026-05-06T10:30:00",
    "updated_at": "2026-05-06T10:30:00"
  }
]
```

#### 2. Add New Opportunity
```
POST /opportunities
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Full Stack Web Development",
  "description": "Learn HTML, CSS, JavaScript, React, Node.js, MongoDB"
}

Success Response (201):
{
  "message": "Opportunity added successfully",
  "id": 1
}
```

#### 3. Get Opportunity Details
```
GET /opportunities/{id}
Authorization: Bearer {access_token}

Success Response (200):
{
  "id": 1,
  "title": "Full Stack Web Development",
  "description": "Learn web development from scratch",
  "admin_id": 1,
  "created_at": "2026-05-06T10:30:00",
  "updated_at": "2026-05-06T10:30:00"
}
```

#### 4. Update Opportunity
```
PUT /opportunities/{id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description"
}

Success Response (200):
{
  "message": "Opportunity updated successfully"
}
```

#### 5. Delete Opportunity
```
DELETE /opportunities/{id}
Authorization: Bearer {access_token}

Success Response (200):
{
  "message": "Opportunity deleted successfully"
}
```

---

## 🧪 Test Workflow

### Step 1: Signup (Create Admin Account)
```bash
# Using curl
curl -X POST http://127.0.0.1:5000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "Admin User",
    "email": "admin@test.com",
    "password": "Admin@123456"
  }'

# Expected: 201 Created
```

### Step 2: Login (Get Access Token)
```bash
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "Admin@123456"
  }'

# Expected: 200 OK with access_token
# Save the token: eyJ0eXAi...
```

### Step 3: Add Opportunity (Requires Token)
```bash
curl -X POST http://127.0.0.1:5000/opportunities \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAi..." \
  -d '{
    "title": "Python for Beginners",
    "description": "Learn Python programming from zero to hero. Includes variables, loops, functions, OOP, file handling, and real-world projects."
  }'

# Expected: 201 Created with id
```

### Step 4: Get All Opportunities
```bash
curl -X GET http://127.0.0.1:5000/opportunities \
  -H "Authorization: Bearer eyJ0eXAi..."

# Expected: 200 OK with list of opportunities
```

### Step 5: Update Opportunity
```bash
curl -X PUT http://127.0.0.1:5000/opportunities/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAi..." \
  -d '{
    "title": "Advanced Python Programming",
    "description": "Master Python with advanced concepts"
  }'

# Expected: 200 OK
```

### Step 6: Delete Opportunity
```bash
curl -X DELETE http://127.0.0.1:5000/opportunities/1 \
  -H "Authorization: Bearer eyJ0eXAi..."

# Expected: 200 OK
```

---

## 📱 Testing with Thunder Client (VS Code Extension)

### Installation
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Thunder Client"
4. Click Install

### Create Collection & Test Requests

**1. Environment Setup**
- Click "Env" in Thunder Client
- Add: `base_url`: `http://127.0.0.1:5000`
- Add: `token`: `(will be filled after login)`

**2. Create Signup Request**
```
POST {{base_url}}/auth/signup
Headers:
  Content-Type: application/json

Body (JSON):
{
  "username": "TestAdmin",
  "email": "testadmin@certify.com",
  "password": "TestPass@123"
}
```

**3. Create Login Request**
```
POST {{base_url}}/auth/login
Headers:
  Content-Type: application/json

Body (JSON):
{
  "email": "testadmin@certify.com",
  "password": "TestPass@123"
}
```
**After this request, update `token` var with `access_token` value**

**4. Create Opportunity**
```
POST {{base_url}}/opportunities
Headers:
  Content-Type: application/json
  Authorization: Bearer {{token}}

Body (JSON):
{
  "title": "Web Development Bootcamp",
  "description": "Complete web development course including frontend and backend technologies"
}
```

**5. Get All Opportunities**
```
GET {{base_url}}/opportunities
Headers:
  Authorization: Bearer {{token}}
```

**6. Update Opportunity**
```
PUT {{base_url}}/opportunities/1
Headers:
  Content-Type: application/json
  Authorization: Bearer {{token}}

Body (JSON):
{
  "title": "Advanced Web Development",
  "description": "Advanced techniques for modern web applications"
}
```

**7. Delete Opportunity**
```
DELETE {{base_url}}/opportunities/1
Headers:
  Authorization: Bearer {{token}}
```

---

## ✅ Success Criteria

✓ Signup creates new admin  
✓ Login returns valid JWT token  
✓ Token needed for opportunity access  
✓ Can create opportunities  
✓ Can read own opportunities  
✓ Can update own opportunities  
✓ Can delete own opportunities  
✓ Data persists in database  
✓ Each admin sees only their opportunities  

---

## 🐛 Common Error Codes

| Code | Error | Solution |
|------|-------|----------|
| 400 | Username/email/password required | Check request body |
| 401 | Invalid credentials | Verify email and password |
| 404 | Email not found | Use correct email in forgot-password |
| 401 | Token missing/expired | Login again and use new token |
| 404 | Opportunity not found | Check opportunity ID |
| 422 | Invalid data | Ensure all required fields are provided |

---

## 📂 Frontend Integration

The frontend (`Test1/sky/admin.html`) automatically connects to the backend via `api-integration.js`.

**Key Features:**
- Auto-saves JWT token in localStorage
- Auto-restores session on page reload
- CORS enabled for cross-origin requests
- Error handling with user-friendly messages

**File Structure:**
```
Test1/sky/
├── admin.html          # UI with forms
├── admin.css           # Styling  
├── admin.js            # UI logic
└── api-integration.js  # Backend API calls
```

---

## 🚀 Database

- **Type**: SQLite
- **Location**: `backend/instance/app.db`
- **Tables**: Admin, Opportunity
- **Auto-created** on first run

View database contents:
```bash
sqlite3 backend/instance/app.db ".tables"
sqlite3 backend/instance/app.db "SELECT * FROM admin;"
sqlite3 backend/instance/app.db "SELECT * FROM opportunity;"
```

---

## ⚙️ Environment Variables

Update `backend/.env`:
```
SECRET_KEY=your-very-long-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///instance/app.db
```

---

## 📝 Notes

- All timestamps are in UTC
- Passwords are hashed with Werkzeug security
- JWT tokens expire after request
- Each admin is isolated to their own opportunities
- No hardcoded data - everything from database

Happy testing! 🎉