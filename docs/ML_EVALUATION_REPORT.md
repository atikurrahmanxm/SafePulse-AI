# CyberShield AI — Machine Learning Evaluation Report

## 1. Pipeline Overview

- **Algorithm**: `FeatureUnion` of Word TF-IDF (`ngram_range=(1, 2)`, max 4,500 features) + Character-wb TF-IDF (`ngram_range=(3, 5)`, max 4,500 features), classified by balanced `LogisticRegression(C=2.0, max_iter=1000)`.
- **Explainability Layer**: Paired with transparent regex-based social engineering rules (`urgency_pressure`, `credential_or_otp_request`, `suspicious_payment_or_upi_scam`, `impersonation_authority`, `remote_access_or_malware`, `suspicious_link_or_shortener`, `secrecy_or_bypass`) plus benign protective-notice dampening (e.g., `"Never share OTP with anyone"`).
- **Risk Scoring**: Blended 0–100 application score mapped to:
  - `0–24`: Low Risk
  - `25–49`: Moderate Risk
  - `50–74`: High Risk
  - `75–100`: Critical Risk

## 2. Dataset Description

- **Total Curated Samples**: 128 labeled SME messages across Email, SMS, and WhatsApp (64 phishing/scam, 64 legitimate communications).
- **Phishing Categories Covered**: Bank KYC suspension lures, UPI collect-request PIN traps, GST/Income Tax impersonation, CEO/owner WhatsApp impersonation, courier redelivery fee scams, BEC vendor invoice fraud, remote-access (`AnyDesk`/`TeamViewer`/`.apk`) scams, and SaaS billing lures.
- **Hard-Negative Legitimate Samples**: Genuine SBI/HDFC/ICICI credit/debit alerts, official OTP notices with explicit anti-sharing warnings, GST filing receipts, supplier invoices, and internal shop WhatsApp messages.
- **Split Strategy**: 75% Training (96 samples) / 25% Stratified Held-Out Test Set (32 samples, `random_state=42`).

## 3. Actual Held-Out Evaluation Results

Measured directly on the 32-sample held-out test split:

| Metric | Observed Score |
| :--- | :--- |
| **Accuracy** | **0.8750 (87.5%)** |
| **Precision (Phishing)** | **0.9286 (92.9%)** |
| **Recall (Phishing)** | **0.8125 (81.3%)** |
| **F1-Score (Phishing)** | **0.8667 (86.7%)** |
| **ROC-AUC** | **0.9531** |
| **5-Fold Cross-Validation Mean F1** | **0.8929 ± 0.0721** |

### Held-Out Confusion Matrix

| Actual \ Predicted | Legitimate (0) | Phishing (1) |
| :--- | :---: | :---: |
| **Legitimate (0)** | **TN = 15** | FP = 1 |
| **Phishing (1)** | FN = 3 | **TP = 13** |

## 4. Known Limitations & Responsible Use

1. **Corpus Size**: Trained on a curated 128-sample SME benchmark rather than live multi-million-email enterprise telemetry; novel phrasing or non-English scripts outside training patterns may have lower recall.
2. **Short Texts**: Messages under ~12 words carry reduced statistical confidence and rely more heavily on heuristic indicators and user verification.
3. **Triage Aid Only**: Automated classification assists SME owners in spotting red flags and never replaces out-of-band phone verification with banks or suppliers.

