import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  Grid, 
  Column,
  Tile,
  Button
} from '@carbon/react'
import { 
  Code, 
  Ai, 
  DocumentTasks,
  ChartLineSmooth 
} from '@carbon/icons-react'
import UploadForm from '../components/UploadForm'
import './HomePage.css'

function HomePage() {
  const navigate = useNavigate()

  const handleAnalysisStart = (projectId) => {
    // Navigate to analysis page
    navigate(`/analysis/${projectId}`)
  }

  const features = [
    {
      icon: <Code size={32} />,
      title: 'Multi-Language Analysis',
      description: 'Analyze Python, Java, JavaScript, and TypeScript codebases with advanced AST parsing and metrics calculation.'
    },
    {
      icon: <Ai size={32} />,
      title: 'AI-Powered Insights',
      description: 'Get intelligent code explanations and documentation powered by IBM watsonx.ai Granite models.'
    },
    {
      icon: <DocumentTasks size={32} />,
      title: 'Automated Onboarding',
      description: 'Generate comprehensive onboarding documentation automatically for new team members.'
    },
    {
      icon: <ChartLineSmooth size={32} />,
      title: 'Code Metrics & Visualization',
      description: 'Visualize code complexity, dependencies, and quality metrics with interactive dashboards.'
    }
  ]

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <Grid>
          <Column lg={16} md={8} sm={4}>
            <div className="hero-content">
              <h1 className="hero-title">
                Code Understanding & Onboarding Accelerator
              </h1>
              <p className="hero-subtitle">
                Accelerate developer onboarding with AI-powered code analysis and intelligent documentation generation.
                Built with IBM watsonx.ai for enterprise-grade insights.
              </p>
              <div className="hero-badges">
                <span className="badge">IBM watsonx.ai</span>
                <span className="badge">Carbon Design</span>
                <span className="badge">Multi-Language</span>
                <span className="badge">Enterprise Ready</span>
              </div>
            </div>
          </Column>
        </Grid>
      </section>

      {/* Upload Section */}
      <section className="upload-section">
        <Grid>
          <Column lg={16} md={8} sm={4}>
            <div className="section-header">
              <h2 className="section-title">Get Started</h2>
              <p className="section-description">
                Enter a GitHub repository URL to begin analyzing your codebase
              </p>
            </div>
            <UploadForm onAnalysisStart={handleAnalysisStart} />
          </Column>
        </Grid>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <Grid>
          <Column lg={16} md={8} sm={4}>
            <div className="section-header">
              <h2 className="section-title">Key Features</h2>
              <p className="section-description">
                Powerful tools to understand and document your codebase
              </p>
            </div>
          </Column>
          
          {features.map((feature, index) => (
            <Column key={index} lg={4} md={4} sm={4}>
              <Tile className="feature-tile">
                <div className="feature-icon">{feature.icon}</div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </Tile>
            </Column>
          ))}
        </Grid>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works-section">
        <Grid>
          <Column lg={16} md={8} sm={4}>
            <div className="section-header">
              <h2 className="section-title">How It Works</h2>
            </div>
          </Column>

          <Column lg={16} md={8} sm={4}>
            <div className="steps-container">
              <div className="step-item">
                <div className="step-number">1</div>
                <div className="step-content">
                  <h4 className="step-title">Upload Repository</h4>
                  <p className="step-description">
                    Provide a GitHub repository URL or upload your codebase
                  </p>
                </div>
              </div>

              <div className="step-divider"></div>

              <div className="step-item">
                <div className="step-number">2</div>
                <div className="step-content">
                  <h4 className="step-title">Analyze Code</h4>
                  <p className="step-description">
                    Our engine parses and analyzes your code structure, metrics, and dependencies
                  </p>
                </div>
              </div>

              <div className="step-divider"></div>

              <div className="step-item">
                <div className="step-number">3</div>
                <div className="step-content">
                  <h4 className="step-title">Get AI Insights</h4>
                  <p className="step-description">
                    IBM watsonx.ai generates intelligent explanations and documentation
                  </p>
                </div>
              </div>

              <div className="step-divider"></div>

              <div className="step-item">
                <div className="step-number">4</div>
                <div className="step-content">
                  <h4 className="step-title">Onboard Faster</h4>
                  <p className="step-description">
                    Use generated insights to accelerate developer onboarding
                  </p>
                </div>
              </div>
            </div>
          </Column>
        </Grid>
      </section>

      {/* Footer */}
      <footer className="home-footer">
        <Grid>
          <Column lg={16} md={8} sm={4}>
            <p className="footer-text">
              Powered by IBM watsonx.ai • Built with Carbon Design System
            </p>
          </Column>
        </Grid>
      </footer>
    </div>
  )
}

export default HomePage

// Made with Bob - Enterprise Edition