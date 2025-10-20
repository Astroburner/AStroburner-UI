import torch
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class GPUMonitor:
    """Monitor GPU usage and VRAM"""
    
    def __init__(self):
        self.has_cuda = torch.cuda.is_available()
        self.device_count = torch.cuda.device_count() if self.has_cuda else 0
        
    def get_gpu_info(self) -> Dict:
        """Get current GPU information"""
        if not self.has_cuda:
            return {
                "available": False,
                "message": "No CUDA GPU detected",
                "device": "cpu"
            }
        
        try:
            gpu_id = torch.cuda.current_device()
            gpu_name = torch.cuda.get_device_name(gpu_id)
            
            # Memory stats
            total_memory = torch.cuda.get_device_properties(gpu_id).total_memory
            allocated = torch.cuda.memory_allocated(gpu_id)
            reserved = torch.cuda.memory_reserved(gpu_id)
            free = total_memory - allocated
            
            return {
                "available": True,
                "device": f"cuda:{gpu_id}",
                "name": gpu_name,
                "memory": {
                    "total_gb": round(total_memory / 1024**3, 2),
                    "allocated_gb": round(allocated / 1024**3, 2),
                    "reserved_gb": round(reserved / 1024**3, 2),
                    "free_gb": round(free / 1024**3, 2),
                    "utilization_percent": round((allocated / total_memory) * 100, 1)
                },
                "compute_capability": f"{torch.cuda.get_device_capability(gpu_id)[0]}.{torch.cuda.get_device_capability(gpu_id)[1]}"
            }
        except Exception as e:
            logger.error(f"Error getting GPU info: {e}")
            return {
                "available": False,
                "error": str(e)
            }
    
    def clear_cache(self):
        """Clear GPU cache"""
        if self.has_cuda:
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            logger.info("GPU cache cleared")
    
    def get_optimal_device(self) -> str:
        """Get optimal device for inference"""
        if self.has_cuda:
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"

# Global instance
gpu_monitor = GPUMonitor()
