# IBM watsonx.ai Setup Guide - Complete Instructions

## 🔑 What You Need

For IBM watsonx.ai integration, you need **3 things**:

1. **API Key** ✅ (You have this)
2. **Project ID** ❓ (You provided this, but might need verification)
3. **Proper Account Setup** ⚠️ (This is the issue)

---

## 📝 Understanding IBM watsonx.ai IDs

### Project ID vs Service ID vs Space ID

**Project ID** (What we need):
- Found in watsonx.ai Studio projects
- Format: `12345678-1234-1234-1234-123456789abc`
- Used for: Development and experimentation
- Location: watsonx.ai Studio → Your Project → Manage tab

**Service ID** (NOT what we need):
- Used for service-to-service authentication
- Different from Project ID
- Not required for this integration

**Space ID** (Alternative to Project ID):
- Used for deployment spaces
- Can be used instead of Project ID
- For production deployments

---

## 🔍 How to Find Your Correct Project ID

### Method 1: From watsonx.ai Studio

1. Go to: https://dataplatform.cloud.ibm.com/
2. Log in with your IBM Cloud account
3. Click on **Projects** in the left menu
4. Click on your project name
5. Click on the **Manage** tab
6. Look for **Project ID** - it should be a UUID format

### Method 2: From URL

When you're in your project, the URL looks like:
```
https://dataplatform.cloud.ibm.com/projects/YOUR-PROJECT-ID-HERE?context=wx
```

The UUID in the URL is your Project ID.

---

## ⚠️ Current Authentication Error

**Error:** `Failed to verify user profile existence: aryan.deshpande29@gmail.com`

**This means one of these issues:**

### Issue 1: Account Not Fully Set Up
Your IBM Cloud account might not be fully configured for watsonx.ai.

**Solution:**
1. Go to https://cloud.ibm.com/
2. Complete your profile setup
3. Verify email if not done
4. Accept any pending terms of service

### Issue 2: watsonx.ai Service Not Provisioned
You might not have watsonx.ai service activated.

**Solution:**
1. Go to https://cloud.ibm.com/catalog
2. Search for "watsonx.ai"
3. Click on "watsonx.ai"
4. Click "Create" or "Launch"
5. Follow the setup wizard

### Issue 3: API Key Doesn't Have Correct Permissions
The API key might not have access to watsonx.ai.

**Solution:**
1. Go to https://cloud.ibm.com/iam/apikeys
2. Find your API key
3. Check it has these permissions:
   - **Watson Machine Learning** service access
   - **watsonx.ai** access
   - **Editor** or **Manager** role

### Issue 4: Wrong Project ID
The Project ID might be incorrect or from a different account.

**Solution:**
1. Double-check the Project ID from watsonx.ai Studio
2. Make sure you're logged in with `aryan.deshpande29@gmail.com`
3. Verify the project exists and you have access

---

## 🔧 Alternative: Use Deployment Space

If you're having trouble with Project ID, you can use a **Deployment Space** instead:

### Create a Deployment Space:

1. Go to https://dataplatform.cloud.ibm.com/
2. Click **Deployments** in the left menu
3. Click **New deployment space**
4. Name it (e.g., "watsonx-ai-space")
5. Associate it with your Watson Machine Learning service
6. Get the **Space ID**

### Update .env to use Space ID:

Instead of `WATSONX_PROJECT_ID`, you would use `WATSONX_SPACE_ID`.

However, our current code uses Project ID, so this would require a small code change.

---

## 🎯 Recommended Steps to Fix

### Step 1: Verify Your Account
```bash
# Check if you can access watsonx.ai
1. Go to: https://dataplatform.cloud.ibm.com/
2. Log in with: aryan.deshpande29@gmail.com
3. Can you see the Projects page? ✓ or ✗
4. Can you see your project? ✓ or ✗
```

### Step 2: Verify Project Access
```bash
1. Open your project in watsonx.ai Studio
2. Go to Manage → Access Control
3. Is aryan.deshpande29@gmail.com listed? ✓ or ✗
4. What role do you have? (Viewer/Editor/Admin)
```

### Step 3: Verify API Key
```bash
1. Go to: https://cloud.ibm.com/iam/apikeys
2. Find your API key
3. Check "Service IDs" - should show Watson Machine Learning
4. Check permissions - should have Editor or Manager
```

### Step 4: Try Creating New API Key
```bash
1. Go to: https://cloud.ibm.com/iam/apikeys
2. Click "Create"
3. Name: "watsonx-ai-integration"
4. Description: "For code analysis project"
5. Copy the new key
6. Update backend/.env with new key
7. Restart server and test
```

---

## 🧪 Quick Test

After fixing the authentication, test with:

```bash
cd backend
python -c "from ibm_watsonx_ai import Credentials; from ibm_watsonx_ai.foundation_models import ModelInference; creds = Credentials(api_key='YOUR_KEY', url='https://us-south.ml.cloud.ibm.com'); print('Credentials OK')"
```

---

## 📞 Need Help?

### IBM Cloud Support
- Support Center: https://cloud.ibm.com/unifiedsupport/supportcenter
- Community: https://community.ibm.com/community/user/watsonai/home

### watsonx.ai Documentation
- Getting Started: https://dataplatform.cloud.ibm.com/docs/content/wsj/getting-started/welcome-main.html
- API Reference: https://ibm.github.io/watsonx-ai-python-sdk/

### Common Issues
- **404 User Not Found**: Account not fully set up
- **401 Unauthorized**: API key lacks permissions
- **403 Forbidden**: No access to project/space
- **400 Bad Request**: Wrong Project ID format

---

## ✅ What to Do Now

1. **Verify your IBM Cloud account is fully set up**
2. **Check you can access watsonx.ai Studio**
3. **Confirm the Project ID is correct**
4. **Try creating a new API key with full permissions**
5. **Contact IBM support if issues persist**

The code is 100% ready - it's just an IBM Cloud account configuration issue!