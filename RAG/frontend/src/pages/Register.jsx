import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { UserPlus } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

export default function Register() {
  const [formData, setFormData] = useState({ name: '', username: '', email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/user/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (res.ok) {
        alert("Registration successful! Please login.");
        navigate('/login');
      } else {
        const error = await res.json();
        alert(error.detail);
      }
    } catch (err) {
      alert("Registration failed");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <div className="glass-card auth-card">
        <UserPlus size={40} color="var(--primary)" style={{marginBottom: 20}} />
        <h2>Create Account</h2>
        <form onSubmit={handleRegister}>
          <input type="text" placeholder="Full Name" onChange={e => setFormData({...formData, name: e.target.value})} required />
          <input type="text" placeholder="Username" onChange={e => setFormData({...formData, username: e.target.value})} required />
          <input type="email" placeholder="Email Address" onChange={e => setFormData({...formData, email: e.target.value})} required />
          <input type="password" placeholder="Password" onChange={e => setFormData({...formData, password: e.target.value})} required />
          <button type="submit" disabled={loading}>{loading ? 'Creating...' : 'Register'}</button>
        </form>
        <p className="auth-link">Already have an account? <Link to="/login">Login here</Link></p>
      </div>
    </div>
  );
}
