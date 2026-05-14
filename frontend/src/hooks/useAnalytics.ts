import { useQuery } from '@tanstack/react-query';
import api from '../lib/api';
import type { AnalyticsResponse } from '../types';

export const useAnalytics = (id: string | number | undefined) => {
  return useQuery({
    queryKey: ['analytics', id],
    queryFn: async () => {
      const response = await api.get<AnalyticsResponse>(`/api/analytics/${id}`);
      return response.data;
    },
    enabled: !!id,
    refetchInterval: (query) => {
        if (!query.state.data) return 5000;
        return false;
    }
  });
};
