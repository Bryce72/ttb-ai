# **ttb-ai**

The goal of this project is to create an MVP to read a document and image of a label and determine if it passes the TTB guidelines.

## Tech Stack
- **OCR**: Google Vision API 
- **LLM**: Claude API for field matching
- **Frontend**: React or TBD (simple upload interface)
- **Backend**: Python

## Core Features
- Upload a label image (JPEG/PNG) and a text file containing application data
- Extract all text from the label image via OCR
- Compare extracted label fields against application data and TTB requirements
- Return a pass/fail compliance report with flagged mismatches

## TTB Fields Verified
- Brand name (case insensitive fuzzy matching)
- Class/type designation
- Alcohol content (ABV / proof)
- Net contents
- Name and address of bottler/producer
- Country of origin (imports)
- Government Health Warning Statement (exact wording, `GOVERNMENT WARNING:` must be all caps and bold)

## Constraints & Requirements
- Response time must be **under 5 seconds** per label - but will work on MVP originally.
- UI must be simple enough for the older gen, no buried buttons, obvious workflow
- Batch upload support for processing multiple labels at once
- Standalone app — no COLA system integration required
- No sensitive data retention

## Compliance Logic
- **Exact match required**: Government Warning text (word-for-word, `GOVERNMENT WARNING:` in all caps)
- **Fuzzy match acceptable**: Brand name casing/formatting differences (e.g., `STONE'S THROW` vs `Stone's Throw`)
- **Numeric validation**: ABV percentage and proof values must be consistent and match application data
- **Presence check**: All mandatory fields must exist on the label

## Assumptions
- Prototype only 
- Label images are of common alcohol beverages (beer, wine, distilled spirits)
- Text file input follows a consistent key:value format for application data
- No direct integration with TTB's COLA system

## Trade-offs & Limitations
- API costs
- TBD




## How to Test Run this
- TBD