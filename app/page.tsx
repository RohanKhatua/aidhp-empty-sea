"use client"

import Link from "next/link"
import { Mail, ChevronRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { formatDate, isClient } from "@/lib/utils"
import { useEffect, useState } from "react"
import axios from "axios"
import { Email, DuplicateEmail } from "@/types"
import { toast, ToastContainer } from "react-toastify"
import "react-toastify/dist/ReactToastify.css"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { ThemeToggle } from "@/components/ui/theme-toggle"
import { useTheme } from "next-themes"

// Client-only component for date display
function ClientOnlyDate({ timestamp }: { timestamp: string }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <span className="text-xs text-muted-foreground">Loading...</span>;
  }

  return (
    <span className="text-xs text-muted-foreground">
      {formatDate(timestamp)}
    </span>
  );
}

export default function Home() {
  const [emails, setEmails] = useState<Email[]>([])
  const [dupes, setDupes] = useState<Email[]>([])

  useEffect(() => {
    async function fetchEmails() {
      try {
        const response = await axios.get('/api/emails?collection=emails')
        setEmails(response.data)
      } catch (error) {
        toast.error("Failed to fetch emails.")
      }
    }

    async function fetchDupes() {
      try {
        const response = await axios.get('/api/emails?collection=dupes')
        setDupes(response.data)
      } catch (error) {
        toast.error("Failed to fetch duplicate emails.")
      }
    }

    fetchEmails()
    fetchDupes()
  }, [])

  const renderEmails = (emails: Email[] | DuplicateEmail[], isDupes: boolean = false) => (
    <div className="space-y-4">
      {emails.length === 0 ? (
        <p className="text-center text-muted-foreground">No {isDupes ? "duplicate " : ""}emails found.</p>
      ) : (
        emails.map((email) => {
          const emailData = isDupes ? (email as DuplicateEmail).duplicate_email : email as Email;
          return (
            <Link href={`/emails/${emailData.email_id}`} key={emailData.email_id}>
              <Card className="overflow-hidden transition-all hover:border-primary/50 hover:shadow-sm mb-4">
                <CardContent className="p-0">
                  <div className="grid grid-cols-12 items-start gap-4 p-6">
                    <div className="col-span-12 sm:col-span-9">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-medium line-clamp-1">{emailData.subject}</h3>
                        <Badge variant="outline" className="ml-2 text-xs font-normal">
                          {emailData.sender ? emailData.sender.split("@")[1] : "Unknown"}
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground mb-2">
                        From: <span className="text-foreground">{emailData.sender}</span>
                      </p>
                      <p className="text-sm text-muted-foreground mb-2">
                        To: <span className="text-foreground">{emailData.recipients ? emailData.recipients.join(", ") : "Unknown"}</span>
                      </p>
                      <p className="line-clamp-2 text-sm text-muted-foreground">{emailData.text_to_process}</p>
                    </div>

                    <div className="col-span-12 sm:col-span-3 flex flex-col items-end justify-between h-full">
                      <ClientOnlyDate timestamp={emailData.timestamp} />
                      {isDupes && (
                        <Badge variant="destructive" className="mt-2 sm:mt-0">
                          Duplicate
                        </Badge>
                      )}
                      <Button variant="ghost" size="sm" className="mt-2 sm:mt-0">
                        <span className="sr-only">View email</span>
                        <ChevronRight className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </Link>
          )
        })
      )}
    </div>
  )

  return (
    <div className="container mx-auto py-12 max-w-4xl">
      <ToastContainer />
      <div className="flex items-center justify-between gap-3 mb-8">
        <div className="flex items-center gap-3">
          <Mail className="h-6 w-6 text-primary" />
          <h1 className="text-2xl font-semibold tracking-tight">Wells Fargo Commercial Lending Inbox</h1>
        </div>
        <ThemeToggle />
      </div>

      <Tabs defaultValue="emails">
        <TabsList>
          <TabsTrigger value="emails">Emails</TabsTrigger>
          <TabsTrigger value="dupes">Duplicates</TabsTrigger>
        </TabsList>
        <TabsContent value="emails">
          {renderEmails(emails)}
        </TabsContent>
        <TabsContent value="dupes">
          {renderEmails(dupes, true)}
        </TabsContent>
      </Tabs>
    </div>
  )
}

