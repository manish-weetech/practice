import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { LogIn } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/user/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem('access_token', data.token);
        window.location.href = '/';
      } else {
        alert(data.detail);
      }
    } catch (err) {
      alert("Login failed");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <div className="glass-card auth-card">
        <LogIn size={40} color="var(--primary)" style={{marginBottom: 20}} />
        <h2>Welcome Back</h2>
        <p className="subtitle">Sign in to access your secure document matrix</p>
        <form onSubmit={handleLogin}>
          <input type="email" placeholder="Email Address" value={email} onChange={e => setEmail(e.target.value)} required />
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
          <button type="submit" disabled={loading}>{loading ? 'Authenticating...' : 'Sign In'}</button>
        </form>
        <p className="auth-link">New here? <Link to="/register">Create an account</Link></p>
      </div>
    </div>
  );
}
