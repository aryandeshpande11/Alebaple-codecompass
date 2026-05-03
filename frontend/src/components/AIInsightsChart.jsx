import { useMemo } from 'react'
import { Tile, Tag } from '@carbon/react'
import {
  CheckmarkFilled,
  WarningFilled,
  Code,
  Renew,
  FlowData,
  DecisionTree
} from '@carbon/icons-react'
import './AIInsightsChart.css'

function AIInsightsChart({ explanation }) {
  // Parse complexity metrics from explanation text
  const metrics = useMemo(() => {
    if (!explanation || !explanation.explanation) return null

    const text = explanation.explanation
    
    // Extract complexity score
    const scoreMatch = text.match(/Complexity Score[:\s]+(\d+)\/10/)
    const complexityScore = scoreMatch ? parseInt(scoreMatch[1]) : 5
    
    // Extract complexity level
    const levelMatch = text.match(/Complexity Level[:\s]+(\w+)/)
    const complexityLevel = levelMatch ? levelMatch[1] : 'Medium'
    
    // Extract maintainability
    const maintainMatch = text.match(/Maintainability[:\s]+(\w+(?:\s+\w+)?)/)
    const maintainability = maintainMatch ? maintainMatch[1] : 'Good'
    
    // Extract component presence
    const hasClasses = text.includes('Classes: Yes') || text.includes('Object-Oriented')
    const hasFunctions = text.includes('Functions: Yes') || text.includes('function definitions')
    const hasLoops = text.includes('Loops: Yes') || text.includes('Iterative Processing')
    const hasConditionals = text.includes('Conditionals: Yes') || text.includes('Conditional Logic')
    
    return {
      complexityScore,
      complexityLevel,
      maintainability,
      components: {
        classes: hasClasses,
        functions: hasFunctions,
        loops: hasLoops,
        conditionals: hasConditionals
      }
    }
  }, [explanation])

  if (!metrics) return null

  const getComplexityColor = (level) => {
    switch (level.toLowerCase()) {
      case 'low': return '#24a148'
      case 'medium': return '#0f62fe'
      case 'high': return '#ff832b'
      case 'very high': return '#da1e28'
      default: return '#0f62fe'
    }
  }

  const getMaintainabilityColor = (level) => {
    if (level.includes('Excellent')) return '#24a148'
    if (level.includes('Good')) return '#0f62fe'
    if (level.includes('Moderate')) return '#ff832b'
    return '#da1e28'
  }

  const complexityPercentage = (metrics.complexityScore / 10) * 100

  return (
    <div className="ai-insights-chart">
      {/* Complexity Score Gauge */}
      <Tile className="chart-tile">
        <h5 className="chart-title">Complexity Analysis</h5>
        <div className="complexity-gauge">
          <div className="gauge-container">
            <svg viewBox="0 0 200 120" className="gauge-svg">
              {/* Background arc */}
              <path
                d="M 20 100 A 80 80 0 0 1 180 100"
                fill="none"
                stroke="#e0e0e0"
                strokeWidth="20"
                strokeLinecap="round"
              />
              {/* Colored arc */}
              <path
                d="M 20 100 A 80 80 0 0 1 180 100"
                fill="none"
                stroke={getComplexityColor(metrics.complexityLevel)}
                strokeWidth="20"
                strokeLinecap="round"
                strokeDasharray={`${complexityPercentage * 2.51} 251`}
                className="gauge-fill"
              />
              {/* Center text */}
              <text x="100" y="85" textAnchor="middle" className="gauge-score">
                {metrics.complexityScore}
              </text>
              <text x="100" y="105" textAnchor="middle" className="gauge-label">
                / 10
              </text>
            </svg>
          </div>
          <div className="gauge-info">
            <Tag type={
              metrics.complexityLevel === 'Low' ? 'green' :
              metrics.complexityLevel === 'Medium' ? 'blue' :
              metrics.complexityLevel === 'High' ? 'orange' : 'red'
            } size="md">
              {metrics.complexityLevel} Complexity
            </Tag>
          </div>
        </div>
      </Tile>

      {/* Maintainability Score */}
      <Tile className="chart-tile">
        <h5 className="chart-title">Maintainability</h5>
        <div className="maintainability-bar">
          <div className="bar-container">
            <div 
              className="bar-fill"
              style={{
                width: `${
                  metrics.maintainability.includes('Excellent') ? 90 :
                  metrics.maintainability.includes('Good') ? 70 :
                  metrics.maintainability.includes('Moderate') ? 50 : 30
                }%`,
                backgroundColor: getMaintainabilityColor(metrics.maintainability)
              }}
            />
          </div>
          <div className="bar-label">
            <span className="label-text">{metrics.maintainability}</span>
            {metrics.maintainability.includes('Excellent') && (
              <CheckmarkFilled size={20} className="icon-success" />
            )}
            {metrics.maintainability.includes('Needs') && (
              <WarningFilled size={20} className="icon-warning" />
            )}
          </div>
        </div>
      </Tile>

      {/* Code Components */}
      <Tile className="chart-tile components-tile">
        <h5 className="chart-title">Code Components</h5>
        <div className="components-grid">
          <div className={`component-item ${metrics.components.classes ? 'active' : 'inactive'}`}>
            <Code size={24} />
            <span>Classes</span>
            {metrics.components.classes ? (
              <CheckmarkFilled size={16} className="check-icon" />
            ) : (
              <span className="x-icon">✗</span>
            )}
          </div>
          <div className={`component-item ${metrics.components.functions ? 'active' : 'inactive'}`}>
            <Code size={24} />
            <span>Functions</span>
            {metrics.components.functions ? (
              <CheckmarkFilled size={16} className="check-icon" />
            ) : (
              <span className="x-icon">✗</span>
            )}
          </div>
          <div className={`component-item ${metrics.components.loops ? 'active' : 'inactive'}`}>
            <Renew size={24} />
            <span>Loops</span>
            {metrics.components.loops ? (
              <CheckmarkFilled size={16} className="check-icon" />
            ) : (
              <span className="x-icon">✗</span>
            )}
          </div>
          <div className={`component-item ${metrics.components.conditionals ? 'active' : 'inactive'}`}>
            <DecisionTree size={24} />
            <span>Conditionals</span>
            {metrics.components.conditionals ? (
              <CheckmarkFilled size={16} className="check-icon" />
            ) : (
              <span className="x-icon">✗</span>
            )}
          </div>
        </div>
      </Tile>

      {/* Complexity Breakdown */}
      <Tile className="chart-tile breakdown-tile">
        <h5 className="chart-title">Complexity Breakdown</h5>
        <div className="breakdown-bars">
          <div className="breakdown-item">
            <span className="breakdown-label">Structure</span>
            <div className="breakdown-bar">
              <div 
                className="breakdown-fill"
                style={{ 
                  width: `${metrics.components.classes ? 80 : 40}%`,
                  backgroundColor: '#0f62fe'
                }}
              />
            </div>
            <span className="breakdown-value">{metrics.components.classes ? 'High' : 'Low'}</span>
          </div>
          <div className="breakdown-item">
            <span className="breakdown-label">Logic</span>
            <div className="breakdown-bar">
              <div 
                className="breakdown-fill"
                style={{ 
                  width: `${(metrics.components.loops && metrics.components.conditionals) ? 85 : 
                           (metrics.components.loops || metrics.components.conditionals) ? 60 : 35}%`,
                  backgroundColor: '#8a3ffc'
                }}
              />
            </div>
            <span className="breakdown-value">
              {(metrics.components.loops && metrics.components.conditionals) ? 'High' : 
               (metrics.components.loops || metrics.components.conditionals) ? 'Medium' : 'Low'}
            </span>
          </div>
          <div className="breakdown-item">
            <span className="breakdown-label">Modularity</span>
            <div className="breakdown-bar">
              <div 
                className="breakdown-fill"
                style={{ 
                  width: `${metrics.components.functions ? 75 : 30}%`,
                  backgroundColor: '#24a148'
                }}
              />
            </div>
            <span className="breakdown-value">{metrics.components.functions ? 'Good' : 'Limited'}</span>
          </div>
        </div>
      </Tile>
    </div>
  )
}

export default AIInsightsChart

// Made with Bob - Enterprise Edition