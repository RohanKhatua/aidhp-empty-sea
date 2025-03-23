import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { formatDate } from "@/lib/utils"
import { emails } from "@/lib/data"

export default function Home() {
  return (
    <div className="container mx-auto py-10">
      <h1 className="text-3xl font-bold mb-6">Email Viewer</h1>
      <div className="grid gap-6">
        {emails.map((email) => (
          <Card key={email.email_id} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <CardTitle className="flex justify-between items-start">
                <span className="line-clamp-1">{email.subject}</span>
                <span className="text-sm font-normal text-muted-foreground">{formatDate(email.timestamp)}</span>
              </CardTitle>
              <CardDescription>From: {email.sender}</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="line-clamp-2 text-sm text-muted-foreground">{email.body}</p>
            </CardContent>
            <CardFooter>
              <Link href={`/email/${email.email_id}`} passHref>
                <Button>View Email</Button>
              </Link>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  )
}

