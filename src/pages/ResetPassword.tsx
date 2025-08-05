import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import { apiService } from '@/services/api';
import { toast } from '@/hooks/use-toast';

const ResetPassword: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [token, setToken] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Extract token from URL parameters
    const urlToken = searchParams.get('token');
    if (urlToken) {
      setToken(urlToken);
    } else {
      setError('Invalid or missing reset token. Please request a new password reset.');
    }
  }, [searchParams]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setMessage('');

    // Validate passwords match
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    // Validate password strength
    if (newPassword.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    if (!token) {
      setError('Invalid reset token');
      return;
    }

    setLoading(true);
    try {
      const data = await apiService.resetPassword(token, newPassword);
      setMessage(data.message || 'Password has been reset successfully!');
      
      toast({
        title: 'Password Reset Successful',
        description: 'Your password has been updated. Redirecting to login...',
      });
      
      // Redirect to login page after 3 seconds
      setTimeout(() => {
        navigate('/login');
      }, 3000);
    } catch (err: any) {
      const errorMessage = err.message || 'Something went wrong. Please try again.';
      setError(errorMessage);
      toast({
        title: 'Reset Failed',
        description: errorMessage,
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  if (!token && !error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#f5e9da] via-[#e3c9a3] to-[#b97a56]">
        <div className="w-full max-w-md bg-white/90 rounded-2xl shadow-xl p-8 md:p-10">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#b97a56] mx-auto"></div>
            <p className="mt-2 text-[#6b3e26]">Loading...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#f5e9da] via-[#e3c9a3] to-[#b97a56]">
      <div className="w-full max-w-md bg-white/90 rounded-2xl shadow-xl p-8 md:p-10">
        <div className="text-center mb-6">
          <h2 className="text-2xl md:text-3xl font-serif font-bold text-[#6b3e26] mb-2">
            Reset Your Password
          </h2>
          <p className="text-[#a67c52] text-sm">
            Enter your new password below
          </p>
        </div>
        
        {!message ? (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="newPassword" className="block text-[#6b3e26] font-medium mb-1">
                New Password
              </label>
              <input
                id="newPassword"
                type="password"
                placeholder="Enter your new password"
                value={newPassword}
                onChange={e => setNewPassword(e.target.value)}
                required
                className="w-full px-4 py-3 rounded-lg border border-[#e3c9a3] focus:outline-none focus:ring-2 focus:ring-[#b97a56] bg-[#f9f6f2] text-[#6b3e26] font-medium disabled:opacity-50"
                disabled={loading}
              />
            </div>
            
            <div>
              <label htmlFor="confirmPassword" className="block text-[#6b3e26] font-medium mb-1">
                Confirm New Password
              </label>
              <input
                id="confirmPassword"
                type="password"
                placeholder="Confirm your new password"
                value={confirmPassword}
                onChange={e => setConfirmPassword(e.target.value)}
                required
                className="w-full px-4 py-3 rounded-lg border border-[#e3c9a3] focus:outline-none focus:ring-2 focus:ring-[#b97a56] bg-[#f9f6f2] text-[#6b3e26] font-medium disabled:opacity-50"
                disabled={loading}
              />
            </div>
            
            <button 
              type="submit" 
              disabled={loading}
              className="w-full py-3 rounded-lg bg-gradient-to-r from-[#b97a56] to-[#e3c9a3] text-white font-bold text-lg shadow-md hover:from-[#a67c52] hover:to-[#e3c9a3] transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Resetting Password...
                </div>
              ) : (
                'Reset Password'
              )}
            </button>
          </form>
        ) : (
          <div className="text-center space-y-4">
            <div className="text-green-600 text-lg font-medium">✓ {message}</div>
            <p className="text-[#6b3e26]">You will be redirected to login in a few seconds...</p>
            <button
              onClick={() => navigate('/login')}
              className="bg-gradient-to-r from-[#b97a56] to-[#e3c9a3] text-white px-6 py-2 rounded-lg hover:from-[#a67c52] hover:to-[#e3c9a3] transition-colors duration-200"
            >
              Go to Login Now
            </button>
          </div>
        )}
        
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
            {error}
          </div>
        )}

        <div className="mt-6 text-center">
          <Link 
            to="/login" 
            className="text-[#b97a56] font-medium hover:underline text-sm"
          >
            ← Back to Login
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword; 