import axios from 'axios';
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
export const api = axios.create({ baseURL: API_URL });
api.interceptors.request.use((config) => { const token = localStorage.getItem('token'); if (token) config.headers.Authorization = `Bearer ${token}`; return config; });
export const saveAuth = (data) => { localStorage.setItem('token', data.access_token); localStorage.setItem('user', JSON.stringify(data.user)); };
export const logout = () => { localStorage.removeItem('token'); localStorage.removeItem('user'); };
export const currentUser = () => JSON.parse(localStorage.getItem('user') || 'null');
