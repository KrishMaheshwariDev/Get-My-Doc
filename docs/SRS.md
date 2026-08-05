# Get-My-Doc

## Software Requirements Specification (SRS)

Version: 1.0

---

# 1. Vision

Get-My-Doc is an AI-powered Personal Document Intelligence Platform that enables users to retrieve important documents using natural language instead of filenames, folders, or storage locations.

The system transforms document retrieval from a storage-centric workflow into a context-centric experience.

---

# 2. Problem Statement

Modern users store documents across multiple platforms including cloud storage, email, messaging applications, downloads, and local folders.

During urgent situations users often remember the context of a document rather than where it was stored.

Traditional file systems optimize storage.

Get-My-Doc optimizes retrieval.

---

# 3. Goals

- Retrieve documents within seconds.
- Search using natural language.
- Eliminate dependency on filenames.
- Automatically understand uploaded documents.
- Work across multiple storage providers.
- Build a foundation for future document intelligence.

---

# 4. Scope

## Version 1

Included

- Authentication
- Cloud Storage Integration
- Document Upload
- OCR
- Metadata Extraction
- Automatic Classification
- Semantic Search
- Keyword Search
- Hybrid Retrieval
- Document Preview
- Duplicate Detection

Excluded

- Mobile Apps
- Offline Mode
- Tax Assistant
- Visa Assistant
- Legal Analysis

---

# 5. Target Users

- Students
- Working Professionals
- Families
- Freelancers
- Small Businesses
- Travelers

---

# 6. User Journey

Connect Storage

↓

Index Documents

↓

AI Processes Documents

↓

User Searches Naturally

↓

Relevant Documents Retrieved

↓

User Opens Document

---

# 7. Core Features

## Authentication

- Secure login
- Cloud account connection

## Document Acquisition

- File Upload
- Folder Import
- Cloud Sync

## Document Processing

- OCR
- Metadata Extraction
- Summary Generation
- Duplicate Detection
- Classification

## Search

- Natural Language Search
- Keyword Search
- Hybrid Search
- Filters
- Ranking

## Retrieval

- Open Best Match
- Candidate List
- Preview
- Reveal File

## Intelligence

- Timeline Generation
- Knowledge Graph

---

# 8. Non-Functional Requirements

Performance

- Search < 1 second
- Automatic indexing

Availability

- Cloud-first
- 99.9% uptime target

Security

- Authentication
- Authorization
- Encryption
- Secure communication

Scalability

- Horizontal scaling
- Modular architecture

Privacy

- User-owned documents
- End-to-end encryption
- Minimum data collection

---

# 9. MVP

The first release shall support:

- Authentication
- Google Drive integration
- Upload
- OCR
- Metadata extraction
- Embeddings
- Hybrid search
- Document preview

Success means a user can retrieve an uploaded document within seconds using natural language.

---

# 10. Future Scope

- Knowledge Graph
- Timeline
- Warranty Tracking
- Expiry Detection
- AI Assistant
- Tax Assistant
- Visa Assistant
- Cross-document reasoning

---

# 11. Success Metrics

- Average retrieval time < 1 second
- High retrieval accuracy
- Successful automatic indexing
- Low duplicate rate
- Positive user feedback