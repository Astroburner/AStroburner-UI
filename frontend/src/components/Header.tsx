import { FiCpu, FiSettings, FiImage, FiClock, FiLoader } from 'react-icons/fi';
import { useAppStore } from '../hooks/useAppStore';
import { useEffect } from 'react';
import { apiService } from '../services/api';

export default function Header() {
  const { 
    gpuInfo, 
    setGpuInfo, 
    selectedTab, 
    setSelectedTab,
    currentModel,
    isGenerating,
    prompt,
    negativePrompt,
    width,
    height,
    steps,
    guidanceScale,
    numImages,
    seed,
    scheduler,
    denoiseStrength,
    inputImage,
    setIsGenerating,
    addGeneratedImages
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

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      alert('Bitte gib einen Prompt ein');
      return;
    }

    setIsGenerating(true);

    try {
      const response = await apiService.generateImage({
        prompt,
        negative_prompt: negativePrompt,
        width,
        height,
        num_inference_steps: steps,
        guidance_scale: guidanceScale,
        num_images: numImages,
        seed: seed || undefined,
        scheduler: scheduler,
        denoise_strength: inputImage ? denoiseStrength : undefined,
        input_image: inputImage || undefined,
      });

      if (response.success) {
        addGeneratedImages(response.images);
      }
    } catch (err: any) {
      alert(err.response?.data?.detail || err.message || 'Generation fehlgeschlagen');
      console.error('Generation error:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <header className="bg-dark-800 border-b border-dark-600 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Logo & Title */}
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-accent-500 rounded-lg flex items-center justify-center">
            <FiImage className="text-white text-xl" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Astroburner-UI</h1>
            <p className="text-xs text-gray-400">Desktop AI Generation</p>
          </div>
        </div>

        {/* Generate Button (Center) */}
        <button
          onClick={handleGenerate}
          disabled={isGenerating || !prompt.trim() || selectedTab !== 'generate'}
          className="px-8 py-3 bg-gradient-to-r from-primary-600 to-accent-600 hover:from-primary-500 hover:to-accent-500 disabled:from-gray-600 disabled:to-gray-600 text-white font-bold rounded-lg transition-all flex items-center gap-3 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
        >
          {isGenerating ? (
            <>
              <FiLoader className="animate-spin text-xl" />
              <span>Generiere...</span>
            </>
          ) : (
            <>
              <FiImage className="text-xl" />
              <span>Bild Generieren</span>
            </>
          )}
        </button>

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
