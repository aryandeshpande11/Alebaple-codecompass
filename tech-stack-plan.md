# Code Understanding and Onboarding Accelerator - Tech Stack Plan

## Project Overview
A proof of concept to analyze Python code repositories, help users understand code structure and interactions, and generate onboarding materials using IBM watsonx.ai and watsonx Orchestrate.

---

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph Frontend
        A[React UI] --> B[Code Viewer]
        A --> C[Analysis Dashboard]
        A --> D[Onboarding Portal]
    end
    
    subgraph Backend
        E[FastAPI Server] --> F[Code Parser]
        E --> G[Analysis Engine]
        E --> H[API Gateway]
    end
    
    subgraph AI Layer
        I[watsonx.ai SDK] --> J[Granite Models]
        K[watsonx Orchestrate] --> L[Workflow Automation]
    end
    
    subgraph Storage
        M[PostgreSQL] --> N[Metadata & Users]
        O[IBM Cloud Object Storage] --> P[Code Repos & Artifacts]
        Q[Redis] --> R[Cache & Sessions]
    end
    
    A --> E
    E --> I
    E --> K
    E --> M
    E --> O
    E --> Q
```

---

## 📦 Technology Stack

### **1. Frontend Layer**

**Primary Framework: React 18+**
- **Reasoning**: Modern, component-based, excellent ecosystem, team expertise
- **State Management**: Zustand or Redux Toolkit
  - Zustand for simpler state needs (recommended for PoC)
  - Redux Toolkit if complex state management needed
- **UI Component Library**: Material-UI (MUI) or IBM Carbon Design System
  - **Recommended**: IBM Carbon Design System for IBM ecosystem consistency
- **Code Display**: Monaco Editor (VS Code's editor)
  - Syntax highlighting, code navigation, diff viewing
- **Visualization**: D3.js or Mermaid.js
  - Component dependency graphs, architecture diagrams
- **API Client**: Axios or React Query
  - React Query recommended for caching and state synchronization

**Key Dependencies**:
```json
{
  "react": "^18.2.0",
  "@carbon/react": "^1.x",
  "@monaco-editor/react": "^4.x",
  "react-query": "^3.x",
  "mermaid": "^10.x",
  "axios": "^1.x"
}
```

---

### **2. Backend Layer**

**Primary Framework: FastAPI (Python 3.10+)**
- **Reasoning**: 
  - Fast, modern, async support
  - Automatic API documentation (OpenAPI/Swagger)
  - Type hints and validation with Pydantic
  - Excellent for AI/ML integration

**Core Components**:

1. **API Server**: FastAPI
   - RESTful endpoints
   - WebSocket support for real-time updates
   - Automatic request/response validation

2. **Code Analysis Engine**:
   - **AST Parser**: Python's built-in `ast` module
   - **Static Analysis**: `pylint`, `radon` (complexity metrics)
   - **Dependency Analysis**: `pipreqs`, `modulegraph`
   - **Documentation Extraction**: `pydoc`, custom parsers

3. **Task Queue**: Celery with Redis
   - Async processing for large repository analysis
   - Background job management

**Key Dependencies**:
```python
fastapi==0.104.0
uvicorn[standard]==0.24.0
pydantic==2.4.0
celery==5.3.0
redis==5.0.0
sqlalchemy==2.0.0
alembic==1.12.0
python-multipart==0.0.6
```

---

### **3. AI/LLM Integration Layer**

**IBM watsonx.ai Integration**

**Primary SDK**: `ibm-watsonx-ai` Python SDK
- **Reasoning**: Official IBM SDK, optimized for watsonx.ai services

**Use Cases & Models**:

1. **Code Explanation** (Granite-13B-Chat or Granite-20B-Code)
   - Generate natural language explanations of code blocks
   - Explain complex algorithms and logic flows

2. **Architecture Analysis** (Granite-13B-Chat)
   - Identify design patterns
   - Suggest architectural improvements
   - Generate component interaction descriptions

3. **Onboarding Content Generation** (Granite-13B-Chat)
   - Create learning paths
   - Generate documentation
   - Produce onboarding checklists

4. **Code Summarization** (Granite-20B-Code)
   - Function/class summaries
   - Module-level overviews

**Implementation Pattern**:
```python
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# Initialize model
model = Model(
    model_id="ibm/granite-13b-chat-v2",
    credentials={...},
    project_id="your-project-id"
)

