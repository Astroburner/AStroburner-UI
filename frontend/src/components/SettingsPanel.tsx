import { useEffect, useState } from 'react';
import { FiRefreshCw, FiDownload, FiBarChart2, FiPackage } from 'react-icons/fi';
import { useAppStore } from '../hooks/useAppStore';
import { apiService } from '../services/api';
import type { AppStats } from '../types';
import LoRAAddForm from './LoRAAddForm';
import LoRAList from './LoRAList';

type SettingsTab = 'models' | 'loras';

export default function SettingsPanel() {
  const { models, setModels, currentModel, setCurrentModel, setIsLoadingModel, isLoadingModel } =
    useAppStore();
  const [stats, setStats] = useState<AppStats | null>(null);
  const [activeTab, setActiveTab] = useState<SettingsTab>('models');

  useEffect(() => {
    loadModels();
    loadStats();
  }, []);

  const loadModels = async () => {
    try {
      const response = await apiService.listModels();
      setModels(response.models);
      
      // Check current model
      const current = await apiService.getCurrentModel();
      if (current.loaded) {
        const currentModelInfo = response.models.find((m) => m.key === current.key);
        if (currentModelInfo) {
          setCurrentModel(currentModelInfo);
        }
      }
    } catch (error) {
      console.error('Error loading models:', error);
    }
  };

  const loadStats = async () => {
    try {
      const response = await apiService.getStats();
      setStats(response);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handleLoadModel = async (modelKey: string) => {
    try {
      setIsLoadingModel(true);
      const response = await apiService.loadModel(modelKey);
      if (response.success) {
        const model = models.find((m) => m.key === modelKey);
        if (model) {
          setCurrentModel(model);
        }
        await loadModels(); // Refresh model list
      }
    } catch (error) {
      console.error('Error loading model:', error);
      alert('Fehler beim Laden des Models');
    } finally {
      setIsLoadingModel(false);
    }
  };

  const handleClearCache = async () => {
    try {
      await apiService.clearGPUCache();
      alert('GPU Cache geleert');
    } catch (error) {
      console.error('Error clearing cache:', error);
    }
  };

  const handleLoRAsChanged = () => {
    // Refresh models/stats when LoRAs change
    loadModels();
    loadStats();
  };

  return (
    <div className="h-full bg-dark-800 overflow-auto p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Tab Navigation */}
        <div className="flex gap-2 border-b border-dark-600">
          <button
            onClick={() => setActiveTab('models')}
            className={`px-6 py-3 font-medium transition-colors flex items-center gap-2 ${
              activeTab === 'models'
                ? 'text-primary-400 border-b-2 border-primary-500'
                : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            <FiDownload />
            Models
          </button>
          <button
            onClick={() => setActiveTab('loras')}
            className={`px-6 py-3 font-medium transition-colors flex items-center gap-2 ${
              activeTab === 'loras'
                ? 'text-primary-400 border-b-2 border-primary-500'
                : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            <FiPackage />
            LoRAs
          </button>
        </div>

        {/* Statistics - Always visible */}
        <section className="bg-dark-700 border border-dark-600 rounded-lg p-6">
          <div className="flex items-center gap-2 mb-4">
            <FiBarChart2 className="text-primary-500" />
            <h2 className="text-xl font-bold text-white">Statistiken</h2>
          </div>
          
          {stats ? (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-dark-800 rounded-lg p-4">
                <div className="text-2xl font-bold text-white">
                  {stats.stats.total_generations}
                </div>
                <div className="text-sm text-gray-400">Total Generierungen</div>
              </div>
              <div className="bg-dark-800 rounded-lg p-4">
                <div className="text-2xl font-bold text-white">
                  {stats.stats.models_used}
                </div>
                <div className="text-sm text-gray-400">Models Verwendet</div>
              </div>
              <div className="bg-dark-800 rounded-lg p-4">
                <div className="text-2xl font-bold text-white">
                  {stats.stats.avg_steps.toFixed(0)}
                </div>
                <div className="text-sm text-gray-400">Ø Steps</div>
              </div>
              <div className="bg-dark-800 rounded-lg p-4">
                <div className="text-2xl font-bold text-white">
                  {stats.stats.avg_guidance.toFixed(1)}
                </div>
                <div className="text-sm text-gray-400">Ø Guidance</div>
              </div>
            </div>
          ) : (
            <div className="text-gray-400">Lade Statistiken...</div>
          )}
        </section>

        {/* Models Tab Content */}
        {activeTab === 'models' && (
          <>
            {/* Models */}
        <section className="bg-dark-700 border border-dark-600 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <FiDownload className="text-primary-500" />
              <h2 className="text-xl font-bold text-white">Models</h2>
            </div>
            <button
              onClick={loadModels}
              className="px-3 py-1 bg-dark-600 hover:bg-dark-500 text-white rounded-lg text-sm transition-colors flex items-center gap-2"
            >
              <FiRefreshCw className="text-sm" />
              Aktualisieren
            </button>
          </div>

          <div className="space-y-3">
            {models.map((model) => (
              <div
                key={model.key}
                className={`flex items-center justify-between p-4 rounded-lg border-2 transition-all ${
                  model.loaded
                    ? 'bg-primary-500/10 border-primary-500'
                    : 'bg-dark-800 border-dark-600 hover:border-dark-500'
                }`}
              >
                <div>
                  <div className="text-white font-medium">{model.name}</div>
                  <div className="text-sm text-gray-400">{model.type}</div>
                </div>
                <div className="flex items-center gap-2">
                  {model.loaded ? (
                    <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm font-medium">
                      Geladen
                    </span>
                  ) : (
                    <button
                      onClick={() => handleLoadModel(model.key)}
                      disabled={isLoadingModel}
                      className="px-4 py-2 bg-primary-600 hover:bg-primary-500 disabled:bg-gray-600 text-white rounded-lg transition-colors disabled:cursor-not-allowed"
                    >
                      {isLoadingModel ? 'Lädt...' : 'Laden'}
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* GPU Settings */}
        <section className="bg-dark-700 border border-dark-600 rounded-lg p-6">
          <h2 className="text-xl font-bold text-white mb-4">GPU Einstellungen</h2>
          
          <div className="space-y-3">
            <button
              onClick={handleClearCache}
              className="w-full px-4 py-3 bg-dark-600 hover:bg-dark-500 text-white rounded-lg transition-colors flex items-center justify-center gap-2"
            >
              <FiRefreshCw />
              GPU Cache Leeren
            </button>

            {stats?.gpu && (
              <div className="p-4 bg-dark-800 rounded-lg">
                <div className="text-sm space-y-2 text-gray-300">
                  <div className="flex justify-between">
                    <span>Device:</span>
                    <span className="font-medium">{stats.gpu.device}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Name:</span>
                    <span className="font-medium">{stats.gpu.name}</span>
                  </div>
                  {stats.gpu.compute_capability && (
                    <div className="flex justify-between">
                      <span>Compute:</span>
                      <span className="font-medium">{stats.gpu.compute_capability}</span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </section>

        {/* Info */}
        <section className="bg-dark-700 border border-dark-600 rounded-lg p-6">
          <h2 className="text-xl font-bold text-white mb-4">Info</h2>
          <div className="text-gray-300 space-y-2 text-sm">
            <div className="flex justify-between">
              <span>Version:</span>
              <span className="font-medium">1.6.0</span>
            </div>
            <div className="flex justify-between">
              <span>Build:</span>
              <span className="font-medium">Desktop</span>
            </div>
          </div>
        </section>
          </>
        )}

        {/* LoRAs Tab Content */}
        {activeTab === 'loras' && (
          <>
            <LoRAAddForm onSuccess={handleLoRAsChanged} />
            <LoRAList onLoRAsChanged={handleLoRAsChanged} />
          </>
        )}
      </div>
    </div>
  );
}
