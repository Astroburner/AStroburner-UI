import { create } from 'zustand';
import type { GeneratedImage, ModelInfo, GPUInfo } from '../types';

interface AppState {
  // Generation state
  generatedImages: GeneratedImage[];
  isGenerating: boolean;
  generationProgress: number;
  
  // Current generation params
  prompt: string;
  negativePrompt: string;
  width: number;
  height: number;
  steps: number;
  guidanceScale: number;
  numImages: number;
  seed: number | null;
  sampler: string;
  scheduler: string;
  
  // Models
  models: ModelInfo[];
  currentModel: ModelInfo | null;
  isLoadingModel: boolean;
  
  // GPU
  gpuInfo: GPUInfo | null;
  
  // UI state
  showSettings: boolean;
  showHistory: boolean;
  selectedTab: 'generate' | 'history' | 'settings';
  
  // Actions
  setGeneratedImages: (images: GeneratedImage[]) => void;
  addGeneratedImages: (images: GeneratedImage[]) => void;
  setIsGenerating: (value: boolean) => void;
  setGenerationProgress: (value: number) => void;
  
  setPrompt: (prompt: string) => void;
  setNegativePrompt: (prompt: string) => void;
  setWidth: (width: number) => void;
  setHeight: (height: number) => void;
  setSteps: (steps: number) => void;
  setGuidanceScale: (scale: number) => void;
  setNumImages: (num: number) => void;
  setSeed: (seed: number | null) => void;
  setSampler: (sampler: string) => void;
  setScheduler: (scheduler: string) => void;
  
  setModels: (models: ModelInfo[]) => void;
  setCurrentModel: (model: ModelInfo | null) => void;
  setIsLoadingModel: (value: boolean) => void;
  
  setGpuInfo: (info: GPUInfo) => void;
  
  setShowSettings: (value: boolean) => void;
  setShowHistory: (value: boolean) => void;
  setSelectedTab: (tab: 'generate' | 'history' | 'settings') => void;
  
  resetParams: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Initial state
  generatedImages: [],
  isGenerating: false,
  generationProgress: 0,
  
  prompt: '',
  negativePrompt: '',
  width: 512,
  height: 512,
  steps: 30,
  guidanceScale: 7.5,
  numImages: 1,
  seed: null,
  sampler: 'DPMSolverMultistep',
  scheduler: 'DDIM',
  
  models: [],
  currentModel: null,
  isLoadingModel: false,
  
  gpuInfo: null,
  
  showSettings: false,
  showHistory: false,
  selectedTab: 'generate',
  
  // Actions
  setGeneratedImages: (images) => set({ generatedImages: images }),
  addGeneratedImages: (images) => set((state) => ({ 
    generatedImages: [...images, ...state.generatedImages] 
  })),
  setIsGenerating: (value) => set({ isGenerating: value }),
  setGenerationProgress: (value) => set({ generationProgress: value }),
  
  setPrompt: (prompt) => set({ prompt }),
  setNegativePrompt: (prompt) => set({ negativePrompt: prompt }),
  setWidth: (width) => set({ width }),
  setHeight: (height) => set({ height }),
  setSteps: (steps) => set({ steps }),
  setGuidanceScale: (scale) => set({ guidanceScale: scale }),
  setNumImages: (num) => set({ numImages: num }),
  setSeed: (seed) => set({ seed }),
  setSampler: (sampler) => set({ sampler }),
  setScheduler: (scheduler) => set({ scheduler }),
  
  setModels: (models) => set({ models }),
  setCurrentModel: (model) => set({ currentModel: model }),
  setIsLoadingModel: (value) => set({ isLoadingModel: value }),
  
  setGpuInfo: (info) => set({ gpuInfo: info }),
  
  setShowSettings: (value) => set({ showSettings: value }),
  setShowHistory: (value) => set({ showHistory: value }),
  setSelectedTab: (tab) => set({ selectedTab: tab }),
  
  resetParams: () => set({
    width: 1024,
    height: 1024,
    steps: 30,
    guidanceScale: 7.5,
    numImages: 1,
    seed: null,
    sampler: 'DPMSolverMultistep',
    scheduler: 'DDIM',
  }),
}));