# Generate explanations
response = model.generate_text(
    prompt=f"Explain this Python code:\n{code_snippet}",
    params={
        GenParams.MAX_NEW_TOKENS: 500,
        GenParams.TEMPERATURE: 0.7
    }
)
```

**watsonx Orchestrate Integration**

**Purpose**: Automate onboarding workflows and task management

**Use Cases**:
1. **Automated Onboarding Workflows**
   - Trigger learning module assignments
   - Schedule code review sessions
   - Track onboarding progress

2. **Task Automation**
   - Generate and assign documentation tasks
   - Create JIRA/GitHub issues for code improvements
   - Send notifications and reminders

**Integration Approach**:
- REST API integration via watsonx Orchestrate APIs
- Webhook-based event triggers
- Skill flows for multi-step processes

---

### **4. Data Storage Solutions**

**Multi-Database Strategy**:

1. **PostgreSQL 15+ (Primary Database)**
   - **Use Cases**:
     - User accounts and authentication
     - Project metadata
     - Analysis results and metrics
     - Onboarding progress tracking
   - **Reasoning**: ACID compliance, complex queries, JSON support
   - **Hosting**: IBM Cloud Databases for PostgreSQL

2. **IBM Cloud Object Storage (File Storage)**
   - **Use Cases**:
     - Cloned repository storage
     - Generated documentation artifacts
     - Code snapshots and versions
     - Large analysis reports
   - **Reasoning**: Scalable, cost-effective, IBM ecosystem integration

3. **Redis 7+ (Caching & Sessions)**
   - **Use Cases**:
     - API response caching
     - Session management
     - Celery task queue backend
     - Rate limiting
   - **Reasoning**: Fast in-memory operations, pub/sub support
   - **Hosting**: IBM Cloud Databases for Redis

**Data Models (Key Entities)**:
- Users (authentication, roles)
- Projects (repository metadata)
- AnalysisResults (code metrics, insights)
- OnboardingPlans (checklists, learning paths)
- CodeComponents (functions, classes, modules)
- Dependencies (component relationships)

---

### **5. Code Analysis Strategy**

**Python Repository Analysis Pipeline**:

1. **Repository Ingestion**
   - Git clone via `GitPython` library
   - Support for GitHub, GitLab, Bitbucket
   - Branch and commit selection

2. **Static Analysis**
   - **AST Parsing**: Extract functions, classes, imports
   - **Complexity Metrics**: Cyclomatic complexity (radon)
   - **Code Quality**: Linting scores (pylint)
   - **Documentation Coverage**: Docstring analysis

3. **Dependency Mapping**
   - Import graph generation
   - External package identification
   - Internal module relationships

4. **AI-Powered Analysis**
   - Send code snippets to watsonx.ai
   - Generate explanations and summaries
   - Identify critical logic paths

5. **Knowledge Graph Construction**
   - Build component relationship graph
   - Identify entry points and core modules
   - Map data flow patterns

**Tools & Libraries**:
```python
GitPython==3.1.40
ast (built-in)
radon==6.0.1
pylint==3.0.0
networkx==3.2  # For dependency graphs
```

---

### **6. API Architecture**

**RESTful API Design**:

**Core Endpoints**:

```
POST   /api/v1/projects                    # Create new project
GET    /api/v1/projects/{id}               # Get project details
POST   /api/v1/projects/{id}/analyze       # Trigger analysis
GET    /api/v1/projects/{id}/analysis      # Get analysis results

GET    /api/v1/components/{id}             # Get component details
GET    /api/v1/components/{id}/explain     # AI explanation
GET    /api/v1/components/{id}/dependencies # Dependency graph

POST   /api/v1/onboarding/generate         # Generate onboarding plan
GET    /api/v1/onboarding/{id}             # Get onboarding plan
PUT    /api/v1/onboarding/{id}/progress    # Update progress

