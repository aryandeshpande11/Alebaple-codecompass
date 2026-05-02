# Developer C: AI Integration & Enhanced Analysis - Detailed Instructions

## 🎯 Your Mission
Integrate AI explanations into the existing code analysis flow and create an enhanced analysis endpoint that combines code metrics with AI-generated insights.

---

## 📦 Prerequisites

1. **Pull Latest Code**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/stage4-ai-integration
   ```

2. **Dependencies**
   - Wait for Developer A to complete AI service
   - Wait for Developer B to complete API endpoints
   - You can start with mock AI responses initially

---

## 📝 Task 1: Create Enhanced Analysis Schemas

**File:** `backend/app/schemas/analysis_enhanced.py`

```python
"""
Enhanced analysis schemas with AI-generated insights.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class AIInsight(BaseModel):
    """AI-generated insight for code."""
    explanation: str = Field(..., description="AI explanation of the code")
    key_concepts: List[str] = Field(default_factory=list)
    complexity_note: Optional[str] = None
    suggestions: List[str] = Field(default_factory=list)


class FileWithAI(BaseModel):
    """File analysis with AI insights."""
    file_path: str
    language: str
    has_error: bool = False
    error: Optional[str] = None
    
    # Code structure
    structure: Dict[str, Any]
    
    # Metrics
    metrics: Dict[str, Any]
    
    # AI insights
    ai_summary: Optional[str] = None
    ai_explanation: Optional[AIInsight] = None
    important_functions: List[Dict[str, Any]] = Field(default_factory=list)


class ProjectAnalysisWithAI(BaseModel):
    """Complete project analysis with AI insights."""
    project_id: str
    status: str
    analysis_timestamp: str
    analysis_duration_seconds: float
    
    # Repository info
    repository_info: Optional[Dict[str, Any]] = None
    
    # Summary with AI
    summary: Dict[str, Any]
    ai_project_summary: Optional[str] = None
    ai_architecture_overview: Optional[str] = None
    
    # Files with AI insights
    files: List[FileWithAI]
    
    # Top files by importance (with AI explanations)
    important_files: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Dependencies
    dependencies: Dict[str, Any]
    
    # File structure
    file_structure: Dict[str, Any]
    
    # AI processing stats
    ai_stats: Optional[Dict[str, Any]] = None


class AnalyzeWithAIRequest(BaseModel):
    """Request to analyze project with AI insights."""
    include_ai_explanations: bool = Field(True, description="Include AI explanations")
    max_files_to_explain: int = Field(5, description="Maximum files to generate AI explanations for")
    prioritize_complex: bool = Field(True, description="Prioritize complex files for AI explanation")
```

**Action Items:**
- [ ] Create enhanced schemas
- [ ] Add proper type hints
- [ ] Test schema validation

---

## 📝 Task 2: Create AI Helper Utilities

**File:** `backend/app/utils/ai_helpers.py`

```python
"""
Helper utilities for AI integration with code analysis.
"""
from typing import List, Dict, Any, Tuple
import re


def extract_important_functions(file_analysis: Dict[str, Any], max_functions: int = 3) -> List[Dict[str, Any]]:
    """
    Extract the most important functions from a file based on complexity and size.
    
    Args:
        file_analysis: File analysis data
        max_functions: Maximum number of functions to extract
        
    Returns:
        List of important functions with their details
    """
    functions = file_analysis.get('structure', {}).get('functions', [])
    complexity_data = file_analysis.get('metrics', {}).get('complexity', [])
    
    # Create a map of function complexity
    complexity_map = {c['name']: c['complexity'] for c in complexity_data}
    
    # Score functions by complexity
    scored_functions = []
    for func in functions:
        name = func.get('name', '')
        complexity = complexity_map.get(name, 0)
        
        scored_functions.append({
            'name': name,
            'line_number': func.get('line_number', 0),
            'complexity': complexity,
            'score': complexity  # Can be enhanced with more factors
        })
    
    # Sort by score and return top N
    scored_functions.sort(key=lambda x: x['score'], reverse=True)
    return scored_functions[:max_functions]


def select_files_for_ai_explanation(
    files: List[Dict[str, Any]], 
    max_files: int = 5,
    prioritize_complex: bool = True
) -> List[Dict[str, Any]]:
    """
    Select the most important files for AI explanation.
    
    Args:
        files: List of file analysis data
        max_files: Maximum number of files to select
        prioritize_complex: Whether to prioritize complex files
        
    Returns:
        List of selected files
    """
    scored_files = []
    
    for file_data in files:
        if file_data.get('has_error'):
            continue
        
        metrics = file_data.get('metrics', {})
        raw_metrics = metrics.get('raw', {})
        complexity = metrics.get('complexity', [])
        
        # Calculate importance score
        loc = raw_metrics.get('loc', 0)
        num_classes = len(file_data.get('structure', {}).get('classes', []))
        num_functions = len(file_data.get('structure', {}).get('functions', []))
        avg_complexity = sum(c.get('complexity', 0) for c in complexity) / len(complexity) if complexity else 0
        
        # Scoring formula
        score = (
            loc * 0.3 +
            num_classes * 10 +
            num_functions * 5 +
            avg_complexity * 20
        )
        
        if prioritize_complex:
            score += avg_complexity * 30
        
        scored_files.append({
            'file_data': file_data,
            'score': score,
            'loc': loc,
            'complexity': avg_complexity
        })
    
    # Sort by score and return top N
    scored_files.sort(key=lambda x: x['score'], reverse=True)
    return [sf['file_data'] for sf in scored_files[:max_files]]


def extract_code_snippet(file_path: str, start_line: int, end_line: int) -> str:
    """
    Extract a code snippet from a file.
    
    Args:
        file_path: Path to the file
        start_line: Starting line number (1-based)
        end_line: Ending line number (1-based)
        
    Returns:
        Code snippet as string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Convert to 0-based indexing
        start_idx = max(0, start_line - 1)
        end_idx = min(len(lines), end_line)
        
        return ''.join(lines[start_idx:end_idx])
    except Exception:
        return ""


