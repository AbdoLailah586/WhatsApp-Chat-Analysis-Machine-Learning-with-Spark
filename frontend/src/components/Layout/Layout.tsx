import { Sidebar } from "./Sidebar"
import { ThemeToggle } from "../ThemeToggle"
import { Menu } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-background overflow-hidden">
      {/* Desktop Sidebar */}
      <div className="hidden md:block">
        <Sidebar />
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top Navbar */}
        <header className="h-16 flex items-center justify-between border-b px-4 lg:px-8 bg-card">
          <div className="flex items-center gap-4">
            {/* Mobile Sidebar Trigger */}
            <Sheet>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="md:hidden">
                  <Menu className="h-5 w-5" />
                </Button>
              </SheetTrigger>
              <SheetContent side="left" className="p-0 w-64">
                <Sidebar />
              </SheetContent>
            </Sheet>
            
            <div className="md:hidden font-bold text-lg bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
              InboxMind
            </div>
          </div>

          <div className="flex items-center gap-4">
            <ThemeToggle />
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto p-4 lg:p-8">
          <div className="mx-auto max-w-6xl">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
