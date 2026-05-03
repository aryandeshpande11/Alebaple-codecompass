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
  BreadcrumbItem,
  Tile
} from '@carbon/react'
import {
  ArrowLeft,
  Renew,
  Download,
  DocumentExport
} from '@carbon/icons-react'
import Dashboard from '../components/Dashboard'
import CodeViewer from '../components/CodeViewer'
import ExplanationPanel from '../components/ExplanationPanel'
import FileTree from '../components/FileTree'
import LoadingState from '../components/LoadingState'
import DependencyGraph from '../components/DependencyGraph'
import { projectAPI, analysisAPI, aiAPI } from '../services/api'
import { exportAsMarkdown, exportAsJSON, exportAsHTML, printReport } from '../utils/exportUtils'
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

      // Check if file has content
      if (!file.content || file.content.trim() === '' || file.content.startsWith('// Error reading file')) {
        setAiError('File content is not available or could not be read from the repository.')
        setAiLoading(false)
        return
      }

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
      
      // Handle different error formats
      let errorMessage = 'Failed to get AI explanation'
      
      if (err.response?.data) {
        const data = err.response.data
        
        // Handle validation errors (array of error objects)
        if (Array.isArray(data.detail)) {
          errorMessage = data.detail.map(e => e.msg || JSON.stringify(e)).join(', ')
        }
        // Handle string detail
        else if (typeof data.detail === 'string') {
          errorMessage = data.detail
        }
        // Handle object detail
        else if (typeof data.detail === 'object') {
          errorMessage = JSON.stringify(data.detail)
        }
      } else if (err.message) {
        errorMessage = err.message
      }
      
      setAiError(errorMessage)
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
        <LoadingState
          type="fullpage"
          message="Loading project data..."
          description="Please wait while we fetch your analysis results"
        />
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
                {project?.github_url && (
                  <p className="project-url">{project.github_url}</p>
                )}
              </div>
              <div className="header-actions">
                <Button
                  kind="ghost"
                  size="sm"
                  renderIcon={Download}
                  onClick={() => exportAsMarkdown(project, analysis)}
                  disabled={!analysis}
                  hasIconOnly
                  iconDescription="Export as Markdown"
                  tooltipPosition="bottom"
                />
                <Button
                  kind="ghost"
                  size="sm"
                  renderIcon={DocumentExport}
                  onClick={() => exportAsHTML(project, analysis)}
                  disabled={!analysis}
                  hasIconOnly
                  iconDescription="Export as HTML"
                  tooltipPosition="bottom"
                />
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
                  <Tab>Dependencies</Tab>
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
                          <h4 className="section-subtitle">File Explorer</h4>
                          <FileTree
                            files={analysis.files || []}
                            onFileSelect={(file) => handleFileSelect({
                              ...file,
                              path: file.file_path || file.path,
                              lines: file.metrics?.raw?.loc || file.lines || 0
                            })}
                            selectedFile={selectedFile}
                          />
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

                  {/* Dependencies Tab */}
                  <TabPanel>
                    <Grid>
                      <Column lg={16} md={8} sm={4}>
                        <DependencyGraph files={analysis.files || []} />
                      </Column>
                    </Grid>
                  </TabPanel>

                  {/* AI Insights Tab */}
                  <TabPanel>
                    <Grid>
                      <Column lg={16} md={8} sm={4}>
                        {!selectedFile && (
                          <div className="ai-prompt">
                            <Tile className="prompt-tile">
                              <h4>Get AI-Powered Code Insights</h4>
                              <p>Select a file from the Code Explorer tab to get detailed AI analysis including:</p>
                              <ul>
                                <li>Comprehensive code explanation</li>
                                <li>Complexity metrics and visualizations</li>
                                <li>Best practices recommendations</li>
                                <li>Potential improvements</li>
                              </ul>
                            </Tile>
                          </div>
                        )}
                        {selectedFile && (
                          <ExplanationPanel
                            explanation={explanation}
                            loading={aiLoading}
                            error={aiError}
                            onRefresh={() => selectedFile && handleExplainRequest(selectedFile)}
                          />
                        )}
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