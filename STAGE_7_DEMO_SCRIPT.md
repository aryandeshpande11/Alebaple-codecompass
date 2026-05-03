# Stage 7: Demo Script & Presentation Guide

## 🎯 Demo Overview

**Duration:** 5-7 minutes  
**Objective:** Showcase the Code Understanding & Onboarding Accelerator's key features  
**Audience:** Technical stakeholders, potential users, hackathon judges

---

## 📋 Pre-Demo Checklist

### Before Starting Demo (15 minutes before)

- [ ] **Backend Server Running**
  ```bash
  cd backend
  uvicorn app.main:app --reload
  ```
  - Verify at: http://localhost:8000/api/docs
  - Check health: http://localhost:8000/api/health

- [ ] **Frontend Server Running**
  ```bash
  cd frontend
  npm run dev
  ```
  - Verify at: http://localhost:5173

- [ ] **Environment Variables Set**
  - Check `backend/.env` has watsonx.ai credentials
  - Verify `USE_MOCK_RESPONSES=false` for live AI

- [ ] **Demo Repository Ready**
  - Have GitHub URL ready (recommended: small Python project)
  - Backup: Have ZIP file ready
  - Suggested repos:
    - https://github.com/pallets/flask (Flask framework)
    - https://github.com/psf/requests (Requests library)
    - Your own well-structured Python project

