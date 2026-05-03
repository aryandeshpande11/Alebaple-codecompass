import { useEffect, useRef, useState } from 'react'
import { Tile, Toggle, Tag } from '@carbon/react'
import { Diagram, FlowData } from '@carbon/icons-react'
import './DependencyGraph.css'

function DependencyGraph({ files }) {
  const canvasRef = useRef(null)
  const [showLabels, setShowLabels] = useState(true)
  const [dependencies, setDependencies] = useState([])

  useEffect(() => {
    if (!files || files.length === 0) return

    // Extract dependencies from files
    const deps = extractDependencies(files)
    setDependencies(deps)
  }, [files])

  useEffect(() => {
    if (!canvasRef.current || dependencies.length === 0) return

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    
    // Set canvas size
    const container = canvas.parentElement
    canvas.width = container.clientWidth
    canvas.height = 500

    // Draw the dependency graph
    drawGraph(ctx, dependencies, canvas.width, canvas.height, showLabels)
  }, [dependencies, showLabels])

  const extractDependencies = (files) => {
    const deps = []
    const fileMap = new Map()

    // Create a map of files
    files.forEach((file, index) => {
      const fileName = file.file_path || file.path || `file-${index}`
      fileMap.set(fileName, {
        id: index,
        name: fileName.split('/').pop(),
        fullPath: fileName,
        imports: [],
        language: file.language || 'unknown'
      })
    })

    // Extract import relationships
    files.forEach((file) => {
      const fileName = file.file_path || file.path
      const content = file.content || ''
      
      if (!content) return

      // Extract imports based on language
      const imports = extractImports(content, file.language)
      
      imports.forEach(importPath => {
        // Try to match with existing files
        const matchedFile = Array.from(fileMap.values()).find(f => 
          f.fullPath.includes(importPath) || importPath.includes(f.name)
        )

        if (matchedFile) {
          deps.push({
            from: fileMap.get(fileName).id,
            to: matchedFile.id,
            fromName: fileMap.get(fileName).name,
            toName: matchedFile.name
          })
        }
      })
    })

    return {
      nodes: Array.from(fileMap.values()),
      edges: deps
    }
  }

  const extractImports = (content, language) => {
    const imports = []
    
    if (!content) return imports

    // Python imports
    if (language === 'python') {
      const pythonImports = content.match(/(?:from|import)\s+([a-zA-Z0-9_.]+)/g)
      if (pythonImports) {
        pythonImports.forEach(imp => {
          const match = imp.match(/(?:from|import)\s+([a-zA-Z0-9_.]+)/)
          if (match) imports.push(match[1])
        })
      }
    }
    
    // JavaScript/TypeScript imports
    if (language === 'javascript' || language === 'typescript') {
      const jsImports = content.match(/import\s+.*?from\s+['"]([^'"]+)['"]/g)
      if (jsImports) {
        jsImports.forEach(imp => {
          const match = imp.match(/from\s+['"]([^'"]+)['"]/)
          if (match) imports.push(match[1])
        })
      }
      
      const requireImports = content.match(/require\(['"]([^'"]+)['"]\)/g)
      if (requireImports) {
        requireImports.forEach(imp => {
          const match = imp.match(/require\(['"]([^'"]+)['"]\)/)
          if (match) imports.push(match[1])
        })
      }
    }

    return imports
  }

  const drawGraph = (ctx, deps, width, height, showLabels) => {
    // Clear canvas
    ctx.clearRect(0, 0, width, height)

    const { nodes, edges } = deps
    
    if (nodes.length === 0) {
      ctx.fillStyle = '#525252'
      ctx.font = '14px IBM Plex Sans'
      ctx.textAlign = 'center'
      ctx.fillText('No dependencies detected', width / 2, height / 2)
      return
    }

    // Calculate node positions in a circular layout
    const centerX = width / 2
    const centerY = height / 2
    const radius = Math.min(width, height) * 0.35

    const nodePositions = nodes.map((node, index) => {
      const angle = (index / nodes.length) * 2 * Math.PI - Math.PI / 2
      return {
        ...node,
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle)
      }
    })

    // Draw edges
    ctx.strokeStyle = '#8a3ffc'
    ctx.lineWidth = 1.5
    ctx.globalAlpha = 0.3

    edges.forEach(edge => {
      const fromNode = nodePositions[edge.from]
      const toNode = nodePositions[edge.to]
      
      if (fromNode && toNode) {
        ctx.beginPath()
        ctx.moveTo(fromNode.x, fromNode.y)
        ctx.lineTo(toNode.x, toNode.y)
        ctx.stroke()

        // Draw arrow
        const angle = Math.atan2(toNode.y - fromNode.y, toNode.x - fromNode.x)
        const arrowSize = 8
        ctx.beginPath()
        ctx.moveTo(toNode.x, toNode.y)
        ctx.lineTo(
          toNode.x - arrowSize * Math.cos(angle - Math.PI / 6),
          toNode.y - arrowSize * Math.sin(angle - Math.PI / 6)
        )
        ctx.lineTo(
          toNode.x - arrowSize * Math.cos(angle + Math.PI / 6),
          toNode.y - arrowSize * Math.sin(angle + Math.PI / 6)
        )
        ctx.closePath()
        ctx.fill()
      }
    })

    // Draw nodes
    ctx.globalAlpha = 1
    nodePositions.forEach(node => {
      // Node circle
      ctx.beginPath()
      ctx.arc(node.x, node.y, 20, 0, 2 * Math.PI)
      ctx.fillStyle = '#0f62fe'
      ctx.fill()
      ctx.strokeStyle = '#ffffff'
      ctx.lineWidth = 2
      ctx.stroke()

      // Node label
      if (showLabels) {
        ctx.fillStyle = '#161616'
        ctx.font = '11px IBM Plex Sans'
        ctx.textAlign = 'center'
        ctx.fillText(node.name.substring(0, 15), node.x, node.y + 35)
      }
    })
  }

  const stats = {
    totalFiles: dependencies.nodes?.length || 0,
    totalDependencies: dependencies.edges?.length || 0,
    avgDependencies: dependencies.nodes?.length > 0 
      ? (dependencies.edges?.length / dependencies.nodes?.length).toFixed(1) 
      : 0
  }

  return (
    <div className="dependency-graph">
      <Tile className="graph-tile">
        <div className="graph-header">
          <div className="graph-title">
            <Diagram size={24} />
            <h4>Dependency Graph</h4>
          </div>
          <div className="graph-controls">
            <Toggle
              id="show-labels-toggle"
              labelText="Show Labels"
              size="sm"
              toggled={showLabels}
              onToggle={(checked) => setShowLabels(checked)}
            />
          </div>
        </div>

        <div className="graph-stats">
          <div className="stat-item">
            <span className="stat-label">Files</span>
            <Tag type="blue" size="sm">{stats.totalFiles}</Tag>
          </div>
          <div className="stat-item">
            <span className="stat-label">Dependencies</span>
            <Tag type="purple" size="sm">{stats.totalDependencies}</Tag>
          </div>
          <div className="stat-item">
            <span className="stat-label">Avg per File</span>
            <Tag type="cyan" size="sm">{stats.avgDependencies}</Tag>
          </div>
        </div>

        <div className="graph-canvas-container">
          <canvas ref={canvasRef} className="graph-canvas" />
        </div>

        {stats.totalDependencies === 0 && (
          <div className="graph-empty">
            <FlowData size={48} />
            <p>No dependencies detected in the analyzed files</p>
            <p className="empty-hint">
              Dependencies are extracted from import statements in the code
            </p>
          </div>
        )}
      </Tile>
    </div>
  )
}

export default DependencyGraph

// Made with Bob - Enterprise Edition