# Stage 4: AI Integration - Work Assignments

**Duration:** Hour 5-7  
**Team Size:** 3 Developers (Developer A, Developer B, Developer C)  
**Strategy:** Parallel development with separate files to avoid merge conflicts

---

## 🎯 Stage 4 Overview

Integrate IBM watsonx.ai for code explanation and documentation generation across multiple programming languages (Python, Java, JavaScript, TypeScript).

---

## 👨‍💻 Developer A: AI Service Core & watsonx.ai Integration

### Responsibilities
Build the core AI service layer and integrate with IBM watsonx.ai SDK.

### Tasks
1. **Install watsonx.ai SDK**
   ```bash
   cd backend
   pip install ibm-watsonx-ai ibm-cloud-sdk-core
   ```

2. **Create AI Configuration** (`backend/app/core/ai_config.py`)
   - watsonx.ai API credentials management
   - Model configuration (granite-13b-chat-v2 or similar)
   - Token limits and retry logic
   - Environment variable loading

3. **Create AI Service** (`backend/app/services/ai_service.py`)
   - Initialize watsonx.ai client
   - `explain_code(code: str, language: str) -> str` - Explain code snippet
   - `summarize_file(file_content: str, language: str) -> str` - Summarize file
   - `generate_documentation(code: str, language: str) -> str` - Generate docs
   - Error handling and fallbacks
   - Response caching mechanism

4. **Create Prompt Templates** (`backend/app/services/prompt_templates.py`)
   - Code explanation prompts for each language
   - Documentation generation prompts
   - Summary generation prompts
   - Context-aware prompt building

### Files to Create
- `backend/app/core/ai_config.py`
- `backend/app/services/ai_service.py`
- `backend/app/services/prompt_templates.py`
- `backend/.env.example` (add watsonx.ai credentials template)

### Testing
- Test watsonx.ai connection
- Test code explanation with sample Python code
- Test multi-language support
- Verify response caching

### Estimated Time: 2-3 hours

---

## 👨‍💻 Developer B: API Endpoints & Response Caching

### Responsibilities
Create API endpoints for AI features and implement caching system.

### Tasks
1. **Create AI Endpoints** (`backend/app/api/v1/endpoints/ai.py`)
   - `POST /api/v1/ai/explain` - Explain code snippet
   - `POST /api/v1/ai/explain-file` - Explain entire file
   - `POST /api/v1/ai/summarize` - Summarize module/class
   - `POST /api/v1/ai/document` - Generate documentation
   - Request validation with Pydantic schemas

2. **Create AI Schemas** (`backend/app/schemas/ai.py`)
   - `ExplainRequest` - Code explanation request
   - `ExplainResponse` - Code explanation response
   - `SummaryRequest` - Summary request
   - `SummaryResponse` - Summary response
   - `DocumentationRequest` - Documentation request
   - `DocumentationResponse` - Documentation response

3. **Implement Caching** (`backend/app/utils/cache.py`)
   - Simple file-based cache for AI responses
   - Cache key generation (hash of code + language + prompt type)
   - Cache expiration (24 hours)
   - Cache statistics

4. **Update API Router** (`backend/app/api/v1/__init__.py`)
   - Include AI router
   - Update API documentation

### Files to Create
- `backend/app/api/v1/endpoints/ai.py`
- `backend/app/schemas/ai.py`
- `backend/app/utils/cache.py`
- `backend/data/cache/` (directory for cache files)

### Testing
- Test all AI endpoints with curl/Postman
- Verify request validation
- Test caching mechanism
- Check API documentation

### Estimated Time: 2-3 hours

---

## 👨‍💻 Developer C: Integration & Enhanced Analysis

### Responsibilities
Integrate AI explanations into existing analysis flow and enhance project analysis.

### Tasks
1. **Enhance Analysis Endpoint** (`backend/app/api/v1/endpoints/analysis_enhanced.py`)
   - Create new endpoint: `POST /api/v1/projects/{id}/analyze-with-ai`
   - Trigger code analysis + AI explanations
   - Generate AI summaries for key files
   - Background task processing

