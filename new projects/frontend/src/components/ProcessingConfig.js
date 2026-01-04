/**
 * Processing Configuration Component
 * ===================================
 * Qayta ishlash sozlamalarini tanlash
 */

import React from 'react';
import { FiSettings, FiPlay, FiFile } from 'react-icons/fi';

const ProcessingConfig = ({ config, setConfig, onStartProcessing, uploadedFile }) => {
  const updateConfig = (key, value) => {
    setConfig({ ...config, [key]: value });
  };

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        ⚙️ Qayta Ishlash Sozlamalari
      </h2>

      {/* Uploaded File Info */}
      <div className="bg-blue-50 rounded-lg p-4 mb-6 flex items-center">
        <FiFile className="text-2xl text-blue-600 mr-3" />
        <div>
          <p className="font-medium text-gray-900">{uploadedFile?.name}</p>
          <p className="text-sm text-gray-600">
            {(uploadedFile?.size / 1024 / 1024).toFixed(2)} MB
          </p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Whisper Model */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            🤖 Whisper Model
          </label>
          <select
            value={config.whisper_model}
            onChange={(e) => updateConfig('whisper_model', e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="tiny">Tiny (39 MB) - Juda tez</option>
            <option value="base">Base (74 MB) - Tez</option>
            <option value="small">Small (244 MB) - O'rtacha</option>
            <option value="medium">Medium (769 MB) - Yaxshi ✅</option>
            <option value="large">Large (1550 MB) - Eng yaxshi</option>
          </select>
          <p className="text-xs text-gray-500 mt-1">
            Medium model tezlik va aniqlik uchun optimal
          </p>
        </div>

        {/* Language */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            🇺🇿 Til
          </label>
          <select
            value={config.language}
            onChange={(e) => updateConfig('language', e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="uz">O'zbek 🇺🇿</option>
            <option value="ru">Rus 🇷🇺</option>
            <option value="en">Ingliz 🇬🇧</option>
          </select>
        </div>
      </div>

      {/* Processing Options */}
      <div className="mt-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          🎯 Qo'shimcha Funksiyalar
        </h3>

        <div className="space-y-3">
          {/* Preprocessing */}
          <label className="flex items-center p-4 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition">
            <input
              type="checkbox"
              checked={config.enable_preprocessing}
              onChange={(e) =>
                updateConfig('enable_preprocessing', e.target.checked)
              }
              className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
            />
            <div className="ml-3">
              <p className="font-medium text-gray-900">
                🔧 Audio Preprocessing
              </p>
              <p className="text-sm text-gray-600">
                Shovqin tozalash, sukut kesish va normalizatsiya
              </p>
            </div>
          </label>

          {/* Speaker Diarization */}
          <label className="flex items-center p-4 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition">
            <input
              type="checkbox"
              checked={config.enable_diarization}
              onChange={(e) =>
                updateConfig('enable_diarization', e.target.checked)
              }
              className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
            />
            <div className="ml-3">
              <p className="font-medium text-gray-900">
                👥 Speaker Diarization
              </p>
              <p className="text-sm text-gray-600">
                Kim gapirayotganini aniqlash
              </p>
            </div>
          </label>

          {/* Emotion Detection */}
          <label className="flex items-center p-4 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition">
            <input
              type="checkbox"
              checked={config.enable_emotion}
              onChange={(e) => updateConfig('enable_emotion', e.target.checked)}
              className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
            />
            <div className="ml-3">
              <p className="font-medium text-gray-900">😊 Emotion Detection</p>
              <p className="text-sm text-gray-600">
                Hissiy holatni aniqlash
              </p>
            </div>
          </label>

          {/* Subtitles */}
          <label className="flex items-center p-4 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition">
            <input
              type="checkbox"
              checked={config.enable_subtitles}
              onChange={(e) =>
                updateConfig('enable_subtitles', e.target.checked)
              }
              className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
            />
            <div className="ml-3">
              <p className="font-medium text-gray-900">📝 Subtitrlar</p>
              <p className="text-sm text-gray-600">
                SRT va VTT formatlarida yaratish
              </p>
            </div>
          </label>
        </div>
      </div>

      {/* Start Button */}
      <button
        onClick={onStartProcessing}
        className="w-full mt-8 bg-blue-600 text-white py-4 rounded-lg font-semibold text-lg hover:bg-blue-700 transition flex items-center justify-center"
      >
        <FiPlay className="mr-2" />
        Qayta Ishlashni Boshlash
      </button>

      {/* Info */}
      <div className="mt-6 bg-yellow-50 rounded-lg p-4">
        <p className="text-sm text-gray-700">
          <strong>⏱️ Taxminiy vaqt:</strong> Qayta ishlash vaqti audio
          davomiyligi va tanlangan model'ga bog'liq. Medium model uchun 5
          daqiqalik audio ~3-5 daqiqada qayta ishlanadi.
        </p>
      </div>
    </div>
  );
};

export default ProcessingConfig;
