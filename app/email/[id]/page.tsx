"use client"

import { useParams, notFound } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { formatDate } from "@/lib/utils"
import { emails, classifications } from "@/lib/data"
import { AttachmentList } from "@/components/attachment-list"
import { ChevronLeft, Mail, FileText, Tag } from "lucide-react"
import HighlightedText from "@/components/highlighted-text"

export default function EmailPage() {
  const { id } = useParams()
  const email = emails.find((email) => email.email_id === id)
  const classification = classifications.find((c) => c.email_id === id)

  if (!email || !classification) {
    return notFound()
  }

  return (
    <div className="container mx-auto py-12 max-w-5xl">
      <div className="mb-8">
        <Link href="/" passHref>
          <Button variant="ghost" size="sm" className="pl-0 hover:bg-transparent">
            <ChevronLeft className="mr-2 h-4 w-4" />
            Back to Inbox
          </Button>
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <Card className="border-0 shadow-sm">
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <Mail className="h-5 w-5 text-primary" />
                  <CardTitle className="text-xl font-semibold">{email.subject}</CardTitle>
                </div>
                <Badge variant="outline" className="text-xs font-normal">
                  {email.sender.split("@")[1]}
                </Badge>
              </div>
              <div className="flex flex-col gap-1 text-sm text-muted-foreground">
                <div className="flex items-center justify-between">
                  <span>
                    From: <span className="text-foreground">{email.sender}</span>
                  </span>
                  <span className="text-xs">{formatDate(email.timestamp)}</span>
                </div>
              </div>
            </CardHeader>
            <Separator />
            <CardContent className="pt-6">
              <div className="prose max-w-none text-foreground">
                <HighlightedText body={email.body} entities={email.entities} />
              </div>

              {email.attachments.length > 0 && (
                <>
                  <Separator className="my-6" />
                  <div>
                    <div className="flex items-center gap-2 mb-4">
                      <FileText className="h-4 w-4 text-primary" />
                      <h3 className="text-sm font-medium">Attachments ({email.attachments.length})</h3>
                    </div>
                    <AttachmentList attachments={email.attachments} />
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        </div>

        <div>
          <Card className="border-0 shadow-sm">
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2">
                <Tag className="h-4 w-4 text-primary" />
                <CardTitle className="text-base font-medium">Classification</CardTitle>
              </div>
            </CardHeader>
            <Separator />
            <CardContent className="pt-6 space-y-6">
              <div>
                <div className="text-xs font-medium uppercase text-muted-foreground mb-2">Request Type</div>
                <Badge className="bg-primary/10 text-primary hover:bg-primary/15 border-0">
                  {classification.request_type}
                </Badge>
              </div>

              <div>
                <div className="text-xs font-medium uppercase text-muted-foreground mb-2">Subtype</div>
                <Badge variant="outline" className="font-normal">
                  {classification.request_subtype}
                </Badge>
              </div>

              <div>
                <div className="text-xs font-medium uppercase text-muted-foreground mb-2">Confidence</div>
                <div className="w-full bg-muted rounded-full h-1.5">
                  <div
                    className="bg-primary h-1.5 rounded-full"
                    style={{ width: `${classification.confidence * 100}%` }}
                  ></div>
                </div>
                <div className="text-right text-xs text-muted-foreground mt-1">
                  {Math.round(classification.confidence * 100)}%
                </div>
              </div>

              <div>
                <div className="text-xs font-medium uppercase text-muted-foreground mb-2">Reasoning</div>
                <p className="text-sm text-muted-foreground leading-relaxed">{classification.reasoning}</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

