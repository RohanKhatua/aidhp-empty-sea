export type Attachment = {
    fileName: string
    data: string // Base64 encoded content OR parsed content
    extractedData?: string // Extracted text content
}

export type Entity = {
    entity: string
    label: string
    start_idx: number
    end_idx: number
}

export interface Email {
    email_id: string;
    subject: string;
    sender: string;
    timestamp: string;
    text_to_process: string;
    extracted_data: Entity[];
    classification: string; // JSON string of Classification
}

export type Classification = {
    email_id: string
    request_type: string
    request_subtype: string
    confidence: number
    reasoning: string // Explanation of classification decision
}
