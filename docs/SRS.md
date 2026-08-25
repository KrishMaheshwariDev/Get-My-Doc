# Get-My-Doc

## Software Requirements Specification (SRS)

Version: 1.0 (Draft)

---

# 1. Product Definition
### Working definition

Get-My-Doc is a local-first personal retrieval assistant that accepts natural-language requests through text or voice and retrieves the user's requested documents or resources without requiring the user to know their filename or storage location. In future, it will serve as an extension of the OS file management system, enabling AI-driven file operations as part of an AI OS.

The key phrase is retrieval assistant.

It is not initially:

- a general-purpose AI assistant
- a file manager
- a cloud drive
- a document editor
- a chatbot
- an autonomous computer agent

Its primary job is:
```
Understand request
        ↓
Determine what resource the user means
        ↓
Search available resources
        ↓
Rank candidates
        ↓
Return the most relevant resource
        ↓
Allow user to open/use it
```
---
# 2. Actors

For V1, there's essentially one actor: **User**

The user interacts with Get-My-Doc through:
```
Text Query OR Voice Query
     ↓
Get-My-Doc
     ↓
Retrieved Resource
```
We don't need accounts, teams, roles, administrators, etc. yet.

That would be architecture pollution at this stage.

---

# 3. Functional Requirements

### **FR-01: Text Query**

The system shall accept a natural-language text query.

```
Example:

"Find my resume."
```

### **FR-02: Voice Query**

The system shall accept a voice query and convert it into text for processing.
```
Example:

🎙️

"Bring me the internship offer letter."

↓

"Bring me the internship offer letter."
```
The retrieval system should ideally not care whether the query originated from text or speech.

That's an important architectural boundary.
```
          ┌── Text ──┐
User ─────┤          ├──→ Query
          └── Voice ─┘
```

### **FR-03: Resource Discovery**

The system shall discover resources available to the user.

For V1, I'd define resources primarily as:

- PDF
- DOC/DOCX
- TXT
- Images
- XLS/XLSX
- PPT/PPTX

Potentially other files later.

### **FR-04: Resource Indexing**

The system shall maintain metadata about discovered resources.

For example:
```
Resource
├── id
├── filename
├── path
├── extension
├── size
├── created_at
├── modified_at
└── indexed_at
```
Later we can add:
```
content
embeddings
entities
keywords
document_type
```
But don't prematurely lock those into V1.

### **FR-05: Natural-Language Retrieval**

The system shall interpret queries semantically rather than requiring exact filenames.

For example:
```
Query:
"Find the PDF containing my internship offer."
```

should potentially find:
```
Arakoo_Internship_Offer_Letter.pdf
```
even though the words aren't identical.

This is arguably the core feature of the entire project.

### **FR-06: Result Ranking**

If multiple resources match, the system shall rank them by relevance.

Example:
```
Query:
"my college resume"
```
Results:
```
1. Resume_2026.pdf          0.94
2. Resume_old.pdf           0.71
3. College_Profile.docx     0.42
```
The exact ranking algorithm is something we'll design during LLD.

###  **FR-07: Resource Presentation**
The system shall present the retrieved resource to the user.

At minimum:
```
Resume_2026.pdf

[ Open ]
[ Show Location ]
```
Potentially:
```
[ Preview ]
[ Open ]
[ Copy Path ]
```

### **FR-08: Resource Opening**

The system shall allow the user to open the selected resource using the operating system's default application.

### **FR-09: Continuous Availability**

The application shall remain available in the background so the user can invoke it without manually launching it every time.

This is where the desktop application distinction becomes important.

The UI isn't necessarily the application.

Conceptually:
```
                Get-My-Doc
                    │
        ┌───────────┴───────────┐
        │                       │
 Background Service             UI
        │                       │
        │                  React frontend
        │
 Retrieval Engine
        │
 Resource Index
        │
 Local Files
```
This will matter significantly when we reach HLD.

### **FR-10: Query History**

### **FR-11: File System Watcher**

The system shall monitor registered files and directories for changes using the OS's file system event listener. It will detect modifications, creations, deletions, and attribute changes, and update the index accordingly. Only files and directories that have been explicitly registered by the user will be watched to avoid unnecessary overhead.

Potentially store previous queries:
```
"Find my resume"
"Bring the electricity bill"
"Open my project report"
```
But I'd classify this as V1.1, not core V1.

---
# 4. Non-Functional Requirements
This system has some unusual NFRs because it is supposed to feel like an assistant.

### **NFR-01: Low perceived latency**
The user should not feel like they're submitting a traditional search job.

Target:
```
Query
 ↓
Processing
 ↓
Results
```
Preferably < 1–2 seconds

for already-indexed resources.

We shouldn't blindly promise this yet. We'll benchmark it.

### **NFR-02: Local-first**

The user's documents are potentially extremely sensitive.

Therefore:
```
The default architecture should keep document discovery, indexing, metadata and retrieval local whenever possible.
```
Cloud APIs should not be a hidden requirement for the basic product.

### **NFR-03: Privacy**

The system should not upload a user's documents simply because they searched for them.

This is one of the architectural principles I'd make explicit from day one.

### **NFR-04: Resource efficiency**

Because the application is expected to remain running:
```
24/7 background process
```
it shouldn't constantly consume:

- CPU
- RAM
- GPU
- disk I/O

This is particularly important for indexing.

We don't want:
```
Get-My-Doc running
       ↓
CPU: 30%
Disk: constantly active
RAM: 4 GB
```
just because it's sitting idle.

### **NFR-05: Extensibility**

The retrieval engine should eventually support different retrieval strategies without rewriting the entire application.

Potentially:
```
Keyword Retrieval
Semantic Retrieval
Metadata Retrieval
Hybrid Retrieval
```

---
# 5. V1 Scope

V1 should be:
```
Desktop application
      +
Text query
      +
Voice query
      +
Local filesystem indexing
      +
Natural-language retrieval
      +
Result ranking
      +
Open resource
```

---
# 6. Explicitly OUT of V1

This is just as important.

❌ Email integration

❌ Google Drive

❌ OneDrive

❌ Dropbox

❌ Multi-user accounts

❌ Cloud synchronization

❌ General AI assistant

❌ Autonomous computer control

❌ Document editing

❌ Calendar

❌ Web search

❌ Wake-word detection

❌ Complex mobile application

❌ C++ optimization before benchmarking

Those can come later if the core retrieval problem is actually solved.

