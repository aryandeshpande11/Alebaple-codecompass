import { useState } from 'react'
import {
  Search
} from '@carbon/react'
import {
  Folder,
  FolderOpen,
  Document
} from '@carbon/icons-react'
import './FileTree.css'

function FileTree({ files, onFileSelect, selectedFile }) {
  const [expandedNodes, setExpandedNodes] = useState(new Set())
  const [searchQuery, setSearchQuery] = useState('')

  // Build tree structure from flat file list
  const buildTree = (files) => {
    const tree = {}
    
    files.forEach(file => {
      const path = file.file_path || file.path || ''
      const parts = path.split(/[/\\]/).filter(Boolean)
      
      let current = tree
      parts.forEach((part, index) => {
        if (!current[part]) {
          current[part] = {
            name: part,
            path: parts.slice(0, index + 1).join('/'),
            isFile: index === parts.length - 1,
            children: {},
            fileData: index === parts.length - 1 ? file : null
          }
        }
        current = current[part].children
      })
    })
    
    return tree
  }

  const toggleNode = (nodePath) => {
    const newExpanded = new Set(expandedNodes)
    if (newExpanded.has(nodePath)) {
      newExpanded.delete(nodePath)
    } else {
      newExpanded.add(nodePath)
    }
    setExpandedNodes(newExpanded)
  }

  // Filter files based on search query
  const filterFiles = (files) => {
    if (!searchQuery.trim()) return files
    
    const query = searchQuery.toLowerCase()
    return files.filter(file => {
      const path = (file.file_path || file.path || '').toLowerCase()
      return path.includes(query)
    })
  }

  const renderTree = (nodes, level = 0) => {
    return Object.values(nodes).map(node => {
      const isExpanded = expandedNodes.has(node.path)
      const isSelected = selectedFile?.path === node.path || selectedFile?.file_path === node.path
      
      if (node.isFile) {
        return (
          <div
            key={node.path}
            className={`file-tree-item file-item ${isSelected ? 'selected' : ''}`}
            style={{ paddingLeft: `${level * 20 + 8}px` }}
            onClick={() => onFileSelect(node.fileData)}
          >
            <Document size={16} className="file-icon" />
            <span className="file-name">{node.name}</span>
          </div>
        )
      } else {
        const hasChildren = Object.keys(node.children).length > 0
        return (
          <div key={node.path} className="file-tree-folder">
            <div
              className={`file-tree-item folder-item ${isExpanded ? 'expanded' : ''}`}
              style={{ paddingLeft: `${level * 20 + 8}px` }}
              onClick={() => toggleNode(node.path)}
            >
              {isExpanded ? (
                <FolderOpen size={16} className="folder-icon" />
              ) : (
                <Folder size={16} className="folder-icon" />
              )}
              <span className="folder-name">{node.name}</span>
              {hasChildren && (
                <span className="folder-count">
                  ({Object.keys(node.children).length})
                </span>
              )}
            </div>
            {isExpanded && hasChildren && (
              <div className="folder-children">
                {renderTree(node.children, level + 1)}
              </div>
            )}
          </div>
        )
      }
    })
  }

  if (!files || files.length === 0) {
    return (
      <div className="file-tree-empty">
        <p>No files to display</p>
      </div>
    )
  }

  const filteredFiles = filterFiles(files)
  const tree = buildTree(filteredFiles)

  return (
    <div className="file-tree-container">
      <div className="file-tree-search">
        <Search
          size="lg"
          placeholder="Search files..."
          labelText="Search files"
          closeButtonLabelText="Clear search"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onClear={() => setSearchQuery('')}
        />
      </div>
      <div className="file-tree">
        {filteredFiles.length === 0 ? (
          <div className="file-tree-empty">
            <p>No files match your search</p>
          </div>
        ) : (
          renderTree(tree)
        )}
      </div>
    </div>
  )
}

export default FileTree

// Made with Bob - Enterprise Edition