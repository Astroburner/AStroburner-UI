import { useState, useEffect } from 'react';
import { FiList, FiTrash2, FiRefreshCw, FiCheck, FiImage, FiDownload } from 'react-icons/fi';
import { useAppStore } from '../hooks/useAppStore';

interface CustomModel {
  id: number;
  name: string;
  file_path: string;
  model_type: string;
  precision: string;
  description: string | null;
  thumbnail_path: string | null;
  is_active: boolean;
  created_at: string;
}

interface CustomModelListProps {
  onModelsChanged: () => void;
}

export default function CustomModelList({ onModelsChanged }: CustomModelListProps) {
  const { showToast, setCurrentModel } = useAppStore();
  const [models, setModels] = useState<CustomModel[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadModels();
  }, []);

  const loadModels = async () => {
    try {
      setIsLoading(true);
      const response = await fetch('http://127.0.0.1:8000/api/custom-models');
      const data = await response.json();
      setModels(data.models);
    } catch (error) {
      console.error('Error loading custom models:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (model: CustomModel) => {
    if (!confirm(`Custom Model "${model.name}" wirklich löschen?`)) {
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/custom-models/${model.id}`, {
        method: 'DELETE'
      });

      if (!response.ok) {
        throw new Error('Fehler beim Löschen');
      }

      await loadModels();
      onModelsChanged();
    } catch (error) {
      console.error('Error deleting custom model:', error);
      alert('Fehler beim Löschen des Custom Models');
    }
  };

  const handleLoadModel = async (model: CustomModel) => {
    try {
      showToast('Custom Model wird geladen...', 'loading');
      
      const response = await fetch('http://127.0.0.1:8000/api/custom-models/load', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model_id: model.id })
      });

      if (!response.ok) {
        throw new Error('Fehler beim Laden');
      }

      showToast('Fertig in VRAM geladen', 'success');
      
      // CRITICAL: Update currentModel in App Store after loading custom model
      setCurrentModel({
        key: `custom:${model.name}`,
        name: model.name,
        type: model.model_type,
        loaded: true,
        downloaded: true
      });
      
      await loadModels();
      onModelsChanged();
    } catch (error) {
      console.error('Error loading custom model:', error);
      showToast('Fehler beim Laden', 'error');
    }
  };

  return (
    <div className="bg-dark-700 border border-dark-600 rounded-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <FiList className="text-primary-500" />
          <h2 className="text-xl font-bold text-white">
            Custom Models
            {models.length > 0 && (
              <span className="ml-2 text-sm font-normal text-gray-400">
                ({models.length})
              </span>
            )}
          </h2>
        </div>
        <button
          onClick={loadModels}
          disabled={isLoading}
          className="px-3 py-1 bg-dark-600 hover:bg-dark-500 text-white rounded-lg text-sm transition-colors flex items-center gap-2 disabled:opacity-50"
        >
          <FiRefreshCw className={`text-sm ${isLoading ? 'animate-spin' : ''}`} />
          Aktualisieren
        </button>
      </div>

      {models.length === 0 ? (
        <div className="text-center py-8 text-gray-400">
          <FiList className="text-4xl mx-auto mb-2 opacity-50" />
          <p>Keine Custom Models gefunden</p>
          <p className="text-sm mt-1">Füge oben ein Custom Model hinzu</p>
        </div>
      ) : (
        <div className="space-y-3">
          {models.map((model) => (
            <div
              key={model.id}
              className="p-4 rounded-lg border-2 bg-dark-800 border-dark-600 hover:border-dark-500 transition-all"
            >
              <div className="flex gap-4">
                {/* Thumbnail */}
                {model.thumbnail_path ? (
                  <div className="w-24 h-24 bg-dark-600 rounded-lg flex-shrink-0 overflow-hidden border border-dark-500">
                    <img
                      src={`http://127.0.0.1:8000/api/thumbnail?path=${encodeURIComponent(model.thumbnail_path)}`}
                      alt={model.name}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        const target = e.currentTarget;
                        target.style.display = 'none';
                        const parent = target.parentElement;
                        if (parent) {
                          parent.innerHTML = '<div class="w-full h-full flex items-center justify-center text-gray-500 text-2xl">🖼️</div>';
                        }
                      }}
                    />
                  </div>
                ) : (
                  <div className="w-24 h-24 bg-dark-600 rounded-lg flex-shrink-0 flex items-center justify-center border border-dark-500">
                    <FiImage className="text-gray-500 text-3xl" />
                  </div>
                )}

                {/* Info */}
                <div className="flex-1 min-w-0">
                  {/* Title Row */}
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="text-white font-semibold text-base">{model.name}</h3>
                    {model.is_active && (
                      <span className="px-2 py-0.5 bg-green-500/20 text-green-400 rounded text-xs font-medium flex items-center gap-1 whitespace-nowrap">
                        <FiCheck className="text-xs" />
                        Aktiv
                      </span>
                    )}
                  </div>
                  
                  {/* Badges Row */}
                  <div className="flex items-center gap-2 mb-2 flex-wrap">
                    <span className="px-2 py-0.5 bg-primary-500/20 text-primary-400 rounded text-xs font-medium whitespace-nowrap">
                      {model.model_type}
                    </span>
                    <span className="px-2 py-0.5 bg-accent-500/20 text-accent-400 rounded text-xs font-medium whitespace-nowrap">
                      {model.precision}
                    </span>
                  </div>

                  {/* Description */}
                  {model.description && (
                    <p className="text-sm text-gray-300 mb-2 line-clamp-2">{model.description}</p>
                  )}

                  {/* File Path - with proper wrapping */}
                  <div className="text-xs text-gray-500 mb-2 break-all line-clamp-1" title={model.file_path}>
                    📁 {model.file_path}
                  </div>

                  {/* Bottom Row: Date + Action Buttons */}
                  <div className="flex items-center justify-between gap-2">
                    <div className="text-xs text-gray-600">
                      {new Date(model.created_at).toLocaleDateString('de-DE')}
                    </div>

                    {/* Action Buttons */}
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleLoadModel(model)}
                        disabled={model.is_active}
                        className="px-3 py-1.5 bg-primary-600 hover:bg-primary-500 text-white rounded-lg text-sm transition-colors flex items-center gap-1.5 disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
                        title={model.is_active ? "Bereits geladen" : "Model laden"}
                      >
                        <FiDownload className="text-sm" />
                        Laden
                      </button>
                      <button
                        onClick={() => handleDelete(model)}
                        className="px-3 py-1.5 bg-dark-600 hover:bg-red-600 text-gray-400 hover:text-white rounded-lg text-sm transition-colors flex items-center gap-1.5"
                        title="Löschen"
                      >
                        <FiTrash2 className="text-sm" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