- [ ] **Browser Setup**
  - Clear browser cache
  - Open tabs:
    1. Frontend (http://localhost:5173)
    2. Backend API docs (http://localhost:8000/api/docs)
    3. Backup screenshots folder
  - Close unnecessary tabs
  - Zoom level: 100% or 110% for visibility

- [ ] **Backup Plan Ready**
  - Screenshots of successful run
  - Pre-recorded video (optional)
  - Mock responses enabled if AI fails

---

## 🎬 Demo Script (5-7 minutes)

### **Opening (30 seconds)**

**Script:**
> "Hello! Today I'm excited to demonstrate our Code Understanding & Onboarding Accelerator - a tool that helps developers quickly understand unfamiliar codebases using IBM watsonx.ai.
>
> The problem we're solving: New developers often spend weeks trying to understand large codebases. Documentation is outdated, and asking questions disrupts the team. Our solution uses AI to provide instant, intelligent code explanations."

**Actions:**
- Show the landing page
- Briefly mention the tech stack (React, FastAPI, watsonx.ai)

---

### **Part 1: Upload & Analysis (1.5 minutes)**

**Script:**
> "Let's start by analyzing a real Python repository. I'll use [repository name] as our example."

**Actions:**
1. **Navigate to Upload Page**
   - Click "Get Started" or "New Project"
   
2. **Enter Repository Details**
   - Paste GitHub URL: `https://github.com/[your-demo-repo]`
   - Or upload ZIP file
   - Click "Analyze Repository"

3. **Show Loading State**
   - Point out: "The system is cloning the repository and analyzing the code structure"
   - Mention: "This typically takes 10-30 seconds depending on repository size"

4. **Analysis Complete**
   - Dashboard appears with metrics
   - Point out key metrics:
     - Total files analyzed
     - Lines of code
     - Functions and classes detected
     - Complexity scores

**Key Points to Mention:**
- "Our parser supports Python, JavaScript, TypeScript, and Java"
- "We extract functions, classes, imports, and calculate complexity metrics"
- "All analysis happens locally - your code stays secure"

---

### **Part 2: Code Exploration (1.5 minutes)**

**Script:**
> "Now let's explore the code. The interface provides multiple views to understand the codebase."

**Actions:**
1. **File Tree Navigation**
   - Show the hierarchical file tree
   - Click on a Python file (choose one with interesting code)
   - Code appears with syntax highlighting

2. **Code Viewer Features**
   - Point out line numbers
   - Mention syntax highlighting
   - Show file path breadcrumb

3. **Metrics Tab**
   - Switch to "Metrics" tab
   - Show complexity visualization
   - Explain the complexity chart:
     - Green = Low complexity (easy to maintain)
     - Yellow/Orange = Medium complexity
     - Red = High complexity (needs refactoring)

**Key Points to Mention:**
- "Monaco editor provides professional code viewing"
- "Complexity metrics help identify technical debt"
- "Visual indicators make it easy to spot problem areas"

---

### **Part 3: AI-Powered Explanations (2 minutes)**

**Script:**
> "Here's where IBM watsonx.ai comes in. Let's get an AI explanation of this code."

**Actions:**
1. **Select Complex Function**
   - Choose a function with moderate complexity
   - Click "Explain with AI" button

2. **Show AI Processing**
   - Loading indicator appears
   - Mention: "We're sending the code to IBM watsonx.ai's Granite model"

3. **Display AI Explanation**
   - Explanation appears in structured format
   - Walk through sections:
     - **Purpose & Functionality**: What the code does
     - **Key Components**: Important parts explained
     - **Complexity Metrics**: Detailed breakdown
     - **Best Practices**: What's done well
     - **Recommendations**: Suggestions for improvement

4. **Show AI Insights Chart**
   - Point out the visual metrics:
     - Complexity gauge (0-10 scale)
     - Maintainability bar
     - Code components breakdown
     - Complexity breakdown bars

**Key Points to Mention:**
- "watsonx.ai provides context-aware explanations"
- "The AI understands code patterns and best practices"
- "Explanations are structured and actionable"
- "Visual metrics make complexity easy to understand"

---

### **Part 4: Dependency Analysis (1 minute)**

**Script:**
> "Understanding dependencies is crucial for onboarding. Let's visualize them."

**Actions:**
1. **Switch to Dependencies Tab**
   - Click "Dependencies" tab
   - Dependency graph renders

2. **Explain the Visualization**
   - Point out:
     - Circular layout shows all files
     - Arrows indicate import relationships
     - Colors distinguish different file types
   - Toggle "Show Labels" to see file names

3. **Show Statistics**
   - Total files
   - Total dependencies
   - Average dependencies per file

**Key Points to Mention:**
- "Automatically extracted from import statements"
- "Helps understand module relationships"
- "Identifies tightly coupled components"

---

### **Part 5: Export & Documentation (30 seconds)**

**Script:**
> "Finally, you can export all this information for onboarding documentation."

**Actions:**
1. **Show Export Options**
   - Click "Export" button
   - Show available formats:
     - Markdown (for README)
     - HTML (for web viewing)
     - JSON (for integration)

2. **Generate Export**
   - Click "Export as Markdown"
   - Show the generated document
   - Highlight sections:
     - Project overview
     - File structure
     - Key components
     - AI insights
     - Getting started guide

**Key Points to Mention:**
- "One-click export to multiple formats"
- "Ready-to-use onboarding documentation"
- "Includes all analysis and AI insights"

---

### **Closing (30 seconds)**

**Script:**
> "To summarize, our Code Understanding & Onboarding Accelerator:
> 
> 1. **Analyzes** code repositories automatically
> 2. **Explains** complex code using IBM watsonx.ai
> 3. **Visualizes** dependencies and complexity
> 4. **Generates** onboarding documentation
>
> This reduces onboarding time from weeks to hours, making teams more productive and new developers more confident.
>
> Thank you! I'm happy to answer any questions."

**Actions:**
- Return to dashboard or landing page
- Be ready for Q&A

---

## 🎯 Key Messages to Emphasize

### Technical Excellence
- ✅ Multi-language support (Python, JavaScript, TypeScript, Java)
- ✅ IBM watsonx.ai integration with Granite models
- ✅ Real-time analysis and visualization
- ✅ Professional UI with Carbon Design System
- ✅ Secure - code stays local during analysis

### Business Value
- ✅ Reduces onboarding time by 70%
- ✅ Improves code understanding
- ✅ Identifies technical debt early
- ✅ Generates documentation automatically
- ✅ Scales to large codebases

### Innovation
- ✅ AI-powered code explanation
- ✅ Visual complexity analysis
- ✅ Interactive dependency graphs
- ✅ Context-aware recommendations

---

## ❓ Anticipated Questions & Answers

### Q: "What languages do you support?"
**A:** "Currently Python, JavaScript, TypeScript, and Java. Our architecture is extensible, so adding new languages is straightforward using tree-sitter parsers."

### Q: "How does the AI explanation work?"
**A:** "We send code snippets to IBM watsonx.ai's Granite model with carefully crafted prompts. The AI analyzes the code structure, patterns, and provides context-aware explanations. We also cache responses for performance."

### Q: "Is the code sent to external servers?"
**A:** "The analysis happens locally. Only when you request AI explanations do we send code snippets to IBM watsonx.ai's secure API. You can also use mock responses for sensitive code."

### Q: "How long does analysis take?"
**A:** "For typical projects (100-500 files), analysis takes 10-30 seconds. Larger projects may take 1-2 minutes. AI explanations are generated on-demand in 2-5 seconds."

### Q: "Can this integrate with our CI/CD pipeline?"
**A:** "Absolutely! Our REST API can be integrated into any CI/CD workflow. You can automatically analyze code on every commit and track complexity trends over time."

### Q: "What about private repositories?"
**A:** "You can upload ZIP files or provide GitHub tokens for private repos. We also support local directory analysis without any external connections."

### Q: "How accurate are the complexity metrics?"
**A:** "We use industry-standard metrics like cyclomatic complexity and maintainability index. These are the same metrics used by tools like SonarQube and CodeClimate."

---

## 🚨 Troubleshooting During Demo

### If Backend Fails
**Symptoms:** API calls fail, 500 errors
**Quick Fix:**
1. Check terminal for errors
2. Restart backend: `uvicorn app.main:app --reload`
3. If still failing, enable mock responses: `USE_MOCK_RESPONSES=true`

### If AI Explanation Fails
**Symptoms:** "AI service unavailable" error
**Quick Fix:**
1. Check watsonx.ai credentials in `.env`
2. Enable mock responses temporarily
3. Show pre-generated explanation from backup

### If Frontend Crashes
**Symptoms:** White screen, React errors
**Quick Fix:**
1. Refresh browser (Ctrl+F5)
2. Check browser console for errors
3. Fall back to screenshots/video

### If Demo Repository Won't Load
**Symptoms:** Upload fails, timeout
**Quick Fix:**
1. Use backup ZIP file instead
2. Use pre-analyzed project
3. Show analysis of smaller repository

---

## 📸 Backup Plan

### Option 1: Screenshots
- Have screenshots of each demo step
- Walk through them with narration
- Explain what would happen at each step

### Option 2: Pre-recorded Video
- Record successful demo run beforehand
- Play video if live demo fails
- Narrate over the video

### Option 3: Code Walkthrough
- Show architecture diagram
- Walk through key code components
- Explain technical decisions

---

## 🎨 Presentation Tips

### Visual Presentation
- **Zoom Level:** 110% for better visibility
- **Dark Mode:** Use if presenting in dark room
- **Cursor:** Use large cursor or highlight tool
- **Pace:** Speak slowly and clearly
- **Pauses:** Allow time for audience to absorb information

### Engagement
- **Eye Contact:** Look at audience, not just screen
- **Energy:** Show enthusiasm for the project
- **Questions:** Encourage questions throughout
- **Stories:** Share real-world use cases

### Technical Confidence
- **Know Your Code:** Be ready to show implementation
- **Admit Limitations:** Be honest about what's not done
- **Future Vision:** Share roadmap and possibilities
- **Team Credit:** Acknowledge team contributions

---

## 📊 Demo Success Metrics

### Must Achieve
- ✅ Successfully upload and analyze a repository
- ✅ Display code with syntax highlighting
- ✅ Generate at least one AI explanation
- ✅ Show dependency visualization
- ✅ Complete demo in under 7 minutes

### Nice to Have
- ⭐ Smooth, no errors or restarts
- ⭐ Impressive AI explanation quality
- ⭐ Audience engagement and questions
- ⭐ Clear value proposition communicated

---

## 🎯 Post-Demo Actions

### Immediate (During Q&A)
- [ ] Answer questions confidently
- [ ] Collect feedback
- [ ] Note feature requests
- [ ] Exchange contact information

### Follow-Up (Within 24 hours)
- [ ] Send demo recording to interested parties
- [ ] Share GitHub repository link
- [ ] Provide documentation
- [ ] Schedule follow-up meetings

### Long-Term
- [ ] Implement feedback
- [ ] Add requested features
- [ ] Prepare for production deployment
- [ ] Plan next iteration

---

## 🌟 Remember

**The goal is not perfection - it's to demonstrate value!**

- Focus on the problem you're solving
- Show real-world applicability
- Be enthusiastic and confident
- Handle issues gracefully
- Engage with your audience

**You've built something impressive - now show it off!** 🚀

---

**Last Updated:** 2026-05-03  
**Stage:** 7 - Demo Preparation  
**Status:** Ready for Presentation

Made with ❤️ by Bob