import { DropZone } from "@/components/FileUpload/DropZone"
import { Button } from "@/components/ui/button"
import { ArrowRight, Bot, Filter, Zap } from "lucide-react"

export default function Home() {
  const scrollToUpload = () => {
    document.getElementById('upload-section')?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <div className="flex flex-col min-h-[calc(100vh-4rem)]">
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48 flex flex-col items-center justify-center text-center">
          <div className="container px-4 md:px-6 space-y-6">
            <h1 className="text-4xl font-extrabold tracking-tighter sm:text-5xl md:text-6xl lg:text-7xl">
              <span className="bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">InboxMind</span>
            </h1>
            <p className="mx-auto max-w-[700px] text-xl text-muted-foreground font-medium">
              Your WhatsApp, organized intelligently.
            </p>
            <p className="mx-auto max-w-[600px] text-muted-foreground">
              Upload your chat export and let AI categorize every message into Work, Friends, Family, Urgent, and more.
            </p>
            <div className="flex justify-center mt-6">
              <Button size="lg" onClick={scrollToUpload} className="gap-2">
                Start Analyzing <ArrowRight className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </section>

        <section className="w-full py-12 md:py-24 bg-muted/50">
          <div className="container px-4 md:px-6">
            <div className="grid gap-8 sm:grid-cols-3">
              <div className="flex flex-col items-center space-y-3 text-center">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary">
                  <Bot className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold">Auto-Categorization</h3>
                <p className="text-muted-foreground">Our AI understands context. It accurately tags messages as Work, Spam, Friends, and more.</p>
              </div>
              <div className="flex flex-col items-center space-y-3 text-center">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-red-100 text-red-600 dark:bg-red-900/30">
                  <Zap className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold">Priority Detection</h3>
                <p className="text-muted-foreground">Never miss what's important. Urgent messages are automatically surfaced and highlighted.</p>
              </div>
              <div className="flex flex-col items-center space-y-3 text-center">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-100 text-green-600 dark:bg-green-900/30">
                  <Filter className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold">Smart Filtering</h3>
                <p className="text-muted-foreground">Find exactly what you're looking for with color-coded filters and advanced search.</p>
              </div>
            </div>
          </div>
        </section>

        <section id="upload-section" className="w-full py-12 md:py-24 flex justify-center">
          <div className="container px-4 md:px-6 max-w-2xl">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold tracking-tighter">Upload Chat Export</h2>
              <p className="text-muted-foreground mt-2">Export your WhatsApp chat without media and drop the .txt file here.</p>
            </div>
            <DropZone />
          </div>
        </section>
      </main>
      
      <footer className="w-full py-6 border-t bg-background flex justify-center">
        <p className="text-xs text-muted-foreground">
          © 2026 InboxMind. Built with React and FastAPI.
        </p>
      </footer>
    </div>
  )
}
