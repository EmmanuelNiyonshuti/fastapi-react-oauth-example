export const AuthService = {
  setToken(token) {
    localStorage.setItem('access_token', token);
  },

  getToken() {
    return localStorage.getItem('access_token');
  },

  removeToken() {
    localStorage.removeItem('access_token');
  },

  isAuthenticated() {
    return !!this.getToken();
  },

  logout() {
    this.removeToken();
    window.location.href = '/';
  }
};