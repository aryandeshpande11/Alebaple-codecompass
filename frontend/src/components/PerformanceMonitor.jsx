import { useState, useEffect } from 'react';
import './PerformanceMonitor.css';

/**
 * Performance Monitor Component
 * Displays API response times and system health
 */
const PerformanceMonitor = ({ show = false }) => {
  const [metrics, setMetrics] = useState({
    apiResponseTime: 0,
    lastUpdate: null,
    status: 'healthy'
  });

  useEffect(() => {
    // Monitor performance from API headers
    const originalFetch = window.fetch;
    window.fetch = async (...args) => {
      const startTime = performance.now();
      const response = await originalFetch(...args);
      const endTime = performance.now();
      const responseTime = endTime - startTime;

      // Update metrics
      setMetrics(prev => ({
        apiResponseTime: responseTime,
        lastUpdate: new Date(),
        status: response.ok ? 'healthy' : 'degraded'
      }));

      return response;
    };

    return () => {
      window.fetch = originalFetch;
    };
  }, []);

  if (!show) return null;

  return (
    <div className="performance-monitor">
      <div className="performance-indicator">
        <span className={`status-dot ${metrics.status}`}></span>
        <span className="response-time">
          {metrics.apiResponseTime > 0 
            ? `${metrics.apiResponseTime.toFixed(0)}ms` 
            : 'Ready'}
        </span>
      </div>
    </div>
  );
};

export default PerformanceMonitor;

// Made with Bob
