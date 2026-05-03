import { useState, useEffect } from 'react'
import Editor from '@monaco-editor/react'
import { 
  Tile, 
  Button,
  InlineLoading 
} from '@carbon/react'
import { Ai } from '@carbon/icons-react'
import './CodeViewer.css'

function CodeViewer({ file, onExplainRequest, theme }) {
  const [editorTheme, setEditorTheme] = useState('vs-light')

  useEffect(() => {
    setEditorTheme(theme === 'white' ? 'vs-light' : 'vs-dark')
  }, [theme])

  if (!file) {
    return (
      <div className="code-viewer-container">
        <Tile className="code-viewer-empty">
          <p>Select a file to view its contents</p>
        </Tile>
      </div>
    )
  }

  const getLanguage = (filePath) => {
    if (!filePath || typeof filePath !== 'string') {
      return 'plaintext'
    }
    const ext = filePath.split('.').pop().toLowerCase()
    const languageMap = {
      'py': 'python',
      'js': 'javascript',
      'jsx': 'javascript',
      'ts': 'typescript',
      'tsx': 'typescript',
      'java': 'java',
      'json': 'json',
      'md': 'markdown',
      'html': 'html',
      'css': 'css',
      'yml': 'yaml',
      'yaml': 'yaml',
    }
    return languageMap[ext] || 'plaintext'
  }

  return (
    <div className="code-viewer-container">
      <div className="code-viewer-header">
        <h4 className="file-path">{file.path}</h4>
        <div className="code-viewer-actions">
          {onExplainRequest && (
            <Button
              kind="tertiary"
              size="sm"
              renderIcon={Ai}
              onClick={() => onExplainRequest(file)}
            >
              Explain with AI
            </Button>
          )}
        </div>
      </div>

      <div className="code-viewer-editor">
        <Editor
          height="600px"
          language={getLanguage(file.path)}
          value={file.content || '// No content available'}
          theme={editorTheme}
          options={{
            readOnly: true,
            minimap: { enabled: true },
            fontSize: 14,
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            automaticLayout: true,
            wordWrap: 'on',
          }}
          loading={<InlineLoading description="Loading code..." />}
        />
      </div>

      {file.analysis && (
        <div className="code-viewer-info">
          <Tile>
            <h5>File Statistics</h5>
            <div className="file-stats">
              <div className="stat-item">
                <span className="stat-label">Lines:</span>
                <span className="stat-value">{file.analysis.lines || 0}</span>
              </div>
              {file.analysis.functions && (
                <div className="stat-item">
                  <span className="stat-label">Functions:</span>
                  <span className="stat-value">{file.analysis.functions.length || 0}</span>
                </div>
              )}
              {file.analysis.classes && (
                <div className="stat-item">
                  <span className="stat-label">Classes:</span>
                  <span className="stat-value">{file.analysis.classes.length || 0}</span>
                </div>
              )}
            </div>
          </Tile>
        </div>
      )}
    </div>
  )
}

export default CodeViewer

// Made with Bob - Enterprise Edition
