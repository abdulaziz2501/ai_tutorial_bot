/**
 * Results Component
 * =================
 * Qayta ishlash natijalarini ko'rsatish va yuklab olish
 */

import React from 'react';
import { FiDownload, FiCheckCircle, FiFile } from 'react-icons/fi';
import { downloadFile } from '../services/api';

const Results = ({ taskId, taskStatus }) => {
  const handleDownload = async (fileType) => {
    try {
      await downloadFile(taskId, fileType);
    } catch (error) {
      console.error('Yuklab olishda xatolik:', error);
      alert('Faylni yuklab olishda xatolik yuz berdi');
    }
  };

  const result = taskStatus?.result || {};
  const files = result.files || {};

  return (
    <div className="text-center">
      {/* Success Message */}
      <div className="bg-green-50 rounded-lg p-6 mb-8">
        <FiCheckCircle className="text-6xl text-green-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          ✅ Qayta Ishlash Tugallandi!
        </h2>
        <p className="text-gray-700">
          Audio muvaffaqiyatli qayta ishlandi. Natijalarni yuklab oling.
        </p>
      </div>

      {/* Statistics */}
      <div className="grid md:grid-cols-3 gap-4 mb-8">
        <div className="bg-blue-50 rounded-lg p-4">
          <p className="text-sm text-gray-600 mb-1">Davomiylik</p>
          <p className="text-2xl font-bold text-blue-600">
            {result.duration?.toFixed(2)} s
          </p>
        </div>
        <div className="bg-purple-50 rounded-lg p-4">
          <p className="text-sm text-gray-600 mb-1">Segmentlar</p>
          <p className="text-2xl font-bold text-purple-600">
            {result.segments_count || 0}
          </p>
        </div>
        <div className="bg-green-50 rounded-lg p-4">
          <p className="text-sm text-gray-600 mb-1">Fayllar</p>
          <p className="text-2xl font-bold text-green-600">
            {Object.values(files).filter((f) => f).length}
          </p>
        </div>
      </div>

      {/* Download Files */}
      <div className="text-left">
        <h3 className="text-xl font-bold text-gray-900 mb-4">
          💾 Natijalarni Yuklab Olish
        </h3>

        <div className="grid md:grid-cols-2 gap-4">
          {/* Transcript */}
          {files.transcript && (
            <DownloadCard
              icon="📄"
              title="Transkripsiya"
              description="To'liq matn (TXT)"
              fileType="transcript"
              onDownload={handleDownload}
            />
          )}

          {/* SRT Subtitles */}
          {files.srt && (
            <DownloadCard
              icon="📝"
              title="SRT Subtitr"
              description="SubRip format"
              fileType="srt"
              onDownload={handleDownload}
            />
          )}

          {/* VTT Subtitles */}
          {files.vtt && (
            <DownloadCard
              icon="🎬"
              title="VTT Subtitr"
              description="WebVTT format"
              fileType="vtt"
              onDownload={handleDownload}
            />
          )}

          {/* Speakers */}
          {files.speakers && (
            <DownloadCard
              icon="👥"
              title="Spikerlar"
              description="Speaker diarization"
              fileType="speakers"
              onDownload={handleDownload}
            />
          )}

          {/* Emotions */}
          {files.emotions && (
            <DownloadCard
              icon="😊"
              title="Emotsiyalar"
              description="Emotion detection"
              fileType="emotions"
              onDownload={handleDownload}
            />
          )}

          {/* Clean Audio */}
          {files.clean_audio && (
            <DownloadCard
              icon="🔊"
              title="Tozalangan Audio"
              description="Processed WAV"
              fileType="audio"
              onDownload={handleDownload}
            />
          )}
        </div>
      </div>

      {/* Tips */}
      <div className="mt-8 bg-blue-50 rounded-lg p-6 text-left">
        <h4 className="font-semibold text-gray-900 mb-3">💡 Maslahatlar:</h4>
        <ul className="space-y-2 text-sm text-gray-700">
          <li>
            • SRT va VTT subtitllarni video playerlar (VLC, YouTube) qabul
            qiladi
          </li>
          <li>
            • Transkripsiya TXT faylida vaqt belgilari bilan saqlanadi
          </li>
          <li>
            • Tozalangan audio'ni boshqa proyektlar uchun ishlatish mumkin
          </li>
          <li>• Barcha fayllar UTF-8 kodlashda</li>
        </ul>
      </div>
    </div>
  );
};

const DownloadCard = ({ icon, title, description, fileType, onDownload }) => {
  return (
    <div className="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center">
          <span className="text-3xl mr-3">{icon}</span>
          <div>
            <h4 className="font-semibold text-gray-900">{title}</h4>
            <p className="text-sm text-gray-600">{description}</p>
          </div>
        </div>
        <button
          onClick={() => onDownload(fileType)}
          className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 transition"
          title="Yuklab olish"
        >
          <FiDownload />
        </button>
      </div>
    </div>
  );
};

export default Results;
