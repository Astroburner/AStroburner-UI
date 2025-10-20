import { useState, useEffect } from 'react';
import { FiPlus, FiFolder, FiImage } from 'react-icons/fi';
import { open } from '@tauri-apps/plugin-dialog';
import { apiService } from '../services/api';

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
  const [isAdding, setIsAdding] = useState(false);
  const [isDetecting, setIsDetecting] = useState(false);
  const [autoDetect, setAutoDetect] = useState(true);
  
  const [modelTypes, setModelTypes] = useState<string[]>([]);
  const [precisions, setPrecisions] = useState<string[]>([]);

  useEffect(() => {
    loadModelTypes();
  }, []);

  const loadModelTypes = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/custom-models/model-types');
      const data = await response.json();
      setModelTypes(data.model_types);
      setPrecisions(data.precisions);
    } catch (error) {
      console.error('Error loading model types:', error);
    }
  };

  const handleSelectFile = async () => {
    try {
      const selected = await open({
        multiple: false,
        filters: [
          {
            name: 'Safetensors Files',
            extensions: ['safetensors']
          }
        ]
      });

      if (selected && typeof selected === 'string') {
        setFilePath(selected);
        
        // Auto-fill name from filename if empty
        if (!name) {
          const filename = selected.split(/[\\/]/).pop()?.replace('.safetensors', '') || '';
          setName(filename);
        }

        // Auto-detect model type if enabled
        if (autoDetect) {
          await detectModelType(selected);
        }
      }
    } catch (error) {
      console.error('Error selecting file:', error);
      alert('Fehler beim Datei-Auswahl');
    }
  };

  const handleSelectThumbnail = async () => {
    try {
      const selected = await open({
        multiple: false,
        filters: [
          {
            name: 'Image Files',
            extensions: ['png', 'jpg', 'jpeg', 'webp']
          }
        ]
      });

      if (selected && typeof selected === 'string') {
        setThumbnailPath(selected);
      }
    } catch (error) {
      console.error('Error selecting thumbnail:', error);
    }
  };

  const detectModelType = async (path: string) => {
    try {
      setIsDetecting(true);
      const response = await fetch('http://127.0.0.1:8000/api/custom-models/detect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: path })
      });
      
      const data = await response.json();
      setModelType(data.model_type);
      setPrecision(data.precision);
    } catch (error) {
      console.error('Error detecting model type:', error);
    } finally {
      setIsDetecting(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!name.trim() || !filePath.trim()) {
      alert('Name und Dateipfad sind erforderlich');
      return;
    }

    try {
      setIsAdding(true);
      const response = await fetch('http://127.0.0.1:8000/api/custom-models', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name.trim(),
          file_path: filePath.trim(),
          model_type: autoDetect ? null : modelType,
          precision: autoDetect ? null : precision,
          description: description.trim() || null,
          thumbnail_path: thumbnailPath.trim() || null
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Fehler beim Hinzufügen');
      }

      const data = await response.json();
      
      // Show detection results
      alert(`Model hinzugefügt!\nTyp: ${data.detected_type}\nPräzision: ${data.detected_precision}`);

      // Reset form
      setName('');
      setFilePath('');
      setModelType('');
      setPrecision('');
      setDescription('');
      setThumbnailPath('');

      onSuccess();
    } catch (error: any) {
      console.error('Error adding custom model:', error);
      alert(error.message || 'Fehler beim Hinzufügen des Custom Models');
    } finally {
      setIsAdding(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-dark-700 border border-dark-600 rounded-lg p-6">
      <div className="flex items-center gap-2 mb-4">
        <FiPlus className="text-primary-500" />
        <h2 className="text-xl font-bold text-white">Custom Model Hinzufügen</h2>
      </div>

      <div className="space-y-4">
        {/* File Path */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Model Datei (.safetensors) *
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={filePath}
              onChange={(e) => setFilePath(e.target.value)}
              placeholder="C:\path\to\model.safetensors"
              className="flex-1 px-4 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-primary-500"
              required
            />
            <button
              type="button"
              onClick={handleSelectFile}
              className="px-4 py-2 bg-dark-600 hover:bg-dark-500 text-white rounded-lg transition-colors flex items-center gap-2"
            >
              <FiFolder />
              Durchsuchen
            </button>
          </div>
          <p className="mt-1 text-xs text-gray-500">
            Unterstützt: FP32, FP16, BF16, FP8 Safetensors
          </p>
        </div>

        {/* Name */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Name *
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Mein Custom Model"
            className="w-full px-4 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-primary-500"
            required
          />
        </div>

        {/* Auto-Detect Toggle */}
        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            id="autoDetect"
            checked={autoDetect}
            onChange={(e) => setAutoDetect(e.target.checked)}
            className="w-4 h-4"
          />
          <label htmlFor="autoDetect" className="text-sm text-gray-300">
            Automatische Typ-Erkennung
          </label>
          {isDetecting && (
            <span className="text-xs text-primary-400">Erkenne...</span>
          )}
        </div>

        {/* Manual Model Type Selection */}
        {!autoDetect && (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Model Typ
              </label>
              <select
                value={modelType}
                onChange={(e) => setModelType(e.target.value)}
                className="w-full px-4 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white focus:outline-none focus:border-primary-500"
              >
                <option value="">-- Typ auswählen --</option>
                {modelTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Präzision
              </label>
              <select
                value={precision}
                onChange={(e) => setPrecision(e.target.value)}
                className="w-full px-4 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white focus:outline-none focus:border-primary-500"
              >
                <option value="">-- Präzision auswählen --</option>
                {precisions.map(prec => (
                  <option key={prec} value={prec}>{prec}</option>
                ))}
              </select>
            </div>
          </>
        )}

        {/* Detected Type Display (when auto-detect) */}
        {autoDetect && (modelType || precision) && (
          <div className="p-3 bg-primary-500/10 border border-primary-500/50 rounded-lg">
            <div className="text-sm text-primary-300">
              <strong>Erkannt:</strong>
              {modelType && <span className="ml-2">Typ: {modelType}</span>}
              {precision && <span className="ml-2">Präzision: {precision}</span>}
            </div>
          </div>
        )}

        {/* Thumbnail (Optional) */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Vorschau Thumbnail (Optional)
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={thumbnailPath}
              onChange={(e) => setThumbnailPath(e.target.value)}
              placeholder="C:\path\to\thumbnail.png"
              className="flex-1 px-4 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-primary-500"
            />
            <button
              type="button"
              onClick={handleSelectThumbnail}
              className="px-4 py-2 bg-dark-600 hover:bg-dark-500 text-white rounded-lg transition-colors flex items-center gap-2"
            >
              <FiImage />
              Bild
            </button>
          </div>
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Beschreibung (Optional)
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Informationen über dieses Model..."
            rows={3}
            className="w-full px-4 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-primary-500 resize-none"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isAdding || !name.trim() || !filePath.trim()}
          className="w-full px-4 py-3 bg-primary-600 hover:bg-primary-500 disabled:bg-gray-600 text-white rounded-lg font-medium transition-colors disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {isAdding ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Wird hinzugefügt...
            </>
          ) : (
            <>
              <FiPlus />
              Custom Model Hinzufügen
            </>
          )}
        </button>
      </div>
    </form>
  );
}
