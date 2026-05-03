import { useState } from 'react'
import { 
  Form, 
  TextInput, 
  Button, 
  InlineLoading,
  InlineNotification
} from '@carbon/react'
import { Upload } from '@carbon/icons-react'
import { projectAPI, analysisAPI } from '../services/api'
import './UploadForm.css'

function UploadForm({ onAnalysisStart }) {
  const [githubUrl, setGithubUrl] = useState('')
  const [projectName, setProjectName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      // Create project
      const project = await projectAPI.create({
        name: projectName || 'Untitled Project',
        repository_url: githubUrl,
        description: `Analysis of ${githubUrl}`,
      })

      console.log('Project created:', project)

      // Trigger analysis
      await analysisAPI.analyze(project.id)
      
      console.log('Analysis started for project:', project.id)

      // Notify parent component
      if (onAnalysisStart) {
        onAnalysisStart(project.id)
      }

    } catch (err) {
      console.error('Error:', err)
      setError(err.response?.data?.detail || err.message || 'Failed to analyze repository')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="upload-form-container">
      <Form onSubmit={handleSubmit}>
        <div className="form-group">
          <TextInput
            id="project-name"
            labelText="Project Name (Optional)"
            placeholder="My Awesome Project"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <TextInput
            id="github-url"
            labelText="GitHub Repository URL"
            placeholder="https://github.com/username/repository"
            value={githubUrl}
            onChange={(e) => setGithubUrl(e.target.value)}
            required
            disabled={loading}
            helperText="Enter a public GitHub repository URL"
          />
        </div>

        {error && (
          <div className="form-group">
            <InlineNotification
              kind="error"
              title="Error"
              subtitle={error}
              onCloseButtonClick={() => setError(null)}
              lowContrast
            />
          </div>
        )}

        <div className="form-actions">
          {loading ? (
            <InlineLoading description="Analyzing repository..." />
          ) : (
            <Button
              type="submit"
              renderIcon={Upload}
              disabled={!githubUrl}
            >
              Analyze Repository
            </Button>
          )}
        </div>
      </Form>
    </div>
  )
}

export default UploadForm

// Made with Bob
