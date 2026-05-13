import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { UploadCloud, CheckCircle2, Loader2, AlertCircle } from 'lucide-react'
import { useUploadChat } from '@/hooks/useUploadChat'
import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'
import { cn } from '@/lib/utils'

export function DropZone() {
  const { upload, isUploading, isClassifying, isSuccess, uploadData, error } = useUploadChat()
  const navigate = useNavigate()
  
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return
    const file = acceptedFiles[0]
    
    if (file.size > 10 * 1024 * 1024) {
      toast.error("File is too large. Max size is 10MB.")
      return
    }
    
    upload(file)
  }, [upload])

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.txt']
    },
    maxFiles: 1
  })

  // Redirect on success
  if (isSuccess && uploadData) {
    setTimeout(() => {
      navigate(`/dashboard/${uploadData.upload_id}`)
    }, 1500)
  }

  const isLoading = isUploading || isClassifying

  return (
    <div
      {...getRootProps()}
      className={cn(
        "relative flex flex-col items-center justify-center w-full h-64 p-6 border-2 border-dashed rounded-xl cursor-pointer transition-all duration-200",
        isDragActive ? "border-primary bg-primary/5 scale-[1.02]" : "border-muted-foreground/25 hover:border-primary/50 hover:bg-muted/50",
        isDragReject || error ? "border-destructive bg-destructive/5" : "",
        isSuccess ? "border-green-500 bg-green-500/5" : ""
      )}
    >
      <input {...getInputProps()} />
      
      {isLoading ? (
        <div className="flex flex-col items-center space-y-4">
          <Loader2 className="w-12 h-12 text-primary animate-spin" />
          <p className="text-sm font-medium text-muted-foreground">
            {isUploading ? "Uploading file..." : "AI is analyzing messages..."}
          </p>
        </div>
      ) : isSuccess ? (
        <div className="flex flex-col items-center space-y-4 text-green-600">
          <CheckCircle2 className="w-12 h-12" />
          <p className="text-sm font-medium">
            Success! Analyzed {uploadData?.message_count} messages.
          </p>
          <p className="text-xs opacity-70">Redirecting to dashboard...</p>
        </div>
      ) : (
        <div className="flex flex-col items-center space-y-4 text-muted-foreground">
          {error ? (
            <AlertCircle className="w-12 h-12 text-destructive" />
          ) : (
            <UploadCloud className="w-12 h-12 opacity-50" />
          )}
          
          <div className="text-center">
            {error ? (
              <p className="text-sm font-medium text-destructive">Upload failed. Please try again.</p>
            ) : isDragActive ? (
              <p className="text-sm font-medium text-primary">Drop the file here...</p>
            ) : (
              <>
                <p className="text-sm font-medium">
                  <span className="text-primary hover:underline">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs mt-1">WhatsApp Chat Export (.txt) up to 10MB</p>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
