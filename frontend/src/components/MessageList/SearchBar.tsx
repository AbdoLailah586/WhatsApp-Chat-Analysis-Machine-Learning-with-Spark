import { Input } from "@/components/ui/input"
import { Search, X } from "lucide-react"
import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"

interface Props {
  value: string
  onChange: (val: string) => void
}

export function SearchBar({ value, onChange }: Props) {
  const [localVal, setLocalVal] = useState(value)

  useEffect(() => {
    const timer = setTimeout(() => {
      onChange(localVal)
    }, 300)
    return () => clearTimeout(timer)
  }, [localVal, onChange])

  return (
    <div className="relative w-full max-w-sm">
      <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
      <Input
        type="text"
        placeholder="Search messages..."
        className="pl-9 pr-9"
        value={localVal}
        onChange={(e) => setLocalVal(e.target.value)}
      />
      {localVal && (
        <Button
          variant="ghost"
          size="icon"
          className="absolute right-1 top-1 h-7 w-7"
          onClick={() => setLocalVal("")}
        >
          <X className="h-3 w-3" />
        </Button>
      )}
    </div>
  )
}
