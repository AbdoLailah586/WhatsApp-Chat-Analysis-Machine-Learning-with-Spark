import { useMutation } from '@tanstack/react-query';
import api from '../lib/api';
import type { UploadResponse, ClassifyResponse } from '../types';

export const useUploadChat = () => {
  const classifyMutation = useMutation({
    mutationFn: async (uploadId: number) => {
      const response = await api.post<ClassifyResponse>('/api/classify', {
        upload_id: uploadId,
        messages: [], // backend ignores this now
      });
      return response.data;
    },
  });

  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await api.post<UploadResponse>('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    },
    onSuccess: (data) => {
      // Chain classification
      classifyMutation.mutate(data.upload_id);
    }
  });

  return {
    upload: uploadMutation.mutate,
    isUploading: uploadMutation.isPending,
    isClassifying: classifyMutation.isPending,
    isSuccess: classifyMutation.isSuccess,
    isError: uploadMutation.isError || classifyMutation.isError,
    error: uploadMutation.error || classifyMutation.error,
    uploadData: uploadMutation.data,
    classifiedData: classifyMutation.data,
  };
};
