import { useEffect, useState } from 'react'
import './App.css'

const stats = [
  { value: '1M+', label: 'units monitored' },
  { value: '3.2x', label: 'faster review' },
  { value: '94%', label: 'issue detection' },
]

const features = [
  {
    icon: 'fa-solid fa-file-lines',
    title: 'Lease intelligence',
    text: 'Turns dense lease language into clear, searchable findings in seconds.',
  },
  {
    icon: 'fa-solid fa-scale-balanced',
    title: 'Legal cross-checking',
    text: 'Matches terms against housing rules and documentation for stronger evidence.',
  },
  {
    icon: 'fa-solid fa-envelope-open-text',
    title: 'Demand letter drafting',
    text: 'Produces polished tenant-ready letters you can send with confidence.',
  },
]

const violationExamples = [
  'Illegal rent increase above allowable caps',
  'Missing lead paint disclosure or hazard notice',
  'Failure to provide rent history records',
]

const steps = [
  'Upload lease PDF',
  'AI extracts the terms',
  'Report + letter generated',
]

const API_BASE = import.meta.env.VITE_API_BASE || ''

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [letter, setLetter] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState('')
  const [backendReady, setBackendReady] = useState(false)

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch(`${API_BASE}/health`)
        if (response.ok) {
          setBackendReady(true)
        }
      } catch {
        setBackendReady(false)
      }
    }

    checkHealth()
  }, [])

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please choose a PDF lease file first.')
      return
    }

    setIsAnalyzing(true)
    setError('')
    setLetter('')

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const response = await fetch(`${API_BASE}/api/lease/analyze`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.detail || 'The analysis failed.')
      }

      setAnalysis(data)
    } catch (err) {
      setError(err.message || 'Something went wrong while analyzing the lease.')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleGenerateLetter = async () => {
    if (!analysis || !analysis.violations?.length) {
      setError('Run the lease analysis first so the violations are available.')
      return
    }

    setIsGenerating(true)
    setError('')

    const payload = {
      tenant_name: analysis.extracted_terms?.tenant_name || 'Tenant',
      landlord_name: analysis.extracted_terms?.landlord_name || 'Landlord',
      address: analysis.extracted_terms?.address || 'Property Address',
      violations: analysis.violations,
    }

    try {
      const response = await fetch(`${API_BASE}/api/letters/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.detail || 'The demand letter could not be generated.')
      }

      setLetter(data.letter)
    } catch (err) {
      setError(err.message || 'Something went wrong while generating the letter.')
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="app-shell">
      <header className="top-nav">
        <div className="brand-wrap">
          <img className="brand-logo" src="/favicon.svg" alt="RentGhost logo" />
          <span>RentGhost</span>
        </div>
        <nav>
          <a href="#features">Features</a>
          <a href="#demo">Demo</a>
          <a href="#about">About</a>
        </nav>
        <a className="nav-cta" href="#demo">
          Start now
        </a>
      </header>

      <main>
        <section className="hero-section">
          <div className="hero-copy">
            <span className="eyebrow">AI tenant protection</span>
            <h1>Spot lease issues before they become a problem.</h1>
            <p>
              RentGhost scans your documents, highlights risky clauses, and prepares a
              demand letter that helps you push back with evidence.
            </p>
            <div className="hero-actions">
              <a className="primary-btn" href="#demo">
                <i className="fa-solid fa-file-arrow-up" /> Upload lease
              </a>
              <a className="secondary-btn" href="#features">
                <i className="fa-solid fa-circle-play" /> How it works
              </a>
            </div>
            <div className="hero-footnote">
              <span className={backendReady ? 'status-live' : 'status-offline'}>
                {backendReady ? 'Live backend' : 'Backend offline'}
              </span>
              <div className="mini-dots">
                <span />
                <span />
                <span />
              </div>
            </div>
          </div>

          <div className="hero-visual">
            <div className="hero-card-shell">
              <div className="hero-card-top">
                <span className="glass-dot" />
                <span className="glass-dot" />
                <span className="glass-dot" />
              </div>
              <div className="hero-card-body">
                <div className="report-pill">Lease review</div>
                <div className="hero-ring-wrap">
                  <div className="hero-ring">
                    <div className="hero-ring-inner">98%</div>
                  </div>
                </div>
                <div className="hero-metrics">
                  <div>
                    <span>Detected</span>
                    <strong>{analysis?.violations?.length || 3} violations</strong>
                  </div>
                  <div>
                    <span>Risk</span>
                    <strong>High priority</strong>
                  </div>
                </div>
              </div>
              <div className="floating-note note-one">
                <span>Rent increase</span>
                <strong>{analysis?.extracted_terms?.rent_amount || '+18.7%'}</strong>
              </div>
              <div className="floating-note note-two">
                <span>Lead notice</span>
                <strong>{analysis?.missing_disclosures?.length ? 'Review needed' : 'Missing'}</strong>
              </div>
            </div>
          </div>
        </section>

        <section className="stats-strip">
          {stats.map((stat) => (
            <div key={stat.label}>
              <strong>{stat.value}</strong>
              <span>{stat.label}</span>
            </div>
          ))}
        </section>

        <section className="features-section" id="features">
          <div className="section-heading">
            <span className="eyebrow">Why it works</span>
            <h2>A cleaner path from paperwork to evidence.</h2>
          </div>
          <div className="feature-grid">
            {features.map((feature) => (
              <article key={feature.title} className="feature-card">
                <div className="feature-icon">
                  <i className={feature.icon} />
                </div>
                <h3>{feature.title}</h3>
                <p>{feature.text}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="demo-section" id="demo">
          <div className="demo-panel left-panel">
            <div className="section-heading compact">
              <span className="eyebrow">Live analysis</span>
              <h2>Upload your lease</h2>
            </div>

            <div className="upload-panel">
              <label htmlFor="lease-upload" className="upload-button">
                <i className="fa-solid fa-cloud-arrow-up" />
                <span>{selectedFile ? selectedFile.name : 'Choose PDF lease'}</span>
              </label>
              <input
                id="lease-upload"
                type="file"
                accept=".pdf"
                onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
              />
              <button
                className="primary-btn upload-submit"
                onClick={handleAnalyze}
                disabled={isAnalyzing}
              >
                <i className="fa-solid fa-magnifying-glass" />{' '}
                {isAnalyzing ? 'Analyzing...' : 'Analyze lease'}
              </button>
            </div>

            {error && <p className="error-text">{error}</p>}

            <div className="violation-list">
              {analysis?.violations?.length ? (
                analysis.violations.map((item, index) => (
                  <div key={`${item.title}-${index}`} className="violation-row">
                    <span className="violation-index">0{index + 1}</span>
                    <div>
                      <strong>{item.title}</strong>
                      <p>{item.description}</p>
                    </div>
                  </div>
                ))
              ) : (
                violationExamples.map((item, index) => (
                  <div key={item} className="violation-row">
                    <span className="violation-index">0{index + 1}</span>
                    <p>{item}</p>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="demo-panel right-panel">
            <div className="report-card">
              <div className="report-top">
                <span>Violation report</span>
                <span className="pill">{analysis ? 'Ready' : 'Pending'}</span>
              </div>
              <h3>{analysis?.summary || 'Lease review complete'}</h3>
              <div className="report-meter">
                <div className="meter-fill" style={{ width: analysis ? '82%' : '58%' }} />
              </div>
              <ul>
                <li>{analysis?.extracted_terms?.address || 'Address will appear here'}</li>
                <li>{analysis?.extracted_terms?.rent_amount || 'Rent terms will appear here'}</li>
                <li>{analysis?.missing_disclosures?.length || 0} disclosures checked</li>
              </ul>
            </div>

            <div className="step-row">
              {steps.map((step, index) => (
                <div key={step} className="step-pill">
                  <span>{index + 1}</span>
                  <p>{step}</p>
                </div>
              ))}
            </div>

            <button
              className="primary-btn letter-button"
              onClick={handleGenerateLetter}
              disabled={isGenerating || !analysis?.violations?.length}
            >
              <i className="fa-solid fa-file-contract" />{' '}
              {isGenerating ? 'Generating...' : 'Generate demand letter'}
            </button>

            {letter && (
              <div className="letter-output">
                <h4>Draft demand letter</h4>
                <pre>{letter}</pre>
              </div>
            )}
          </div>
        </section>

        <section className="about-section" id="about">
          <div>
            <span className="eyebrow">Mission</span>
            <h2>Protecting renters from predatory housing practices.</h2>
          </div>
          <p>
            We built RentGhost to turn confusing paperwork into clear, actionable evidence so
            tenants can push back with confidence.
          </p>
        </section>
      </main>
    </div>
  )
}

export default App
