import React, { useState } from 'react';
import { useParams, useSearchParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Send } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

export default function Chat() {
  const { docId } = useParams();
  const [searchParams] = useSearchParams();
  const filename = searchParams.get('filename') || 'Document';
  const navigate = useNavigate();
  
  const [question, setQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const token = localStorage.getItem('access_token');

  const handleAsk = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    
    const newChat = [...chatHistory, { role: 'user', text: question }];
    setChatHistory(newChat);
    setLoading(true);
    setQuestion('');
    
    try {
      const res = await fetch(`${API_BASE}/rag/ask`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ doc_id: docId, question })
      });
      const data = await res.json();
      if (res.ok) {
        setChatHistory(prev => [...prev, { role: 'ai', text: data.answer }]);
      } else {
        if (res.status === 401) {
          localStorage.removeItem('access_token');
          window.location.href = '/login';
        } else {
          alert(data.detail);
        }
      }
    } catch (err) {
      alert("Query failed");
    }
    setLoading(false);
  };

  return (
    <div className="container chat-container">
      <div className="chat-header">
        <button onClick={() => navigate('/')} className="back-btn"><ArrowLeft size={18} /> Dashboard</button>
        <div className="header-title">
          <h2>{filename}</h2>
          <span className="doc-id-badge">ID: {docId.substring(0,8)}...</span>
        </div>
      </div>
      
      <div className="glass-card main-chat-card">
        <div className="chat-history">
          {chatHistory.length === 0 && <p className="empty-chat">Data vectorized. Ask a question regarding {filename}...</p>}
          {chatHistory.map((msg, i) => (
            <div key={i} className={`message ${msg.role}`}>
              <p>{msg.text}</p>
            </div>
          ))}
          {loading && <div className="message ai"><p className="pulsate">Thinking...</p></div>}
        </div>
        
        <form onSubmit={handleAsk} className="ask-form">
          <input type="text" placeholder={`Query ${filename}...`} value={question} onChange={e => setQuestion(e.target.value)} disabled={loading} />
          <button type="submit" disabled={loading || !question}><Send size={18} /></button>
        </form>
      </div>
    </div>
  );
}
