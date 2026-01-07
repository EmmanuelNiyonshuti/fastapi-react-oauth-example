import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthService } from '../utils/auth';
import { apiRequest } from '../utils/api';

export default function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Check if authenticated
    if (!AuthService.isAuthenticated()) {
      navigate('/login');
      return;
    }

    // Fetch user profile
    fetchUserProfile();
  }, [navigate]);

  async function fetchUserProfile() {
    try {
      const userData = await apiRequest('/api/users/me');
      setUser(userData);
    } catch (err) {
      setError('Failed to load user profile');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  function handleLogout() {
    AuthService.logout();
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={() => navigate('/login')}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            Back to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-xl font-bold text-gray-900">Dashboard</h1>
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="flex items-center gap-6 mb-8">
            <div className="w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center">
              <span className="text-2xl font-bold text-indigo-600">
                {user?.email?.[0]?.toUpperCase()}
              </span>
            </div>
            <div>
              <h2 className="text-3xl font-bold text-gray-900">
                Welcome back!
              </h2>
              <p className="text-gray-600 mt-1">
                {user?.email}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-6 bg-gray-50 rounded-xl">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                User ID
              </h3>
              <p className="text-gray-600 font-mono text-sm">
                {user?.uid}
              </p>
            </div>

            <div className="p-6 bg-gray-50 rounded-xl">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Username
              </h3>
              <p className="text-gray-600">
                {user?.username || 'N/A'}
              </p>
            </div>

            <div className="p-6 bg-gray-50 rounded-xl">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Email
              </h3>
              <p className="text-gray-600">
                {user?.email}
              </p>
            </div>

            <div className="p-6 bg-gray-50 rounded-xl">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Account Status
              </h3>
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                Active
              </span>
            </div>
          </div>

          <div className="mt-8 p-6 bg-blue-50 rounded-xl border border-blue-200">
            <h3 className="text-lg font-semibold text-blue-900 mb-2">
              🎉 Authentication Successful!
            </h3>
          </div>
        </div>
      </main>
    </div>
  );
}