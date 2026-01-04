/**
 * API Service
 * ===========
 * FastAPI backend bilan aloqa qilish uchun service
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 600000, // 10 daqiqa (uzoq transkripsiya uchun)
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Audio fayl yuklash
 */
export const uploadFile = async (file, onProgress) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent) => {
      const percentCompleted = Math.round(
        (progressEvent.loaded * 100) / progressEvent.total
      );
      if (onProgress) {
        onProgress(percentCompleted);
      }
    },
  });

  return response.data;
};

/**
 * Audio qayta ishlashni boshlash
 */
export const processAudio = async (fileId, config) => {
  const response = await api.post(`/process/${fileId}`, config);
  return response.data;
};

/**
 * Task statusini tekshirish
 */
export const getTaskStatus = async (taskId) => {
  const response = await api.get(`/status/${taskId}`);
  return response.data;
};

/**
 * Natija faylni yuklab olish
 */
export const downloadFile = async (taskId, fileType) => {
  const response = await api.get(`/download/${taskId}/${fileType}`, {
    responseType: 'blob',
  });

  // Blob'dan faylni yuklab olish
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  
  // Fayl nomini aniqlash
  const fileNames = {
    transcript: 'transcript.txt',
    srt: 'subtitles.srt',
    vtt: 'subtitles.vtt',
    speakers: 'speakers.txt',
    emotions: 'emotions.txt',
    audio: 'clean_audio.wav',
  };
  
  link.setAttribute('download', fileNames[fileType] || 'file.txt');
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};

/**
 * Taskni o'chirish
 */
export const deleteTask = async (taskId) => {
  const response = await api.delete(`/task/${taskId}`);
  return response.data;
};

/**
 * Barcha tasklarni olish
 */
export const getAllTasks = async () => {
  const response = await api.get('/tasks');
  return response.data;
};

/**
 * Health check
 */
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
