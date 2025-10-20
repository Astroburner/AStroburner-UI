import { useState } from 'react';
import { FiImage, FiLoader } from 'react-icons/fi';
import { useAppStore } from '../hooks/useAppStore';
import { apiService } from '../services/api';

export default function GeneratePanel() {
  const {
    prompt,
    negativePrompt,
    width,
    height,
    steps,
    guidanceScale,
    numImages,
    seed,
    isGenerating,
    setPrompt,
    setNegativePrompt,
    setWidth,
    setHeight,
    setSteps,
    setGuidanceScale,
    setNumImages,
    setSeed,
    setIsGenerating,
    addGeneratedImages,
  } = useAppStore();

  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Bitte gib einen Prompt ein');
      return;
    }

    setError(null);
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
      });

      if (response.success) {
        addGeneratedImages(response.images);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Generation fehlgeschlagen');
      console.error('Generation error:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="h-full flex flex-col gap-4 p-6 bg-dark-800">
      {/* Prompt Input */}
      <div className="space-y-2">
        <label className="text-sm font-medium text-gray-300">Prompt</label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Beschreibe was du generieren möchtest..."
          className="w-full h-24 px-4 py-3 bg-dark-700 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none"
          disabled={isGenerating}
        />
      </div>

      {/* Negative Prompt */}
      <div className="space-y-2">
        <label className="text-sm font-medium text-gray-300">Negative Prompt (Optional)</label>
        <textarea
          value={negativePrompt}
          onChange={(e) => setNegativePrompt(e.target.value)}
          placeholder="Was soll nicht im Bild sein..."
          className="w-full h-20 px-4 py-3 bg-dark-700 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none"
          disabled={isGenerating}
        />
      </div>

      {/* Parameters Grid */}
      <div className="grid grid-cols-2 gap-4">
        {/* Width */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">
            Breite: {width}px
          </label>
          <input
            type="range"
            min="256"
            max="1024"
            step="64"
            value={width}
            onChange={(e) => setWidth(Number(e.target.value))}
            className="w-full"
            disabled={isGenerating}
          />
        </div>

        {/* Height */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">
            Höhe: {height}px
          </label>
          <input
            type="range"
            min="256"
            max="1024"
            step="64"
            value={height}
            onChange={(e) => setHeight(Number(e.target.value))}
            className="w-full"
            disabled={isGenerating}
          />
        </div>

        {/* Steps */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">
            Steps: {steps}
          </label>
          <input
            type="range"
            min="10"
            max="150"
            step="5"
            value={steps}
            onChange={(e) => setSteps(Number(e.target.value))}
            className="w-full"
            disabled={isGenerating}
          />
        </div>

        {/* Guidance Scale */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">
            Guidance: {guidanceScale.toFixed(1)}
          </label>
          <input
            type="range"
            min="1"
            max="20"
            step="0.5"
            value={guidanceScale}
            onChange={(e) => setGuidanceScale(Number(e.target.value))}
            className="w-full"
            disabled={isGenerating}
          />
        </div>

        {/* Number of Images */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">
            Anzahl Bilder: {numImages}
          </label>
          <input
            type="range"
            min="1"
            max="4"
            step="1"
            value={numImages}
            onChange={(e) => setNumImages(Number(e.target.value))}
            className="w-full"
            disabled={isGenerating}
          />
        </div>

        {/* Seed */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">Seed (Optional)</label>
          <input
            type="number"
            value={seed || ''}
            onChange={(e) => setSeed(e.target.value ? Number(e.target.value) : null)}
            placeholder="Random"
            className="w-full px-4 py-2 bg-dark-700 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
            disabled={isGenerating}
          />
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm">
          {error}
        </div>
      )}

      {/* Generate Button */}
      <button
        onClick={handleGenerate}
        disabled={isGenerating || !prompt.trim()}
        className="w-full py-4 bg-gradient-to-r from-primary-600 to-accent-600 hover:from-primary-500 hover:to-accent-500 disabled:from-gray-600 disabled:to-gray-600 text-white font-medium rounded-lg transition-all flex items-center justify-center gap-2 disabled:cursor-not-allowed"
      >
        {isGenerating ? (
          <>
            <FiLoader className="animate-spin" />
            Generiere...
          </>
        ) : (
          <>
            <FiImage />
            Bild Generieren
          </>
        )}
      </button>
    </div>
  );
}
