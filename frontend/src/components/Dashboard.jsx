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
  const languageStats = analysis.language_stats || {}

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
              <h4 className="metric-value">{summary.total_lines?.toLocaleString() || 0}</h4>
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

      {Object.keys(languageStats).length > 0 && (
        <div className="language-stats">
          <Tile>
            <h4 className="section-title">Language Distribution</h4>
            <div className="language-list">
              {Object.entries(languageStats).map(([language, stats]) => (
                <div key={language} className="language-item">
                  <span className="language-name">{language}</span>
                  <span className="language-count">{stats.file_count} files</span>
                  <span className="language-lines">{stats.total_lines?.toLocaleString()} lines</span>
                </div>
              ))}
            </div>
          </Tile>
        </div>
      )}
    </div>
  )
}

export default Dashboard

// Made with Bob
