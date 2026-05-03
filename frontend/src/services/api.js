import axios from 'axios'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 60000, // 60 seconds for analysis operations
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// Project APIs
export const projectAPI = {
  // Create a new project
  create: async (data) => {
    const response = await api.post('/projects', data)
    return response.data
  },

  // Get all projects
  getAll: async () => {
    const response = await api.get('/projects')
    return response.data
  },

  // Get project by ID
  getById: async (id) => {
    const response = await api.get(`/projects/${id}`)
    return response.data
  },

  // Update project
  update: async (id, data) => {
    const response = await api.put(`/projects/${id}`, data)
    return response.data
  },

  // Delete project
  delete: async (id) => {
    const response = await api.delete(`/projects/${id}`)
    return response.data
  },
}

// Analysis APIs
export const analysisAPI = {
  // Trigger code analysis
  analyze: async (projectId) => {
    const response = await api.post(`/projects/${projectId}/analyze`)
    return response.data
  },

  // Get analysis results
  getResults: async (projectId) => {
    const response = await api.get(`/projects/${projectId}/analysis`)
    return response.data
  },

  // Get file analysis
  getFileAnalysis: async (projectId, filePath) => {
    const response = await api.get(`/projects/${projectId}/files/${encodeURIComponent(filePath)}`)
    return response.data
  },

  // Trigger AI-enhanced analysis
  analyzeWithAI: async (projectId, options = {}) => {
    const response = await api.post(`/projects/${projectId}/analyze-with-ai`, options)
    return response.data
  },

  // Get AI-enhanced analysis results
  getAIResults: async (projectId) => {
    const response = await api.get(`/projects/${projectId}/analysis-with-ai`)
    return response.data
  },
}

// AI APIs
export const aiAPI = {
  // Explain code snippet
  explainCode: async (code, language, context = '') => {
    const response = await api.post('/ai/explain', {
      code,
      language,
      context,
    })
    return response.data
  },

  // Explain entire file
  explainFile: async (filePath, code, language) => {
    // Normalize language to match backend validation
    const normalizedLanguage = language?.toLowerCase() || 'python'
    const validLanguages = ['python', 'java', 'javascript', 'typescript']
    const finalLanguage = validLanguages.includes(normalizedLanguage) ? normalizedLanguage : 'python'
    
    const response = await api.post('/ai/explain-file', {
      file_path: filePath,
      file_content: code,  // Backend expects 'file_content', not 'code'
      language: finalLanguage,
    })
    return response.data
  },

  // Summarize code
  summarize: async (code, language, summaryType = 'module') => {
    const response = await api.post('/ai/summarize', {
      code,
      language,
      summary_type: summaryType,
    })
    return response.data
  },

  // Generate documentation
  generateDocs: async (code, language, docType = 'function') => {
    const response = await api.post('/ai/document', {
      code,
      language,
      doc_type: docType,
    })
    return response.data
  },

  // Get AI service health
  getHealth: async () => {
    const response = await api.get('/ai/health')
    return response.data
  },

  // Get cache statistics
  getCacheStats: async () => {
    const response = await api.get('/ai/cache/stats')
    return response.data
  },

  // Clear cache
  clearCache: async () => {
    const response = await api.delete('/ai/cache/clear')
    return response.data
  },
}

// Health check
export const healthCheck = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    console.error('Health check failed:', error)
    return { status: 'error', message: error.message }
  }
}

export default api

// Made with Bob
