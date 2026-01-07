export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  googleAuth: `${API_BASE_URL}/auth/authorize/google`,
  githubAuth: `${API_BASE_URL}/auth/authorize/github`,
  userProfile: `${API_BASE_URL}/api/users/me`,
};