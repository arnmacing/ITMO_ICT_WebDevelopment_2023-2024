import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    role: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    getUserRole: (state) => state.role,
  },
  actions: {
    setToken(token) {
      this.token = token;
    },
    setRole(role) {
      this.role = role;
    },
    logout() {
      this.token = null;
      this.role = null;
    },
  },
});
