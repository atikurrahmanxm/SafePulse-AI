"""Curated, documented labeled dataset for small-business phishing & scam detection.

Dataset provenance & design:
- Domain: Small and Medium Enterprises (SMEs), retail shops, pharmacies, and startups
  (including Indian MSME contexts such as GST, UPI, KYC, courier, and bank alerts,
  alongside global SaaS/cloud/invoice scams).
- Channels covered: Email, SMS, and WhatsApp messages.
- Labels:
    1 = Phishing / Social Engineering / Scam attempt
    0 = Benign / Legitimate business communication
- Important note: This curated benchmark dataset is designed for lightweight,
  interpretable TF-IDF + Logistic Regression training in an offline-capable SME
  security tool. It includes hard negatives (legitimate bank/OTP/GST notices that
  contain financial terms without malicious lures) to reduce false positives.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class LabeledSample:
    text: str
    label: int  # 1 = phishing/scam, 0 = legitimate
    channel: str
    category: str


DATASET: List[LabeledSample] = [
    # --- PHISHING / SCAM SAMPLES (label=1) ---
    LabeledSample(
        "URGENT: Your SBI corporate bank account will be suspended within 2 hours due to incomplete KYC. Update PAN and netbanking password immediately at http://sbi-kyc-verify-portal.xyz/login",
        1, "sms", "bank_kyc_lure"
    ),
    LabeledSample(
        "Dear Customer, your HDFC current account is temporarily blocked. Click https://hdfc-secure-unlock.top/verify and enter your OTP and debit card PIN to restore access today.",
        1, "sms", "bank_kyc_lure"
    ),
    LabeledSample(
        "FINAL NOTICE: Your business GSTIN registration faces cancellation for mismatch in GSTR-3B. Pay penalty Rs 4,850 via UPI link http://gst-portal-pay.click/penalty within 24 hours.",
        1, "email", "gov_tax_impersonation"
    ),
    LabeledSample(
        "Income Tax Department Alert: Your MSME tax refund of Rs 38,420 is approved. Confirm your bank account number and ATM PIN on http://incometax-refund-claim.info to receive credit.",
        1, "email", "gov_tax_impersonation"
    ),
    LabeledSample(
        "Hi, this is the pharmacy owner speaking from a new WhatsApp number. I am stuck in a hospital meeting. Transfer Rs 25,000 urgently to this UPI ID merchantpay88@ybl for supplier clearance. Will settle tonight.",
        1, "whatsapp", "ceo_whatsapp_impersonation"
    ),
    LabeledSample(
        "Hello team, I changed my mobile number today. Please buy 5 Amazon gift vouchers worth Rs 5,000 each for an urgent client visit and send me the voucher codes immediately. Do not call me.",
        1, "whatsapp", "gift_card_scam"
    ),
    LabeledSample(
        "Microsoft 365 Security Alert: Unusual sign-in detected from Moscow on your business email. Your mailbox will be deactivated in 1 hour unless you verify credentials at http://198.51.100.42/o365-login",
        1, "email", "credential_harvesting"
    ),
    LabeledSample(
        "Google Workspace Admin: Your domain email storage is 99% full and incoming supplier emails are queued. Sign in now at http://mail-quota-upgrade.gq/auth to keep receiving orders.",
        1, "email", "credential_harvesting"
    ),
    LabeledSample(
        "India Post Delivery Failed: Your wholesale stock parcel could not be delivered due to incomplete address. Pay Rs 29 redelivery fee and enter card details at http://bit.ly/indpost-track-fee",
        1, "sms", "delivery_scam"
    ),
    LabeledSample(
        "BlueDart Express: Customs duty of Rs 1,299 is pending on your shop shipment AWB884920. Clear payment within 3 hours at http://bluedart-customs-pay.shop or package will be returned.",
        1, "sms", "delivery_scam"
    ),
    LabeledSample(
        "URGENT INVOICE OVERDUE: Attached updated bank details for our wholesale medicine supply. Please remit Rs 1,42,000 to our new beneficiary account today to avoid dispatch hold.",
        1, "email", "bec_invoice_fraud"
    ),
    LabeledSample(
        "Vendor Payment Update: Our regular ICICI account is under audit. Send this month's hardware invoice payment to our alternate account immediately and reply with UTR screenshot.",
        1, "email", "bec_invoice_fraud"
    ),
    LabeledSample(
        "Congratulations! Your shop phone number won Rs 2,50,000 in the Digital Vyapar Lucky Draw. Share Aadhaar, PAN photo, and Rs 1,999 processing charge on WhatsApp to claim prize.",
        1, "whatsapp", "lottery_advance_fee"
    ),
    LabeledSample(
        "WhatsApp Support Warning: Your business WhatsApp account has been reported for policy violation and will be banned permanently in 12 hours. Appeal now: http://wa-business-appeal.cc/verify",
        1, "whatsapp", "account_suspension_lure"
    ),
    LabeledSample(
        "Paytm Business Merchant Alert: Your QR settlement of Rs 18,900 is on hold. Scan the attached QR code and enter your UPI PIN to receive funds into your bank account.",
        1, "whatsapp", "upi_pin_scam"
    ),
    LabeledSample(
        "PhonePe Merchant: To accept your pending Rs 9,500 customer payment, open the request link and type your 6-digit UPI PIN immediately.",
        1, "sms", "upi_pin_scam"
    ),
    LabeledSample(
        "Electricity Board Disconnection Notice: Your shop power supply will be disconnected tonight at 9:30 PM because last month bill was not updated. Call officer 9876500011 and share AnyDesk code.",
        1, "sms", "remote_access_scam"
    ),
    LabeledSample(
        "Dear Merchant, install our quick KYC verification APK file from http://kyc-update-apk.ru/app.apk and allow screen sharing so our executive can reactivate your POS machine.",
        1, "whatsapp", "malware_apk_lure"
    ),
    LabeledSample(
        "Meta Business Suite: Your shop Facebook and Instagram page infringes trademark rights. Confirm page ownership within 24 hours at http://meta-copyright-support.ml/login or face deletion.",
        1, "email", "social_media_phishing"
    ),
    LabeledSample(
        "Axis Bank Corporate: Your digital signature token expires tonight. Re-authenticate your login ID, password, and transaction PIN at http://axis-corp-renew.cf/portal",
        1, "email", "credential_harvesting"
    ),
    LabeledSample(
        "ICICI NetBanking: Suspicious international transaction of Rs 74,500 attempted. If not initiated by you, cancel immediately by entering OTP at http://icici-cancel-txn.buzz",
        1, "sms", "credential_harvesting"
    ),
    LabeledSample(
        "Razorpay Merchant Desk: Your settlement payout is frozen pending compliance review. Upload director PAN and banking password at http://razorpay-compliance-desk.site",
        1, "email", "payment_gateway_phishing"
    ),
    LabeledSample(
        "Zoho Books Subscription Suspended: Your billing card was declined. Update card number and CVV within 2 hours at http://zoho-billing-retry.info to avoid accounting data loss.",
        1, "email", "saas_billing_phishing"
    ),
    LabeledSample(
        "EPFO Employer Alert: PF filings rejected due to UAN verification error. Log in via http://epfo-employer-fix.xyz with employer password immediately.",
        1, "email", "gov_tax_impersonation"
    ),
    LabeledSample(
        "Special MSME Mudra Loan Approved! Get Rs 10 Lakh collateral-free business loan in 15 minutes. Pay Rs 2,500 file charge today via UPI to unlock instant disbursement.",
        1, "whatsapp", "loan_advance_fee"
    ),
    LabeledSample(
        "Attention HR: Download the revised employee salary sheet Resume_2026.zip.exe from http://hr-payroll-docs.top and enable macros to view bonus allocation.",
        1, "email", "malware_attachment_lure"
    ),
    LabeledSample(
        "Shopify Store Warning: Your online storefront violated merchant terms and checkout is disabled. Verify store admin login at http://shopify-merchant-appeal.com-security.pw",
        1, "email", "credential_harvesting"
    ),
    LabeledSample(
        "HDFC Credit Card Reward Points worth Rs 14,200 expire today! Redeem cash directly into account by entering card expiry and CVV on http://tinyurl.com/hdfc-redeem99",
        1, "sms", "reward_points_scam"
    ),
    LabeledSample(
        "Urgent Customs Clearance: Your international sample shipment contains restricted items. Pay Rs 19,500 fine immediately to avoid legal action and arrest warrant.",
        1, "whatsapp", "extortion_impersonation"
    ),
    LabeledSample(
        "Canara Bank Alert: Your mobile banking is locked due to multiple wrong attempts. Click http://canara-unblock-online.work and submit MPIN and ATM PIN.",
        1, "sms", "bank_kyc_lure"
    ),
    LabeledSample(
        "Dear Business Partner, we shared a confidential tender quote on Google Drive. Sign in with your corporate email and password at http://drive-tender-share.online/auth to view.",
        1, "email", "credential_harvesting"
    ),
    LabeledSample(
        "Security Warning: Your TallyPrime cloud backup failed due to expired license key. Renew immediately using unverified link http://tally-cloud-renew.icu or lose ledger files.",
        1, "email", "saas_billing_phishing"
    ),
    LabeledSample(
        "Airtel Business Fiber: Your internet plan will terminate in 3 hours for unpaid Rs 899 balance. Click http://airtel-bill-instant.life to pay via netbanking login.",
        1, "sms", "utility_disconnection_scam"
    ),
    LabeledSample(
        "Boss here, are you at the counter? Need you to send Rs 15,000 GPay to vendor Ramesh right now, I am on a flight and cannot open my banking app. Keep this confidential.",
        1, "whatsapp", "ceo_whatsapp_impersonation"
    ),
    LabeledSample(
        "Verify your PAN-Aadhaar linking today! Penalty of Rs 10,000 will be debited automatically unless you submit OTP at http://pan-aadhaar-linknow.space",
        1, "sms", "gov_tax_impersonation"
    ),
    LabeledSample(
        "Amazon Seller Central: Your seller payouts are paused due to unverified bank account. Log in immediately at http://sellercentral-amazon-verify.net/signin",
        1, "email", "credential_harvesting"
    ),
    LabeledSample(
        "Flipkart Seller Hub: Action required within 4 hours! Confirm your GST certificate and password on http://flipkart-seller-kyc.biz to prevent account suspension.",
        1, "email", "credential_harvesting"
    ),
    LabeledSample(
        "Hi, I mistakenly transferred Rs 8,000 to your shop GPay number instead of my brother. Please click this collect request and enter your UPI PIN to refund Rs 8,000 back.",
        1, "whatsapp", "upi_pin_scam"
    ),
    LabeledSample(
        "Cyber Cell Notice: Illegal activity traced to your shop IP address. Respond within 6 hours with ID proof and security deposit to avoid FIR registration.",
        1, "email", "extortion_impersonation"
    ),
    LabeledSample(
        "Urgent: Your domain name registration expires in 2 hours! Click http://domain-renew-fast.click to enter credit card details and prevent website shutdown.",
        1, "email", "saas_billing_phishing"
    ),
    LabeledSample(
        "Kotak Mahindra Bank: Your corporate netbanking token has been de-registered. Re-activate immediately at http://kotak-netbank-fix.top/login using CRN and password.",
        1, "sms", "bank_kyc_lure"
    ),
    LabeledSample(
        "Dear Sir, your shop has been selected for Government Solar Subsidy 90% off. Send Rs 4,500 registration fee and bank passbook photo to our WhatsApp agent today.",
        1, "whatsapp", "gov_subsidy_scam"
    ),
    LabeledSample(
        "FedEx Parcel Held: Incorrect pincode on package #FDX9012. Update address and pay Rs 45 verification fee at http://fedex-india-rebook.xyz",
        1, "sms", "delivery_scam"
    ),
    LabeledSample(
        "Password Expiry Alert: Your company email password expires today. Keep your same password by signing into http://webmail-keep-password.gq/verify",
        1, "email", "credential_harvesting"
    ),
    LabeledSample(
        "Urgent Wire Request: Please process Rs 95,000 advance to new supplier account before 3 PM bank cutoff. Attached invoice is marked confidential.",
        1, "email", "bec_invoice_fraud"
    ),
    LabeledSample(
        "Dear merchant, install TeamViewer QuickSupport and read out the 9-digit session ID so our bank representative can credit your cashback of Rs 5,000.",
        1, "whatsapp", "remote_access_scam"
    ),
    LabeledSample(
        "Notice: Your FSSAI food license renewal is overdue! Pay late fee Rs 3,200 immediately via http://fssai-renew-portal.info to avoid shop sealing.",
        1, "sms", "gov_tax_impersonation"
    ),
    LabeledSample(
        "DocuSign Secure Document: You received an urgent partnership contract from Legal Team. Open and sign in with email password at http://docusign-view-contract.club",
        1, "email", "credential_harvesting"
    ),
    LabeledSample(
        "Zoom Missed Meeting: Your supplier recorded an urgent pricing update. Download meeting transcript player at http://zoom-recording-dl.pw/setup.exe",
        1, "email", "malware_attachment_lure"
    ),
    LabeledSample(
        "SBI YONO Business: Your profile password will be blocked tonight. Update KYC details and share 6-digit OTP on http://yono-sbi-kyc24.site",
        1, "sms", "bank_kyc_lure"
    ),
    LabeledSample(
        "Urgent HR Policy Update: All staff must verify bank salary account details before Friday at http://staff-payroll-confirm.buzz or salary will be held.",
        1, "email", "credential_harvesting"
    ),
    LabeledSample(
        "Congratulations! Your pharmacy won a freePOS terminal upgrade. Pay Rs 999 refundable deposit via QR scan and enter UPI PIN.",
        1, "whatsapp", "upi_pin_scam"
    ),
    LabeledSample(
        "Cloudflare DNS Alert: Your business website SSL certificate was revoked. Re-verify admin credentials at http://cloudflare-ssl-fix.top",
        1, "email", "credential_harvesting"
    ),
    LabeledSample(
        "DTDC Courier Alert: Package returned to hub due to unpaid Rs 35 handling charge. Complete card payment at http://dtdc-pay-hub.click",
        1, "sms", "delivery_scam"
    ),
    LabeledSample(
        "Hi, I am calling from customer care. Your UPI merchant wallet is deactivated. Forward the SMS verification code you just received to reactivate immediately.",
        1, "whatsapp", "otp_theft"
    ),
    LabeledSample(
        "Bank of Baroda: Dear user your debit card is blocked. Click http://bob-card-unblock.xyz and enter 16-digit card number, CVV, and ATM PIN.",
        1, "sms", "bank_kyc_lure"
    ),
    LabeledSample(
        "Your Google Business Profile has 3 policy strikes and will be removed from Maps within 24 hours. Verify business owner account at http://gbp-appeal-center.site",
        1, "email", "account_suspension_lure"
    ),
    LabeledSample(
        "Urgent: Your WhatsApp backup encryption key expired. Enter your 6-digit two-step verification PIN at http://wa-pin-restore.online to avoid chat deletion.",
        1, "whatsapp", "otp_theft"
    ),
    LabeledSample(
        "QuickBooks Invoice #88412 overdue Rs 64,000. Download compressed PDF invoice script at http://qb-invoice-view.icu/inv88412.zip",
        1, "email", "malware_attachment_lure"
    ),
    LabeledSample(
        "Immediate Action Required: Someone logged into your business Gmail from Lagos. Click http://gmail-security-recover.ml to confirm password now.",
        1, "email", "credential_harvesting"
    ),
    LabeledSample(
        "Warning: Your shop GST e-way bill portal access is suspended. Reset credentials urgently at http://ewaybill-gst-reset.work",
        1, "email", "gov_tax_impersonation"
    ),
    LabeledSample(
        "Dear customer, your NEFT transfer of Rs 49,000 failed. Re-initiate by entering netbanking ID and transaction password at http://neft-retry-help.shop",
        1, "sms", "credential_harvesting"
    ),
    LabeledSample(
        "Hi boss, supplier wants immediate payment in crypto or gift cards for customs release. Please transfer right now and do not discuss with accounts team.",
        1, "whatsapp", "ceo_whatsapp_impersonation"
    ),
    LabeledSample(
        "HDFC NetBanking Alert: Mandatory PAN update required today before 5 PM or all outbound payments freeze. Verify at http://hdfc-pan-update.pw",
        1, "sms", "bank_kyc_lure"
    ),

    # --- LEGITIMATE / BENIGN SAMPLES (label=0) ---
    LabeledSample(
        "Hi Priya, attached is our monthly medicine supply invoice #INV-2026-0412 for Rs 32,450 as discussed on yesterday's call. Payment terms remain Net 15 to our registered bank account on file.",
        0, "email", "legit_vendor_invoice"
    ),
    LabeledSample(
        "SBI Alert: Rs 12,500.00 credited to your A/c XX4821 via UPI/NEFT on 10-Nov-2026. Available balance is Rs 1,84,220.50. Never share OTP, PIN, or CVV with anyone.",
        0, "sms", "legit_bank_alert"
    ),
    LabeledSample(
        "Your OTP for logging into the official GST Portal (gst.gov.in) is 492817. It is valid for 10 minutes. Do not share this OTP with anyone including GST officials.",
        0, "sms", "legit_otp_notice"
    ),
    LabeledSample(
        "Good morning team, please review our weekly store inventory checklist before Thursday's stock audit. Let me know in the shop WhatsApp group if any shelf labels need reprinting.",
        0, "whatsapp", "legit_internal_ops"
    ),
    LabeledSample(
        "HDFC Bank: Thank you for your NEFT payment of Rs 18,400 to MedPlus Distributors. Reference ID HDFC99201847. If you did not authorize this, call our official helpline printed on your card.",
        0, "sms", "legit_bank_alert"
    ),
    LabeledSample(
        "Dear Business Owner, your GST GSTR-1 return for October 2026 was filed successfully on the GST portal. Acknowledgement Reference Number AA181126004921K.",
        0, "email", "legit_gov_receipt"
    ),
    LabeledSample(
        "Hello, this is Rakesh from Guwahati Paper Packaging. Can you confirm if we should deliver 200 corrugated boxes tomorrow morning at 10 AM to your Zoo Road shop?",
        0, "whatsapp", "legit_supplier_chat"
    ),
    LabeledSample(
        "BlueDart Shipment Update: Waybill 5582910342 has arrived at Guwahati Hub and is out for delivery today. No additional payment is required for prepaid orders.",
        0, "sms", "legit_delivery_update"
    ),
    LabeledSample(
        "Reminder: Our monthly bookkeeping review meeting with CA Sharma is scheduled for Friday at 4:00 PM at the office. Please bring the October purchase register.",
        0, "email", "legit_meeting_reminder"
    ),
    LabeledSample(
        "Google Workspace Billing Receipt: Your monthly invoice for Rs 1,350 has been paid using your saved corporate Visa ending in 4012. View details anytime in admin.google.com.",
        0, "email", "legit_billing_receipt"
    ),
    LabeledSample(
        "Customer Inquiry: Hi, do you have Accu-Chek Active 50 test strips in stock at your pharmacy? Please let me know the price and closing time today.",
        0, "whatsapp", "legit_customer_inquiry"
    ),
    LabeledSample(
        "Paytm for Business: Daily settlement of Rs 24,680.00 for 42 QR transactions has been transferred to your linked bank account XX9012. Check your Paytm Business app for summary.",
        0, "sms", "legit_settlement_alert"
    ),
    LabeledSample(
        "Airtel Business: Your monthly broadband invoice for November 2026 is Rs 1,179.00, due on 25-Nov-2026. Pay securely through the official Airtel Thanks app.",
        0, "email", "legit_utility_bill"
    ),
    LabeledSample(
        "Hi Ananya, thanks for sending the quotation for 15 office chairs. Our management approved the budget and we will issue a formal purchase order by Monday.",
        0, "email", "legit_sales_thread"
    ),
    LabeledSample(
        "India Post Tracking: Article EK482910445IN has been delivered to recipient at Dispur SO on 11-Nov-2026 at 14:22 hrs.",
        0, "sms", "legit_delivery_update"
    ),
    LabeledSample(
        "Team Notice: We are updating our shop Wi-Fi router password this Saturday evening. Please ask the store manager in person for the new staff credentials.",
        0, "whatsapp", "legit_internal_ops"
    ),
    LabeledSample(
        "Microsoft 365: Your scheduled backup report for November completed with zero errors. Sign in directly through portal.office.com if you want to review audit logs.",
        0, "email", "legit_system_report"
    ),
    LabeledSample(
        "ICICI Bank Update: Your KYC documents submitted at the Fancy Bazar branch have been verified successfully. Thank you for banking with us.",
        0, "sms", "legit_bank_alert"
    ),
    LabeledSample(
        "Hi sir, I have shared the updated product catalog PDF on our shared office folder. Let me know which items to reorder for the festival season.",
        0, "whatsapp", "legit_internal_ops"
    ),
    LabeledSample(
        "Razorpay Settlement: Payout #pyt_99281 of Rs 41,200.00 is processed to your registered bank account. No action is needed from your side.",
        0, "email", "legit_settlement_alert"
    ),
    LabeledSample(
        "Appointment Confirmation: Your laptop hardware servicing appointment is confirmed for tomorrow 11:30 AM at the Authorized Service Center.",
        0, "sms", "legit_appointment"
    ),
    LabeledSample(
        "Dear Partner, please find our quarterly price list attached. Note that our bank details and GST number remain completely unchanged from last year.",
        0, "email", "legit_vendor_invoice"
    ),
    LabeledSample(
        "Zoho Books: Automated weekly summary — 14 invoices issued totaling Rs 1,12,000 and 3 bills pending approval inside your Zoho Books dashboard.",
        0, "email", "legit_system_report"
    ),
    LabeledSample(
        "Hello, I paid Rs 650 via UPI at your counter just now for groceries. Transaction ID 431982041122. Please confirm receipt.",
        0, "whatsapp", "legit_customer_inquiry"
    ),
    LabeledSample(
        "CERT-In Advisory Summary: Businesses are advised to enable multi-factor authentication on all email accounts and verify vendor bank changes by phone call.",
        0, "email", "legit_security_bulletin"
    ),
    LabeledSample(
        "Your Amazon Business order #402-8819201 for printer toner cartridges has shipped and is expected to arrive by Thursday.",
        0, "email", "legit_delivery_update"
    ),
    LabeledSample(
        "Staff Schedule: Deepika will cover the morning counter shift from 8 AM to 2 PM and Rohan will handle evening billing from 2 PM to 8 PM.",
        0, "whatsapp", "legit_internal_ops"
    ),
    LabeledSample(
        "Axis Bank Reminder: Your quarterly current account statement is ready in your Axis Mobile app. We never ask for passwords or OTP over SMS or links.",
        0, "sms", "legit_bank_alert"
    ),
    LabeledSample(
        "Thank you for registering for the AdtU MSME Digital Safety Workshop on 18-Nov-2026 at 10:30 AM. Venue: Auditorium Block B.",
        0, "email", "legit_event_confirmation"
    ),
    LabeledSample(
        "Good evening, please send the batch numbers for today's cold-chain vaccine delivery so we can log them in our pharmacy compliance register.",
        0, "whatsapp", "legit_internal_ops"
    ),
    LabeledSample(
        "TallyPrime Support: Ticket #TP-44102 regarding GST e-invoicing printer margin has been resolved. Reply to this ticket if you still need assistance.",
        0, "email", "legit_support_ticket"
    ),
    LabeledSample(
        "APDCL Electricity Bill: Your consumer number 104928102 bill for Rs 3,420 has been generated. Pay conveniently via the official APDCL app or authorized bill counters.",
        0, "sms", "legit_utility_bill"
    ),
    LabeledSample(
        "Hi Priya, can we reschedule our supplier call to 3:30 PM today? I am finishing an inventory check with the warehouse team.",
        0, "whatsapp", "legit_supplier_chat"
    ),
    LabeledSample(
        "Kotak Bank: Rs 4,200.00 debited from A/c XX3310 via POS purchase at Metro Cash & Carry. Call 1860-266-2666 if unauthorized.",
        0, "sms", "legit_bank_alert"
    ),
    LabeledSample(
        "Your domain safepulse-demo.in auto-renewal succeeded for 1 year. Receipt available inside your registrar account control panel.",
        0, "email", "legit_billing_receipt"
    ),
    LabeledSample(
        "Dear Merchant, PhonePe never asks you to enter your UPI PIN to receive money or claim cashback. Stay alert against collect-request scams.",
        0, "sms", "legit_security_bulletin"
    ),
    LabeledSample(
        "Monthly Rent Receipt: Received Rs 22,000 via bank transfer towards shop premises rent for November 2026. Regards, Landlord.",
        0, "email", "legit_billing_receipt"
    ),
    LabeledSample(
        "Hey team, remember to lock your billing PC screen before stepping out for lunch and keep customer phone numbers private.",
        0, "whatsapp", "legit_internal_ops"
    ),
    LabeledSample(
        "Flipkart Seller Update: Settlement of Rs 19,840 for delivered orders has been scheduled for tomorrow's NEFT cycle.",
        0, "email", "legit_settlement_alert"
    ),
    LabeledSample(
        "One-Time Password for updating your store Wi-Fi router admin settings is 773109. Do not share this code with anyone.",
        0, "sms", "legit_otp_notice"
    ),
    LabeledSample(
        "Hi, we need 30 boxes of paracetamol 650mg and 10 bottles of antiseptic liquid for our clinic tomorrow. Please share the GST bill amount.",
        0, "whatsapp", "legit_customer_inquiry"
    ),
    LabeledSample(
        "EPFO Update: Monthly ECR challan for October 2026 has been reconciled. Download payment receipt directly from unifiedportal-emp.epfindia.gov.in.",
        0, "email", "legit_gov_receipt"
    ),
    LabeledSample(
        "Your Zoom meeting 'Q4 Stock Planning' starts in 15 minutes. Join via the official Zoom desktop app using meeting ID 842 9910 3312.",
        0, "email", "legit_meeting_reminder"
    ),
    LabeledSample(
        "Canara Bank: Cheque No. 004812 for Rs 15,000 has been cleared. Thank you for banking with Canara Bank.",
        0, "sms", "legit_bank_alert"
    ),
    LabeledSample(
        "Hello, please keep the printout of our FSSAI license framed near the billing counter as requested during routine inspection.",
        0, "whatsapp", "legit_internal_ops"
    ),
    LabeledSample(
        "Amazon Seller Digest: 12 new customer orders received today. Log in through sellercentral.amazon.in to print shipping labels.",
        0, "email", "legit_system_report"
    ),
    LabeledSample(
        "Dear Customer, your insurance policy renewal notice for Shopkeeper Package Policy is attached for your records. Renew via your branch advisor or official portal.",
        0, "email", "legit_billing_receipt"
    ),
    LabeledSample(
        "Hi, could you check if invoice #2088 from last Tuesday included 18% GST? Our accountant is reconciling the ledger today.",
        0, "email", "legit_sales_thread"
    ),
    LabeledSample(
        "Delivery Notice: Your stationery order from LocalMart has been dropped off at your reception desk and signed by Aman.",
        0, "sms", "legit_delivery_update"
    ),
    LabeledSample(
        "Reminder to all staff: Always verify payment confirmation in our official merchant app before handing over goods.",
        0, "whatsapp", "legit_internal_ops"
    ),
    LabeledSample(
        "Income Tax Portal: Your e-filing password was changed at your request. If you did not do this, visit incometax.gov.in immediately.",
        0, "email", "legit_system_report"
    ),
    LabeledSample(
        "Good afternoon! Sharing the revised holiday calendar for our Guwahati store for the upcoming Bihu and winter season.",
        0, "email", "legit_internal_ops"
    ),
    LabeledSample(
        "Bank of Baroda Alert: Your fixed deposit #FD99201 matured today and proceeds of Rs 1,06,400 have been auto-credited to your linked account.",
        0, "sms", "legit_bank_alert"
    ),
    LabeledSample(
        "Hi, can you send a copy of yesterday's cash memo #412 on email when you get a free moment? Need it for warranty claim.",
        0, "whatsapp", "legit_customer_inquiry"
    ),
    LabeledSample(
        "Shopify Order Notification: Order #1048 for Rs 2,499 paid via Razorpay. Prepare item for standard courier pickup.",
        0, "email", "legit_system_report"
    ),
    LabeledSample(
        "Meta Business Help: Here is your monthly page reach summary — 1,420 local views this week, up 12% from last week.",
        0, "email", "legit_system_report"
    ),
    LabeledSample(
        "DTDC Tracking: Shipment D99120412 is in transit at Kolkata Hub and scheduled for normal delivery in 2 business days.",
        0, "sms", "legit_delivery_update"
    ),
    LabeledSample(
        "Please find attached the minutes from today's local retail association meeting regarding digital payment reconciliation.",
        0, "email", "legit_meeting_reminder"
    ),
    LabeledSample(
        "Hello, we received your payment of Rs 8,500 for printing 500 product brochures. Delivery will be ready by Wednesday afternoon.",
        0, "whatsapp", "legit_supplier_chat"
    ),
    LabeledSample(
        "Your Google Drive backup for 'Shop Accounts FY26' synced successfully 20 minutes ago.",
        0, "email", "legit_system_report"
    ),
    LabeledSample(
        "SBI Card: Statement for period ending 05-Nov-2026 is ready. Total due Rs 11,240.00, due date 25-Nov-2026. Pay via SBI Card app.",
        0, "sms", "legit_bank_alert"
    ),
    LabeledSample(
        "Hi team, please verify that the CCTV recorder clock is synced before closing the store tonight.",
        0, "whatsapp", "legit_internal_ops"
    ),
    LabeledSample(
        "Thank you for contacting Zoho Support. Your GST HSN code configuration question has been answered in our help portal.",
        0, "email", "legit_support_ticket"
    ),
    LabeledSample(
        "Your electricity meter reading was recorded today at 11:10 AM. Monthly bill will be available in 3 days on the official portal.",
        0, "sms", "legit_utility_bill"
    ),
]

