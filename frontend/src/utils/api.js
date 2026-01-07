import { AuthService } from './auth';
import { API_BASE_URL } from '../config/api';

export async function apiRequest(endpoint, options = {}) {
  const token = AuthService.getToken();
  
  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  };
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    if (response.status === 401) {
      AuthService.logout();
      throw new Error('Unauthorized');
    }

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.detail || 'Request failed');
    }

    return data;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}