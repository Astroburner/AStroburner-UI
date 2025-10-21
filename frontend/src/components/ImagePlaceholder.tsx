import { FiLoader } from 'react-icons/fi';

interface ImagePlaceholderProps {
  index: number;
}

export default function ImagePlaceholder({ index }: ImagePlaceholderProps) {
  return (
    <div className="group relative aspect-square bg-dark-800 rounded-lg overflow-hidden border border-dark-600 animate-pulse">
      <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 bg-gradient-to-br from-primary-900/30 to-accent-900/30">
        <FiLoader className="text-primary-400 text-4xl animate-spin" />
        <div className="text-gray-400 text-sm font-medium">
          Generiere Bild {index + 1}...
        </div>
      </div>
      
      {/* Animated gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-primary-500/10 to-transparent animate-shimmer"></div>
    </div>
  );
}
