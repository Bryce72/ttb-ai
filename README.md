# **ttb-ai**

The goal of this project is to create an MVP to read a document and image of a label and determine if it passes the TTB Guidelines.

🔗 **[Live Demo](https://ttb-ai.onrender.com)**

- Do note I have set some safety features. Maximum of 5 uploads per minute or 100 uploads per day per IP. 
- Maximum of a 5mb file allowed to be uploaded.

---

## Two Files Needed

1. **Application** in a `.txt` file — contains the approved application data
2. **Label image** in `.png` or `.jpg` — a photo or scan of the physical label

## Example of Label Image in `.png`


 ![Example Label](/static/testLabel4.png)

## Application File Format

The application `.txt` file must use `KEY=VALUE` pairs, one per line. These values represent the approved application data that the label will be checked against.

**Required keys:**

| Key | Description | Example |
|-----|-------------|---------|
| `BRAND` | Brand name as approved | `Malt & Hop Brewing Co.` |
| `CLASS` | Product class/type | `Dark Ale` |
| `ABV` | Alcohol by volume | `12%` |
| `NET` | Net contents / volume | `12 FL OZ` |

**Example `application.txt`:**

```
BRAND=Malt & Hop Brewing Co.
CLASS=Dark Ale
ABV=12%
NET=12 FL OZ
```

> **Note:** The file must be plain text (`.txt`). No headers, no extra formatting. One field per line.

---

## Tech Stack

- **LLM / OCR**: [Claude API](https://docs.anthropic.com/en/docs/about-claude/models) (vision + text reasoning)
- **Frontend**: HTML / CSS / JavaScript
- **Backend**: [Python](https://www.python.org/)
- **Hosting**: [Render](https://render.com/)

## Core Features

- Upload a label image (JPEG/PNG) and a text file containing application data
- Extract all text from the label image via Claude's vision capabilities
- Compare extracted label fields against application data
- Return a pass/fail compliance report with flagged mismatches

---

## TTB Fields Verified

| Field | Example Value |
|-------|---------------|
| `BRAND` | `Malt & Hop Brewing Co.` |
| `CLASS` | `Dark Ale` |
| `ABV` | `12%` |
| `NET` | `12 FL OZ` |

---

## Compliance Logic

| Check | Rule |
|-------|------|
| **Government Warning** | Both paragraphs must be present in substance. Minor spacing, line breaks, or punctuation differences are acceptable. Any orientation (horizontal/vertical) is valid. |
| **ABV** | Alcohol percentage on label must match application data. |
| **Brand Name** | Must match between label and application. |
| **Class/Type** | Must match between label and application. |
| **Net Contents** | Must match between label and application. |
| **Name & Address** | Bottler/importer must be present on label. City and state are sufficient. |

---

## Constraints & Requirements

- Response time aims to be **under 5 seconds** per label
- UI must be simple enough for non-technical users — no buried buttons, obvious workflow
- Batch upload support for processing multiple labels at once
- Standalone app — no COLA System integration required
- No sensitive data retention

---

## Assumptions

- Label images are clear enough for AI vision to read all text fields.
- Government Warning does not need to be in a specific orientation or exact formatting — only that all required content is present in substance.
- City and state are sufficient for the name/address requirement (full street address not required).
- Minor formatting differences (casing, spacing, line breaks) are not grounds for failure.
- This is a prototype aid for reviewers, **not a replacement** for official TTB Review.

---

## Trade-offs & Limitations

| Limitation | Details |
|------------|---------|
| **API Costs** | This is a prototype designed to demonstrate the concept. For production use, training a local OCR model would be more cost-effective, faster, and more secure. |
| **Data Privacy** | This application sends data to [Anthropic's Claude API](https://www.anthropic.com/). If handling sensitive or proprietary label data, a self-hosted solution would be advisable. |
| **Rate Limits** | Anthropic's API enforces per-minute token limits. High-resolution label images consume significant tokens, which can throttle throughput on lower API tiers. |

---

## How to Run Locally

```bash
# Clone the repo
git clone https://github.com/bryce72/ttb-ai.git
cd ttb-ai

# Install dependencies
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY=your_key_here

# Run the app
python app.py


# Then run the HTML file on a local server port of your choice (I used 5500)
```

## How to Test

🔗 Go to: **[https://ttb-ai.onrender.com](https://ttb-ai.onrender.com)**

1. Upload a `.txt` application file
2. Upload a `.png` or `.jpg` label image
3. Click verify
4. Review the compliance result

---

## Prompt Used

<details>
<summary>Click to expand the compliance prompt</summary>

```
TTB label compliance review.

APPLICATION:
{text_content}

Verify label against application for:
1. The Government Warning may appear in any orientation (horizontal or vertical).
   Minor spacing, line breaks, or punctuation differences are acceptable.
   All required words and both paragraphs (1) and (2) must be present in substance.
2. ABV matches ABV
3. BRAND matches BRAND
4. CLASS matches CLASS
5. NET matches NET
6. Name and address present on label (city and state are sufficient)

If all pass, output exactly:
APPROVED

If any fail, output exactly:
NEEDS REVISION:
- Item number - reason

Do not explain passed items.
```

</details>