2. **Create AI Integration Service** (`backend/app/services/analysis_ai_integration.py`)
   - `add_ai_explanations(analysis_result: dict) -> dict` - Add AI to analysis
   - Select important files for AI explanation
   - Batch process AI requests
   - Merge AI results with code analysis

3. **Update Analysis Schema** (`backend/app/schemas/analysis_enhanced.py`)
   - Add AI explanation fields to analysis response
   - `FileWithAI` - File analysis + AI explanation
   - `ProjectAnalysisWithAI` - Complete analysis with AI insights

4. **Create AI Utilities** (`backend/app/utils/ai_helpers.py`)
   - Code snippet extraction
   - Important function detection
   - Complexity-based prioritization
   - Token counting and optimization

### Files to Create
- `backend/app/api/v1/endpoints/analysis_enhanced.py`
- `backend/app/services/analysis_ai_integration.py`
- `backend/app/schemas/analysis_enhanced.py`
- `backend/app/utils/ai_helpers.py`

### Testing
- Test enhanced analysis endpoint
- Verify AI integration with code analysis
- Test with multi-language projects
- Check performance with large codebases

### Estimated Time: 2-3 hours

---

## 📋 Coordination Points

### Before Starting
1. All developers pull latest code from Stage 3
2. Create individual feature branches:
   - `feature/stage4-ai-core` (Developer A)
   - `feature/stage4-ai-endpoints` (Developer B)
   - `feature/stage4-ai-integration` (Developer C)

### During Development
- **Communication:** Use team chat for questions
- **Dependencies:** Developer B and C depend on Developer A's AI service
- **Mock Data:** Developer B and C can use mock AI responses initially

### Integration Meeting (After 2 hours)
1. Developer A demonstrates AI service working
2. Developer B shows API endpoints
3. Developer C shows integration approach
4. Resolve any interface mismatches

### Final Integration
1. Developer A merges first (core AI service)
2. Developer B merges second (API endpoints)
3. Developer C merges last (integration)
4. Team testing session
5. Update PROGRESS.md together

---

## 🔑 Shared Interfaces

### AI Service Interface (Developer A provides)
```python
class AIService:
    def explain_code(self, code: str, language: str) -> str:
        """Explain code snippet"""
        pass
    
    def summarize_file(self, file_content: str, language: str) -> str:
        """Summarize file"""
        pass
    
    def generate_documentation(self, code: str, language: str) -> str:
        """Generate documentation"""
        pass
```

### Expected Response Format
```python
{
    "explanation": "This code does...",
    "key_concepts": ["concept1", "concept2"],
    "complexity_note": "This is moderately complex",
    "suggestions": ["suggestion1", "suggestion2"]
}
```

---

## 📝 Environment Setup

All developers need to add to `.env`:
```bash
# IBM watsonx.ai Configuration
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-13b-chat-v2
```

---

## ✅ Definition of Done

### Developer A
- [ ] AI service connects to watsonx.ai successfully
- [ ] Code explanation works for all supported languages
- [ ] Prompt templates are comprehensive
- [ ] Caching mechanism implemented
- [ ] Unit tests written

### Developer B
- [ ] All AI endpoints functional
- [ ] Request/response validation working
- [ ] API documentation updated
- [ ] Cache system operational
- [ ] Integration tests written

### Developer C
- [ ] Enhanced analysis endpoint working
- [ ] AI integrated with code analysis
- [ ] Performance acceptable for large projects
- [ ] End-to-end tests written
- [ ] Documentation updated

---

## 🚀 Success Criteria

- [ ] watsonx.ai integration working
- [ ] Code explanations generated for Python, Java, JS, TS
- [ ] API endpoints responding correctly
- [ ] Caching reduces API calls
- [ ] Enhanced analysis includes AI insights
- [ ] No merge conflicts during integration
- [ ] All tests passing
- [ ] Server running without errors

---

**Next Stage:** Stage 5 - Frontend Foundation (React + Carbon Design System)