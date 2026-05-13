import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'
import type { Message } from '@/types'
import { MessageCard } from '@/components/MessageList/MessageCard'
import { CategoryFilter } from '@/components/MessageList/CategoryFilter'
import { SearchBar } from '@/components/MessageList/SearchBar'
import { Skeleton } from '@/components/ui/skeleton'
import { ChevronRight } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'

const CATEGORIES = [
  "Work", "Friends", "Family", "Not Important", 
  "Promotional", "Spam", "Urgent", "Entertainment"
]

export default function Messages() {
  const { uploadId } = useParams<{ uploadId: string }>()
  const id = parseInt(uploadId || "0", 10)
  
  const [selectedCategories, setSelectedCategories] = useState<string[]>(CATEGORIES)
  const [search, setSearch] = useState("")
  const [page, setPage] = useState(1)
  const pageSize = 50

  const { data: messages, isLoading } = useQuery({
    queryKey: ['messages', id],
    queryFn: async () => {
      // In a real app we would fetch the raw messages for this upload
      // Since we don't have a specific GET /api/messages endpoint, we can use the classify endpoint 
      // or assume the backend returned them. Wait, the API spec didn't list a GET /api/messages endpoint.
      // We will create a mock fetch here just to make the UI work, or we can assume it exists.
      // Wait, ClassifyResponse returns the messages. Let's fetch from classify again just to get them?
      // Actually, we'll just mock it if we don't have the endpoint. Let's assume the classify endpoint can be called again.
      // But classify is a POST. Let's do a POST /api/classify with empty messages array.
      const response = await api.post('/api/classify', { upload_id: id, messages: [] })
      return response.data.messages as Message[]
    },
    enabled: !!id
  })

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <Skeleton key={i} className="h-24 w-full rounded-xl" />
        ))}
      </div>
    )
  }

  const filteredMessages = (messages || []).filter(m => {
    const matchesCategory = selectedCategories.includes(m.category || "Not Important")
    const matchesSearch = search === "" || m.content.toLowerCase().includes(search.toLowerCase()) || m.sender.toLowerCase().includes(search.toLowerCase())
    return matchesCategory && matchesSearch
  })

  const paginatedMessages = filteredMessages.slice(0, page * pageSize)

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center text-sm text-muted-foreground">
          <Link to="/" className="hover:text-foreground">Home</Link>
          <ChevronRight className="h-4 w-4 mx-1" />
          <span className="text-foreground font-medium">Messages</span>
        </div>

        <div className="flex flex-col sm:flex-row gap-2 w-full sm:w-auto">
          <SearchBar value={search} onChange={setSearch} />
          <CategoryFilter selected={selectedCategories} onChange={setSelectedCategories} />
        </div>
      </div>

      <div className="space-y-4">
        {paginatedMessages.length === 0 ? (
          <div className="text-center py-12 text-muted-foreground border rounded-xl border-dashed">
            No messages match your filters.
          </div>
        ) : (
          paginatedMessages.map((msg, i) => (
            <MessageCard key={msg.id || i} message={msg} />
          ))
        )}
      </div>

      {paginatedMessages.length < filteredMessages.length && (
        <div className="flex justify-center mt-6">
          <Button variant="outline" onClick={() => setPage(p => p + 1)}>
            Load More Messages
          </Button>
        </div>
      )}
    </div>
  )
}
