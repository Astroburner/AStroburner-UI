export interface GenerateImageRequest {
  prompt: string;
  negative_prompt?: string;
  width?: number;
  height?: number;
  num_inference_steps?: number;
  guidance_scale?: number;
  num_images?: number;
  seed?: number;
  scheduler?: string;
  denoise_strength?: number;
  input_image?: string;
}

export interface GeneratedImage {
  filename: string;
  path: string;
  base64: string;
}

export interface GenerateImageResponse {
  success: boolean;
  images: GeneratedImage[];
  count: number;
  prompt: string;
  model: string;
}

export interface ModelInfo {
  key: string;
  name: string;
  type: string;
  loaded: boolean;
}

export interface GPUInfo {
  available: boolean;
  device?: string;
  name?: string;
  memory?: {
    total_gb: number;
    allocated_gb: number;
    reserved_gb: number;
    free_gb: number;
    utilization_percent: number;
  };
  compute_capability?: string;
  message?: string;
  error?: string;
}

export interface Generation {
  id: number;
  prompt: string;
  negative_prompt: string;
  model_key: string;
  width: number;
  height: number;
  steps: number;
  guidance_scale: number;
  seed: number | null;
  file_path: string;
  thumbnail_path: string | null;
  created_at: string;
  metadata: string | null;
}

export interface AppStats {
  stats: {
    total_generations: number;
    models_used: number;
    avg_steps: number;
    avg_guidance: number;
  };
  gpu: GPUInfo;
}
