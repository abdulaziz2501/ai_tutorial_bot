/**
 * Task Progress Component
 * =======================
 * Qayta ishlash jarayonini ko'rsatish
 */

import React from 'react';
import { FiLoader } from 'react-icons/fi';

const TaskProgress = ({ taskStatus }) => {
  if (!taskStatus) {
    return (
      <div className="text-center py-12">
        <FiLoader className="animate-spin text-6xl text-blue-600 mx-auto mb-4" />
        <p className="text-lg text-gray-700">Kutilmoqda...</p>
      </div>
    );
  }

  const { status, progress, message } = taskStatus;

  return (
    <div className="text-center py-12">
      <h2 className="text-2xl font-bold text-gray-900 mb-8">
        🔄 Audio Qayta Ishlanmoqda
      </h2>

      {/* Progress Circle */}
      <div className="relative w-48 h-48 mx-auto mb-8">
        <svg className="transform -rotate-90 w-48 h-48">
          <circle
            cx="96"
            cy="96"
            r="88"
            stroke="currentColor"
            strokeWidth="12"
            fill="transparent"
            className="text-gray-200"
          />
          <circle
            cx="96"
            cy="96"
            r="88"
            stroke="currentColor"
            strokeWidth="12"
            fill="transparent"
            strokeDasharray={`${2 * Math.PI * 88}`}
            strokeDashoffset={`${
              2 * Math.PI * 88 * (1 - (progress || 0) / 100)
            }`}
            className="text-blue-600 transition-all duration-500"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <p className="text-4xl font-bold text-gray-900">
              {Math.round(progress || 0)}%
            </p>
            <p className="text-sm text-gray-600 mt-1">Bajarildi</p>
          </div>
        </div>
      </div>

      {/* Status Message */}
      <div className="bg-blue-50 rounded-lg p-6 max-w-md mx-auto">
        <p className="text-lg font-medium text-gray-900 mb-2">{message}</p>
        <div className="flex items-center justify-center text-sm text-gray-600">
          <FiLoader className="animate-spin mr-2" />
          <span>Iltimos, kuting...</span>
        </div>
      </div>

      {/* Processing Steps */}
      <div className="mt-8 max-w-md mx-auto text-left">
        <h3 className="font-semibold text-gray-900 mb-3">
          📋 Qayta Ishlash Bosqichlari:
        </h3>
        <div className="space-y-2">
          <ProcessingStep
            label="Audio yuklash"
            completed={progress >= 10}
            active={progress >= 0 && progress < 20}
          />
          <ProcessingStep
            label="Preprocessing"
            completed={progress >= 20}
            active={progress >= 10 && progress < 40}
          />
          <ProcessingStep
            label="Transkripsiya"
            completed={progress >= 60}
            active={progress >= 20 && progress < 60}
          />
          <ProcessingStep
            label="Speaker & Emotsiya"
            completed={progress >= 75}
            active={progress >= 60 && progress < 90}
          />
          <ProcessingStep
            label="Subtitrlar"
            completed={progress >= 90}
            active={progress >= 75 && progress < 100}
          />
        </div>
      </div>
    </div>
  );
};

const ProcessingStep = ({ label, completed, active }) => {
  return (
    <div className="flex items-center">
      <div
        className={`w-6 h-6 rounded-full flex items-center justify-center ${
          completed
            ? 'bg-green-500'
            : active
            ? 'bg-blue-500 animate-pulse'
            : 'bg-gray-300'
        }`}
      >
        {completed && (
          <svg
            className="w-4 h-4 text-white"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path d="M5 13l4 4L19 7" />
          </svg>
        )}
        {active && !completed && (
          <div className="w-2 h-2 bg-white rounded-full" />
        )}
      </div>
      <span
        className={`ml-3 ${
          completed
            ? 'text-green-600 font-medium'
            : active
            ? 'text-blue-600 font-medium'
            : 'text-gray-500'
        }`}
      >
        {label}
      </span>
    </div>
  );
};

export default TaskProgress;
