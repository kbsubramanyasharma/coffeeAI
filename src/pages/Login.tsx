import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Coffee } from 'lucide-react';
import { useUser } from '@/context/UserContext';
import { apiService } from '@/services/api';

const Login: React.FC = () => {
  const [form, setForm] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();
  const { setUser } = useUser();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      const res = await fetch('http://localhost:8000/api/v1/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || data.message || 'Login failed');
      setSuccess('Login successful! Redirecting...');
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('token', data.access_token); // <-- Ensure this is set
      localStorage.setItem('user_id', String(data.user_id)); // <-- Ensure this is set as string
      
      // Try to get user profile to get the real first name
      try {
        const userProfile = await apiService.getUserProfile(data.access_token);
        const displayName = userProfile.first_name || 
                           userProfile.email.split('@')[0].replace(/[._]/g, ' ')
                           .split(' ')
                           .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                           .join(' ');
        
        setUser({ id: data.user_id, name: displayName });
        localStorage.setItem('user_name', displayName);
      } catch (profileError) {
        // Fallback: Create a better name from email if profile fetch fails
        console.warn('Could not fetch user profile, using email fallback:', profileError);
        const emailName = form.email.split('@')[0];
        const betterName = emailName.replace(/[._]/g, ' ')
                          .split(' ')
                          .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                          .join(' ');
        
        setUser({ id: data.user_id, name: betterName });
        localStorage.setItem('user_name', betterName);
      }
      
      console.log('Login success', data.access_token, data.user_id);
      setTimeout(() => navigate('/'), 1200);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#f5e9da] via-[#e3c9a3] to-[#b97a56]">
      <div className="w-full max-w-md bg-white/90 rounded-2xl shadow-xl p-8 md:p-10 flex flex-col items-center">
        <div className="mb-4 flex flex-col items-center">
          <span className="bg-gradient-to-r from-[#b97a56] to-[#e3c9a3] rounded-full p-3 mb-2">
            <Coffee className="h-10 w-10 text-[#b97a56]" />
          </span>
          <h1 className="text-2xl md:text-3xl font-serif font-bold text-[#6b3e26] mb-1">Welcome Back to Coffee Corner</h1>
          <p className="text-[#a67c52] text-sm mb-2">Log in to chat with our baristas and manage your orders!</p>
        </div>
        <form className="w-full space-y-4" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="email" className="block text-[#6b3e26] font-medium mb-1">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              placeholder="you@email.com"
              className="w-full px-4 py-2 rounded-lg border border-[#e3c9a3] focus:outline-none focus:ring-2 focus:ring-[#b97a56] bg-[#f9f6f2] text-[#6b3e26] font-medium"
              value={form.email}
              onChange={handleChange}
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-[#6b3e26] font-medium mb-1">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              required
              placeholder="Enter your password"
              className="w-full px-4 py-2 rounded-lg border border-[#e3c9a3] focus:outline-none focus:ring-2 focus:ring-[#b97a56] bg-[#f9f6f2] text-[#6b3e26] font-medium"
              value={form.password}
              onChange={handleChange}
            />
          </div>
          <div className="text-right">
            <Link to="/forgot-password" className="text-[#b97a56] text-sm font-medium hover:underline">
              Forgot Password?
            </Link>
          </div>
          {error && <div className="text-red-600 text-sm font-medium text-center">{error}</div>}
          {success && <div className="text-green-700 text-sm font-medium text-center">{success}</div>}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 mt-2 rounded-lg bg-gradient-to-r from-[#b97a56] to-[#e3c9a3] text-white font-bold text-lg shadow-md hover:from-[#a67c52] hover:to-[#e3c9a3] transition-colors duration-200 disabled:opacity-60"
          >
            {loading ? 'Logging In...' : 'Login'}
          </button>
        </form>
        <div className="mt-6 text-center">
          <span className="text-[#6b3e26]">Don't have an account? </span>
          <Link to="/register" className="text-[#b97a56] font-semibold hover:underline">Sign Up</Link>
        </div>
      </div>
    </div>
  );
};

export default Login; 