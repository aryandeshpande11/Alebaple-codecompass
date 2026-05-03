# How to Get Your IBM watsonx.ai Project ID

## Steps:

1. **Go to IBM Cloud Console**
   - Visit: https://cloud.ibm.com/
   - Log in with your IBM Cloud account

2. **Navigate to watsonx.ai**
   - Click on the hamburger menu (☰) in the top left
   - Select "AI / Machine Learning"
   - Click on "watsonx.ai"

3. **Find or Create a Project**
   - If you already have a project, click on it
   - If not, click "Create project" and follow the wizard

4. **Get the Project ID**
   - Once in your project, click on the "Manage" tab
   - Look for "Project ID" or "General" section
   - Copy the Project ID (it looks like: `12345678-1234-1234-1234-123456789abc`)

5. **Add to .env File**
   - Open `backend/.env`
   - Replace `PLEASE_ADD_YOUR_PROJECT_ID_HERE` with your actual Project ID
   - Save the file

6. **Restart the Server**
   - The server should auto-reload when you save `.env`
   - Or manually restart: `python -m uvicorn app.main:app --reload --port 8000`

## Example .env Configuration:

```env
WATSONX_API_KEY=mvIw-HwLTQcSHjMEWbWguvj38rObX49amtmgufbfsRnJ
WATSONX_PROJECT_ID=12345678-1234-1234-1234-123456789abc  # Your actual Project ID
WATSONX_URL=https://us-south.ml.cloud.ibm.com
USE_MOCK_RESPONSES=false
```

## After Adding Project ID:

The server will automatically reload and start using the real IBM watsonx.ai API instead of mock responses.

You can then test with:
```bash
cd backend
python test_enhanced_analysis.py
```

Or test individual endpoints:
```bash
# Test AI health
curl http://localhost:8000/api/v1/ai/health

# Test code explanation
curl -X POST http://localhost:8000/api/v1/ai/explain \
  -H "Content-Type: application/json" \
  -d '{"code": "def hello(): print(\"Hello\")", "language": "python"}'