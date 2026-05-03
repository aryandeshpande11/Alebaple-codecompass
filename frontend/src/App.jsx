import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Theme, Content } from '@carbon/react'
import Header from './components/Header'
import HomePage from './pages/HomePage'
import AnalysisPage from './pages/AnalysisPage'
import ErrorBoundary from './components/ErrorBoundary'
import './App.css'

function App() {
  // Use white theme by default for professional enterprise look
  const [theme, setTheme] = useState('white')

  return (
    <Router>
      <Theme theme={theme}>
        <ErrorBoundary showReload={true}>
          <div className="app">
            <Header theme={theme} setTheme={setTheme} />
            <Content>
              <ErrorBoundary>
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/analysis/:projectId" element={<AnalysisPage />} />
                </Routes>
              </ErrorBoundary>
            </Content>
          </div>
        </ErrorBoundary>
      </Theme>
    </Router>
  )
}

export default App

// Made with Bob - Enterprise Edition
