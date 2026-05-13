import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Filter } from "lucide-react"

const CATEGORIES = [
  "Work", "Friends", "Family", "Not Important", 
  "Promotional", "Spam", "Urgent", "Entertainment"
]

interface Props {
  selected: string[]
  onChange: (selected: string[]) => void
}

export function CategoryFilter({ selected, onChange }: Props) {
  const toggle = (category: string) => {
    if (selected.includes(category)) {
      onChange(selected.filter(c => c !== category))
    } else {
      onChange([...selected, category])
    }
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" className="gap-2">
          <Filter className="h-4 w-4" />
          Categories
          {selected.length > 0 && (
            <span className="ml-1 rounded-full bg-primary w-5 h-5 text-[10px] text-primary-foreground flex items-center justify-center">
              {selected.length}
            </span>
          )}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56">
        <DropdownMenuLabel>Filter by Category</DropdownMenuLabel>
        <DropdownMenuSeparator />
        {CATEGORIES.map(category => (
          <DropdownMenuCheckboxItem
            key={category}
            checked={selected.includes(category)}
            onCheckedChange={() => toggle(category)}
          >
            {category}
          </DropdownMenuCheckboxItem>
        ))}
        <DropdownMenuSeparator />
        <div className="flex gap-2 p-2">
          <Button variant="ghost" size="sm" className="w-full text-xs" onClick={() => onChange(CATEGORIES)}>
            Select All
          </Button>
          <Button variant="ghost" size="sm" className="w-full text-xs" onClick={() => onChange([])}>
            Clear
          </Button>
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
