import { useState, useEffect } from 'react';
import { FiList, FiTrash2, FiRefreshCw, FiCheck, FiX } from 'react-icons/fi';
import { apiService } from '../services/api';
import { useAppStore } from '../hooks/useAppStore';
import type { LoRA } from '../types';

interface LoRAListProps {
  onLoRAsChanged: () => void;
}

export default function LoRAList({ onLoRAsChanged }: LoRAListProps) {
  const [loras, setLoras] = useState<LoRA[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { currentModel, setActiveLoras } = useAppStore();

  useEffect(() => {
    loadLoRAs();
  }, [currentModel]);

  const loadLoRAs = async () => {
    try {
      setIsLoading(true);
      
      // Load all LoRAs, optionally filter by current model type
      const modelType = currentModel?.type;
      const response = await apiService.listLoRAs(modelType);
      setLoras(response.loras);

      // Update active LoRAs in store
      const activeResponse = await apiService.getActiveLoRAs();
      setActiveLoras(activeResponse.loras);
      
    } catch (error) {
      console.error('Error loading LoRAs:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleActive = async (lora: LoRA) => {
    try {
      const newActiveState = !lora.is_active;
      
      await apiService.setLoRAActive(lora.id, {
        is_active: newActiveState,
        weight: lora.weight
      });

      await loadLoRAs();
      onLoRAsChanged();
      
    } catch (error: any) {
      console.error('Error toggling LoRA:', error);
      
      // Show user-friendly error for max limit
      if (error.response?.status === 400) {
        alert(error.response?.data?.detail || 'Fehler beim Aktivieren der LoRA');
      } else {
        alert('Fehler beim Aktivieren der LoRA');
      }
    }
  };

  const handleDelete = async (lora: LoRA) => {
    if (!confirm(`LoRA "${lora.name}" wirklich löschen?`)) {
      return;
    }

    try {
      await apiService.deleteLoRA(lora.id);
      await loadLoRAs();
      onLoRAsChanged();
    } catch (error) {
      console.error('Error deleting LoRA:', error);
      alert('Fehler beim Löschen der LoRA');
    }
  };

  const handleDeactivateAll = async () => {
    try {
      await apiService.deactivateAllLoRAs();
      await loadLoRAs();
      onLoRAsChanged();
    } catch (error) {
      console.error('Error deactivating all LoRAs:', error);
      alert('Fehler beim Deaktivieren der LoRAs');
    }
  };

  const activeCount = loras.filter(l => l.is_active).length;

  return (
    <div className="bg-dark-700 border border-dark-600 rounded-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <FiList className="text-primary-500" />
          <h2 className="text-xl font-bold text-white">
            Meine LoRAs
            {activeCount > 0 && (
              <span className="ml-2 text-sm font-normal text-primary-400">
                ({activeCount}/5 aktiv)
              </span>
            )}
          </h2>
        </div>
        <div className="flex gap-2">
          {activeCount > 0 && (
            <button
              onClick={handleDeactivateAll}
              className="px-3 py-1 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-lg text-sm transition-colors flex items-center gap-2"
            >
              <FiX className="text-sm" />
              Alle Deaktivieren
            </button>
          )}
          <button
            onClick={loadLoRAs}
            disabled={isLoading}
            className="px-3 py-1 bg-dark-600 hover:bg-dark-500 text-white rounded-lg text-sm transition-colors flex items-center gap-2 disabled:opacity-50"
          >
            <FiRefreshCw className={`text-sm ${isLoading ? 'animate-spin' : ''}`} />
            Aktualisieren
          </button>
        </div>
      </div>

      {loras.length === 0 ? (
        <div className="text-center py-8 text-gray-400">
          <FiList className="text-4xl mx-auto mb-2 opacity-50" />
          <p>Keine LoRAs gefunden</p>
          <p className="text-sm mt-1">Fügen Sie oben eine LoRA hinzu</p>
        </div>
      ) : (
        <div className="space-y-3">
          {loras.map((lora) => (
            <div
              key={lora.id}
              className={`p-4 rounded-lg border-2 transition-all ${
                lora.is_active
                  ? 'bg-primary-500/10 border-primary-500'
                  : 'bg-dark-800 border-dark-600'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  {/* Name & Model Type */}
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="text-white font-medium truncate">{lora.name}</h3>
                    <span className="px-2 py-0.5 bg-dark-600 text-gray-300 rounded text-xs font-medium">
                      {lora.model_type}
                    </span>
                    {lora.is_active && (
                      <span className="px-2 py-0.5 bg-green-500/20 text-green-400 rounded text-xs font-medium flex items-center gap-1">
                        <FiCheck className="text-xs" />
                        Aktiv
                      </span>
                    )}
                  </div>

                  {/* File Path */}
                  <div className="text-xs text-gray-500 truncate mb-2">
                    {lora.file_path}
                  </div>

                  {/* Trigger Words */}
                  {lora.trigger_words && (
                    <div className="mb-2">
                      <span className="text-xs text-gray-400">Trigger: </span>
                      <span className="text-xs text-primary-400">{lora.trigger_words}</span>
                    </div>
                  )}

                  {/* Description */}
                  {lora.description && (
                    <p className="text-sm text-gray-400 mb-2">{lora.description}</p>
                  )}

                  {/* Weight */}
                  <div className="text-sm text-gray-400">
                    Stärke: <span className="text-white font-medium">{lora.weight.toFixed(2)}</span>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex flex-col gap-2 ml-4">
                  <button
                    onClick={() => handleToggleActive(lora)}
                    className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                      lora.is_active
                        ? 'bg-red-600/20 hover:bg-red-600/30 text-red-400'
                        : 'bg-primary-600 hover:bg-primary-500 text-white'
                    }`}
                  >
                    {lora.is_active ? 'Deaktivieren' : 'Aktivieren'}
                  </button>
                  
                  <button
                    onClick={() => handleDelete(lora)}
                    className="px-3 py-1.5 bg-dark-600 hover:bg-red-600 text-gray-400 hover:text-white rounded-lg text-sm transition-colors flex items-center justify-center gap-1"
                    title="Löschen"
                  >
                    <FiTrash2 className="text-xs" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
