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
import './ExplanationPanel.css'

function ExplanationPanel({ explanation, loading, onRefresh, error }) {
  const [expanded, setExpanded] = useState(true)

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

  return (
    <div className="explanation-panel">
      <Tile className="explanation-tile">
        <div className="explanation-header">
          <div className="explanation-title">
            <Ai size={24} className="ai-icon" />
            <h4>AI Analysis</h4>
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
          {explanation.summary && (
            <div className="explanation-section">
              <h5 className="section-title">Summary</h5>
              <p className="section-text">{explanation.summary}</p>
            </div>
          )}

          {explanation.explanation && (
            <div className="explanation-section">
              <h5 className="section-title">Detailed Explanation</h5>
              <p className="section-text">{explanation.explanation}</p>
            </div>
          )}

          {explanation.key_points && explanation.key_points.length > 0 && (
            <div className="explanation-section">
              <h5 className="section-title">Key Points</h5>
              <ul className="key-points-list">
                {explanation.key_points.map((point, index) => (
                  <li key={index} className="key-point-item">
                    <CheckmarkFilled size={16} className="check-icon" />
                    <span>{point}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {explanation.complexity && (
            <div className="explanation-section">
              <h5 className="section-title">Complexity Analysis</h5>
              <div className="complexity-info">
                {typeof explanation.complexity === 'object' && explanation.complexity.level ? (
                  <>
                    <Tag type={
                      explanation.complexity.level === 'low' ? 'green' :
                      explanation.complexity.level === 'medium' ? 'blue' : 'red'
                    }>
                      {explanation.complexity.level.toUpperCase()}
                    </Tag>
                    <p className="section-text">{explanation.complexity.description || ''}</p>
                  </>
                ) : (
                  <p className="section-text">{String(explanation.complexity)}</p>
                )}
              </div>
            </div>
          )}

          {explanation.suggestions && explanation.suggestions.length > 0 && (
            <div className="explanation-section">
              <Accordion>
                <AccordionItem title="Improvement Suggestions">
                  <ul className="suggestions-list">
                    {explanation.suggestions.map((suggestion, index) => (
                      <li key={index} className="suggestion-item">
                        {suggestion}
                      </li>
                    ))}
                  </ul>
                </AccordionItem>
              </Accordion>
            </div>
          )}

          {explanation.dependencies && explanation.dependencies.length > 0 && (
            <div className="explanation-section">
              <h5 className="section-title">Dependencies</h5>
              <div className="dependencies-tags">
                {explanation.dependencies.map((dep, index) => (
                  <Tag key={index} type="cool-gray" size="sm">
                    {dep}
                  </Tag>
                ))}
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