"use client"

import Link from "next/link"
import { Mail, ChevronRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { formatDate } from "@/lib/utils"
import { useEffect, useState } from "react"
import axios from "axios"
import { Email } from "@/types"
import { toast, ToastContainer } from "react-toastify"
import "react-toastify/dist/ReactToastify.css"

export default function Home() {
  const [emails, setEmails] = useState<Email[]>([])

  useEffect(() => {
    async function fetchEmails() {
      try {
        const response = await axios.get('/api/emails')
        setEmails(response.data)
      } catch (error) {
        toast.error("Failed to fetch emails.")
      }
    }
    fetchEmails()
  }, [])

  return (
    <div className="container mx-auto py-12 max-w-4xl">
      <ToastContainer />
      <div className="flex items-center gap-3 mb-8">
        <Mail className="h-6 w-6 text-primary" />
        <h1 className="text-2xl font-semibold tracking-tight">Inbox</h1>
      </div>

      <div className="space-y-4">
        {emails.map((email) => (
          <Link href={`/emails/${email.email_id}`} key={email.email_id}>
            <Card className="overflow-hidden transition-all hover:border-primary/50 hover:shadow-sm">
              <CardContent className="p-0">
                <div className="grid grid-cols-12 items-start gap-4 p-6">
                  <div className="col-span-12 sm:col-span-9">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-medium line-clamp-1">{email.subject}</h3>
                      <Badge variant="outline" className="ml-2 text-xs font-normal">
                        {email.sender.split("@")[1]}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground mb-2">
                      From: <span className="text-foreground">{email.sender}</span>
                    </p>
                    <p className="line-clamp-2 text-sm text-muted-foreground">{email.text_to_process}</p>
                  </div>

                  <div className="col-span-12 sm:col-span-3 flex flex-col items-end justify-between h-full">
                    <span className="text-xs text-muted-foreground">{formatDate(email.timestamp)}</span>
                    <Button variant="ghost" size="sm" className="mt-2 sm:mt-0">
                      <span className="sr-only">View email</span>
                      <ChevronRight className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}

