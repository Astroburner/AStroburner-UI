import { useState, useEffect } from 'react';
import { FiPlus, FiX, FiFolder, FiImage } from 'react-icons/fi';
import { open } from '@tauri-apps/plugin-dialog';

interface CustomModelAddFormProps {
  onSuccess: () => void;
}

export default function CustomModelAddForm({ onSuccess }: CustomModelAddFormProps) {
  const [name, setName] = useState('');
  const [filePath, setFilePath] = useState('');
  const [modelType, setModelType] = useState('');
  const [precision, setPrecision] = useState('');
  const [description, setDescription] = useState('');
  const [thumbnailPath, setThumbnailPath] = useState('');
  const [autoDetect, setAutoDetect] = useState(true);
  const [isDetecting, setIsDetecting] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [availableModelTypes, setAvailableModelTypes] = useState<string[]>([]);
  const [availablePrecisions, setAvailablePrecisions] = useState<string[]>([]);

  useEffect(() => {
    loadSupportedTypes();
  }, []);

  const loadSupportedTypes = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/custom-models/model-types');
      const data = await response.json();
      setAvailableModelTypes(data.model_types);
      setAvailablePrecisions(data.precisions);
    } catch (error) {
      console.error('Error loading supported types:', error);
    }
  };

  const handleSelectFile = async () => {
    try {
      const selected = await open({
        multiple: false,
        filters: [{ name: 'Safetensors Files', extensions: ['safetensors'] }]
      });

      if (selected && typeof selected === 'string') {
        setFilePath(selected);
        
        // Auto-extract name from filename if name is empty
        if (!name) {
          const filename = selected.split(/[\\/]/).pop()?.replace('.safetensors', '') || '';
          setName(filename);
        }

        // Auto-detect if enabled
        if (autoDetect) {
          await detectModelType(selected);
        }
      }
    } catch (error) {
      console.error('Error selecting file:', error);
    }
  };

  const handleSelectThumbnail = async () => {
    try {
      const selected = await open({
        multiple: false,
        filters: [{ name: 'Images', extensions: ['png', 'jpg', 'jpeg', 'webp'] }]
      });

      if (selected && typeof selected === 'string') {
        setThumbnailPath(selected);
      }
    } catch (error) {
      console.error('Error selecting thumbnail:', error);
    }
  };

  const detectModelType = async (path: string) => {
    setIsDetecting(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/custom-models/detect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: path })
      });

      if (!response.ok) {
        throw new Error('Detection failed');
      }

      const data = await response.json();
      setModelType(data.model_type);
      setPrecision(data.precision);
    } catch (error) {
      console.error('Error detecting model type:', error);
      alert('Fehler bei der automatischen Erkennung');
    } finally {
      setIsDetecting(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!name || !filePath) {
      alert('Bitte Name und Datei auswählen');
      return;
    }

    setIsSaving(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/custom-models', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name,
          file_path: filePath,
          model_type: autoDetect ? undefined : modelType,
          precision: autoDetect ? undefined : precision,
          description: description || undefined,
          thumbnail_path: thumbnailPath || undefined
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Fehler beim Hinzufügen');
      }

      // Reset form
      setName('');
      setFilePath('');
      setModelType('');
      setPrecision('');
      setDescription('');
      setThumbnailPath('');
      
      onSuccess();
      alert('Custom Model erfolgreich hinzugefügt!');
    } catch (error) {
      console.error('Error adding custom model:', error);
      alert(`Fehler: ${error instanceof Error ? error.message : 'Unbekannter Fehler'}`);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="bg-dark-700 border border-dark-600 rounded-lg p-6 mb-6">
      <div className="flex items-center gap-2 mb-4">
        <FiPlus className="text-primary-500" />
        <h2 className="text-xl font-bold text-white">Custom Model hinzufügen</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Name */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Name *
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="z.B. Big Love XL V04"
            required
            className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-primary-500"
          />
        </div>

        {/* File Path */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Model-Datei (.safetensors) *
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={filePath}
              readOnly
              placeholder="Datei auswählen..."
              className="flex-1 px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none"
            />
            <button
              type="button"
              onClick={handleSelectFile}
              className="px-4 py-2 bg-primary-600 hover:bg-primary-500 text-white rounded-lg transition-colors flex items-center gap-2"
            >
              <FiFolder />
              Durchsuchen
            </button>
          </div>
        </div>

        {/* Auto-Detect Toggle */}
        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            id="autoDetect"
            checked={autoDetect}
            onChange={(e) => setAutoDetect(e.target.checked)}
            className="w-4 h-4 text-primary-600 bg-dark-800 border-dark-600 rounded focus:ring-primary-500"
          />
          <label htmlFor="autoDetect" className="text-sm text-gray-300">
            Model-Typ und Präzision automatisch erkennen
          </label>
          {isDetecting && (
            <span className="text-xs text-primary-400 animate-pulse">Erkenne...</span>
          )}
        </div>

        {/* Manual Model Type & Precision Selection (when auto-detect is off) */}
        {!autoDetect && (
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Model-Typ
              </label>
              <select
                value={modelType}
                onChange={(e) => setModelType(e.target.value)}
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white focus:outline-none focus:border-primary-500"
              >
                <option value="">Wählen...</option>
                {availableModelTypes.map((type) => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Präzision
              </label>
              <select
                value={precision}
                onChange={(e) => setPrecision(e.target.value)}
                className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white focus:outline-none focus:border-primary-500"
              >
                <option value="">Wählen...</option>
                {availablePrecisions.map((prec) => (
                  <option key={prec} value={prec}>{prec}</option>
                ))}
              </select>
            </div>
          </div>
        )}

        {/* Detected/Selected Type & Precision Display */}
        {(modelType || precision) && (
          <div className="flex gap-2">
            {modelType && (
              <span className="px-2.5 py-1 bg-primary-500/20 text-primary-400 rounded text-sm">
                {modelType}
              </span>
            )}
            {precision && (
              <span className="px-2.5 py-1 bg-accent-500/20 text-accent-400 rounded text-sm">
                {precision}
              </span>
            )}
          </div>
        )}

        {/* Optional Thumbnail */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Vorschaubild (optional)
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={thumbnailPath}
              readOnly
              placeholder="Optional: Thumbnail auswählen..."
              className="flex-1 px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none"
            />
            <button
              type="button"
              onClick={handleSelectThumbnail}
              className="px-4 py-2 bg-dark-600 hover:bg-dark-500 text-white rounded-lg transition-colors flex items-center gap-2"
            >
              <FiImage />
              Bild
            </button>
            {thumbnailPath && (
              <button
                type="button"
                onClick={() => setThumbnailPath('')}
                className="px-3 py-2 bg-dark-600 hover:bg-red-600 text-gray-400 hover:text-white rounded-lg transition-colors"
                title="Entfernen"
              >
                <FiX />
              </button>
            )}
          </div>
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Beschreibung (optional)
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="z.B. Hochqualitatives SDXL Model für realistische Portraits..."
            rows={3}
            className="w-full px-3 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-primary-500 resize-none"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isSaving || isDetecting || !name || !filePath}
          className="w-full px-4 py-2 bg-primary-600 hover:bg-primary-500 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
        >
          {isSaving ? 'Wird hinzugefügt...' : 'Custom Model hinzufügen'}
        </button>
      </form>
    </div>
  );
}