def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in text (rough approximation).
    
    Args:
        text: Text to estimate tokens for
        
    Returns:
        Estimated token count
    """
    # Rough estimation: ~4 characters per token
    return len(text) // 4


def truncate_code_for_ai(code: str, max_tokens: int = 2000) -> Tuple[str, bool]:
    """
    Truncate code to fit within token limit.
    
    Args:
        code: Code to truncate
        max_tokens: Maximum tokens allowed
        
    Returns:
        Tuple of (truncated_code, was_truncated)
    """
    estimated_tokens = estimate_tokens(code)
    
    if estimated_tokens <= max_tokens:
        return code, False
    
    # Truncate to approximate character count
    max_chars = max_tokens * 4
    truncated = code[:max_chars]
    
    # Try to truncate at a line boundary
    last_newline = truncated.rfind('\n')
    if last_newline > max_chars * 0.8:  # If we can keep 80% of content
        truncated = truncated[:last_newline]
    
    return truncated + "\n\n... (truncated)", True


def generate_project_summary_prompt(analysis_data: Dict[str, Any]) -> str:
    """
    Generate a prompt for AI to summarize the entire project.
    
    Args:
        analysis_data: Complete project analysis data
        
    Returns:
        Prompt string for AI
    """
    summary = analysis_data.get('summary', {})
    languages = summary.get('languages', {})
    
    prompt = f"""Analyze this software project and provide a comprehensive summary:

Project Statistics:
- Total Files: {summary.get('total_files', 0)}
- Languages: {', '.join(f"{lang} ({count} files)" for lang, count in languages.items())}
- Total Lines of Code: {summary.get('total_loc', 0)}
- Total Classes: {summary.get('total_classes', 0)}
- Total Functions: {summary.get('total_functions', 0)}
- Average Complexity: {summary.get('average_complexity', 0)}

