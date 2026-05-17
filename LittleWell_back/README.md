# AI Ethics and Data Privacy Note
## LittleWell — Iteration 3 | FIT5120 Industry Experience Studio 2026 S1
**Team 14 | Confidential — For PGP Assessment Use**

---

## 1. Overview

LittleWell's Iteration 3 introduces three AI-powered features: the Lunchbox Food Analyser, the Nutrition Classifier, and the "Why This Meal?" explanation generator. This document outlines the ethical considerations, data handling practices, and privacy implications of these features, particularly given that the primary users are parents of children.

---

## 2. Data Collected and Processed

### 2.1 Data sent to Groq API (external)

The following data is included in API requests to Groq's hosted LLM and vision services:

| Data Field | What Is Sent | Sensitivity Level |
|---|---|---|
| Lunchbox image | Binary image bytes (base64 encoded) | Medium — food contents visible |
| child_age | Integer (e.g. 7) | Low — age only, no name |
| child_name | String entered by parent (e.g. "Arya") | Low-Medium — first name only |
| allergens | List of strings (e.g. ["nuts", "dairy"]) | Low |
| dietary_restrictions | List of strings (e.g. ["vegetarian"]) | Low |
| detected foods | List of food names (e.g. ["apple", "sandwich"]) | Low |
| nutrition score | Integer 0-100 and grade string | Low |

**What is NOT sent to Groq:**
- Child's full name or surname
- Child's date of birth
- Child's school or location
- Parent's name, email, or contact details
- Any account credentials or session tokens
- Any medical records or diagnoses

### 2.2 Data processed locally (never leaves the server)

| Data | Where processed | Storage |
|---|---|---|
| AUSNUT 2011-13 dataset | Local app/data/ folder | Static file, no user data |
| nutrition_classifier.pkl | Local app/data/ folder | Model weights only |
| Matched food records | In-memory during request | Not persisted |

---

## 3. Groq API Data Retention Policy

Groq's current data handling policy (as of 2025) states:

- Groq does not use customer API request data to train their models
- API request/response data is not retained beyond the scope of completing the request by default
- Enterprise customers can request zero data retention (ZDR) agreements

**Recommendation for production deployment:** Before launching LittleWell to the public, the team should review Groq's current Terms of Service and Data Processing Agreement (DPA) at `console.groq.com` and confirm ZDR terms are in place, particularly given the involvement of children's health data.

**Reference:** `https://groq.com/privacy-policy/`

---

## 4. Children's Data — Special Considerations

LittleWell's users are parents, and the data relates to children under 18. This triggers additional ethical obligations:

### 4.1 Australian Privacy Act 1988

The Australian Privacy Act applies to organisations that handle personal information. Key obligations relevant to LittleWell:

- **APP 3 (Collection):** Only collect personal information reasonably necessary. LittleWell collects child age and first name — both are necessary for personalised nutrition advice.
- **APP 6 (Use and disclosure):** Information must only be used for the primary purpose of collection. Child age and name are used solely to personalise AI-generated nutrition feedback.
- **APP 11 (Security):** Reasonable steps must be taken to protect personal information. Child data is not persisted beyond the API request.

### 4.2 Recommended Privacy Policy Update

The LittleWell app's privacy policy should be updated to include:

1. What data is collected when using the Food Analyser (age, name, food photo)
2. That image data and child details are sent to Groq's API for processing
3. That Groq does not retain this data beyond the request
4. That no identifiable child information is stored permanently by LittleWell
5. A link to Groq's privacy policy for parents who want full details

---

## 5. Ethical AI Design Principles Applied

### 5.1 Human-Centric Design
All AI outputs are written in warm, parent-friendly language. Technical nutrition data (kJ, mg sodium) is translated into plain English explanations ("high in salt — best limited for children"). The system is designed to inform and support parents, not alarm or shame them.

### 5.2 Transparency
The UI clearly labels AI-generated content with "✨ AI Fusion" and "Powered by Groq LLaMA" badges. Parents know they are reading AI-generated advice, not a registered dietitian's opinion.

### 5.3 Accuracy and Evidence Base
- Nutrition scoring is based on the Australian Dietary Guidelines (ADG), published by the National Health and Medical Research Council (NHMRC)
- The ML classifier is trained on AUSNUT 2011-13, the official Australian food nutrient database published by Food Standards Australia New Zealand (FSANZ)
- All recommendations reference Australian standards, not generic international databases

### 5.4 Avoiding Harm
- The system does not diagnose medical conditions
- AI feedback is framed as general nutritional guidance, not medical advice
- A disclaimer is recommended in the UI: "LittleWell provides general nutrition guidance based on Australian Dietary Guidelines. It is not a substitute for advice from a registered dietitian or medical professional."

### 5.5 Fairness and Bias Awareness
- AUSNUT 2011-13 was collected from Australian dietary surveys and may underrepresent multicultural foods
- The ML model may be less accurate for South Asian, East Asian, or Middle Eastern cuisine items
- This limitation is documented in the ML Evaluation Report and should be disclosed to users

### 5.6 Minimal Data Collection
- The app does not require account creation to use the Food Analyser
- Child first name is optional — a placeholder "your child" is used if not provided
- No data is stored beyond the duration of the analysis request

---

## 6. Model Bias Analysis

| Bias Type | Risk Level | Mitigation |
|---|---|---|
| Western food bias in AUSNUT | Medium | Document limitation; future work to supplement with multicultural food databases |
| Age-group generalisation | Low | ADG thresholds used per age band (2, 4, 7, 11, 14 years) |
| Class imbalance in training data | Low | Addressed with class_weight='balanced' in RandomForestClassifier |
| Rule-based label subjectivity | Medium | Labels derived from peer-reviewed ADG; disclose that thresholds are guidelines not absolutes |

---

## 7. Recommendations for Production

1. Add UI disclaimer: "AI nutrition analysis is for general guidance only. Consult a registered dietitian for personalised advice."
2. Update LittleWell privacy policy to include Food Analyser data handling
3. Confirm Groq ZDR (Zero Data Retention) agreement before public launch
4. Consider allowing parents to opt out of sending the child's name to the AI API
5. Add a feedback mechanism so parents can flag incorrect food detections
6. Review AUSNUT dataset annually — Food Standards Australia releases updates

---

## 8. Summary Statement

LittleWell's AI features are designed to empower parents with evidence-based, personalised nutrition guidance while minimising the collection and external transmission of children's personal data. The system uses real Australian government datasets (AUSNUT 2011-13, ADG), clearly labels AI-generated content, and follows a minimal-data-collection approach. No sensitive personally identifiable information (PII) beyond a child's first name and age is processed, and this data is not retained beyond the scope of a single API request.

---
