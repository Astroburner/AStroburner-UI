import { useEffect, useState } from 'react';
import { FiClock, FiTrash2, FiSearch } from 'react-icons/fi';
import { apiService } from '../services/api';
import type { Generation } from '../types';

export default function HistoryPanel() {
  const [generations, setGenerations] = useState<Generation[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

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

      {/* History List */}
      <div className="flex-1 overflow-auto p-4">
        {generations.length === 0 ? (
          <div className="text-center text-gray-500 py-12">
            <FiClock className="mx-auto text-6xl mb-4 opacity-20" />
            <p>Keine Generationen gefunden</p>
          </div>
        ) : (
          <div className="space-y-4">
            {generations.map((gen) => (
              <div
                key={gen.id}
                className="bg-dark-700 border border-dark-600 rounded-lg p-4 hover:border-primary-500 transition-colors"
              >
                <div className="flex gap-4">
                  {/* Thumbnail placeholder */}
                  <div className="w-24 h-24 bg-dark-600 rounded-lg flex-shrink-0 flex items-center justify-center text-gray-500 text-xs">
                    {gen.width}x{gen.height}
                  </div>

                  {/* Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <h3 className="text-white font-medium truncate">{gen.prompt}</h3>
                      <button
                        onClick={() => handleDelete(gen.id)}
                        className="text-red-400 hover:text-red-300 transition-colors flex-shrink-0"
                        title="Löschen"
                      >
                        <FiTrash2 />
                      </button>
                    </div>
                    
                    <div className="text-sm text-gray-400 space-y-1">
                      <div>Model: <span className="text-gray-300">{gen.model_key}</span></div>
                      <div>
                        Size: <span className="text-gray-300">{gen.width}x{gen.height}</span>
                        {' • '}
                        Steps: <span className="text-gray-300">{gen.steps}</span>
                        {' • '}
                        Guidance: <span className="text-gray-300">{gen.guidance_scale}</span>
                      </div>
                      {gen.seed && (
                        <div>Seed: <span className="text-gray-300">{gen.seed}</span></div>
                      )}
                      <div className="text-xs text-gray-500">
                        {new Date(gen.created_at).toLocaleString('de-DE')}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
