import { FiCpu, FiSettings, FiImage, FiClock } from 'react-icons/fi';
import { useAppStore } from '../hooks/useAppStore';
import { useEffect } from 'react';
import { apiService } from '../services/api';

export default function Header() {
  const { 
    gpuInfo, 
    setGpuInfo, 
    selectedTab, 
    setSelectedTab,
    currentModel 
  } = useAppStore();

  useEffect(() => {
    // Fetch GPU info on mount
    apiService.getGPUInfo().then(setGpuInfo).catch(console.error);
    
    // Update every 5 seconds
    const interval = setInterval(() => {
      apiService.getGPUInfo().then(setGpuInfo).catch(console.error);
    }, 5000);
    
    return () => clearInterval(interval);
  }, [setGpuInfo]);

  return (
    <header className="bg-dark-800 border-b border-dark-600 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Logo & Title */}
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-accent-500 rounded-lg flex items-center justify-center">
            <FiImage className="text-white text-xl" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">AI Studio</h1>
            <p className="text-xs text-gray-400">Desktop AI Generation</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex gap-2">
          <button
            onClick={() => setSelectedTab('generate')}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
              selectedTab === 'generate'
                ? 'bg-primary-600 text-white'
                : 'bg-dark-700 text-gray-400 hover:bg-dark-600'
            }`}
          >
            <FiImage /> Generate
          </button>
          <button
            onClick={() => setSelectedTab('history')}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
              selectedTab === 'history'
                ? 'bg-primary-600 text-white'
                : 'bg-dark-700 text-gray-400 hover:bg-dark-600'
            }`}
          >
            <FiClock /> History
          </button>
          <button
            onClick={() => setSelectedTab('settings')}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
              selectedTab === 'settings'
                ? 'bg-primary-600 text-white'
                : 'bg-dark-700 text-gray-400 hover:bg-dark-600'
            }`}
          >
            <FiSettings /> Settings
          </button>
        </div>

        {/* GPU Info */}
        <div className="flex items-center gap-4">
          {/* Current Model */}
          {currentModel && (
            <div className="text-sm text-gray-400">
              <span className="text-gray-500">Model:</span>{' '}
              <span className="text-white">{currentModel.name}</span>
            </div>
          )}

          {/* GPU Status */}
          <div className="flex items-center gap-2 bg-dark-700 px-4 py-2 rounded-lg">
            <FiCpu className={gpuInfo?.available ? 'text-green-400' : 'text-red-400'} />
            <div className="text-sm">
              {gpuInfo?.available ? (
                <div>
                  <div className="text-white font-medium">{gpuInfo.name}</div>
                  <div className="text-xs text-gray-400">
                    VRAM: {gpuInfo.memory?.allocated_gb.toFixed(1)}GB / {gpuInfo.memory?.total_gb.toFixed(1)}GB
                    <span className={`ml-2 ${
                      (gpuInfo.memory?.utilization_percent || 0) > 80 
                        ? 'text-red-400' 
                        : 'text-green-400'
                    }`}>
                      ({gpuInfo.memory?.utilization_percent}%)
                    </span>
                  </div>
                </div>
              ) : (
                <div className="text-gray-400">No GPU</div>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
