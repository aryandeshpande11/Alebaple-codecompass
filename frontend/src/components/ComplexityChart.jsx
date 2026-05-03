import { useMemo } from 'react'
import { Tile } from '@carbon/react'
import { WarningAlt, CheckmarkFilled } from '@carbon/icons-react'
import './ComplexityChart.css'

function ComplexityChart({ files }) {
  // Calculate complexity distribution
  const complexityData = useMemo(() => {
    if (!files || files.length === 0) return null

    const distribution = {
      low: 0,
      medium: 0,
      high: 0,
      veryHigh: 0
    }

    const complexityFiles = {
      low: [],
      medium: [],
      high: [],
      veryHigh: []
    }

    files.forEach(file => {
      const complexity = file.metrics?.complexity?.cyclomatic || 0
      const fileName = (file.file_path || file.path || '').split('/').pop()

      if (complexity <= 5) {
        distribution.low++
        complexityFiles.low.push({ name: fileName, value: complexity })
      } else if (complexity <= 10) {
        distribution.medium++
        complexityFiles.medium.push({ name: fileName, value: complexity })
      } else if (complexity <= 20) {
        distribution.high++
        complexityFiles.high.push({ name: fileName, value: complexity })
      } else {
        distribution.veryHigh++
        complexityFiles.veryHigh.push({ name: fileName, value: complexity })
      }
    })

    const total = files.length
    return {
      distribution,
      percentages: {
        low: ((distribution.low / total) * 100).toFixed(1),
        medium: ((distribution.medium / total) * 100).toFixed(1),
        high: ((distribution.high / total) * 100).toFixed(1),
        veryHigh: ((distribution.veryHigh / total) * 100).toFixed(1)
      },
      files: complexityFiles,
      total
    }
  }, [files])

  if (!complexityData) {
    return (
      <Tile className="complexity-chart">
        <h4>Complexity Distribution</h4>
        <p className="no-data">No complexity data available</p>
      </Tile>
    )
  }

  const { distribution, percentages } = complexityData

  return (
    <Tile className="complexity-chart">
      <div className="chart-header">
        <h4>Cyclomatic Complexity Distribution</h4>
        <span className="total-files">{complexityData.total} files</span>
      </div>

      <div className="complexity-bars">
        {/* Low Complexity */}
        <div className="complexity-row">
          <div className="complexity-label">
            <CheckmarkFilled size={16} className="icon-low" />
            <span>Low (1-5)</span>
          </div>
          <div className="complexity-bar-container">
            <div 
              className="complexity-bar low"
              style={{ width: `${percentages.low}%` }}
            >
              <span className="bar-label">{distribution.low}</span>
            </div>
          </div>
          <span className="complexity-percentage">{percentages.low}%</span>
        </div>

        {/* Medium Complexity */}
        <div className="complexity-row">
          <div className="complexity-label">
            <CheckmarkFilled size={16} className="icon-medium" />
            <span>Medium (6-10)</span>
          </div>
          <div className="complexity-bar-container">
            <div 
              className="complexity-bar medium"
              style={{ width: `${percentages.medium}%` }}
            >
              <span className="bar-label">{distribution.medium}</span>
            </div>
          </div>
          <span className="complexity-percentage">{percentages.medium}%</span>
        </div>

        {/* High Complexity */}
        <div className="complexity-row">
          <div className="complexity-label">
            <WarningAlt size={16} className="icon-high" />
            <span>High (11-20)</span>
          </div>
          <div className="complexity-bar-container">
            <div 
              className="complexity-bar high"
              style={{ width: `${percentages.high}%` }}
            >
              <span className="bar-label">{distribution.high}</span>
            </div>
          </div>
          <span className="complexity-percentage">{percentages.high}%</span>
        </div>

        {/* Very High Complexity */}
        <div className="complexity-row">
          <div className="complexity-label">
            <WarningAlt size={16} className="icon-very-high" />
            <span>Very High (20+)</span>
          </div>
          <div className="complexity-bar-container">
            <div 
              className="complexity-bar very-high"
              style={{ width: `${percentages.veryHigh}%` }}
            >
              <span className="bar-label">{distribution.veryHigh}</span>
            </div>
          </div>
          <span className="complexity-percentage">{percentages.veryHigh}%</span>
        </div>
      </div>

      <div className="complexity-summary">
        <div className="summary-item">
          <span className="summary-label">Maintainable</span>
          <span className="summary-value good">
            {distribution.low + distribution.medium} files
          </span>
        </div>
        <div className="summary-item">
          <span className="summary-label">Needs Review</span>
          <span className="summary-value warning">
            {distribution.high + distribution.veryHigh} files
          </span>
        </div>
      </div>
    </Tile>
  )
}

export default ComplexityChart

// Made with Bob
