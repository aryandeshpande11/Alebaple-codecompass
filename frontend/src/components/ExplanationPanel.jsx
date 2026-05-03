import { useState } from 'react'
import {
  Tile,
  Button,
  SkeletonText,
  Tag,
  Accordion,
  AccordionItem
} from '@carbon/react'
import {
  Ai,
  Renew,
  CheckmarkFilled,
  WarningFilled
} from '@carbon/icons-react'
import AIInsightsChart from './AIInsightsChart'
import './ExplanationPanel.css'

function ExplanationPanel({ explanation, loading, onRefresh, error }) {
  const [expanded, setExpanded] = useState(true)

  // Parse markdown-style explanation text
  const parseExplanation = (text) => {
    if (!text) return { sections: [] }
    
    const sections = []
    const lines = text.split('\n')
    let currentSection = null
    
    for (const line of lines) {
      // Check for headers
      if (line.startsWith('###')) {
        if (currentSection) sections.push(currentSection)
        currentSection = {
          title: line.replace(/^###\s*/, '').replace(/[📊🎯🔍📈🔄✅⚠️📚🤖]/g, '').trim(),
          content: [],
          type: 'section'
        }
      } else if (line.startsWith('##')) {
        if (currentSection) sections.push(currentSection)
        currentSection = {
          title: line.replace(/^##\s*/, '').replace(/[📊🎯🔍📈🔄✅⚠️📚🤖]/g, '').trim(),
          content: [],
          type: 'header'
        }
      } else if (currentSection && line.trim()) {
        currentSection.content.push(line)
      }
    }
    
    if (currentSection) sections.push(currentSection)
    return { sections }
  }

  if (loading) {
    return (
      <div className="explanation-panel">
        <Tile className="explanation-tile">
          <div className="explanation-header">
            <div className="explanation-title">
              <Ai size={24} className="ai-icon" />
              <h4>AI Analysis</h4>
            </div>
            <Tag type="blue" size="sm">Processing...</Tag>
          </div>
          <div className="explanation-content">
            <SkeletonText paragraph lineCount={4} />
          </div>
        </Tile>
      </div>
    )
  }

  if (error) {
    return (
      <div className="explanation-panel">
        <Tile className="explanation-tile error">
          <div className="explanation-header">
            <div className="explanation-title">
              <WarningFilled size={24} className="error-icon" />
              <h4>Analysis Error</h4>
            </div>
            <Tag type="red" size="sm">Failed</Tag>
          </div>
          <div className="explanation-content">
            <p className="error-message">{error}</p>
            {onRefresh && (
              <Button
                kind="tertiary"
                size="sm"
                renderIcon={Renew}
                onClick={onRefresh}
              >
                Retry Analysis
              </Button>
            )}
          </div>
        </Tile>
      </div>
    )
  }

  if (!explanation) {
    return (
      <div className="explanation-panel">
        <Tile className="explanation-tile empty">
          <div className="explanation-header">
            <div className="explanation-title">
              <Ai size={24} className="ai-icon" />
              <h4>AI Insights</h4>
            </div>
          </div>
          <div className="explanation-content">
            <p className="empty-message">
              Select a code snippet or file to get AI-powered explanations and insights.
            </p>
          </div>
        </Tile>
      </div>
    )
  }

  const parsedExplanation = explanation?.explanation ? parseExplanation(explanation.explanation) : null

  return (
    <div className="explanation-panel">
      {/* AI Insights Charts */}
      {explanation && (
        <AIInsightsChart explanation={explanation} />
      )}

      {/* Main Explanation Content */}
      <Tile className="explanation-tile">
        <div className="explanation-header">
          <div className="explanation-title">
            <Ai size={24} className="ai-icon" />
            <h4>AI Analysis Report</h4>
          </div>
          <div className="explanation-actions">
            <Tag type="green" size="sm" renderIcon={CheckmarkFilled}>
              Complete
            </Tag>
            {onRefresh && (
              <Button
                kind="ghost"
                size="sm"
                renderIcon={Renew}
                onClick={onRefresh}
                iconDescription="Refresh analysis"
                hasIconOnly
              />
            )}
          </div>
        </div>

        <div className="explanation-content">
          {/* Render parsed sections */}
          {parsedExplanation && parsedExplanation.sections.map((section, index) => (
            <div key={index} className="explanation-section">
              <h5 className="section-title">{section.title}</h5>
              <div className="section-content">
                {section.content.map((line, lineIndex) => {
                  // Handle bullet points
                  if (line.trim().startsWith('-') || line.trim().startsWith('•')) {
                    return (
                      <div key={lineIndex} className="bullet-item">
                        <CheckmarkFilled size={16} className="bullet-icon" />
                        <span>{line.replace(/^[-•]\s*/, '').replace(/\*\*/g, '')}</span>
                      </div>
                    )
                  }
                  // Handle numbered lists
                  if (/^\d+\./.test(line.trim())) {
                    return (
                      <div key={lineIndex} className="numbered-item">
                        <span className="number">{line.match(/^\d+/)[0]}</span>
                        <span>{line.replace(/^\d+\.\s*/, '').replace(/\*\*/g, '')}</span>
                      </div>
                    )
                  }
                  // Handle bold text
                  if (line.includes('**')) {
                    const parts = line.split('**')
                    return (
                      <p key={lineIndex} className="section-text">
                        {parts.map((part, i) =>
                          i % 2 === 1 ? <strong key={i}>{part}</strong> : part
                        )}
                      </p>
                    )
                  }
                  // Regular text
                  if (line.trim()) {
                    return <p key={lineIndex} className="section-text">{line}</p>
                  }
                  return null
                })}
              </div>
            </div>
          ))}

          {/* Fallback for old format */}
          {!parsedExplanation && explanation.summary && (
            <div className="explanation-section">
              <h5 className="section-title">Summary</h5>
              <p className="section-text">{explanation.summary}</p>
            </div>
          )}

          {!parsedExplanation && explanation.explanation && (
            <div className="explanation-section">
              <h5 className="section-title">Detailed Explanation</h5>
              <div className="section-text" style={{ whiteSpace: 'pre-wrap' }}>
                {explanation.explanation}
              </div>
            </div>
          )}
        </div>

        {explanation.generated_at && (
          <div className="explanation-footer">
            <p className="timestamp">
              Generated: {new Date(explanation.generated_at).toLocaleString()}
            </p>
          </div>
        )}
      </Tile>
    </div>
  )
}

export default ExplanationPanel

// Made with Bob - Enterprise Edition