Please provide:
1. Overall project purpose and architecture
2. Main components and their responsibilities
3. Code quality assessment
4. Potential areas for improvement
"""
    
    return prompt
```

**Action Items:**
- [ ] Create all helper functions
- [ ] Test with sample data
- [ ] Verify token estimation works

---

## 📝 Task 3: Create AI Integration Service

**File:** `backend/app/services/analysis_ai_integration.py`

```python
"""
Service for integrating AI insights with code analysis.
"""
from typing import Dict, Any, List, Optional
from app.utils.ai_helpers import (
    select_files_for_ai_explanation,
    extract_important_functions,
    generate_project_summary_prompt,
    truncate_code_for_ai
)

# TODO: Import AI service when Developer A completes it
# from app.services.ai_service import ai_service


class AnalysisAIIntegration:
    """Service for adding AI insights to code analysis."""
    
    def __init__(self):
        """Initialize the integration service."""
        self.max_code_tokens = 2000
    
    async def add_ai_insights(
        self,
        analysis_result: Dict[str, Any],
        max_files: int = 5,
        prioritize_complex: bool = True
    ) -> Dict[str, Any]:
        """
        Add AI-generated insights to analysis results.
        
        Args:
            analysis_result: Original analysis results
            max_files: Maximum files to generate AI explanations for
            prioritize_complex: Prioritize complex files
            
        Returns:
            Enhanced analysis with AI insights
        """
        if analysis_result.get('status') != 'completed':
            return analysis_result
        
        files = analysis_result.get('files', [])
        
        # Select important files for AI explanation
        selected_files = select_files_for_ai_explanation(
            files, 
            max_files=max_files,
            prioritize_complex=prioritize_complex
        )
        
        # Generate AI explanations for selected files
        ai_processed_files = []
        for file_data in files:
            if file_data in selected_files:
                # Add AI explanation
                enhanced_file = await self._add_file_ai_explanation(file_data)
                ai_processed_files.append(enhanced_file)
            else:
                # Keep original without AI
                ai_processed_files.append(file_data)
        
        # Generate project-level AI summary
        project_summary = await self._generate_project_summary(analysis_result)
        
        # Build enhanced result
        enhanced_result = {
            **analysis_result,
            'files': ai_processed_files,
            'ai_project_summary': project_summary,
            'important_files': [
                {
                    'file_path': f.get('file_path'),
                    'reason': 'High complexity and importance',
                    'has_ai_explanation': f in selected_files
                }
                for f in selected_files
            ],
            'ai_stats': {
                'files_with_ai': len(selected_files),
                'total_files': len(files),
                'ai_coverage_percent': round(len(selected_files) / len(files) * 100, 2) if files else 0
            }
        }
        
        return enhanced_result
    
    async def _add_file_ai_explanation(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add AI explanation to a single file."""
        file_path = file_data.get('file_path', '')
        language = file_data.get('language', 'unknown')
        
        # Extract important functions
        important_funcs = extract_important_functions(file_data, max_functions=3)
        
        # TODO: Replace with actual AI service call
        # For now, use mock response
        ai_explanation = {
            'explanation': f"This {language} file implements core functionality...",
            'key_concepts': ['classes', 'functions', 'data structures'],
            'complexity_note': 'Moderate complexity',
            'suggestions': ['Consider refactoring complex functions', 'Add more documentation']
        }
        
        ai_summary = f"Summary of {file_path}: Main implementation file with key business logic."
        
        return {
            **file_data,
            'ai_explanation': ai_explanation,
            'ai_summary': ai_summary,
            'important_functions': important_funcs
        }
    
    async def _generate_project_summary(self, analysis_result: Dict[str, Any]) -> str:
        """Generate AI summary for the entire project."""
        # TODO: Replace with actual AI service call
        summary = analysis_result.get('summary', {})
        
        mock_summary = f"""
This project contains {summary.get('total_files', 0)} files across multiple languages.
The codebase demonstrates good organization with {summary.get('total_classes', 0)} classes
and {summary.get('total_functions', 0)} functions. The average complexity is 
{summary.get('average_complexity', 0)}, indicating maintainable code.

Key architectural patterns and best practices are evident throughout the codebase.
        """.strip()
        
        return mock_summary


# Global instance
ai_integration = AnalysisAIIntegration()
```

**Action Items:**
- [ ] Create integration service
- [ ] Implement with mock responses
- [ ] Test with sample analysis data
- [ ] Prepare for real AI service integration

---

## 📝 Task 4: Create Enhanced Analysis Endpoint

**File:** `backend/app/api/v1/endpoints/analysis_enhanced.py`

```python
"""
Enhanced analysis endpoints with AI integration.
"""
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from datetime import datetime

from app.schemas.analysis_enhanced import (
    ProjectAnalysisWithAI,
    AnalyzeWithAIRequest
)
from app.utils.storage import storage
from app.services.code_analyzer import CodeAnalyzer
from app.services.analysis_ai_integration import ai_integration

router = APIRouter()
analyzer = CodeAnalyzer()


async def perform_analysis_with_ai(
    project_id: str,
    repo_url: str,
    max_files_to_explain: int,
    prioritize_complex: bool
):
    """Background task to perform analysis with AI insights."""
    try:
        # Run standard analysis
        analysis_result = analyzer.analyze_repository(repo_url, project_id)
        
        if analysis_result['status'] == 'completed':
            # Add AI insights
            enhanced_result = await ai_integration.add_ai_insights(
                analysis_result,
                max_files=max_files_to_explain,
                prioritize_complex=prioritize_complex
            )
            
            # Store enhanced results
            storage.create_analysis(project_id, enhanced_result)
            storage.update_project(project_id, {"status": "completed"})
        else:
            storage.create_analysis(project_id, analysis_result)
            storage.update_project(project_id, {"status": "failed"})
    
    except Exception as e:
        error_result = {
            "project_id": project_id,
            "status": "failed",
            "error": str(e),
            "analysis_timestamp": datetime.utcnow().isoformat(),
        }
        storage.create_analysis(project_id, error_result)
        storage.update_project(project_id, {"status": "failed"})


