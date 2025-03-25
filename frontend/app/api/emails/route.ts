import { NextApiRequest, NextApiResponse } from 'next';
import { MongoClient } from 'mongodb';

const uri = process.env.MONGODB_URI;
if (!uri) {
    throw new Error('MONGODB_URI is not defined');
}
const client = new MongoClient(uri);

export async function GET(request: Request) {
    const url = new URL(request.url);
    const collectionName = url.searchParams.get('collection') || 'emails';

    try {
        // console.log('Inside GET /api/emails');
        await client.connect();
        const database = client.db('emailDB');
        const emails = database.collection(collectionName);
        const emailList = await emails.find({}).toArray();

        // console.log('Fetched emails:', emailList);
        return new Response(JSON.stringify(emailList), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
        });
    } catch (error) {
        return new Response(JSON.stringify({ error: 'Failed to fetch emails' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    } finally {
        await client.close();
    }
}
