import { useState, useRef, useEffect } from 'react';
import { FiImage, FiLoader, FiUpload, FiX, FiPackage, FiEye, FiEyeOff } from 'react-icons/fi';
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
    scheduler,
    denoiseStrength,
    inputImage,
    isGenerating,
    activeLoras,
    nsfw,
    clipSkip,
    setPrompt,
    setNegativePrompt,
    setWidth,
    setHeight,
    setSteps,
    setGuidanceScale,
    setNumImages,
    setSeed,
    setScheduler,
    setDenoiseStrength,
    setInputImage,
    setIsGenerating,
    setNsfw,
    setClipSkip,
    addGeneratedImages,
    updateLoraWeight,
  } = useAppStore();

  const [error, setError] = useState<string | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  
  // Refs for auto-resizing textareas
  const promptTextareaRef = useRef<HTMLTextAreaElement>(null);
  const negativePromptTextareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea function
  const autoResizeTextarea = (textarea: HTMLTextAreaElement | null) => {
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${textarea.scrollHeight}px`;
    }
  };

  // Auto-resize on prompt changes
  useEffect(() => {
    autoResizeTextarea(promptTextareaRef.current);
  }, [prompt]);

  useEffect(() => {
    autoResizeTextarea(negativePromptTextareaRef.current);
  }, [negativePrompt]);

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64String = reader.result as string;
        setInputImage(base64String);
        setImagePreview(base64String);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRemoveImage = () => {
    setInputImage(null);
    setImagePreview(null);
  };

  return (
    <div className="h-full flex flex-col gap-4 p-6 bg-dark-800 overflow-y-auto">
      {/* Image Upload (Image-to-Image) */}
      <div className="space-y-2">
        <label className="text-sm font-medium text-gray-300">
          Eingabebild (Optional - für Image-to-Image)
        </label>
        <div className="flex gap-2">
          <label className="flex-1 cursor-pointer">
            <div className="w-full px-4 py-3 bg-dark-700 border border-dark-600 rounded-lg text-gray-400 hover:border-primary-500 transition-colors flex items-center justify-center gap-2">
              <FiUpload />
              <span>{imagePreview ? 'Bild ändern' : 'Bild hochladen'}</span>
            </div>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              className="hidden"
              disabled={isGenerating}
            />
          </label>
          {imagePreview && (
            <button
              onClick={handleRemoveImage}
              className="px-4 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
              disabled={isGenerating}
            >
              <FiX />
            </button>
          )}
        </div>
        {imagePreview && (
          <div className="mt-2 relative w-full h-48 bg-dark-700 rounded-lg overflow-hidden">
            <img
              src={imagePreview}
              alt="Input preview"
              className="w-full h-full object-contain"
            />
          </div>
        )}
      </div>

      {/* Denoise Strength (nur für img2img) */}
      {inputImage && (
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">
            Denoise Strength: {denoiseStrength.toFixed(2)}
          </label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={denoiseStrength}
            onChange={(e) => setDenoiseStrength(Number(e.target.value))}
            className="w-full"
            disabled={isGenerating}
          />
          <p className="text-xs text-gray-500">
            Niedrig (0.1-0.3): Kleine Änderungen | Mittel (0.4-0.6): Moderate Änderungen | Hoch (0.7-1.0): Starke Änderungen
          </p>
        </div>
      )}

      {/* Active LoRAs - CRITICAL: Only visible when LoRAs are active */}
      {activeLoras.length > 0 && (
        <div className="bg-primary-500/10 border-2 border-primary-500 rounded-lg p-4 space-y-3">
          <div className="flex items-center gap-2 mb-2">
            <FiPackage className="text-primary-400" />
            <h3 className="text-sm font-bold text-primary-300">
              Aktive LoRAs ({activeLoras.length}/5)
            </h3>
          </div>
          
          {activeLoras.map((lora) => (
            <div key={lora.id} className="bg-dark-700 rounded-lg p-3 space-y-2">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-medium text-white">{lora.name}</div>
                  <div className="text-xs text-gray-400">{lora.model_type}</div>
                </div>
                <div className="text-sm font-medium text-primary-400">
                  {lora.weight.toFixed(2)}
                </div>
              </div>
              
              {lora.trigger_words && (
                <div className="text-xs text-primary-400">
                  Trigger: {lora.trigger_words}
                </div>
              )}
              
              <div className="space-y-1">
                <label className="text-xs text-gray-400">
                  Stärke: {lora.weight.toFixed(2)}
                </label>
                <input
                  type="range"
                  min="-1"
                  max="2"
                  step="0.05"
                  value={lora.weight}
                  onChange={(e) => updateLoraWeight(lora.id, Number(e.target.value))}
                  className="w-full"
                  disabled={isGenerating}
                />
                <div className="flex justify-between text-xs text-gray-500">
                  <span>-1.0</span>
                  <span>0.0</span>
                  <span>1.0</span>
                  <span>2.0</span>
                </div>
              </div>
            </div>
          ))}
          
          <p className="text-xs text-gray-500 mt-2">
            💡 Tipp: Passe die Stärke jeder LoRA individuell an für optimale Ergebnisse
          </p>
        </div>
      )}

      {/* NSFW Toggle */}
      <div className="bg-dark-700 border border-dark-600 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {nsfw ? (
              <FiEye className="text-red-400" />
            ) : (
              <FiEyeOff className="text-green-400" />
            )}
            <span className="text-sm font-medium text-gray-300">NSFW Content</span>
          </div>
          <button
            onClick={() => setNsfw(!nsfw)}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              nsfw
                ? 'bg-red-600 hover:bg-red-500 text-white'
                : 'bg-green-600 hover:bg-green-500 text-white'
            }`}
            disabled={isGenerating}
          >
            {nsfw ? 'Aktiviert' : 'Deaktiviert'}
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          {nsfw 
            ? '⚠️ NSFW-Content wird generiert (Safety Checker deaktiviert)' 
            : '✅ SFW-Modus aktiv (Safety Checker aktiviert)'}
        </p>
      </div>

      {/* Prompt Input */}
      <div className="space-y-2">
        <label className="text-sm font-medium text-gray-300">Prompt</label>
        <textarea
          ref={promptTextareaRef}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Beschreibe was du generieren möchtest..."
          className="w-full min-h-[96px] px-4 py-3 bg-dark-700 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none overflow-hidden"
          disabled={isGenerating}
        />
      </div>

      {/* Negative Prompt */}
      <div className="space-y-2">
        <label className="text-sm font-medium text-gray-300">Negative Prompt (Optional)</label>
        <textarea
          ref={negativePromptTextareaRef}
          value={negativePrompt}
          onChange={(e) => setNegativePrompt(e.target.value)}
          placeholder="Was soll nicht im Bild sein..."
          className="w-full min-h-[80px] px-4 py-3 bg-dark-700 border border-dark-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none overflow-hidden"
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
            max="2048"
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
            max="2048"
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
            max="20"
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

        {/* Scheduler (ersetzt Sampler + Scheduler) */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">
            Scheduler (Denoising Algorithmus)
          </label>
          <select
            value={scheduler}
            onChange={(e) => setScheduler(e.target.value)}
            className="w-full px-4 py-2 bg-dark-700 border border-dark-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
            disabled={isGenerating}
          >
            <optgroup label="Empfohlen für Qualität">
              <option value="DPMSolverMultistep">DPM++ 2M (Schnell & Qualität)</option>
              <option value="DPMSolverSinglestep">DPM++ SDE (Detailliert)</option>
              <option value="UniPCMultistep">UniPC (Sehr schnell)</option>
            </optgroup>
            <optgroup label="Klassisch">
              <option value="DDIM">DDIM (Standard)</option>
              <option value="DDPM">DDPM (Original)</option>
              <option value="PNDM">PNDM (Stabil)</option>
            </optgroup>
            <optgroup label="Euler Familie">
              <option value="EulerDiscrete">Euler (Deterministisch)</option>
              <option value="EulerAncestralDiscrete">Euler Ancestral (Kreativ)</option>
            </optgroup>
            <optgroup label="Weitere">
              <option value="LMSDiscrete">LMS</option>
              <option value="HeunDiscrete">Heun</option>
              <option value="KDPM2Discrete">KDPM2</option>
              <option value="KDPM2AncestralDiscrete">KDPM2 Ancestral</option>
            </optgroup>
          </select>
        </div>

        {/* CLIP Skip */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">
            CLIP Skip: {clipSkip === 0 ? 'Standard' : clipSkip}
          </label>
          <select
            value={clipSkip}
            onChange={(e) => setClipSkip(Number(e.target.value))}
            className="w-full px-4 py-2 bg-dark-700 border border-dark-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
            disabled={isGenerating}
          >
            <option value="0">Standard (Alle Layer)</option>
            <option value="1">CLIP Skip 1 (Realistic)</option>
            <option value="2">CLIP Skip 2 (Pony/Anime)</option>
            <option value="3">CLIP Skip 3 (Extreme Anime)</option>
          </select>
          <p className="text-xs text-gray-500">
            {clipSkip === 0 && '✓ Präzise Interpretation für realistische Models'}
            {clipSkip === 1 && '✓ Leicht lockerer für kreative Freiheit'}
            {clipSkip === 2 && '✓ Empfohlen für Pony Diffusion & Anime Models'}
            {clipSkip === 3 && '✓ Maximum künstlerische Freiheit'}
          </p>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm">
          {error}
        </div>
      )}
    </div>
  );
}
