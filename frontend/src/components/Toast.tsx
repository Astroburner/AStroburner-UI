import { useEffect } from 'react';
import { FiCheckCircle, FiLoader, FiAlertCircle } from 'react-icons/fi';

interface ToastProps {
  message: string;
  type: 'loading' | 'success' | 'error';
  onClose?: () => void;
  duration?: number; // Auto-close after duration (ms)
}

export default function Toast({ message, type, onClose, duration }: ToastProps) {
  useEffect(() => {
    if (duration && type === 'success') {
      const timer = setTimeout(() => {
        onClose?.();
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [duration, type, onClose]);

  const getIcon = () => {
    switch (type) {
      case 'loading':
        return <FiLoader className="text-blue-400 animate-spin text-xl" />;
      case 'success':
        return <FiCheckCircle className="text-green-400 text-xl" />;
      case 'error':
        return <FiAlertCircle className="text-red-400 text-xl" />;
    }
  };

  const getBgColor = () => {
    switch (type) {
      case 'loading':
        return 'bg-blue-500/10 border-blue-500/30';
      case 'success':
        return 'bg-green-500/10 border-green-500/30';
      case 'error':
        return 'bg-red-500/10 border-red-500/30';
    }
  };

  return (
    <div
      className={`fixed top-20 right-6 z-50 flex items-center gap-3 px-4 py-3 rounded-lg border-2 ${getBgColor()} backdrop-blur-sm animate-slide-in shadow-lg`}
      style={{ minWidth: '300px', maxWidth: '400px' }}
    >
      {getIcon()}
      <span className="text-white font-medium flex-1">{message}</span>
    </div>
  );
}
