import { useState } from 'react';
import { FiPlus, FiFolder } from 'react-icons/fi';
import { open } from '@tauri-apps/plugin-dialog';
import { apiService } from '../services/api';

const MODEL_TYPES = [
  'SD1.5',
  'SDXL',
  'SDXL-Turbo',
  'Pony',
  'Illustrious',
  'Flux-Dev',
  'Flux-Kontext',
  'Wan2.1',
  'Wan2.2',
  'Qwen',
  'Qwen-image-edit'
];

interface LoRAAddFormProps {
  onSuccess: () => void;
}

export default function LoRAAddForm({ onSuccess }: LoRAAddFormProps) {
  const [name, setName] = useState('');
  const [filePath, setFilePath] = useState('');
  const [modelType, setModelType] = useState('SDXL');
  const [triggerWords, setTriggerWords] = useState('');
  const [description, setDescription] = useState('');
  const [weight, setWeight] = useState(1.0);
  const [isAdding, setIsAdding] = useState(false);

  const handleSelectFile = async () => {
    try {
      const selected = await open({
        multiple: false,
        filters: [
          {
            name: 'LoRA Files',
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
      }
    } catch (error) {
      console.error('Error selecting file:', error);
      alert('Fehler beim Datei-Auswahl');
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
      await apiService.addLoRA({
        name: name.trim(),
        file_path: filePath.trim(),
        model_type: modelType,
        trigger_words: triggerWords.trim() || undefined,
        description: description.trim() || undefined,
        weight
      });

      // Reset form
      setName('');
      setFilePath('');
      setModelType('SDXL');
      setTriggerWords('');
      setDescription('');
      setWeight(1.0);

      onSuccess();
    } catch (error: any) {
      console.error('Error adding LoRA:', error);
      alert(error.response?.data?.detail || 'Fehler beim Hinzufügen der LoRA');
    } finally {
      setIsAdding(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-dark-700 border border-dark-600 rounded-lg p-6">
      <div className="flex items-center gap-2 mb-4">
        <FiPlus className="text-primary-500" />
        <h2 className="text-xl font-bold text-white">LoRA Hinzufügen</h2>
      </div>

      <div className="space-y-4">
        {/* File Path */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Datei *
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={filePath}
              onChange={(e) => setFilePath(e.target.value)}
              placeholder="C:\path\to\lora.safetensors"
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
            placeholder="Meine LoRA"
            className="w-full px-4 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-primary-500"
            required
          />
        </div>

        {/* Model Type */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Model Type *
          </label>
          <select
            value={modelType}
            onChange={(e) => setModelType(e.target.value)}
            className="w-full px-4 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white focus:outline-none focus:border-primary-500"
            required
          >
            {MODEL_TYPES.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>

        {/* Trigger Words */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Trigger Words (Optional)
          </label>
          <input
            type="text"
            value={triggerWords}
            onChange={(e) => setTriggerWords(e.target.value)}
            placeholder="trigger1, trigger2, trigger3"
            className="w-full px-4 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-primary-500"
          />
          <p className="mt-1 text-xs text-gray-500">
            Komma-getrennte Trigger-Wörter für diese LoRA
          </p>
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Beschreibung (Optional)
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Was macht diese LoRA?"
            rows={3}
            className="w-full px-4 py-2 bg-dark-800 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-primary-500 resize-none"
          />
        </div>

        {/* Default Weight */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Standard Stärke: {weight.toFixed(2)}
          </label>
          <input
            type="range"
            min="0"
            max="2"
            step="0.05"
            value={weight}
            onChange={(e) => setWeight(parseFloat(e.target.value))}
            className="w-full"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>0.0</span>
            <span>1.0</span>
            <span>2.0</span>
          </div>
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
              LoRA Hinzufügen
            </>
          )}
        </button>
      </div>
    </form>
  );
}
