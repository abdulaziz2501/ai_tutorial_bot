/**
 * File Upload Component
 * =====================
 * Drag & drop fayl yuklash interfeysi
 */

import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { FiUploadCloud, FiFile } from 'react-icons/fi';

const FileUpload = ({ onFileUpload, uploadProgress }) => {
  const onDrop = useCallback(
    (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        onFileUpload(acceptedFiles[0]);
      }
    },
    [onFileUpload]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'audio/*': ['.mp3', '.wav', '.flac', '.ogg', '.m4a'],
      'video/*': ['.mp4', '.avi', '.mov', '.mkv', '.webm'],
    },
    multiple: false,
  });

  return (
    <div className="text-center">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        📤 Audio yoki Video Faylni Yuklang
      </h2>

      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`border-4 border-dashed rounded-lg p-12 cursor-pointer transition ${
          isDragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
        }`}
      >
        <input {...getInputProps()} />

        <FiUploadCloud className="mx-auto text-6xl text-gray-400 mb-4" />

        {isDragActive ? (
          <p className="text-lg text-blue-600 font-medium">
            Faylni bu yerga tashlang...
          </p>
        ) : (
          <div>
            <p className="text-lg text-gray-700 font-medium mb-2">
              Faylni bu yerga sudrab tashlang yoki tanlang
            </p>
            <p className="text-sm text-gray-500">
              Qo'llab-quvvatlanadigan formatlar: MP3, WAV, MP4, AVI, va boshqalar
            </p>
          </div>
        )}
      </div>

      {/* Upload Progress */}
      {uploadProgress > 0 && uploadProgress < 100 && (
        <div className="mt-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">
              Yuklanyapti...
            </span>
            <span className="text-sm font-medium text-blue-600">
              {uploadProgress}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
        </div>
      )}

      {/* Qo'llab-quvvatlanadigan formatlar */}
      <div className="mt-8 bg-blue-50 rounded-lg p-6">
        <h3 className="font-semibold text-gray-900 mb-3">
          📋 Qo'llab-quvvatlanadigan formatlar:
        </h3>
        <div className="grid grid-cols-2 gap-4 text-sm text-gray-700">
          <div>
            <p className="font-medium mb-2">Audio:</p>
            <ul className="space-y-1">
              <li>• MP3</li>
              <li>• WAV</li>
              <li>• FLAC</li>
              <li>• OGG</li>
              <li>• M4A</li>
            </ul>
          </div>
          <div>
            <p className="font-medium mb-2">Video:</p>
            <ul className="space-y-1">
              <li>• MP4</li>
              <li>• AVI</li>
              <li>• MOV</li>
              <li>• MKV</li>
              <li>• WEBM</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
