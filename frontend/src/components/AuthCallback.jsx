import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { AuthService } from '../utils/auth';

export default function AuthCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  const [isProcessing, setIsProcessing] = useState(true);

  useEffect(() => {
    const token = searchParams.get('token');
    const errorParam = searchParams.get('error');

    if (errorParam) {
      setError(getErrorMessage(errorParam));
      setIsProcessing(false);
      
      // Redirect to login after 3 seconds
      setTimeout(() => {
        navigate('/login');
      }, 3000);
      return;
    }

    if (token) {
      // Store token
      AuthService.setToken(token);
      
      // Redirect to dashboard
      setTimeout(() => {
        navigate('/dashboard');
      }, 1000);
    } else {
      setError('No authentication token received');
      setIsProcessing(false);
      
      setTimeout(() => {
        navigate('/login');
      }, 3000);
    }
  }, [searchParams, navigate]);

  function getErrorMessage(errorCode) {
    const errorMessages = {
      'provider_not_found': 'Authentication provider not found',
      'invalid_state': 'Invalid authentication state (possible CSRF attack)',
      'no_authorization_code': 'No authorization code received',
      'token_exchange_failed': 'Failed to exchange authorization code',
      'no_access_token': 'No access token received',
      'failed_to_get_user_info': 'Failed to retrieve user information',
      'unexpected_error': 'An unexpected error occurred',
    };
    
    return errorMessages[errorCode] || `Authentication error: ${errorCode}`;
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white p-8 rounded-2xl shadow-xl max-w-md w-full">
          <div className="flex items-center justify-center w-16 h-16 mx-auto bg-red-100 rounded-full mb-4">
            <svg className="w-8 h-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-center text-gray-900 mb-2">
            Authentication Failed
          </h2>
          <p className="text-center text-gray-600 mb-6">
            {error}
          </p>
          <p className="text-sm text-center text-gray-500">
            Redirecting to login page...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-2xl shadow-xl max-w-md w-full">
        <div className="flex items-center justify-center w-16 h-16 mx-auto bg-indigo-100 rounded-full mb-4">
          <svg className="w-8 h-8 text-indigo-600 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-center text-gray-900 mb-2">
          {isProcessing ? 'Processing...' : 'Success!'}
        </h2>
        <p className="text-center text-gray-600">
          {isProcessing ? 'Completing your authentication...' : 'Redirecting to dashboard...'}
        </p>
      </div>
    </div>
  );
}

