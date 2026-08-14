import { useState } from 'react'

const QUERY_ENDPOINT = import.meta.env.VITE_QUERY_ENDPOINT ?? '/api/query'
const SOURCE_ENDPOINT = import.meta.env.VITE_SOURCE_ENDPOINT ?? '/api/sources'

function MicIcon() {
  return <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="3" width="6" height="11" rx="3" /><path d="M6 11a6 6 0 0 0 12 0M12 17v4M8 21h8" /></svg>
}

function SendIcon() {
  return <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12 14-8-4 16-3.5-6.5L5 12Z" /><path d="m11.5 13.5 3-3" /></svg>
}

function FolderIcon() {
  return <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6.5A2.5 2.5 0 0 1 5.5 4h4l2 2h7A2.5 2.5 0 0 1 21 8.5v9a2.5 2.5 0 0 1-2.5 2.5h-13A2.5 2.5 0 0 1 3 17.5v-11Z" /></svg>
}

function App() {
  const [screen, setScreen] = useState('find')
  const [query, setQuery] = useState('')
  const [source, setSource] = useState('')
  const [status, setStatus] = useState('Ready when you are.')
  const [result, setResult] = useState(null)

  async function submitQuery(event) {
    event.preventDefault()
    if (!query.trim()) return
    setStatus('Searching your indexed documents…')
    setResult(null)
    try {
      const response = await fetch(QUERY_ENDPOINT, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query.trim() }),
      })
      if (!response.ok) throw new Error('Request was not accepted')
      setResult(await response.json())
      setStatus('Results received.')
    } catch {
      setStatus('The retrieval service is not connected yet.')
    }
  }

  async function submitSource(event) {
    event.preventDefault()
    if (!source.trim()) return
    setStatus('Sending location to the scan service…')
    try {
      const response = await fetch(SOURCE_ENDPOINT, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: source.trim() }),
      })
      if (!response.ok) throw new Error('Request was not accepted')
      setStatus('Location sent for indexing.')
      setSource('')
    } catch {
      setStatus('The scan service is not connected yet.')
    }
  }

  const resources = Array.isArray(result) ? result : result?.results ?? []

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark">G</span><span>Get-My-Doc</span></div>
        <nav aria-label="Primary navigation">
          <button className={screen === 'find' ? 'nav-button active' : 'nav-button'} onClick={() => setScreen('find')}><span className="nav-dot" />Find my doc</button>
          <button className={screen === 'source' ? 'nav-button active' : 'nav-button'} onClick={() => setScreen('source')}><FolderIcon />Save the source</button>
        </nav>
        <p className="privacy-note">Your documents stay on your device.</p>
      </aside>

      <section className="workspace">
        {screen === 'find' ? (
          <>
            <section className="output-panel" aria-live="polite">
              <div className="panel-heading"><span className="eyebrow">RETRIEVAL RESULTS</span><h1>Find what you need.</h1></div>
              {resources.length > 0 ? <div className="result-list">{resources.map((item, index) => <article className="result-card" key={item.id ?? item.path ?? index}><div><strong>{item.filename ?? item.name ?? 'Untitled document'}</strong><p>{item.path ?? item.extension ?? 'Resource returned by retrieval service'}</p></div><button className="open-button" type="button">Open</button></article>)}</div> : <div className="empty-state"><div className="search-orb" /><h2>Output field</h2><p>{status}</p><span>Ask naturally — file names and locations are not required.</span></div>}
            </section>
            <form className="query-bar" onSubmit={submitQuery}>
              <label className="sr-only" htmlFor="document-query">Describe the document you need</label>
              <input id="document-query" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Find my internship offer letter" autoComplete="off" />
              <button className="icon-button" type="button" aria-label="Start voice query" title="Voice input will be provided by the speech service"><MicIcon /></button>
              <button className="icon-button send" type="submit" aria-label="Search"><SendIcon /></button>
            </form>
          </>
        ) : (
          <section className="source-page">
            <div className="source-heading"><span className="eyebrow">SOURCE MANAGEMENT</span><h1>Add a document location.</h1><p>Choose a local folder for Get-My-Doc to monitor and index.</p></div>
            <form className="source-form" onSubmit={submitSource}>
              <label htmlFor="source-path">Folder path</label>
              <div className="source-input"><FolderIcon /><input id="source-path" value={source} onChange={(event) => setSource(event.target.value)} placeholder="C:\\Users\\You\\Documents" /><button type="submit">Save source</button></div>
              <small>{status}</small>
            </form>
          </section>
        )}
      </section>
    </main>
  )
}

export default App
