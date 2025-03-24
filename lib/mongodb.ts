import { MongoClient, ObjectId } from "mongodb"
import { Email, Classification } from "@/types"

const uri = process.env.MONGODB_URI
if (!uri) {
    throw new Error("MONGODB_URI is not defined")
}
const client = new MongoClient(uri)

export async function getEmailById(id: string): Promise<Email | undefined> {
    try {
        await client.connect()
        const database = client.db("emailDB")
        const emails = database.collection("emails")
        const email = await emails.findOne({ _id: new ObjectId(id) })
        if (email) {
            const { _id, ...rest } = email
            return { _id: _id.toString(), ...rest } as unknown as Email
        }
        return undefined
    } catch (error) {
        console.error("Failed to fetch email:", error)
        return undefined
    } finally {
        await client.close()
    }
}

export async function getClassificationByEmailId(id: string): Promise<Classification | undefined> {
    try {
        await client.connect()
        const database = client.db("emailDB")
        const classifications = database.collection("classifications")
        const classification = await classifications.findOne({ email_id: new ObjectId(id) })
        return classification as unknown as Classification
    } catch (error) {
        console.error("Failed to fetch classification:", error)
        return undefined
    } finally {
        await client.close()
    }
}
