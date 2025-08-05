import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { apiService } from '@/services/api';
import { toast } from '@/hooks/use-toast';

const ForgotPassword: React.FC = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [resetToken, setResetToken] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setMessage('');
    setResetToken('');
    setLoading(true);

    try {
      const data = await apiService.forgotPassword(email);
      setMessage(data.message || 'Check your email for the reset link.');
      setResetToken(data.reset_token || '');
      toast({
        title: 'Reset Email Sent',
        description: 'Please check your email for password reset instructions.',
      });
    } catch (err: any) {
      const errorMessage = err.message || 'Something went wrong. Please try again.';
      setError(errorMessage);
      toast({
        title: 'Error',
        description: errorMessage,
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#f5e9da] via-[#e3c9a3] to-[#b97a56]">
      <div className="w-full max-w-md bg-white/90 rounded-2xl shadow-xl p-8 md:p-10">
        <div className="text-center mb-6">
          <h2 className="text-2xl md:text-3xl font-serif font-bold text-[#6b3e26] mb-2">
            Forgot Password?
          </h2>
          <p className="text-[#a67c52] text-sm">
            No worries! Enter your email and we'll send you a reset link.
          </p>
        </div>

        {!message ? (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-[#6b3e26] font-medium mb-1">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                placeholder="Enter your email address"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
                disabled={loading}
                className="w-full px-4 py-3 rounded-lg border border-[#e3c9a3] focus:outline-none focus:ring-2 focus:ring-[#b97a56] bg-[#f9f6f2] text-[#6b3e26] font-medium disabled:opacity-50"
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
                  Sending Reset Link...
                </div>
              ) : (
                'Send Reset Link'
              )}
            </button>
          </form>
        ) : (
          <div className="text-center space-y-4">
            <div className="text-green-600 text-lg font-medium">✓ Email Sent!</div>
            <p className="text-[#6b3e26]">{message}</p>
            {resetToken && (
              <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                <p className="text-xs text-yellow-800 mb-2">
                  <strong>Development Mode:</strong> Reset token for testing:
                </p>
                <code className="text-xs bg-yellow-100 px-2 py-1 rounded border text-yellow-900 break-all">
                  {resetToken}
                </code>
              </div>
            )}
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

export default ForgotPassword; 