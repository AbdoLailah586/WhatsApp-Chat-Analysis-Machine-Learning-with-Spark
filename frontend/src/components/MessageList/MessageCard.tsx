import { useState } from 'react'
import type { Message } from '@/types'
import { Badge } from '@/components/ui/badge'
import { Card } from '@/components/ui/card'
import { Image as ImageIcon } from 'lucide-react'

const CATEGORY_COLORS: Record<string, string> = {
  "Work": "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
  "Friends": "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200",
  "Family": "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200",
  "Not Important": "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200",
  "Promotional": "bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200",
  "Spam": "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
  "Urgent": "bg-red-600 text-white dark:bg-red-700 dark:text-red-100",
  "Entertainment": "bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200"
}

interface Props {
  message: Message
}

function getRelativeTime(dateString: string) {
  const date = new Date(dateString)
  const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' })
  const daysDifference = Math.round((date.getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24))
  return rtf.format(daysDifference, 'day')
}

export function MessageCard({ message }: Props) {
  const [expanded, setExpanded] = useState(false)
  const initial = message.sender.charAt(0).toUpperCase()
  
  const badgeColor = CATEGORY_COLORS[message.category] || CATEGORY_COLORS["Not Important"]

  return (
    <Card className="p-4 hover:shadow-md transition-shadow">
      <div className="flex gap-4">
        <div className="flex-none">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-primary font-bold">
            {initial}
          </div>
        </div>
        <div className="flex-1 space-y-1">
          <div className="flex items-center justify-between">
            <p className="text-sm font-semibold">{message.sender}</p>
            <div className="flex items-center gap-2">
              <span className="text-xs text-muted-foreground">
                {getRelativeTime(message.timestamp)}
              </span>
              <Badge variant="outline" className={`border-transparent ${badgeColor}`}>
                {message.category}
              </Badge>
              {message.confidence_score > 0 && (
                <span className="text-[10px] text-muted-foreground opacity-50">
                  {Math.round(message.confidence_score * 100)}%
                </span>
              )}
            </div>
          </div>
          
          <div className="text-sm text-foreground/90">
            {message.is_media && (
              <div className="flex items-center gap-2 text-muted-foreground italic mb-1">
                <ImageIcon className="h-4 w-4" />
                Media omitted
              </div>
            )}
            <div className={expanded ? "" : "line-clamp-2 break-words"}>
              {message.content !== "<Media omitted>" ? message.content : ""}
            </div>
            {message.content.length > 150 && !message.is_media && (
              <button 
                onClick={() => setExpanded(!expanded)}
                className="text-xs text-primary hover:underline mt-1"
              >
                {expanded ? "Show less" : "Show more"}
              </button>
            )}
          </div>
        </div>
      </div>
    </Card>
  )
}
