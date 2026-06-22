import React, { useState } from 'react';
import { apiClient } from '../lib/apiClient';
import { McpTool, McpSearchCareerResponse } from '../types/api';

export const McpToolsExplorer: React.FC = () => {
  const [tools, setTools] = useState<McpTool[] | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<McpSearchCareerResponse[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const fetchTools = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const data = await apiClient.getTools();
      const toolsList = Array.isArray(data) ? data : (data as any).tools || [];
      setTools(toolsList);
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to fetch MCP tools catalog.');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setLoading(true);
    setErrorMsg(null);
    try {
      const data = await apiClient.searchCareers(searchQuery);
      setSearchResults(data);
    } catch (err: any) {
      setErrorMsg(err.message || 'Search request failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ marginTop: '2rem' }}>
      <h3 style={{ borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '0.5rem' }}>
        🔍 Model Context Protocol (MCP) Tool Explorer
      </h3>
      <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
        Interactively explore discoverable tool endpoints exported by the local MCP-style API server.
      </p>

      {errorMsg && (
        <div style={{ color: 'var(--color-danger)', fontSize: '0.875rem', margin: '0.5rem 0' }}>
          Error: {errorMsg}
        </div>
      )}

      <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem', flexWrap: 'wrap' }}>
        <button className="btn btn-secondary" onClick={fetchTools} disabled={loading}>
          {loading ? 'Loading...' : 'Fetch Discoverable Tools'}
        </button>
      </div>

      {tools && (
        <div style={{ marginTop: '1.25rem', backgroundColor: 'rgba(0,0,0,0.15)', padding: '1rem', borderRadius: '8px' }}>
          <h4 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>🛠️ Discovered Tool Schema Descriptions:</h4>
          <ul style={{ paddingLeft: '1.25rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
            {tools.map(tool => (
              <li key={tool.name} style={{ marginBottom: '0.5rem' }}>
                <strong style={{ color: 'var(--text-primary)' }}>{tool.name}</strong>: {tool.description}
              </li>
            ))}
          </ul>
        </div>
      )}

      <form onSubmit={handleSearch} style={{ marginTop: '1.5rem' }}>
        <label htmlFor="mcp-search-query" style={{ fontSize: '0.875rem', fontWeight: 600, display: 'block', marginBottom: '0.5rem' }}>
          Search Career Catalog via MCP Tool Endpoint
        </label>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <input
            id="mcp-search-query"
            type="text"
            className="input-field"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            placeholder="e.g. AI, developer, designer..."
            required
          />
          <button className="btn btn-primary" type="submit" disabled={loading}>
            Search
          </button>
        </div>
      </form>

      {searchResults && (
        <div style={{ marginTop: '1.25rem' }}>
          <h4 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>Search Results:</h4>
          {searchResults.length === 0 ? (
            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>No matches found in career catalog.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {searchResults.map(career => (
                <div key={career.career_id} style={{ padding: '0.75rem', backgroundColor: 'rgba(255,255,255,0.02)', borderRadius: '6px' }}>
                  <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>{career.title}</div>
                  <div className="skill-tags" style={{ marginTop: '0.25rem' }}>
                    {career.required_skills.slice(0, 6).map(skill => (
                      <span key={skill} className="skill-tag" style={{ fontSize: '0.75rem' }}>
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
