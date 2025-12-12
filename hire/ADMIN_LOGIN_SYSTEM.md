# Redback Login System - Admin Authentication

## ✅ Changes Implemented

### 1. Branding Update
- Changed all "InterviewFlow" references to **"Redback"**
- Updated throughout templates, base layout, and admin emails
- Admin email: `admin@redback.local`

### 2. Role-Based Login with Dropdown
Added role selection dropdown to login page with 4 options:
- **Admin** (requires token)
- **HR**
- **Interviewer**  
- **Candidate**

### 3. Enhanced Admin Security
Admin login now requires **THREE credentials**:
1. **Email**: `admin@redback.local`
2. **Password**: `Admin@2025`
3. **Admin Token**: `admin-access-token-2025`

### 4. Dynamic Admin Token Field
- Admin token field appears only when "Admin" role is selected
- JavaScript toggles field visibility automatically
- Token is required for admin login

## 🔐 Admin Login Process

### Step 1: Select Admin Role
Login page has dropdown - select "Admin"

### Step 2: Admin Token Field Appears
When Admin is selected, the token field shows automatically

### Step 3: Enter Three Credentials
- Email: `admin@redback.local`
- Password: `Admin@2025`
- Token: `admin-access-token-2025`

### Step 4: Validation
System validates:
1. Email and password match database
2. Selected role matches user's actual role
3. Admin token matches the security token

### Step 5: Redirect
Admin users are automatically redirected to `/admin` panel

## 🛠️ Admin User Creation

### Programmatic Creation
Run the script to create/update admin:
```bash
python create_admin.py
```

This script:
- Creates admin user if doesn't exist
- Updates password if already exists
- Displays all credentials clearly
- Shows login instructions

## 📋 Credentials Reference

| Field | Value |
|-------|-------|
| Email | admin@redback.local |
| Password | Admin@2025 |
| Token | admin-access-token-2025 |
| Role | Admin |

## 🔒 Security Features

### For Admin Login
1. **Three-factor authentication**: Email + Password + Token
2. **Role validation**: System checks if selected role matches user's actual role
3. **Token requirement**: Admin cannot login without valid token
4. **Auto-redirect**: Successful admin login goes to admin panel

### For Other Roles
1. **Two-factor**: Email + Password only
2. **No token required**: HR, Interviewer, Candidate don't need tokens
3. **Role validation**: Must select correct role matching their account

## 🎯 Access Control

| Role | Can Self-Register? | Token Required? | Created By |
|------|-------------------|-----------------|------------|
| **Admin** | ❌ No | ✅ Yes | Script/Programmatic |
| **HR** | ❌ No | ❌ No | Admin Only |
| **Interviewer** | ✅ Yes | ❌ No | Self or Admin |
| **Candidate** | ✅ Yes | ❌ No | Self or Admin |

## 🚀 Testing the System

### Test Admin Login
1. Go to: http://localhost:5000/auth/login
2. Role dropdown: Select "Admin"
3. Email: `admin@redback.local`
4. Password: `Admin@2025`
5. Admin Token: `admin-access-token-2025`
6. Click "Login"
7. Should redirect to `/admin`

### Test Other Roles
1. Select any other role (HR, Interviewer, Candidate)
2. Admin token field hides automatically
3. Only email and password required
4. Redirects to home page

## 📝 Files Modified

1. **auth.py**
   - Added role validation in login
   - Added admin token verification
   - Updated admin email to `admin@redback.local`
   - Auto-redirect admin to `/admin`

2. **templates/auth/login.html**
   - Added role dropdown with 4 options
   - Added dynamic admin token field
   - Added JavaScript to toggle token field
   - Added admin credentials info card
   - Rebranded to "Redback"

3. **templates/base.html**
   - Changed "InterviewFlow" to "Redback"
   - Updated footer copyright

4. **templates/index.html**
   - Changed welcome message to "Redback"

5. **templates/auth/register.html**
   - Updated title to "Redback"

6. **create_admin.py** (NEW)
   - Script to create/update admin user
   - Sets predefined credentials
   - Displays login instructions

## ⚠️ Important Notes

### Security Best Practices
1. Change admin password after first login
2. Keep admin token secure (don't share publicly)
3. Consider changing token in production (update `ADMIN_BYPASS_TOKEN` in `auth.py`)
4. Token is hardcoded for development - use environment variables in production

### Credential Management
- Admin credentials are programmatically created
- Password is hashed in database
- Token validation happens in authentication flow
- All three credentials required for admin access

### Role Validation
- System enforces role matching during login
- Users must select their correct role
- Invalid role selection shows warning message
- Prevents role confusion or unauthorized access

## 🎉 Summary

The Redback system now has:
✅ Role-based login with dropdown selection
✅ Enhanced admin security (email + password + token)
✅ Dynamic token field (shows only for admin)
✅ Programmatic admin user creation
✅ Clear credential display and instructions
✅ Complete rebranding from InterviewFlow to Redback

Admin users now have an extra layer of security while other roles have a streamlined login experience!
