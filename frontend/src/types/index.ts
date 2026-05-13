export interface Message {
  id?: number;
  upload_id?: number;
  sender: string;
  timestamp: string;
  content: string;
  category: string;
  confidence_score: number;
  is_media: boolean;
}

export interface UploadResponse {
  upload_id: number;
  message_count: number;
}

export interface ClassifyResponse {
  messages: Message[];
}

export interface SenderCount {
  sender: string;
  count: number;
}

export interface TimeSeriesData {
  date: string;
  count: number;
}

export interface AnalyticsResponse {
  category_distribution: Record<string, number>;
  category_percentages: Record<string, number>;
  time_series: TimeSeriesData[];
  top_senders: SenderCount[];
  urgency_breakdown: Record<string, number>;
  total_messages: number;
  categorized_count: number;
  uncategorized_count: number;
}
