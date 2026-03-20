import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, Plus, LogOut, Upload } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

export default function Home() {
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const navigate = useNavigate();
  const token = localStorage.getItem('access_token');

  useEffect(() => {
    fetchDocs();
  }, []);

  const fetchDocs = async () => {
    try {
      const res = await fetch(`${API_BASE}/rag/documents`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setDocuments(data);
      } else {
        if (res.status === 401) handleLogout();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    const file = e.target.file.files[0];
    const displayName = e.target.display_name.value;
    if (!file || !displayName) return;
    
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('display_name', displayName);
    
    try {
      const res = await fetch(`${API_BASE}/rag/upload`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });
      const data = await res.json();
      if (res.ok) {
        setShowModal(false);
        navigate(`/chat/${data.doc_id}?filename=${encodeURIComponent(data.display_name)}`);
      } else {
        alert(data.detail);
      }
    } catch (err) {
      alert("Upload failed");
    }
    setUploading(false);
  };

  return (
    <div className="container dashboard-container">
      <div className="dash-header">
        <h1>Study Table</h1>
        <button onClick={handleLogout} className="logout-btn"><LogOut size={16} /> Logout</button>
      </div>
      
      <div className="doc-grid">
        {documents.map(doc => (
          <div key={doc.id} className="glass-card doc-card" onClick={() => navigate(`/chat/${doc.doc_id}?filename=${encodeURIComponent(doc.display_name || doc.filename)}`)}>
            <FileText size={40} className="doc-icon" />
            <h3>{doc.display_name || doc.filename}</h3>
            <p className="doc-date">{new Date(doc.created_at).toLocaleDateString()}</p>
          </div>
        ))}
        
        <div className="glass-card plus-card" onClick={() => setShowModal(true)}>
          <Plus size={50} color="var(--primary)" />
          <p>Upload New Document</p>
        </div>
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => !uploading && setShowModal(false)}>
          <div className="glass-card modal-content" onClick={e => e.stopPropagation()}>
            <h2><Upload size={24} style={{verticalAlign: 'middle', marginRight: 10}}/> Upload Matrix</h2>
            <form onSubmit={handleUpload}>
              <input type="text" name="display_name" placeholder="Friendly Document Name" required style={{marginBottom: 15}} />
              <input type="file" name="file" accept=".pdf,.docx" required />
              <div className="modal-actions">
                <button type="button" className="cancel-btn" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" disabled={uploading}>{uploading ? 'Vectorizing...' : 'Store & Chat'}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
