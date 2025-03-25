import base64
from datetime import datetime, timedelta

from src.models import ParsedEmail, Attachment
from src.data_extractor.extractor import extract_fields


# Create a function to generate test cases
def create_test_cases():
    test_cases = []

    # Test Case 1: Invoice with line items and tax
    test_cases.append(
        ParsedEmail(
            email_id="007",
            parsed_body="""
            Dear Customer,
            
            Please find attached your invoice for recent purchases.
            
            Invoice Summary:
            - Subtotal: $850.00
            - Tax (8.5%): $72.25
            - Total Due: $922.25
            
            Payment is due within 30 days (by 2025-04-25).
            Please remit payment to Accounts Receivable.
            
            Thank you for your business.
            
            Billing Department
            """,
            subject="Invoice #INV-2025-789 for Recent Purchases",
            timestamp="2025-03-26 13:45:22",
            sender="billing@supplier.com",
            attachments=[
                Attachment(
                    fileName="invoice.txt",
                    data=base64.b64encode(
                        """
                    INVOICE
                    
                    Invoice Number: INV-2025-789
                    Date: March 26, 2025
                    Due Date: April 25, 2025
                    
                    Bill To:
                    Acme Corporation
                    123 Business St.
                    Corporate City, BZ 12345
                    
                    Items:
                    1. Professional Services - 10 hours @ $75/hr = $750.00
                    2. Materials Fee = $100.00
                    
                    Subtotal: $850.00
                    Tax (8.5%): $72.25
                    Total Due: $922.25
                    
                    Payment Terms: Net 30
                    """.encode()
                    ).decode(),
                )
            ],
        )
    )

    # Test Case 2: Customer Service
    test_cases.append(
        ParsedEmail(
            email_id="008",
            parsed_body="""
        Dear Support Team,

        I've been experiencing issues with my account login for the past two days. 
        Every time I try to access my account, I receive an error message stating 
        "Invalid credentials". I've double-checked my username and password, and I'm 
        certain they are correct.

        My account details:
        Username: jsmith2023
        Last successful login: 2025-03-20

        I've already tried clearing my browser cache and using a different browser, 
        but the issue persists. Can you please help me regain access to my account?

        Thank you for your assistance.

        Best regards,
        John Smith
        """,
            subject="Unable to Access Account - Urgent Assistance Needed",
            timestamp="2025-03-25 09:30:15",
            sender="john.smith@email.com",
            attachments=[
                Attachment(
                    fileName="error_screenshot.jpg.txt",
                    data=base64.b64encode(
                        """
                    [This would be a base64 encoded image, represented here as text]
                    Error message: "Invalid credentials. Please try again or reset your password."
                    Timestamp: 2025-03-25 09:15:22
                    Browser: Chrome 95.0.4638.69
                    OS: Windows 11
                    """.encode()
                    ).decode(),
                )
            ],
        )
    )

    # Test Case 3: Account Management
    test_cases.append(
        ParsedEmail(
            email_id="009",
            parsed_body="""
        Hello Account Management Team,

        I would like to request an upgrade for my current account from the "Silver" tier 
        to the "Gold" tier. I've been a loyal customer for over 5 years now, and I believe 
        I would benefit from the additional features offered in the Gold tier.

        My current account details:
        Account Number: AC98765432
        Current Tier: Silver
        Account Opening Date: 2020-01-15

        Could you please provide me with information about:
        1. The process for upgrading
        2. Any associated costs
        3. New features I'll gain access to
        4. Estimated time for the upgrade to take effect

        I appreciate your help in this matter.

        Kind regards,
        Sarah Johnson
        """,
            subject="Request for Account Upgrade to Gold Tier",
            timestamp="2025-03-26 14:20:30",
            sender="sarah.johnson@email.com",
            attachments=[],
        )
    )

    # Test Case 4: Loan Department
    test_cases.append(
        ParsedEmail(
            email_id="010",
            parsed_body="""
        Dear Loan Department,

        I'm writing to inquire about refinancing options for my current mortgage. 
        Given the recent changes in interest rates, I believe I might be able to 
        secure a better rate and potentially reduce my monthly payments.

        My current mortgage details:
        Loan Number: ML-2020-45678
        Original Loan Amount: $300,000
        Current Balance: $275,000
        Interest Rate: 4.5%
        Loan Term: 30 years (25 years remaining)
        Property Address: 123 Oak Street, Anytown, ST 12345

        I'm particularly interested in:
        1. Current interest rates for a 25-year fixed-rate mortgage
        2. The possibility of a 20-year term to pay off the loan faster
        3. Any fees associated with refinancing
        4. The estimated break-even point for the refinance

        My credit score has improved since I originally took out the loan, 
        now standing at 780. I have a stable job with an annual income of $90,000.

        Thank you for your assistance. I look forward to discussing my options.

        Best regards,
        Michael Brown
        """,
            subject="Inquiry About Mortgage Refinancing Options",
            timestamp="2025-03-27 10:45:00",
            sender="michael.brown@email.com",
            attachments=[
                Attachment(
                    fileName="current_mortgage_statement.pdf.txt",
                    data=base64.b64encode(
                        """
                    MORTGAGE STATEMENT
                    
                    Statement Date: 2025-03-01
                    Loan Number: ML-2020-45678
                    Borrower: Michael Brown
                    
                    Original Loan Amount: $300,000.00
                    Current Principal Balance: $275,000.00
                    Interest Rate: 4.5%
                    Monthly Payment: $1,520.06
                    Escrow Balance: $3,500.00
                    
                    Next Payment Due: 2025-04-01
                    """.encode()
                    ).decode(),
                )
            ],
        )
    )

    # Test Case 5: Fraud Prevention
    test_cases.append(
        ParsedEmail(
            email_id="011",
            parsed_body="""
        Urgent: Suspicious Account Activity Detected

        We have detected potentially fraudulent activity on the following account:

        Account Number: 9876-5432-1098-7654
        Cardholder Name: Emily Davis
        Last 4 Digits: 7654
        Flagged Transactions:
        1. 2025-03-28 02:15:30 UTC - $500.00 - Online Electronics Store
        2. 2025-03-28 02:17:45 UTC - $750.00 - Online Jewelry Store
        3. 2025-03-28 02:20:10 UTC - $1,000.00 - Online Gift Card Purchase

        These transactions have been flagged due to:
        - Unusual time of transactions (middle of the night)
        - High-value purchases in quick succession
        - Transactions originating from an IP address in a foreign country

        Current account status: Temporarily suspended pending verification

        Immediate action required:
        1. Verify if these transactions are legitimate with the account holder
        2. If fraudulent, initiate our fraud response protocol
        3. Update the account status based on findings

        Please handle this case with high priority.

        Automated Fraud Detection System
        """,
            subject="ALERT: Suspicious Activity on Account 9876-5432-1098-7654",
            timestamp="2025-03-28 02:25:00",
            sender="fraudalert@bank.com",
            attachments=[
                Attachment(
                    fileName="transaction_log.txt",
                    data=base64.b64encode(
                        """
                    Transaction Log for Account 9876-5432-1098-7654
                    Date Range: 2025-03-27 00:00:00 UTC to 2025-03-28 02:25:00 UTC
                    
                    2025-03-27 09:30:15 UTC, $25.00, Local Coffee Shop
                    2025-03-27 12:45:30 UTC, $65.00, Downtown Restaurant
                    2025-03-27 17:20:00 UTC, $50.00, Gas Station
                    2025-03-28 02:15:30 UTC, $500.00, Online Electronics Store
                    2025-03-28 02:17:45 UTC, $750.00, Online Jewelry Store
                    2025-03-28 02:20:10 UTC, $1,000.00, Online Gift Card Purchase
                    """.encode()
                    ).decode(),
                )
            ],
        )
    )

    # Test Case 6: Marketing Team
    test_cases.append(
        ParsedEmail(
            email_id="012",
            parsed_body="""
        Hello Marketing Team,

        I hope this email finds you well. I'm reaching out to discuss our upcoming 
        summer promotion campaign for our new "EcoSave" account package.

        Campaign Details:
        - Product: EcoSave Account Package
        - Target Launch Date: 2025-06-01
        - Duration: 3 months (June, July, August)
        - Target Audience: Environmentally conscious individuals, age 25-45

        Key Features to Highlight:
        1. Paperless statements
        2. Biodegradable debit card
        3. 0.1% of transactions donated to environmental charities
        4. Higher interest rates for larger balances

        We need to prepare the following materials:
        1. Social media content calendar
        2. Email marketing templates
        3. Branch posters and brochures
        4. Website landing page design
        5. Digital ad creatives (display and video)

        Our budget for this campaign is $250,000. Please provide a breakdown of how 
        you propose to allocate this budget across different channels and activities.

        I've attached our brand guidelines and some initial concept sketches for your reference.

        Let's schedule a kick-off meeting next week to discuss this further. Please 
        propose a few time slots that work for your team.

        Best regards,
        Jennifer Lee
        Product Development Manager
        """,
            subject="EcoSave Account - Summer Promotion Campaign Planning",
            timestamp="2025-03-29 11:00:00",
            sender="jennifer.lee@bank.com",
            attachments=[
                Attachment(
                    fileName="brand_guidelines_2025.pdf.txt",
                    data=base64.b64encode(
                        """
                    BRAND GUIDELINES 2025
                    
                    Color Palette:
                    - Primary Green: #00A86B
                    - Secondary Blue: #0077BE
                    - Accent Orange: #FFA500
                    
                    Typography:
                    - Headings: Montserrat Bold
                    - Body: Open Sans Regular
                    
                    Logo Usage:
                    [Base64 encoded logo image would be here]
                    
                    Brand Voice:
                    - Friendly yet professional
                    - Emphasize sustainability and innovation
                    - Use active voice and clear, concise language
                    """.encode()
                    ).decode(),
                ),
                Attachment(
                    fileName="ecosave_concept_sketches.jpg.txt",
                    data=base64.b64encode(
                        """
                    [This would be a base64 encoded image, represented here as text]
                    Sketch 1: EcoSave debit card design with leaf motif
                    Sketch 2: Mobile app interface showing carbon footprint tracker
                    Sketch 3: Branch poster layout with tagline "Bank Green, Save Green"
                    """.encode()
                    ).decode(),
                ),
            ],
        )
    )

    # Test Case 7:
    test_cases.append(
        ParsedEmail(
            email_id="013",
            parsed_body="""
        To: Compliance Department
        
        INTERNAL MEMO: Regulatory Audit Preparation
        
        We have been notified that the Federal Financial Regulatory Authority (FFRA) 
        will be conducting their annual compliance audit of our institution beginning 
        on 2025-05-15. We have approximately 45 days to prepare all necessary documentation.
        
        The audit will focus on the following areas:
        1. Anti-Money Laundering (AML) procedures
        2. Know Your Customer (KYC) documentation
        3. Data privacy compliance
        4. Fair lending practices
        5. Complaint handling procedures
        
        Required Actions:
        - Conduct an internal pre-audit of all compliance systems by 2025-04-15
        - Update all policy documents to reflect recent regulatory changes
        - Ensure all staff have completed mandatory compliance training
        - Prepare sample transaction reports for the period 2024-05-01 to 2025-04-30
        - Review any compliance incidents from the past year and document remediation steps
        
        The estimated cost for this audit preparation is $75,000, which includes 
        consultant fees and staff overtime. This has been approved by the CFO.
        
        Please assign team members to each area and provide a preparation timeline 
        by the end of this week. We will have weekly status meetings starting next Monday.
        
        Regards,
        Robert Chen
        Chief Compliance Officer
        """,
            subject="IMPORTANT: FFRA Annual Compliance Audit - May 2025",
            timestamp="2025-03-30 09:15:00",
            sender="robert.chen@bank.com",
            attachments=[
                Attachment(
                    fileName="audit_notification.pdf.txt",
                    data=base64.b64encode(
                        """
                    FEDERAL FINANCIAL REGULATORY AUTHORITY
                    
                    Date: March 25, 2025
                    
                    RE: Notice of Annual Compliance Audit
                    
                    To: First National Bank
                    Attn: Chief Compliance Officer
                    
                    This letter serves as official notification that the Federal Financial 
                    Regulatory Authority will conduct its annual compliance audit of your 
                    institution beginning May 15, 2025. The audit is expected to last 
                    approximately two weeks.
                    
                    Our audit team will require access to the following:
                    
                    1. All compliance policies and procedures
                    2. Training records for all staff
                    3. Sample customer onboarding documentation
                    4. Transaction monitoring reports
                    5. Internal audit reports
                    6. Complaint register and resolution documentation
                    
                    Please ensure all materials are prepared and relevant staff are 
                    available during the audit period.
                    
                    Sincerely,
                    
                    Elizabeth Warren
                    Director of Financial Institution Audits
                    Federal Financial Regulatory Authority
                    """.encode()
                    ).decode(),
                ),
                Attachment(
                    fileName="compliance_checklist_2025.xlsx.txt",
                    data=base64.b64encode(
                        """
                    COMPLIANCE AUDIT PREPARATION CHECKLIST
                    
                    Category,Item,Status,Responsible Person,Deadline
                    AML,Update transaction monitoring thresholds,Not Started,TBD,2025-04-15
                    AML,Review high-risk customer accounts,Not Started,TBD,2025-04-20
                    AML,Prepare SAR filing summary,Not Started,TBD,2025-04-25
                    KYC,Audit customer identification procedures,Not Started,TBD,2025-04-10
                    KYC,Review enhanced due diligence cases,Not Started,TBD,2025-04-18
                    KYC,Update beneficial ownership documentation,Not Started,TBD,2025-04-22
                    Data Privacy,Review consent management system,Not Started,TBD,2025-04-12
                    Data Privacy,Audit data retention practices,Not Started,TBD,2025-04-17
                    Data Privacy,Test data breach response plan,Not Started,TBD,2025-04-24
                    Fair Lending,Analyze loan approval statistics,Not Started,TBD,2025-04-15
                    Fair Lending,Review denied application justifications,Not Started,TBD,2025-04-20
                    Fair Lending,Audit pricing models for disparate impact,Not Started,TBD,2025-04-25
                    Complaints,Review complaint resolution timeframes,Not Started,TBD,2025-04-10
                    Complaints,Analyze complaint root causes,Not Started,TBD,2025-04-15
                    Complaints,Audit complaint escalation procedures,Not Started,TBD,2025-04-20
                    """.encode()
                    ).decode(),
                ),
            ],
        )
    )

    # Test Case 8: Investment Services
    test_cases.append(
        ParsedEmail(
            email_id="014",
            parsed_body="""
        Dear Investment Services Team,
        
        I'm writing to request a comprehensive portfolio review and rebalancing 
        recommendation based on my changing financial goals and market conditions.
        
        My current portfolio details:
        - Account Number: INV-87654321
        - Current Value: $750,000
        - Current Allocation:
          * Equities: 65% ($487,500)
          * Fixed Income: 25% ($187,500)
          * Alternatives: 5% ($37,500)
          * Cash: 5% ($37,500)
        
        Recent life changes and goals:
        1. I'm now planning to retire in approximately 10 years (previously 15)
        2. My risk tolerance has decreased slightly due to market volatility
        3. I'm interested in increasing exposure to ESG investments
        4. I need to plan for college expenses for my daughter in 5 years
        
        I've recently received a bonus of $100,000 that I would like to invest 
        as part of this rebalancing. I'm also considering whether I should 
        convert some of my traditional IRA to a Roth IRA this year.
        
        Could you please provide:
        1. A recommended new asset allocation
        2. Specific investment recommendations for the $100,000
        3. Tax-efficient rebalancing strategies
        4. A projection of portfolio performance under different market scenarios
        
        I'm available for a video consultation any weekday after 4:00 PM.
        
        Thank you for your assistance.
        
        Best regards,
        David Wilson
        """,
            subject="Request for Portfolio Review and Rebalancing Recommendations",
            timestamp="2025-03-31 15:30:00",
            sender="david.wilson@email.com",
            attachments=[
                Attachment(
                    fileName="current_portfolio_statement.pdf.txt",
                    data=base64.b64encode(
                        """
                    INVESTMENT PORTFOLIO STATEMENT
                    
                    Account: INV-87654321
                    Name: David Wilson
                    Statement Period: 01/01/2025 - 03/31/2025
                    
                    ACCOUNT SUMMARY
                    Beginning Value (01/01/2025): $725,000.00
                    Deposits: $0.00
                    Withdrawals: $0.00
                    Change in Investment Value: $25,000.00
                    Ending Value (03/31/2025): $750,000.00
                    
                    ASSET ALLOCATION
                    
                    Equities: $487,500.00 (65%)
                    - US Large Cap: $243,750.00 (32.5%)
                    - US Mid/Small Cap: $75,000.00 (10%)
                    - International Developed: $112,500.00 (15%)
                    - Emerging Markets: $56,250.00 (7.5%)
                    
                    Fixed Income: $187,500.00 (25%)
                    - US Government Bonds: $75,000.00 (10%)
                    - Corporate Bonds: $75,000.00 (10%)
                    - Municipal Bonds: $37,500.00 (5%)
                    
                    Alternatives: $37,500.00 (5%)
                    - Real Estate: $18,750.00 (2.5%)
                    - Commodities: $18,750.00 (2.5%)
                    
                    Cash & Equivalents: $37,500.00 (5%)
                    
                    PERFORMANCE
                    YTD Return: 3.45%
                    1-Year Return: 8.75%
                    3-Year Annualized Return: 7.25%
                    5-Year Annualized Return: 8.10%
                    
                    ACCOUNT DETAILS
                    Tax Status: Mixed (Taxable and Tax-Advantaged)
                    Beneficiary: Sarah Wilson (Spouse)
                    Investment Objective: Growth with Moderate Income
                    Risk Tolerance: Moderate
                    Time Horizon: 15 Years
                    """.encode()
                    ).decode(),
                )
            ],
        )
    )

    # Test Case 9: Online Banking Support
    test_cases.append(
        ParsedEmail(
            email_id="015",
            parsed_body="""
        To: Online Banking Support
        
        I've been experiencing persistent issues with your mobile banking app 
        since the latest update (version 4.5.2) released on March 25, 2025.
        
        Device Information:
        - Phone: iPhone 16 Pro
        - iOS Version: 18.2
        - App Version: 4.5.2
        - Account Type: Premium Checking
        
        Issues I'm experiencing:
        
        1. App crashes when attempting to deposit checks using the mobile deposit feature
        2. Biometric login (Face ID) works intermittently, often requiring manual password entry
        3. Transaction history only loads partially (shows last 7 days instead of 90 days)
        4. Bill pay feature shows "Error 4302" when attempting to schedule new payments
        5. Push notifications for transactions are delayed by several hours
        
        Steps I've already taken to troubleshoot:
        - Uninstalled and reinstalled the app
        - Restarted my device
        - Cleared app cache
        - Updated to the latest iOS version
        - Checked my internet connection (I have stable 5G and Wi-Fi)
        
        This is significantly impacting my banking experience as I rely heavily on 
        mobile banking for my daily financial management. I need to deposit several 
        checks by April 5, 2025, and pay bills that are due on April 10, 2025.
        
        Please advise on how to resolve these issues or provide a timeline for when 
        a fix might be available. If necessary, I can provide screen recordings of 
        the errors.
        
        Thank you for your assistance.
        
        Regards,
        Amanda Rodriguez
        """,
            subject="Multiple Issues with Mobile Banking App After Update 4.5.2",
            timestamp="2025-04-01 10:45:00",
            sender="amanda.rodriguez@email.com",
            attachments=[
                Attachment(
                    fileName="error_screenshot.jpg.txt",
                    data=base64.b64encode(
                        """
                    [This would be a base64 encoded image, represented here as text]
                    Error 4302: Unable to connect to bill pay service.
                    Please try again later or contact customer support.
                    """.encode()
                    ).decode(),
                ),
                Attachment(
                    fileName="app_crash_log.txt",
                    data=base64.b64encode(
                        """
                    Mobile Banking App Crash Log
                    Date: 2025-04-01
                    Time: 10:30:15
                    
                    Exception Type: EXC_CRASH (SIGABRT)
                    Exception Codes: 0x0000000000000000, 0x0000000000000000
                    Exception Note: EXC_CORPSE_NOTIFY
                    
                    Triggered by Thread: 0
                    
                    Thread 0 name: Dispatch queue: com.apple.main-thread
                    Thread 0 Crashed:
                    0 libsystem_kernel.dylib 0x00000001a7c3a104 __pthread_kill + 8
                    1 libsystem_pthread.dylib 0x00000001a7c78820 pthread_kill + 268
                    2 libsystem_c.dylib 0x00000001a7b7d848 abort + 180
                    3 com.bank.mobilebanking 0x0000000104a8c7f4 TLSCheckFunction + 0
                    4 com.bank.mobilebanking 0x0000000104a8c7f4 CheckDepositModule::processImage + 544
                    5 com.bank.mobilebanking 0x0000000104a8c7f4 CheckDepositViewController::captureOutput + 788
                    
                    Binary Images:
                    0x1047a8000 - 0x104abffff com.bank.mobilebanking arm64 <2f5e67d330533ae9b55428e5fe473b3a>
                    """.encode()
                    ).decode(),
                ),
            ],
        )
    )

    # Test Case 10: Credit Card Services
    test_cases.append(
        ParsedEmail(
            email_id="016",
            parsed_body="""
        Dear Credit Card Services,
        
        I would like to dispute three unauthorized transactions that appeared on my 
        credit card statement this month. I have never made these purchases and do 
        not recognize the merchants.
        
        Card Details:
        - Card Type: Platinum Rewards
        - Last 4 Digits: 7890
        - Cardholder Name: Thomas Garcia
        
        Disputed Transactions:
        1. Date: 2025-03-28, Amount: $259.99, Merchant: TechGadgetsOnline
        2. Date: 2025-03-28, Amount: $189.50, Merchant: LuxuryCosmetics
        3. Date: 2025-03-29, Amount: $450.00, Merchant: DigitalServicesPlus
        
        I discovered these transactions when reviewing my statement on April 1, 2025. 
        I still have physical possession of my card and have not shared my card details 
        with anyone. I have not authorized anyone else to use my card.
        
        I've already taken the following precautions:
        - Requested a card replacement
        - Changed my online banking password
        - Enabled two-factor authentication
        
        Please investigate these transactions and credit my account for the total 
        disputed amount of $899.49. I understand that I may need to provide additional 
        information or sign an affidavit.
        
        I would also appreciate information on any additional steps I should take to 
        protect my account from future unauthorized access.
        
        Thank you for your prompt attention to this matter.
        
        Sincerely,
        Thomas Garcia
        """,
            subject="Dispute of Unauthorized Transactions - Card ending in 7890",
            timestamp="2025-04-02 16:20:00",
            sender="thomas.garcia@email.com",
            attachments=[
                Attachment(
                    fileName="credit_card_statement.pdf.txt",
                    data=base64.b64encode(
                        """
                    CREDIT CARD STATEMENT
                    
                    Statement Date: April 1, 2025
                    Account Number: XXXX-XXXX-XXXX-7890
                    Cardholder: Thomas Garcia
                    
                    Previous Balance: $1,245.67
                    Payments: -$1,245.67
                    New Charges: $1,523.78
                    Fees: $0.00
                    Interest: $0.00
                    Current Balance: $1,523.78
                    
                    Minimum Payment Due: $45.00
                    Payment Due Date: April 25, 2025
                    Available Credit: $8,476.22
                    
                    TRANSACTION DETAILS
                    
                    03/15/2025, $45.00, GROCERY STORE #123
                    03/17/2025, $78.50, GAS STATION
                    03/20/2025, $125.79, DEPARTMENT STORE
                    03/22/2025, $65.00, RESTAURANT
                    03/25/2025, $60.00, PHARMACY
                    03/28/2025, $259.99, TECHGADGETSONLINE
                    03/28/2025, $189.50, LUXURYCOSMETICS
                    03/29/2025, $450.00, DIGITALSERVICESPLUS
                    03/30/2025, $250.00, AIRLINE TICKETS
                    """.encode()
                    ).decode(),
                )
            ],
        )
    )

    return test_cases


# Function to run tests and display results
def test_extraction_functionality():
    test_cases = create_test_cases()
    results = []

    for i, test_case in enumerate(test_cases):
        print(f"\nProcessing Test Case #{i+1}...")

        # Extract data using your function
        extracted_data = extract_fields(test_case)

        # Store results
        results.append(
            {
                "test_case_id": i + 1,
                "email_subject": test_case.subject,
                "extracted_data": extracted_data,
            }
        )

        # Print results
        print(f"Test Case #{i+1} Results:")
        print(f"  Email Subject: {test_case.subject}")
        print(f"  Amount: {extracted_data.amount}")
        print(f"  Currency: {extracted_data.currency}")
        print(f"  Recipient: {extracted_data.recipient}")
        print(f"  Expiration Date: {extracted_data.expiration_date}")
        print(f"  Priority: {extracted_data.priority}")
        print(f"  Category: {extracted_data.category}")
        print(f"  Action Required: {extracted_data.action_required}")
        print(f"  Summary: {extracted_data.summary}")

    return results


if __name__ == "__main__":
    # Run the tests
    test_results = test_extraction_functionality()
