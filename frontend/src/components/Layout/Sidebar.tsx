import { Link, useLocation } from "react-router-dom"
import { Home, BarChart3, MessageSquare, Settings } from "lucide-react"
import { cn } from "@/lib/utils"

export function Sidebar() {
  const location = useLocation()
  const uploadId = location.pathname.split("/").pop() || "1"
  
  const navItems = [
    { name: "Home", href: "/", icon: Home },
    { name: "Dashboard", href: `/dashboard/${uploadId}`, icon: BarChart3 },
    { name: "Messages", href: `/messages/${uploadId}`, icon: MessageSquare },
  ]

  return (
    <div className="flex h-full w-64 flex-col border-r bg-card px-3 py-4">
      <div className="mb-8 px-4">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
          InboxMind
        </h1>
      </div>
      <nav className="flex-1 space-y-2">
        {navItems.map((item) => {
          const isActive = location.pathname === item.href
          return (
            <Link
              key={item.name}
              to={item.href}
              className={cn(
                "flex items-center gap-3 rounded-md px-4 py-3 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )}
            >
              <item.icon className="h-5 w-5" />
              {item.name}
            </Link>
          )
        })}
      </nav>
      <div className="mt-auto">
        <Link
          to="#"
          className="flex items-center gap-3 rounded-md px-4 py-3 text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
        >
          <Settings className="h-5 w-5" />
          Settings
        </Link>
      </div>
    </div>
  )
}
