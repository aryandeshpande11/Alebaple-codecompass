import { 
  Loading,
  InlineLoading,
  SkeletonText,
  SkeletonPlaceholder
} from '@carbon/react'
import './LoadingState.css'

function LoadingState({ 
  type = 'default', 
  message = 'Loading...', 
  description = '',
  withOverlay = false,
  small = false 
}) {
  
  // Full page loading with overlay
  if (type === 'fullpage') {
    return (
      <div className="loading-fullpage">
        <Loading 
          description={description || 'Loading data...'} 
          withOverlay={withOverlay}
          small={small}
        />
      </div>
    )
  }

  // Inline loading for buttons and small areas
  if (type === 'inline') {
    return (
      <InlineLoading 
        description={message}
        status="active"
      />
    )
  }

  // Skeleton loading for content placeholders
  if (type === 'skeleton') {
    return (
      <div className="loading-skeleton">
        <SkeletonText heading paragraph lineCount={4} />
        <SkeletonPlaceholder className="skeleton-chart" />
      </div>
    )
  }

  // Card skeleton for dashboard cards
  if (type === 'card') {
    return (
      <div className="loading-card-skeleton">
        <SkeletonText heading />
        <SkeletonPlaceholder className="skeleton-card-content" />
      </div>
    )
  }

  // Table skeleton for file lists
  if (type === 'table') {
    return (
      <div className="loading-table-skeleton">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="skeleton-row">
            <SkeletonText width="60%" />
          </div>
        ))}
      </div>
    )
  }

  // Default centered loading
  return (
    <div className="loading-default">
      <Loading 
        description={message}
        small={small}
      />
      {description && <p className="loading-description">{description}</p>}
    </div>
  )
}

export default LoadingState

// Made with Bob
