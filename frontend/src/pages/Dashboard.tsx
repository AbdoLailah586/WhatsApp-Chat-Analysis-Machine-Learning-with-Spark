import { useParams } from 'react-router-dom'
import { useAnalytics } from '@/hooks/useAnalytics'
import { StatsCards } from '@/components/Dashboard/StatsCards'
import { CategoryPieChart } from '@/components/Dashboard/CategoryPieChart'
import { TimeSeriesChart } from '@/components/Dashboard/TimeSeriesChart'
import { ChevronRight, RefreshCw, Loader2 } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Skeleton } from '@/components/ui/skeleton'
import { Button } from '@/components/ui/button'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import { toast } from 'sonner'

export default function Dashboard() {
  const { uploadId } = useParams<{ uploadId: string }>()
  const id = parseInt(uploadId || "0", 10)
  const queryClient = useQueryClient()
  
  const { data, isLoading, isError } = useAnalytics(id)

  const reclassifyMutation = useMutation({
    mutationFn: async () => {
      await api.post(`/api/classify/${id}/reclassify`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['analytics', id] })
      toast.success("Messages successfully re-classified!")
    },
    onError: () => {
      toast.error("Failed to re-classify messages.")
    }
  })

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="grid gap-4 md:grid-cols-4">
          <Skeleton className="h-[120px] rounded-xl" />
          <Skeleton className="h-[120px] rounded-xl" />
          <Skeleton className="h-[120px] rounded-xl" />
          <Skeleton className="h-[120px] rounded-xl" />
        </div>
        <div className="grid gap-6 md:grid-cols-2">
          <Skeleton className="h-[400px] rounded-xl" />
          <Skeleton className="h-[400px] rounded-xl" />
        </div>
      </div>
    )
  }

  if (isError || !data) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] text-center">
        <h2 className="text-2xl font-bold mb-2">Upload a chat to see your analytics</h2>
        <p className="text-muted-foreground mb-6">We couldn't find analytics for this upload.</p>
        <Link to="/" className="text-primary hover:underline flex items-center">
          Go to Home <ChevronRight className="h-4 w-4 ml-1" />
        </Link>
      </div>
    )
  }

  const urgentCount = Object.values(data.urgency_breakdown).reduce((a, b) => a + b, 0)
  const activeContacts = data.top_senders.length

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center text-sm text-muted-foreground">
          <Link to="/" className="hover:text-foreground">Home</Link>
          <ChevronRight className="h-4 w-4 mx-1" />
          <span className="text-foreground font-medium">Dashboard</span>
        </div>
        
        <Button 
          variant="outline" 
          size="sm" 
          onClick={() => reclassifyMutation.mutate()}
          disabled={reclassifyMutation.isPending}
          className="gap-2"
        >
          {reclassifyMutation.isPending ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <RefreshCw className="h-4 w-4" />
          )}
          {reclassifyMutation.isPending ? "Re-classifying..." : "Re-classify with Rules"}
        </Button>
      </div>

      <StatsCards 
        totalMessages={data.total_messages}
        categorizedCount={data.categorized_count}
        urgentCount={urgentCount}
        activeContacts={activeContacts}
      />

      <div className="grid gap-6 md:grid-cols-2">
        <CategoryPieChart distribution={data.category_distribution} />
        <TimeSeriesChart data={data.time_series} />
      </div>

      <div className="mt-8 bg-card rounded-xl border p-6">
        <h3 className="text-lg font-semibold mb-4">Top Senders</h3>
        <div className="space-y-4">
          {data.top_senders.slice(0, 5).map((sender, idx) => (
            <div key={sender.sender} className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-muted font-medium text-xs">
                  {idx + 1}
                </div>
                <span className="font-medium">{sender.sender}</span>
              </div>
              <span className="text-muted-foreground">{sender.count} msgs</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
