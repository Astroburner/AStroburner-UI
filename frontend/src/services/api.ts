import axios from 'axios';
import type {
  GenerateImageRequest,
  GenerateImageResponse,
  ModelInfo,
  GPUInfo,
  Generation,
  AppStats
} from '../types';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes for generation
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health check
  async healthCheck() {
    const response = await api.get('/health');
    return response.data;
  },

  // GPU
  async getGPUInfo(): Promise<GPUInfo> {
    const response = await api.get('/gpu/info');
    return response.data;
  },

  async clearGPUCache() {
    const response = await api.post('/gpu/clear-cache');
    return response.data;
  },

  // Models
  async listModels(): Promise<{ models: ModelInfo[] }> {
    const response = await api.get('/models');
    return response.data;
  },

  async getCurrentModel() {
    const response = await api.get('/models/current');
    return response.data;
  },

  async loadModel(modelKey: string) {
    const response = await api.post('/models/load', { model_key: modelKey });
    return response.data;
  },

  // Generation
  async generateImage(params: GenerateImageRequest): Promise<GenerateImageResponse> {
    const response = await api.post('/generate/image', params);
    return response.data;
  },

  // History
  async getHistory(limit: number = 50): Promise<{ generations: Generation[]; count: number }> {
    const response = await api.get('/history', { params: { limit } });
    return response.data;
  },

  async getGeneration(id: number): Promise<Generation> {
    const response = await api.get(`/history/${id}`);
    return response.data;
  },

  async deleteGeneration(id: number) {
    const response = await api.delete(`/history/${id}`);
    return response.data;
  },

  async searchHistory(query: string, limit: number = 50) {
    const response = await api.get('/history/search', { params: { q: query, limit } });
    return response.data;
  },

  // Stats
  async getStats(): Promise<AppStats> {
    const response = await api.get('/stats');
    return response.data;
  },
};