@router.post("/{project_id}/analyze-with-ai")
async def analyze_project_with_ai(
    project_id: str,
    request: AnalyzeWithAIRequest,
    background_tasks: BackgroundTasks
):
    """
    Trigger comprehensive code analysis with AI-generated insights.
    
    - **project_id**: Unique project identifier
    - **include_ai_explanations**: Whether to include AI explanations
    - **max_files_to_explain**: Maximum files to generate AI explanations for
    - **prioritize_complex**: Prioritize complex files for AI explanation
    
    This endpoint performs standard code analysis and enhances it with AI insights.
    Analysis runs in the background.
    """
    # Check if project exists
    project = storage.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID '{project_id}' not found"
        )
    
    # Check if project has a repository URL
    repo_url = project.get("repository_url")
    if not repo_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project does not have a repository URL"
        )
    
    # Update project status
    storage.update_project(project_id, {"status": "analyzing"})
    
    # Start analysis with AI in background
    background_tasks.add_task(
        perform_analysis_with_ai,
        project_id,
        repo_url,
        request.max_files_to_explain,
        request.prioritize_complex
    )
    
    return {
        "message": "Analysis with AI insights started",
        "project_id": project_id,
        "status": "analyzing",
        "ai_enabled": request.include_ai_explanations
    }


@router.get("/{project_id}/analysis-with-ai")
async def get_analysis_with_ai(project_id: str):
    """
    Get enhanced analysis results with AI insights.
    
    - **project_id**: Unique project identifier
    
    Returns comprehensive analysis including AI-generated explanations and summaries.
    """
    # Check if project exists
    project = storage.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID '{project_id}' not found"
        )
    
    # Get analysis results
    analysis = storage.get_analysis(project_id)
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No analysis found for project '{project_id}'. Run analysis first."
        )
    
    return analysis
```

**Action Items:**
- [ ] Create enhanced endpoint
- [ ] Implement background task processing
- [ ] Test with mock AI responses
- [ ] Verify integration with existing analysis

---

## 📝 Task 5: Update API Router

Add the enhanced analysis router to `backend/app/api/v1/__init__.py`:

```python
from .endpoints import projects, analysis, analysis_enhanced

api_router.include_router(
    analysis_enhanced.router,
    prefix="/projects",
    tags=["analysis-ai"]
)
```

**Action Items:**
- [ ] Add enhanced analysis router
- [ ] Verify routes don't conflict
- [ ] Check API docs

---

## 🧪 Testing Checklist

### Test Schemas
```bash
cd backend
python -c "from app.schemas.analysis_enhanced import *; print('Schemas OK')"
```

### Test Helpers
```bash
python -c "from app.utils.ai_helpers import *; print('Helpers OK')"
```

### Test Integration Service
```bash
python -c "from app.services.analysis_ai_integration import ai_integration; print('Integration OK')"
```

### Test Enhanced Endpoint
```bash
# Create a project first, then:
curl -X POST "http://localhost:8000/api/v1/projects/{project_id}/analyze-with-ai" \
  -H "Content-Type: application/json" \
  -d '{"include_ai_explanations": true, "max_files_to_explain": 3}'
```

---

## ✅ Definition of Done

- [ ] Enhanced schemas created
- [ ] AI helper utilities implemented
- [ ] Integration service created with mock responses
- [ ] Enhanced analysis endpoint functional
- [ ] Background task processing works
- [ ] API router updated
- [ ] All tests passing
- [ ] Code committed to feature branch
- [ ] Ready for integration with real AI service

---

## 🤝 Integration Steps

### With Developer A (AI Service)
1. Import AI service when ready
2. Replace mock AI calls with real service calls
3. Test end-to-end functionality

### With Developer B (API Endpoints)
1. Coordinate on response formats
2. Ensure caching works with integration
3. Test combined functionality

---

## 📞 Need Help?

- Check STAGE_4_WORK_ASSIGNMENTS.md for context
- Coordinate with other developers in team chat
- Review existing analysis code in `backend/app/services/code_analyzer.py`

**Good luck! 🚀**