import { useState, useEffect } from 'react';
import { FiList, FiTrash2, FiRefreshCw, FiCheck, FiImage } from 'react-icons/fi';

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
                  <div className="w-20 h-20 bg-dark-600 rounded-lg flex-shrink-0 overflow-hidden">
                    <img
                      src={`file://${model.thumbnail_path}`}
                      alt={model.name}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        e.currentTarget.style.display = 'none';
                        e.currentTarget.parentElement!.innerHTML = `<div class="w-full h-full flex items-center justify-center"><span class="text-gray-500 text-2xl"><FiImage /></span></div>`;
                      }}
                    />
                  </div>
                ) : (
                  <div className="w-20 h-20 bg-dark-600 rounded-lg flex-shrink-0 flex items-center justify-center">
                    <FiImage className="text-gray-500 text-2xl" />
                  </div>
                )}

                {/* Info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="text-white font-medium">{model.name}</h3>
                        {model.is_active && (
                          <span className="px-2 py-0.5 bg-green-500/20 text-green-400 rounded text-xs font-medium flex items-center gap-1">
                            <FiCheck className="text-xs" />
                            Aktiv
                          </span>
                        )}
                      </div>
                      
                      <div className="flex items-center gap-2 mb-2">
                        <span className="px-2 py-0.5 bg-primary-500/20 text-primary-400 rounded text-xs font-medium">
                          {model.model_type}
                        </span>
                        <span className="px-2 py-0.5 bg-accent-500/20 text-accent-400 rounded text-xs font-medium">
                          {model.precision}
                        </span>
                      </div>

                      {model.description && (
                        <p className="text-sm text-gray-400 mb-2">{model.description}</p>
                      )}

                      <div className="text-xs text-gray-500 truncate">
                        {model.file_path}
                      </div>
                    </div>

                    {/* Actions */}
                    <button
                      onClick={() => handleDelete(model)}
                      className="px-3 py-1.5 bg-dark-600 hover:bg-red-600 text-gray-400 hover:text-white rounded-lg text-sm transition-colors flex items-center justify-center gap-1"
                      title="Löschen"
                    >
                      <FiTrash2 className="text-xs" />
                    </button>
                  </div>

                  <div className="text-xs text-gray-500">
                    Hinzugefügt: {new Date(model.created_at).toLocaleDateString('de-DE')}
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
