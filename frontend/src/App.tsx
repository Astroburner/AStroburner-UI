import Header from './components/Header';
import GeneratePanel from './components/GeneratePanel';
import ImageGallery from './components/ImageGallery';
import HistoryPanel from './components/HistoryPanel';
import SettingsPanel from './components/SettingsPanel';
import Toast from './components/Toast';
import { useAppStore } from './hooks/useAppStore';

export default function App() {
  const { selectedTab, toast, hideToast } = useAppStore();

  return (
    <div className="h-screen flex flex-col bg-dark-900 text-white">
      <Header />
      
      {/* Toast Notifications */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={hideToast}
          duration={toast.type === 'success' ? 3000 : undefined}
        />
      )}
      
      <div className="flex-1 flex overflow-hidden">
        {selectedTab === 'generate' ? (
          <>
            {/* Left Panel - Controls */}
            <div className="w-96 border-r border-dark-600 overflow-auto">
              <GeneratePanel />
            </div>

            {/* Right Panel - Gallery */}
            <div className="flex-1">
              <ImageGallery />
            </div>
          </>
        ) : selectedTab === 'history' ? (
          <div className="flex-1">
            <HistoryPanel />
          </div>
        ) : (
          <div className="flex-1">
            <SettingsPanel />
          </div>
        )}
      </div>
    </div>
  );
}