GET    /api/v1/search                      # Search codebase
GET    /api/v1/metrics                     # Get code metrics
```

**WebSocket Endpoints**:
```
WS     /ws/analysis/{project_id}           # Real-time analysis updates
```

**API Documentation**: Auto-generated via FastAPI (Swagger UI)

---

### **7. Authentication & Security**

**Authentication Strategy**:
- **JWT (JSON Web Tokens)** for stateless authentication
- **IBM App ID** integration (optional, for enterprise SSO)
- **OAuth 2.0** support for GitHub/GitLab integration

**Security Measures**:
- HTTPS/TLS encryption (enforced)
- API rate limiting (via Redis)
- Input validation (Pydantic models)
- SQL injection prevention (SQLAlchemy ORM)
- CORS configuration
- Secrets management via IBM Cloud Secrets Manager

**Libraries**:
```python
python-jose[cryptography]==3.3.0  # JWT
passlib[bcrypt]==1.7.4            # Password hashing
python-multipart==0.0.6           # File uploads
```

---

### **8. Deployment Strategy (IBM Cloud)**

**Infrastructure Components**:

1. **Compute**:
   - **IBM Cloud Code Engine** (recommended for PoC)
     - Serverless container platform
     - Auto-scaling
     - Pay-per-use
   - Alternative: IBM Cloud Kubernetes Service (for production)

2. **Databases**:
   - IBM Cloud Databases for PostgreSQL
   - IBM Cloud Databases for Redis

3. **Storage**:
   - IBM Cloud Object Storage

4. **AI Services**:
   - watsonx.ai (hosted service)
   - watsonx Orchestrate (hosted service)

5. **CI/CD**:
   - IBM Cloud Continuous Delivery
   - GitHub Actions (alternative)

**Deployment Architecture**:
```
Frontend (React) → IBM Cloud Code Engine (Static hosting)
Backend (FastAPI) → IBM Cloud Code Engine (Container)
Celery Workers → IBM Cloud Code Engine (Background jobs)
Databases → IBM Cloud Databases (Managed)
```

**Environment Configuration**:
- Development: Local Docker Compose
- Staging: IBM Cloud Code Engine (single instance)
- Production: IBM Cloud Code Engine (auto-scaled)

---

### **9. Development Environment Setup**

**Prerequisites**:
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- Git

**Local Development Stack**:
```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: code_accelerator
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    ports:
      - "5432:5432"
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
```

**Environment Variables**:
```bash
# Backend (.env)
DATABASE_URL=postgresql://dev:dev@localhost:5432/code_accelerator
REDIS_URL=redis://localhost:6379
WATSONX_API_KEY=your_api_key
WATSONX_PROJECT_ID=your_project_id
IBM_CLOUD_API_KEY=your_cloud_api_key
JWT_SECRET=your_secret_key
```

---

## 🎯 Implementation Phases

### **Phase 1: Foundation (Week 1-2)**
- Set up project structure
- Configure development environment
- Implement basic authentication
- Create database schema

### **Phase 2: Code Analysis (Week 3-4)**
- Build repository ingestion
- Implement AST parsing
- Create dependency mapping
- Develop metrics calculation

### **Phase 3: AI Integration (Week 5-6)**
- Integrate watsonx.ai SDK
- Implement code explanation features
- Build architecture analysis
- Create summarization pipeline

### **Phase 4: Frontend & Visualization (Week 7-8)**
- Build React UI components
- Implement code viewer
- Create dependency visualizations
- Develop analysis dashboard

### **Phase 5: Onboarding Features (Week 9-10)**
- Integrate watsonx Orchestrate
- Build onboarding plan generator
- Create progress tracking
- Implement workflow automation

### **Phase 6: Testing & Deployment (Week 11-12)**
- End-to-end testing
- Performance optimization
- IBM Cloud deployment
- Documentation and handoff

---

## 📊 Key Success Metrics

1. **Analysis Speed**: < 5 minutes for medium-sized repos (10K LOC)
2. **AI Response Time**: < 3 seconds for code explanations
3. **Accuracy**: 85%+ accuracy in dependency mapping
4. **User Satisfaction**: Onboarding time reduced by 40%

---

## 🔧 Alternative Considerations

**If Requirements Change**:

1. **Multi-language Support**: Add Tree-sitter for universal parsing
2. **On-Premises**: Replace IBM Cloud with self-hosted Kubernetes
3. **Different Frontend**: Vue.js or Angular (similar architecture)
4. **Different Backend**: Node.js with Express (requires more AI integration work)

---

## 📚 Key Resources

- [IBM watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [IBM Carbon Design System](https://carbondesignsystem.com/)
- [IBM Cloud Code Engine](https://cloud.ibm.com/docs/codeengine)

---

## ✅ Tech Stack Summary

| Layer | Technology | Reasoning |
|-------|-----------|-----------|
| **Frontend** | React 18 + Carbon Design | Modern UI, IBM ecosystem fit |
| **Backend** | FastAPI (Python 3.10+) | Fast, async, great for AI/ML |
| **AI/LLM** | watsonx.ai (Granite models) | Required, powerful code understanding |
| **Workflow** | watsonx Orchestrate | Required, automation capabilities |
| **Database** | PostgreSQL 15 | Robust, ACID, complex queries |
| **Cache** | Redis 7 | Fast, session management |
| **Storage** | IBM Cloud Object Storage | Scalable, cost-effective |
| **Deployment** | IBM Cloud Code Engine | Serverless, auto-scaling |
| **Code Analysis** | AST + radon + pylint | Python-native, comprehensive |
| **Task Queue** | Celery + Redis | Async processing, reliable |

---

**This tech stack is optimized for**:
✅ Python repository analysis
✅ IBM Cloud deployment
✅ Rapid PoC development
✅ Scalability to production
✅ Team expertise (React + Python)
✅ IBM watsonx integration