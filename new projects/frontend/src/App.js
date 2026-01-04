/**
 * Main App Component
 * ==================
 * Uzbek Audio AI Platform - React Frontend
 */

import React, { useState, useEffect } from 'react';
import { FiUpload, FiSettings, FiDownload, FiCheckCircle, FiAlertCircle } from 'react-icons/fi';
import FileUpload from './components/FileUpload';
import ProcessingConfig from './components/ProcessingConfig';
import TaskProgress from './components/TaskProgress';
import Results from './components/Results';
import { uploadFile, processAudio, getTaskStatus } from './services/api';
import './styles/App.css';

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [fileId, setFileId] = useState(null);
  const [config, setConfig] = useState({
    whisper_model: 'medium',
    language: 'uz',
    enable_preprocessing: true,
    enable_diarization: true,
    enable_emotion: true,
    enable_subtitles: true,
  });
  const [taskId, setTaskId] = useState(null);
  const [taskStatus, setTaskStatus] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  // Task statusini polling qilish
  useEffect(() => {
    if (!taskId) return;

    const interval = setInterval(async () => {
      try {
        const status = await getTaskStatus(taskId);
        setTaskStatus(status);

        // Agar tugallangan yoki xato bo'lsa, polling to'xtatish
        if (status.status === 'completed' || status.status === 'failed') {
          clearInterval(interval);
        }
      } catch (error) {
        console.error('Status olishda xatolik:', error);
      }
    }, 2000); // Har 2 soniyada

    return () => clearInterval(interval);
  }, [taskId]);

  // Fayl yuklash
  const handleFileUpload = async (file) => {
    try {
      setUploadedFile(file);
      setUploadProgress(0);

      const response = await uploadFile(file, (progress) => {
        setUploadProgress(progress);
      });

      setFileId(response.file_id);
      setCurrentStep(2);
    } catch (error) {
      console.error('Yuklashda xatolik:', error);
      alert('Fayl yuklashda xatolik yuz berdi');
    }
  };

  // Qayta ishlashni boshlash
  const handleStartProcessing = async () => {
    if (!fileId) return;

    try {
      const response = await processAudio(fileId, config);
      setTaskId(response.task_id);
      setCurrentStep(3);
    } catch (error) {
      console.error('Qayta ishlashda xatolik:', error);
      alert('Qayta ishlashni boshlanishda xatolik');
    }
  };

  // Qaytadan boshlash
  const handleReset = () => {
    setCurrentStep(1);
    setUploadedFile(null);
    setFileId(null);
    setTaskId(null);
    setTaskStatus(null);
    setUploadProgress(0);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                🎙️ Uzbek Audio AI Platform
              </h1>
              <p className="text-gray-600 mt-1">
                O'zbek tilidagi audio va video fayllarni AI bilan qayta ishlash
              </p>
            </div>
            {currentStep > 1 && (
              <button
                onClick={handleReset}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
              >
                🔄 Qaytadan Boshlash
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Progress Steps */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          {/* Step 1 */}
          <div className="flex items-center">
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center ${
                currentStep >= 1
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-300 text-gray-600'
              }`}
            >
              {currentStep > 1 ? <FiCheckCircle /> : '1'}
            </div>
            <span className="ml-2 font-medium text-gray-700">Yuklash</span>
          </div>

          <div className="flex-1 h-1 bg-gray-300 mx-4">
            <div
              className={`h-full transition-all ${
                currentStep >= 2 ? 'bg-blue-600' : 'bg-gray-300'
              }`}
              style={{ width: currentStep >= 2 ? '100%' : '0%' }}
            />
          </div>

          {/* Step 2 */}
          <div className="flex items-center">
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center ${
                currentStep >= 2
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-300 text-gray-600'
              }`}
            >
              {currentStep > 2 ? <FiCheckCircle /> : '2'}
            </div>
            <span className="ml-2 font-medium text-gray-700">Sozlamalar</span>
          </div>

          <div className="flex-1 h-1 bg-gray-300 mx-4">
            <div
              className={`h-full transition-all ${
                currentStep >= 3 ? 'bg-blue-600' : 'bg-gray-300'
              }`}
              style={{ width: currentStep >= 3 ? '100%' : '0%' }}
            />
          </div>

          {/* Step 3 */}
          <div className="flex items-center">
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center ${
                currentStep >= 3
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-300 text-gray-600'
              }`}
            >
              {taskStatus?.status === 'completed' ? <FiCheckCircle /> : '3'}
            </div>
            <span className="ml-2 font-medium text-gray-700">Natijalar</span>
          </div>
        </div>

        {/* Content */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          {/* Step 1: File Upload */}
          {currentStep === 1 && (
            <FileUpload
              onFileUpload={handleFileUpload}
              uploadProgress={uploadProgress}
            />
          )}

          {/* Step 2: Configuration */}
          {currentStep === 2 && (
            <ProcessingConfig
              config={config}
              setConfig={setConfig}
              onStartProcessing={handleStartProcessing}
              uploadedFile={uploadedFile}
            />
          )}

          {/* Step 3: Processing & Results */}
          {currentStep === 3 && (
            <div>
              {taskStatus?.status !== 'completed' ? (
                <TaskProgress taskStatus={taskStatus} />
              ) : (
                <Results taskId={taskId} taskStatus={taskStatus} />
              )}
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white mt-12 py-6 border-t">
        <div className="max-w-7xl mx-auto px-4 text-center text-gray-600">
          <p>🎙️ Uzbek Audio AI Platform</p>
          <p className="text-sm mt-1">
            Powered by Whisper, FastAPI & React | Made with ❤️ in Uzbekistan 🇺🇿
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
