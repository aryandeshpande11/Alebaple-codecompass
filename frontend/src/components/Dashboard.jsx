import {
  Tile,
  Grid,
  Column,
  SkeletonText,
  SkeletonPlaceholder
} from '@carbon/react'
import {
  Code,
  Document,
  Function,
  DataClass
} from '@carbon/icons-react'
import ComplexityChart from './ComplexityChart'
import './Dashboard.css'

function Dashboard({ analysis, loading }) {
  if (loading) {
    return (
      <div className="dashboard-container">
        <Grid>
          <Column lg={4} md={4} sm={4}>
            <Tile className="metric-tile">
              <SkeletonText heading />
              <SkeletonPlaceholder className="metric-skeleton" />
            </Tile>
          </Column>
          <Column lg={4} md={4} sm={4}>
            <Tile className="metric-tile">
              <SkeletonText heading />
              <SkeletonPlaceholder className="metric-skeleton" />
            </Tile>
          </Column>
          <Column lg={4} md={4} sm={4}>
            <Tile className="metric-tile">
              <SkeletonText heading />
              <SkeletonPlaceholder className="metric-skeleton" />
            </Tile>
          </Column>
          <Column lg={4} md={4} sm={4}>
            <Tile className="metric-tile">
              <SkeletonText heading />
              <SkeletonPlaceholder className="metric-skeleton" />
            </Tile>
          </Column>
        </Grid>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className="dashboard-container">
        <Tile>
          <p>No analysis data available</p>
        </Tile>
      </div>
    )
  }

  const summary = analysis.summary || {}
  const languages = summary.languages || {}
  
  // Calculate total lines from metrics
  const totalLines = summary.total_lloc || summary.total_sloc || summary.loc || 0

  return (
    <div className="dashboard-container">
      <Grid>
        <Column lg={4} md={4} sm={4}>
          <Tile className="metric-tile">
            <div className="metric-icon">
              <Document size={32} />
            </div>
            <div className="metric-content">
              <h4 className="metric-value">{summary.total_files || 0}</h4>
              <p className="metric-label">Total Files</p>
            </div>
          </Tile>
        </Column>

        <Column lg={4} md={4} sm={4}>
          <Tile className="metric-tile">
            <div className="metric-icon">
              <Code size={32} />
            </div>
            <div className="metric-content">
              <h4 className="metric-value">{totalLines?.toLocaleString() || 0}</h4>
              <p className="metric-label">Lines of Code</p>
            </div>
          </Tile>
        </Column>

        <Column lg={4} md={4} sm={4}>
          <Tile className="metric-tile">
            <div className="metric-icon">
              <Function size={32} />
            </div>
            <div className="metric-content">
              <h4 className="metric-value">{summary.total_functions || 0}</h4>
              <p className="metric-label">Functions</p>
            </div>
          </Tile>
        </Column>

        <Column lg={4} md={4} sm={4}>
          <Tile className="metric-tile">
            <div className="metric-icon">
              <DataClass size={32} />
            </div>
            <div className="metric-content">
              <h4 className="metric-value">{summary.total_classes || 0}</h4>
              <p className="metric-label">Classes</p>
            </div>
          </Tile>
        </Column>
      </Grid>

      <Grid className="dashboard-charts">
        <Column lg={8} md={8} sm={4}>
          {Object.keys(languages).length > 0 && (
            <div className="language-stats">
              <Tile>
                <h4 className="section-title">Language Distribution</h4>
                <div className="language-list">
                  {Object.entries(languages).map(([language, count]) => {
                    // Ensure count is a number, not an object
                    const fileCount = typeof count === 'number' ? count : (count?.count || 0)
                    return (
                      <div key={language} className="language-item">
                        <span className="language-name">{String(language)}</span>
                        <span className="language-count">{fileCount} {fileCount === 1 ? 'file' : 'files'}</span>
                      </div>
                    )
                  })}
                </div>
              </Tile>
            </div>
          )}
        </Column>

        <Column lg={8} md={8} sm={4}>
          <ComplexityChart files={analysis.files || []} />
        </Column>
      </Grid>
    </div>
  )
}

export default Dashboard

// Made with Bob
