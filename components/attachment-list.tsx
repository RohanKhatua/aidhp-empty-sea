"use client"

import { useState } from "react"
import { FileIcon, FileTextIcon, ImageIcon, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogClose } from "@/components/ui/dialog"
import { ScrollArea } from "@/components/ui/scroll-area"

type Attachment = {
  fileName: string
  data: string
}

type AttachmentListProps = {
  attachments: Attachment[]
}

export function AttachmentList({ attachments }: AttachmentListProps) {
  const [selectedAttachment, setSelectedAttachment] = useState<Attachment | null>(null)

  const getFileIcon = (fileName: string) => {
    const extension = fileName.split(".").pop()?.toLowerCase()

    if (["jpg", "jpeg", "png", "gif", "webp"].includes(extension || "")) {
      return <ImageIcon className="h-5 w-5" />
    } else if (["txt", "doc", "docx", "pdf"].includes(extension || "")) {
      return <FileTextIcon className="h-5 w-5" />
    } else {
      return <FileIcon className="h-5 w-5" />
    }
  }

  return (
    <>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {attachments.map((attachment, index) => (
          <div key={index} className="flex items-center p-3 border rounded-md hover:bg-muted/50 transition-colors">
            <div className="mr-3 text-muted-foreground">{getFileIcon(attachment.fileName)}</div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">{attachment.fileName}</p>
            </div>
            <Button variant="ghost" size="sm" onClick={() => setSelectedAttachment(attachment)}>
              View
            </Button>
          </div>
        ))}
      </div>

      <Dialog open={!!selectedAttachment} onOpenChange={(open) => !open && setSelectedAttachment(null)}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              {selectedAttachment && getFileIcon(selectedAttachment.fileName)}
              {selectedAttachment?.fileName}
            </DialogTitle>
            <DialogClose className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
              <X className="h-4 w-4" />
              <span className="sr-only">Close</span>
            </DialogClose>
          </DialogHeader>
          <ScrollArea className="max-h-[60vh] mt-2">
            <div className="p-4 text-sm whitespace-pre-wrap font-mono bg-muted rounded-md">
              {selectedAttachment?.data}
            </div>
          </ScrollArea>
        </DialogContent>
      </Dialog>
    </>
  )
}

