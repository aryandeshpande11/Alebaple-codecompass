import { Component } from 'react'
import { 
  InlineNotification,
  Button
} from '@carbon/react'
import { Renew } from '@carbon/icons-react'
import './ErrorBoundary.css'

class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { 
      hasError: false,
      error: null,
      errorInfo: null
    }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo)
    this.setState({
      error,
      errorInfo
    })
  }

  handleReset = () => {
    this.setState({ 
      hasError: false,
      error: null,
      errorInfo: null
    })
    // Optionally reload the page
    if (this.props.onReset) {
      this.props.onReset()
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <div className="error-boundary-content">
            <InlineNotification
              kind="error"
              title="Something went wrong"
              subtitle={this.state.error?.message || 'An unexpected error occurred'}
              lowContrast
            />
            
            <div className="error-actions">
              <Button
                kind="tertiary"
                renderIcon={Renew}
                onClick={this.handleReset}
              >
                Try Again
              </Button>
              
              {this.props.showReload && (
                <Button
                  kind="secondary"
                  onClick={() => window.location.reload()}
                >
                  Reload Page
                </Button>
              )}
            </div>

            {process.env.NODE_ENV === 'development' && this.state.errorInfo && (
              <details className="error-details">
                <summary>Error Details (Development Only)</summary>
                <pre>{this.state.errorInfo.componentStack}</pre>
              </details>
            )}
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary

// Made with Bob
