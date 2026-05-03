import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { 
  Grid, 
  Column,
  Tabs,
  TabList,
  Tab,
  TabPanels,
  TabPanel,
  Button,
  InlineLoading,
  InlineNotification,
  Breadcrumb,
  BreadcrumbItem
} from '@carbon/react'
import { 
  ArrowLeft,
  Renew,
  Download
} from '@carbon/icons-react'
import Dashboard from '../components/Dashboard'
import CodeViewer from '../components/CodeViewer'
import ExplanationPanel from '../components/ExplanationPanel'
import { projectAPI, analysisAPI, aiAPI } from '../services/api'
import './AnalysisPage.css'

function AnalysisPage() {
  const { projectId } = useParams()
  const navigate = useNavigate()

  const [project, setProject] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [selectedFile, setSelectedFile] = useState(null)
  const [explanation, setExplanation] = useState(null)
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)
  const [error, setError] = useState(null)
  const [aiLoading, setAiLoading] = useState(false)
  const [aiError, setAiError] = useState(null)

  // Fetch project and analysis data
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)

        // Fetch project details
        const projectData = await projectAPI.getById(projectId)
        setProject(projectData)

        // Try to fetch analysis results
        try {
          const analysisData = await analysisAPI.getResults(projectId)
          setAnalysis(analysisData)
        } catch (err) {
          // Analysis might not be ready yet
          console.log('Analysis not ready, will retry...')
          setAnalyzing(true)
        }
      } catch (err) {
        console.error('Error fetching data:', err)
        setError(err.response?.data?.detail || err.message || 'Failed to load project')
      } finally {
        setLoading(false)
      }
    }

    if (projectId) {
      fetchData()
    }
  }, [projectId])

  // Poll for analysis results if analyzing
  useEffect(() => {
    if (!analyzing) return

    const pollInterval = setInterval(async () => {
      try {
        const analysisData = await analysisAPI.getResults(projectId)
        setAnalysis(analysisData)
        setAnalyzing(false)
      } catch (err) {
        // Still analyzing, continue polling
        console.log('Still analyzing...')
      }
    }, 3000) // Poll every 3 seconds

    return () => clearInterval(pollInterval)
  }, [analyzing, projectId])

  // Handle file selection
  const handleFileSelect = async (file) => {
    setSelectedFile(file)
    setExplanation(null)
    setAiError(null)
  }

  // Handle AI explanation request
  const handleExplainRequest = async (file) => {
    try {
      setAiLoading(true)
      setAiError(null)

      const response = await aiAPI.explainFile(
        file.path,
        file.content,
        file.language || 'python'
      )

      setExplanation({
        summary: response.summary,
        explanation: response.explanation,
        key_points: response.key_points || [],
        complexity: response.complexity,
        suggestions: response.suggestions || [],
        dependencies: response.dependencies || [],
        generated_at: new Date().toISOString()
      })
    } catch (err) {
      console.error('Error getting AI explanation:', err)
      setAiError(err.response?.data?.detail || err.message || 'Failed to get AI explanation')
    } finally {
      setAiLoading(false)
    }
  }

  // Handle refresh
  const handleRefresh = async () => {
    setAnalyzing(true)
    try {
      await analysisAPI.analyze(projectId)
    } catch (err) {
      console.error('Error triggering analysis:', err)
    }
  }

  if (loading) {
    return (
      <div className="analysis-page">
        <div className="loading-container">
          <InlineLoading description="Loading project data..." />
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="analysis-page">
        <div className="error-container">
          <InlineNotification
            kind="error"
            title="Error"
            subtitle={error}
            lowContrast
          />
          <Button
            kind="tertiary"
            renderIcon={ArrowLeft}
            onClick={() => navigate('/')}
          >
            Back to Home
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="analysis-page">
      {/* Page Header */}
      <div className="page-header">
        <Grid>
          <Column lg={16} md={8} sm={4}>
            <Breadcrumb noTrailingSlash>
              <BreadcrumbItem href="/">Home</BreadcrumbItem>
              <BreadcrumbItem href="#" isCurrentPage>
                {project?.name || 'Analysis'}
              </BreadcrumbItem>
            </Breadcrumb>

            <div className="header-content">
              <div className="header-info">
                <h1 className="page-title">{project?.name || 'Project Analysis'}</h1>
                {project?.repository_url && (
                  <p className="project-url">{project.repository_url}</p>
                )}
              </div>
              <div className="header-actions">
                <Button
                  kind="tertiary"
                  size="sm"
                  renderIcon={Renew}
                  onClick={handleRefresh}
                  disabled={analyzing}
                >
                  Refresh
                </Button>
                <Button
                  kind="tertiary"
                  size="sm"
                  renderIcon={ArrowLeft}
                  onClick={() => navigate('/')}
                >
                  Back
                </Button>
              </div>
            </div>
          </Column>
        </Grid>
      </div>

      {/* Analysis Status */}
      {analyzing && (
        <div className="analysis-status">
          <Grid>
            <Column lg={16} md={8} sm={4}>
              <InlineNotification
                kind="info"
                title="Analysis in Progress"
                subtitle="Your code is being analyzed. This may take a few moments..."
                lowContrast
                hideCloseButton
              />
            </Column>
          </Grid>
        </div>
      )}

      {/* Main Content */}
      {analysis && (
        <div className="page-content">
          <Grid>
            <Column lg={16} md={8} sm={4}>
              <Tabs>
                <TabList aria-label="Analysis tabs">
                  <Tab>Overview</Tab>
                  <Tab>Code Explorer</Tab>
                  <Tab>AI Insights</Tab>
                </TabList>
                <TabPanels>
                  {/* Overview Tab */}
                  <TabPanel>
                    <Dashboard analysis={analysis} loading={false} />
                  </TabPanel>

                  {/* Code Explorer Tab */}
                  <TabPanel>
                    <Grid className="code-explorer-grid">
                      <Column lg={6} md={4} sm={4}>
                        <div className="file-list-container">
                          <h4 className="section-subtitle">Files</h4>
                          <div className="file-list">
                            {analysis.files && analysis.files.map((file, index) => (
                              <button
                                key={index}
                                className={`file-item ${selectedFile?.path === file.path ? 'active' : ''}`}
                                onClick={() => handleFileSelect(file)}
                              >
                                <span className="file-name">{file.path}</span>
                                <span className="file-lines">{file.lines} lines</span>
                              </button>
                            ))}
                          </div>
                        </div>
                      </Column>
                      <Column lg={10} md={4} sm={4}>
                        <CodeViewer
                          file={selectedFile}
                          onExplainRequest={handleExplainRequest}
                          theme="white"
                        />
                      </Column>
                    </Grid>
                  </TabPanel>

                  {/* AI Insights Tab */}
                  <TabPanel>
                    <Grid>
                      <Column lg={16} md={8} sm={4}>
                        <ExplanationPanel
                          explanation={explanation}
                          loading={aiLoading}
                          error={aiError}
                          onRefresh={() => selectedFile && handleExplainRequest(selectedFile)}
                        />
                      </Column>
                    </Grid>
                  </TabPanel>
                </TabPanels>
              </Tabs>
            </Column>
          </Grid>
        </div>
      )}
    </div>
  )
}

export default AnalysisPage

// Made with Bob - Enterprise Edition