import { useEffect, useState } from 'react';
import { FiClock, FiTrash2, FiSearch, FiDownload } from 'react-icons/fi';
import { apiService } from '../services/api';
import type { Generation } from '../types';

export default function HistoryPanel() {
  const [generations, setGenerations] = useState<Generation[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  // Helper function to extract filename from Windows/Unix paths
  const getFilename = (filepath: string): string => {
    if (!filepath) return '';
    // Handle both Windows (\) and Unix (/) path separators
    const parts = filepath.split(/[\\/]/);
    return parts[parts.length - 1];
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const response = await apiService.getHistory(100);
      setGenerations(response.generations);
    } catch (error) {
      console.error('Error loading history:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadHistory();
      return;
    }

    try {
      setLoading(true);
      const response = await apiService.searchHistory(searchQuery, 100);
      setGenerations(response.generations);
    } catch (error) {
      console.error('Error searching:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Möchtest du diese Generation wirklich löschen?')) return;

    try {
      await apiService.deleteGeneration(id);
      setGenerations(generations.filter((g) => g.id !== id));
    } catch (error) {
      console.error('Error deleting generation:', error);
    }
  };

  const handleDownload = async (gen: Generation) => {
    try {
      const filename = getFilename(gen.file_path);
      const imageUrl = `http://127.0.0.1:8000/outputs/${filename}`;
      
      const response = await fetch(imageUrl);
      const blob = await response.blob();
      
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error downloading image:', error);
      alert('Fehler beim Herunterladen des Bildes');
    }
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center bg-dark-800">
        <div className="text-gray-400">Lade History...</div>
      </div>
    );
  }

  return (
    <div className="h-full bg-dark-800 flex flex-col">
      {/* Search Bar */}
      <div className="p-4 border-b border-dark-600">
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <FiSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Suche in Prompts..."
              className="w-full pl-10 pr-4 py-2 bg-dark-700 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <button
            onClick={handleSearch}
            className="px-4 py-2 bg-primary-600 hover:bg-primary-500 text-white rounded-lg transition-colors"
          >
            Suchen
          </button>
          {searchQuery && (
            <button
              onClick={() => {
                setSearchQuery('');
                loadHistory();
              }}
              className="px-4 py-2 bg-dark-700 hover:bg-dark-600 text-white rounded-lg transition-colors"
            >
              Reset
            </button>
          )}
        </div>
      </div>

      {/* History List - NEUE KOMPAKTE LAYOUT */}
      <div className="flex-1 overflow-auto p-4">
        {generations.length === 0 ? (
          <div className="text-center text-gray-500 py-12">
            <FiClock className="mx-auto text-6xl mb-4 opacity-20" />
            <p>Keine Generationen gefunden</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
            {generations.map((gen) => (
              <div
                key={gen.id}
                className="bg-dark-700 border border-dark-600 rounded-lg p-4 hover:border-primary-500 transition-colors"
              >
                {/* Header mit Thumbnail und Actions */}
                <div className="flex gap-3 mb-3">
                  {/* Thumbnail - Kleinere, kompaktere Größe */}
                  <div className="w-20 h-20 bg-dark-600 rounded-lg flex-shrink-0 overflow-hidden">
                    {gen.file_path ? (
                      <img
                        src={`http://127.0.0.1:8000/outputs/${getFilename(gen.file_path)}`}
                        alt={gen.prompt}
                        className="w-full h-full object-cover cursor-pointer hover:opacity-80 transition-opacity"
                        onClick={() => window.open(`http://127.0.0.1:8000/outputs/${getFilename(gen.file_path)}`, '_blank')}
                        onError={(e) => {
                          e.currentTarget.style.display = 'none';
                          e.currentTarget.parentElement!.classList.add('flex', 'items-center', 'justify-center');
                          e.currentTarget.parentElement!.innerHTML = `<span class="text-gray-500 text-xs">${gen.width}x${gen.height}</span>`;
                        }}
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-gray-500 text-xs">
                        {gen.width}x{gen.height}
                      </div>
                    )}
                  </div>

                  {/* Prompt und Actions */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <h3 className="text-white font-medium text-sm" title={gen.prompt} style={{ wordWrap: 'break-word', overflowWrap: 'break-word', maxWidth: '100%' }}>
                        {gen.prompt}
                      </h3>
                      <div className="flex gap-1 flex-shrink-0">
                        <button
                          onClick={() => handleDownload(gen)}
                          className="p-2 text-green-400 hover:text-green-300 hover:bg-dark-600 rounded transition-colors"
                          title="Herunterladen"
                        >
                          <FiDownload size={16} />
                        </button>
                        <button
                          onClick={() => handleDelete(gen.id)}
                          className="p-2 text-red-400 hover:text-red-300 hover:bg-dark-600 rounded transition-colors"
                          title="Löschen"
                        >
                          <FiTrash2 size={16} />
                        </button>
                      </div>
                    </div>
                    
                    {/* Datum */}
                    <div className="text-xs text-gray-500">
                      {new Date(gen.created_at).toLocaleString('de-DE')}
                    </div>
                  </div>
                </div>

                {/* Details Grid - Kompakt in 2 Spalten */}
                <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-xs">
                  {/* Linke Spalte */}
                  <div className="space-y-1">
                    <div className="text-gray-400">
                      Model: <span className="text-gray-300">{gen.model_key}</span>
                    </div>
                    <div className="text-gray-400">
                      Size: <span className="text-gray-300">{gen.width}x{gen.height}</span>
                    </div>
                    <div className="text-gray-400">
                      Steps: <span className="text-gray-300">{gen.steps}</span>
                    </div>
                    <div className="text-gray-400">
                      Seed: <span className="text-gray-300">{gen.seed || 'Random'}</span>
                    </div>
                  </div>

                  {/* Rechte Spalte */}
                  <div className="space-y-1">
                    <div className="text-gray-400">
                      CFG: <span className="text-gray-300">{gen.guidance_scale.toFixed(1)}</span>
                    </div>
                    {gen.scheduler && (
                      <div className="text-gray-400">
                        Scheduler: <span className="text-gray-300">{gen.scheduler}</span>
                      </div>
                    )}
                    {gen.denoise_strength !== null && gen.denoise_strength !== undefined && (
                      <div className="text-gray-400">
                        Denoise: <span className="text-gray-300">{gen.denoise_strength.toFixed(2)}</span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Negative Prompt - Wenn vorhanden */}
                {gen.negative_prompt && (
                  <div className="mt-3 pt-3 border-t border-dark-600">
                    <div className="text-xs text-gray-400 mb-1">Negative Prompt:</div>
                    <div className="text-xs text-gray-300 line-clamp-2" title={gen.negative_prompt}>
                      {gen.negative_prompt}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
