"use client"

import { useParams, notFound } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { formatDate } from "@/lib/utils"
import { emails, classifications } from "@/lib/data"
import { AttachmentList } from "@/components/attachment-list"
import { ChevronLeft } from "lucide-react"
import HighlightedText from "@/components/highlighted-text"

export default function EmailPage() {
  const { id } = useParams()
  const email = emails.find((email) => email.email_id === id)
  const classification = classifications.find((c) => c.email_id === id)

  if (!email || !classification) {
    return notFound()
  }

  return (
    <div className="container mx-auto py-10">
      <div className="mb-6">
        <Link href="/" passHref>
          <Button variant="outline" size="sm">
            <ChevronLeft className="mr-2 h-4 w-4" />
            Back to Inbox
          </Button>
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle className="text-2xl">{email.subject}</CardTitle>
              <CardDescription className="flex flex-col gap-1">
                <span>From: {email.sender}</span>
                <span>Date: {formatDate(email.timestamp)}</span>
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="prose max-w-none">
                <HighlightedText body={email.body} entities={email.entities} />
              </div>

              {email.attachments.length > 0 && (
                <>
                  <Separator className="my-6" />
                  <div>
                    <h3 className="text-lg font-medium mb-4">Attachments ({email.attachments.length})</h3>
                    <AttachmentList attachments={email.attachments} />
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        </div>

        <div>
          <Card>
            <CardHeader>
              <CardTitle>Classification</CardTitle>
              <CardDescription>Email type analysis</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="text-sm font-medium mb-1">Request Type</div>
                <Badge variant="outline" className="text-base font-normal">
                  {classification.request_type}
                </Badge>
              </div>

              <div>
                <div className="text-sm font-medium mb-1">Subtype</div>
                <Badge variant="outline" className="text-base font-normal">
                  {classification.request_subtype}
                </Badge>
              </div>

              <div>
                <div className="text-sm font-medium mb-1">Confidence</div>
                <div className="w-full bg-muted rounded-full h-2.5">
                  <div
                    className="bg-primary h-2.5 rounded-full"
                    style={{ width: `${classification.confidence * 100}%` }}
                  ></div>
                </div>
                <div className="text-right text-xs text-muted-foreground mt-1">
                  {Math.round(classification.confidence * 100)}%
                </div>
              </div>

              <div>
                <div className="text-sm font-medium mb-1">Reasoning</div>
                <p className="text-sm text-muted-foreground">{classification.reasoning}</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

