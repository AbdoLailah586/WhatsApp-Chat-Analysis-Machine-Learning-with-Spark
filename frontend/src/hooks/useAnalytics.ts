import { useQuery } from '@tanstack/react-query';
import api from '../lib/api';
import type { AnalyticsResponse } from '../types';

export const useAnalytics = (uploadId: number | undefined) => {
  return useQuery({
    queryKey: ['analytics', uploadId],
    queryFn: async () => {
      const response = await api.get<AnalyticsResponse>(`/api/analytics/${uploadId}`);
      return response.data;
    },
    enabled: !!uploadId,
    // Optional polling if classification happens in background, but our setup is synchronous right now
    refetchInterval: (query) => {
        if (!query.state.data) return 5000;
        return false;
    }
  });
};
