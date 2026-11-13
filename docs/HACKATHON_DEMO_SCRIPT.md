# SafePulse AI — Hackathon Live Demo Script (AdtU Innovation Mela 2026)

**Estimated Live Demo Duration:** 4–5 minutes  
**Note:** All demo scenarios are clearly labeled as demonstration data.

## Step 0: Landing & Bilingual Demo Launch (45 sec)
1. Open `http://localhost:5173`. Show the SaaS landing page (`Your Business Deserves Better Cyber Protection.`).
2. Toggle the top-right **EN / বাংলা** button to demonstrate instant Bengali localization for local shop and pharmacy owners in Assam/Bengal.
3. Click **Launch Hackathon Demo Mode** to enter the pre-seeded demo workspace (*Brahmaputra Care Pharmacy (Demo)*).

## Scenario 1: Suspicious Bank Verification Message (60 sec)
1. Navigate to **Phishing Detector**.
2. Click **"Scenario 1 (Demo): Bank Account Verification Scam"** to load the urgent SBI KYC suspension SMS.
3. Click **Analyze Message**.
4. Highlight to judges:
   - Live Risk Ring & Critical Risk badge
   - Exact suspicious phrases highlighted inline (`URGENT`, `within 2 hours`, `netbanking password`, `http://sbi-kyc-verify-portal.xyz/login`)
   - ML probability + calibrated confidence + actionable recommendations
   - Switch to the **ML Model & Held-Out Evaluation** tab to show real Precision (92.9%), Recall (81.3%), F1 (86.7%), and Confusion Matrix on held-out data.
   - Click **Download PDF Report**.

## Scenario 2: Suspicious Website URL & SSRF Security (45 sec)
1. Navigate to **URL Security Scanner**.
2. Load **"Scenario 2 (Demo): Suspicious Lookalike Bank URL"** and click **Scan URL Safely**.
3. Show brand impersonation + disposable `.xyz` TLD + missing SPF/DMARC DNS records + the explicit **"HTTPS ≠ Safe"** notice.
4. Optionally test `http://127.0.0.1/admin` to demonstrate live **SSRF protection** blocking internal network probes!

## Scenario 3: Business Security Health Check (45 sec)
1. Navigate to **Business Security Assessment**.
2. Show the 10 CERT-In MSME aligned domains, the weighted score gauge, domain bar chart, Critical Gaps (`Multi-Factor Authentication`, `Wi-Fi Security`, `Incident Response Preparedness`), and prioritized actions.

## Scenario 4: Employee Clicks a Phishing Link (45 sec)
1. Navigate to **Incident Response Center**.
2. Open the active **Phishing Link Clicked** playbook (or start a new one) and check off containment items to show live progress tracking and India Helpline **1930** guidance, plus the honest disclaimer that SafePulse AI guides humans rather than claiming automatic malware removal.

