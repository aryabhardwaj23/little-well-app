import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('littlewell_token') || null);
  const user = ref(JSON.parse(localStorage.getItem('littlewell_user') || 'null'));

  const isAuthenticated = computed(() => !!token.value);

  async function login({ username, password }) {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      let message = 'Login failed';
      try {
        const data = await response.json();
        message = data.detail || message;
      } catch {}
      throw new Error(message);
    }

    const data = await response.json();
    token.value = data.access_token;
    user.value = data.user || null;

    localStorage.setItem('littlewell_token', data.access_token);
    if (data.user) {
      localStorage.setItem('littlewell_user', JSON.stringify(data.user));
    }
  }

  async function register({ username, password }) {
    const response = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      let message = 'Registration failed';
      try {
        const data = await response.json();
        message = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail);
      } catch {}
      throw new Error(message);
    }

    const data = await response.json();
    token.value = data.access_token;
    user.value = data.user || null;

    localStorage.setItem('littlewell_token', data.access_token);
    if (data.user) {
      localStorage.setItem('littlewell_user', JSON.stringify(data.user));
    }
  }

  function logout() {
    token.value = null;
    user.value = null;
    localStorage.removeItem('littlewell_token');
    localStorage.removeItem('littlewell_user');
  }

  return { token, user, isAuthenticated, login, register, logout };
});