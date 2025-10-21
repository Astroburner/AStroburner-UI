import { FiDownload, FiMaximize2 } from 'react-icons/fi';
import { useAppStore } from '../hooks/useAppStore';
import { useState } from 'react';
import ImagePlaceholder from './ImagePlaceholder';

export default function ImageGallery() {
  const { generatedImages, isGenerating, numImages } = useAppStore();
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  const handleDownload = (base64: string, filename: string) => {
    const link = document.createElement('a');
    link.href = `data:image/png;base64,${base64}`;
    link.download = filename;
    link.click();
  };

  if (generatedImages.length === 0) {
    return (
      <div className="h-full flex items-center justify-center bg-dark-900">
        <div className="text-center text-gray-500">
          <FiMaximize2 className="mx-auto text-6xl mb-4 opacity-20" />
          <p className="text-lg">Keine Bilder generiert</p>
          <p className="text-sm mt-2">Generiere dein erstes Bild!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full bg-dark-900 p-6 overflow-auto">
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
        {/* Show placeholders when generating */}
        {isGenerating && Array.from({ length: numImages }).map((_, index) => (
          <ImagePlaceholder key={`placeholder-${index}`} index={index} />
        ))}
        
        {/* Show generated images */}
        {generatedImages.map((image, index) => (
          <div
            key={`${image.filename}-${index}`}
            className="group relative aspect-square bg-dark-800 rounded-lg overflow-hidden border border-dark-600 hover:border-primary-500 transition-all cursor-pointer"
          >
            <img
              src={`data:image/png;base64,${image.base64}`}
              alt={image.filename}
              className="w-full h-full object-cover"
              onClick={() => setSelectedImage(image.base64)}
            />
            
            {/* Hover Overlay */}
            <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-4">
              <button
                onClick={() => setSelectedImage(image.base64)}
                className="p-3 bg-primary-600 hover:bg-primary-500 rounded-lg transition-colors"
                title="Vollbild"
              >
                <FiMaximize2 className="text-white" />
              </button>
              <button
                onClick={() => handleDownload(image.base64, image.filename)}
                className="p-3 bg-green-600 hover:bg-green-500 rounded-lg transition-colors"
                title="Download"
              >
                <FiDownload className="text-white" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Fullscreen Modal */}
      {selectedImage && (
        <div
          className="fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-8"
          onClick={() => setSelectedImage(null)}
        >
          <img
            src={`data:image/png;base64,${selectedImage}`}
            alt="Fullscreen"
            className="max-w-full max-h-full object-contain"
          />
          <button
            onClick={() => setSelectedImage(null)}
            className="absolute top-4 right-4 px-4 py-2 bg-dark-700 hover:bg-dark-600 text-white rounded-lg"
          >
            Schließen
          </button>
        </div>
      )}
    </div>
  );
}
