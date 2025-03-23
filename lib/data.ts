// Sample data for the email viewer application

export type Attachment = {
  fileName: string
  data: string // Base64 encoded content OR parsed content
}

export type Entity = {
  entity: string
  label: string
  start_idx: number
  end_idx: number
}

export type Email = {
  email_id: string
  subject: string
  body: string
  timestamp: string // Format: YYYY-MM-DD HH:MM:SS
  sender: string
  attachments: Attachment[]
  entities: Entity[]
}

export type Classification = {
  email_id: string
  request_type: string
  request_subtype: string
  confidence: number
  reasoning: string // Explanation of classification decision
}

// Sample emails
export const emails: Email[] = [
  {
    email_id: "email-001",
    subject: "Quarterly Financial Report for Apple Inc.",
    body: "Apple Inc. has reported a revenue increase of $5M in Berlin for 2024 fiscal year. The company's performance exceeded market expectations, with significant growth in the European market.\n\nThe board has approved a new investment plan for the upcoming quarter, focusing on expanding our operations in Germany and neighboring countries.\n\nPlease review the attached financial report and provide your feedback by the end of the week.",
    timestamp: "2024-03-15 09:30:45",
    sender: "finance@example.com",
    attachments: [
      {
        fileName: "Q1_Financial_Report.pdf",
        data: "APPLE INC.\nQUARTERLY FINANCIAL REPORT\nQ1 2024\n\nEXECUTIVE SUMMARY\n\nApple Inc. has experienced significant growth in the first quarter of 2024, with revenue increasing by $5M compared to the previous quarter. This growth was primarily driven by strong performance in European markets, particularly in Germany and surrounding regions.\n\nKEY FINANCIAL INDICATORS:\n\n- Total Revenue: $97.3 billion\n- Gross Margin: 43.7%\n- Operating Income: $30.1 billion\n- Net Income: $24.2 billion\n- Earnings Per Share: $1.52\n\nREGIONAL PERFORMANCE:\n\n- Americas: $40.9 billion\n- Europe: $25.1 billion\n- Greater China: $18.3 billion\n- Japan: $7.7 billion\n- Rest of Asia Pacific: $5.3 billion\n\nPRODUCT CATEGORY BREAKDOWN:\n\n- iPhone: $50.6 billion\n- Mac: $10.4 billion\n- iPad: $7.6 billion\n- Wearables, Home and Accessories: $8.8 billion\n- Services: $19.9 billion\n\nOUTLOOK:\n\nBased on current market conditions and product pipeline, we project continued growth in the upcoming quarters, with particular emphasis on services and wearable technology segments.",
      },
      {
        fileName: "Market_Analysis.xlsx",
        data: "MARKET ANALYSIS REPORT\n\nCOMPETITIVE LANDSCAPE\n\n1. Samsung Electronics\n   - Market Share: 19.2%\n   - Key Strengths: Diverse product portfolio, strong presence in emerging markets\n   - Key Weaknesses: Lower profit margins, fragmented software ecosystem\n\n2. Microsoft Corporation\n   - Market Share: 15.7%\n   - Key Strengths: Enterprise solutions, cloud services\n   - Key Weaknesses: Limited hardware presence\n\n3. Google (Alphabet Inc.)\n   - Market Share: 12.3%\n   - Key Strengths: Search dominance, Android ecosystem\n   - Key Weaknesses: Hardware profitability\n\nMARKET TRENDS:\n\n1. Artificial Intelligence Integration\n   - Growing consumer demand for AI-powered features\n   - Competitors rapidly expanding AI capabilities\n   - Opportunity for differentiation through unique AI implementations\n\n2. Sustainability Focus\n   - Increasing regulatory pressure for environmental compliance\n   - Consumer preference shifting toward eco-friendly products\n   - Potential for brand enhancement through sustainability initiatives\n\n3. Supply Chain Resilience\n   - Ongoing global supply chain disruptions\n   - Strategic advantages for companies with diversified manufacturing\n   - Opportunity to strengthen regional production capabilities\n\nRECOMMENDATIONS:\n\n1. Increase investment in Berlin operations to capitalize on European market growth\n2. Accelerate AI integration across product lines\n3. Expand services ecosystem to enhance customer retention\n4. Develop stronger sustainability messaging to appeal to environmentally conscious consumers",
      },
    ],
    entities: [
      {
        "entity": "Apple Inc.",
        "label": "ORG",
        "start_idx": 0,
        "end_idx": 10
      },
      {
        "entity": "$5M",
        "label": "MONEY",
        "start_idx": 46,
        "end_idx": 49
      },
      {
        "entity": "Berlin",
        "label": "GPE",
        "start_idx": 53,
        "end_idx": 59
      },
      {
        "entity": "2024 fiscal year",
        "label": "DATE",
        "start_idx": 64,
        "end_idx": 80
      },
      {
        "entity": "European",
        "label": "NORP",
        "start_idx": 169,
        "end_idx": 177
      },
      {
        "entity": "the upcoming quarter",
        "label": "DATE",
        "start_idx": 236,
        "end_idx": 256
      },
      {
        "entity": "Germany",
        "label": "GPE",
        "start_idx": 298,
        "end_idx": 305
      },
      {
        "entity": "the end of the week",
        "label": "DATE",
        "start_idx": 407,
        "end_idx": 426
      }
    ]
  }
]

// Sample classifications
export const classifications: Classification[] = [
  {
    email_id: "email-001",
    request_type: "Financial Report",
    request_subtype: "Quarterly Update",
    confidence: 0.92,
    reasoning:
      "The email contains financial figures, mentions a quarterly report, and includes financial document attachments. The language and context clearly indicate this is a financial reporting email.",
  },
  {
    email_id: "email-002",
    request_type: "Meeting Request",
    request_subtype: "Product Launch",
    confidence: 0.87,
    reasoning:
      "The email explicitly requests a meeting, provides a specific date, and discusses a product launch. The presence of budget information and potential partnership details further confirms this classification.",
  },
]

