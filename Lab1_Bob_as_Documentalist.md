# Lab 1 — Meet Bob, Your AI Documentalist
## *Exploring the Document Class Model, Relationships & Cleaning Recommendations*

> **Duration:** ~30 minutes  
> **Audience:** Mixed — content administrators & business analysts  
> **Prerequisites:** Bob is running with the IBM Content Services MCP server configured (see [`README_Labs.md`](README_Labs.md))  
> **Environment:** Live FNCM repository (`fncm-dev-demo-emea-10`, Object Store: `OS1`)

---

## 🎬 The Story

> *It's Monday morning. You've just been handed a spreadsheet with 91 document class names and told: "We need to clean this up." You don't know what half of them do. Some were created years ago by people who have since left. Some look like duplicates. Some are clearly demo classes that somehow ended up in production.*
>
> *You open Bob.*

---

## 🎯 What You Will Learn

By the end of this lab, you will be able to:

1. Use Bob to **inventory all document classes** in a live IBM Content Services repository
2. Understand the **class hierarchy** — how `Document` is the root and all other classes inherit from it
3. **Deep-dive into a specific class** (HRDocument) to see all its properties, types, and searchability
4. Ask Bob to **identify historical debt** — duplicates, legacy classes, naming inconsistencies
5. Get a **prioritized cleaning roadmap** from Bob based on what he finds

---

## 🔧 MCP Tools Bob Will Use

| Tool | What It Does |
|------|-------------|
| `list_root_classes` | Lists all root class types in the repository (Document, Folder, etc.) |
| `determine_class` | Finds classes matching keywords — used to explore the class catalog |
| `get_class_property_descriptions` | Returns all properties of a specific class with full metadata |
| `get_searchable_property_descriptions` | Returns only the searchable properties of a class |

---

## 📋 Scene 1 — "Bob, What Do We Have?"

### The Situation
You need a complete inventory of all document classes. Instead of navigating the admin console, you ask Bob.

### 💬 Prompt to Bob

```
Bob, I want to understand our IBM Content Services repository. 
Can you give me a complete inventory of all the document classes we have? 
Group them by domain if you can.
```

### 🔍 What Bob Does Behind the Scenes
1. Calls `list_root_classes` → discovers `Document` as the root class type
2. Calls `determine_class` with keyword `"Document"` → retrieves all 91 subclasses
3. Analyzes the symbolic names and display names
4. Groups them by domain (HR, Financial, Legal, System, Integration, Specialized)

### ✅ Expected Output from Bob

Bob should return a structured catalog similar to:

```
📁 Document Class Inventory — IBM Content Services Repository
═══════════════════════════════════════════════════════════════

HR & Employment (3 classes)
  • HRDocument — HR Document
  • EmploymentApplication — Employment Application  
  • SalaryCertificate — Salary Certificate

Financial & Accounting (8 classes)
  • Invoice — Invoice
  • Invoice_ach — Invoice (ACH variant)
  • Contract — Contract
  • Collateral — Collateral
  • FinancialDocuments — Financial Documents
  • Customer — Customer
  • CustomerDocuments — Customer Documents
  • ClientDocument — Client Document

Legal & Compliance (10 classes)
  • LG_PolicyDocument — Policy Document
  • LG_MortgageDocument — Mortgage Document
  • LG_LicenseDocument — License Document
  [... and 7 more]

System & Workflow (12 classes)
  • WorkflowDefinition — Workflow Definition
  • FormTemplate — Form Template
  [... and 10 more]

Specialized / Custom (40+ classes)
  • AIngelDokument — DocumentAIngel Document
  • DynDos — DynDos
  • HHNKDocs — HHNKDocs
  • usr1_Client_Document — usr1_Client_Document
  • usr2_Client_document — usr2_Client_document
  [... and many more]

Total: 91 document classes
```

### 💡 Instructor Callout — For Business Analysts
> Bob can describe the **business purpose** of each class without you needing to read technical documentation. Notice how he groups them by domain — this is AI reasoning about naming patterns, not a pre-configured taxonomy.

### 💡 Instructor Callout — For Administrators
> The `determine_class` tool queries the live repository. This is the **actual current state** of your object store, not a cached or static view. Any class created or deleted since the last deployment will appear here.

---

## 📋 Scene 2 — "Bob, What Looks Wrong?"

### The Situation
Now that you have the full list, you want Bob to flag anything suspicious — duplicates, legacy classes, naming inconsistencies, demo classes that shouldn't be in production.

### 💬 Prompt to Bob

```
Bob, looking at that class inventory, which classes look like duplicates, 
legacy classes, or things we should clean up? 
I'm particularly worried about classes that seem to serve the same purpose.
```

### 🔍 What Bob Does Behind the Scenes
1. Analyzes the class names for patterns: prefix groups (`LG_`, `usr1_`, `usr2_`, `wel`, `ZV_`), naming inconsistencies, obvious demo names
2. Calls `get_class_property_descriptions` on suspect classes to compare their property sets
3. Identifies classes with identical or near-identical property structures

### ✅ Expected Output from Bob

Bob should identify the following problem categories:

**🔴 Duplicate Classes (same purpose, different names)**
```
Client Document Variants (4 classes doing the same thing):
  • ClientDocument
  • usr1_Client_Document  ← user-specific, should not exist in production
  • usr2_Client_document  ← user-specific, should not exist in production
  • welClientDocument     ← unclear prefix, overlapping purpose

Invoice Variants (3 classes):
  • Invoice
  • Invoice_ach           ← could be a property value, not a separate class
  • JKJInvoice            ← appears to be a customer-specific class

Customer/Client Overlap:
  • Customer
  • CustomerDocuments     ← unclear distinction from Customer
  • ClientDocument        ← overlaps with Customer concept
```

**🟡 Legacy / Demo Classes**
```
  • DemoDocument          ← explicitly named "Demo", should not be in production
  • AIngelDokument        ← unclear purpose, non-standard naming
  • DynDos                ← no description, unclear purpose
  • HHNKDocs              ← no description, unclear purpose
  • MitaDoc               ← no description, unclear purpose
  • JARDNI                ← no description, unclear purpose
  • JARDocument           ← no description, unclear purpose
```

**🟡 User-Specific Classes (should be consolidated)**
```
  • usr1_Client_Document  ← belongs to a specific user, not a business class
  • usr2_Client_document  ← same issue
```

**🟡 Inconsistent Naming Conventions**
```
Mixed prefixes with no clear standard:
  • LG_ prefix (10 classes) — Legal domain
  • SF prefix (2 classes) — Salesforce integration
  • wel prefix (3 classes) — unclear domain
  • ZV_ prefix (2 classes) — unclear domain
  • CDS_ prefix (3 classes) — certification system
  • UAX_ prefix (2 classes) — specific implementation
```

### 💡 Instructor Callout — Key Insight
> Bob identified **~15 classes** that are candidates for consolidation or removal. This is the "historical debt" — classes created over time without governance, by different teams, for overlapping purposes. In a well-governed repository, you'd have **fewer than 50 classes** with clear ownership.

---

## 📋 Scene 3 — "Bob, Show Me HRDocument in Detail"

### The Situation
The HR team is your biggest user group. You want to understand the `HRDocument` class deeply — all its properties, what's searchable, what's inherited from the base class, and what's HR-specific.

### 💬 Prompt to Bob

```
Bob, show me everything about the HRDocument class. 
I want to see all its properties — their data types, whether they're searchable, 
and which ones are system-owned vs custom business properties.
```

### 🔍 What Bob Does Behind the Scenes
1. Calls `determine_class` with keyword `"HRDocument"` to confirm the symbolic name
2. Calls `get_class_property_descriptions HRDocument` → returns all properties including inherited ones
3. Categorizes properties by origin (system vs custom) and purpose

### ✅ Expected Output from Bob

Bob should return a structured property breakdown:

```
📋 HRDocument Class — Full Property Specification
═══════════════════════════════════════════════════

Inherited from base Document class: 79 properties
HR-specific custom properties: 40 properties
Total: 119 properties accessible on HRDocument

━━━ HR-Specific Properties (Custom) ━━━

Personal Information:
  • FirstName        STRING   SINGLE   Searchable ✓
  • LastName         STRING   SINGLE   Searchable ✓
  • PersonalID       STRING   SINGLE   Searchable ✓
  • Birthdate        DATE     SINGLE   Searchable ✓

Employment Details:
  • EmployeeID       STRING   SINGLE   Searchable ✓  ← Key identifier
  • SAPEmployeeID    STRING   SINGLE   Searchable ✓  ← SAP integration
  • JobRole          STRING   SINGLE   Searchable ✓
  • JobFunction      STRING   SINGLE   Searchable ✓
  • JobCode          STRING   SINGLE   Searchable ✓
  • JobLevel         STRING   SINGLE   Searchable ✓
  • JobStatus        STRING   SINGLE   Searchable ✓
  • EmploymentType   STRING   SINGLE   Searchable ✓
  • CurrentStatus    STRING   SINGLE   Searchable ✓
  • StartDate        DATE     SINGLE   Searchable ✓
  • TerminationDate  DATE     SINGLE   Searchable ✓

Organizational Structure:
  • Company          STRING   SINGLE   Searchable ✓
  • CompanyCode      STRING   SINGLE   Searchable ✓
  • BusinessUnit     STRING   SINGLE   Searchable ✓
  • Department       STRING   SINGLE   Searchable ✓
  • Division         STRING   SINGLE   Searchable ✓
  • CostCenter       STRING   SINGLE   Searchable ✓
  • Location         STRING   SINGLE   Searchable ✓

Document Classification:
  • DocType          STRING   SINGLE   Searchable ✓  ← Critical for Lab 3
  • DocumentCategory STRING   SINGLE   Searchable ✓
  • ClassDocType     STRING   SINGLE   Searchable ✓

SAP Integration:
  • SAPDocId         STRING   SINGLE   Searchable ✓
  • SAPDocProt       STRING   SINGLE   Searchable ✓
  • SAPComps         STRING   SINGLE   Searchable ✓
  • SAPContType      STRING   SINGLE   Searchable ✓
  • SAPCompVersion   STRING   SINGLE   Searchable ✓
  • SapLinkTrigger   BOOLEAN  SINGLE   Searchable ✓
  • sapLinked        STRING   SINGLE   Searchable ✓

Salesforce Integration:
  • SFLinkTrigger    BOOLEAN  SINGLE   Searchable ✓

Workflow Integration:
  • docuflowTimestamp DATE    SINGLE   Searchable ✓
  • docuflowUsername  STRING  SINGLE   Searchable ✓
```

### 💡 Instructor Callout — For Business Analysts
> Notice the `DocType` property — this is how we distinguish between a Job Application, a Payslip, a Performance Review, and an Employment Contract. They're all `HRDocument` instances, but `DocType` tells you which kind. This is a key design pattern in IBM Content Services: **use properties to differentiate, not separate classes**.

### 💡 Instructor Callout — For Administrators
> The SAP integration properties (`SAPDocId`, `SapLinkTrigger`, `sapLinked`) show that this class is connected to an external system. Before modifying or deprecating this class, you'd need to check with the SAP integration team. Bob can help you identify these dependencies.

---

## 📋 Scene 4 — "Bob, Explain the Inheritance"

### The Situation
A business analyst in the room asks: "Why does HRDocument have 119 properties? That seems like a lot." You ask Bob to explain the inheritance model.

### 💬 Prompt to Bob

```
Bob, can you explain the relationship between the base Document class and HRDocument? 
Why does HRDocument have so many properties? 
What does it inherit and what does it add?
```

### ✅ Expected Output from Bob

Bob should explain:

```
📐 Class Inheritance Model
═══════════════════════════

Document (Root Class)
│
│  79 base properties covering:
│  • Identity & Metadata (Id, Creator, DateCreated, etc.)
│  • Version Control (MajorVersionNumber, IsCurrentVersion, etc.)
│  • Security & Permissions (Owner, Permissions, SecurityPolicy, etc.)
│  • Content Management (ContentSize, MimeType, StoragePolicy, etc.)
│  • Lifecycle Management (CmRetentionDate, DocumentLifecyclePolicy, etc.)
│  • Workflow & Tasks (WorkflowSubscriptions, CoordinatedTasks)
│  • Records Management (RecordInformation, CmHoldRelationships)
│  • AI & Analytics (GenaiWatsonxSummary, GenaiDateIndexed)
│
└── HRDocument (Subclass)
       Inherits all 79 Document properties PLUS adds:
       40 HR-specific properties covering:
       • Personal Information (FirstName, LastName, Birthdate)
       • Employment Details (EmployeeID, JobRole, StartDate)
       • Organizational Structure (Department, CostCenter, Location)
       • Document Classification (DocType, DocumentCategory)
       • SAP Integration (SAPDocId, SapLinkTrigger)
       • Salesforce Integration (SFLinkTrigger)
       • Workflow Integration (docuflowTimestamp)

Key Design Principle:
  When you create an HRDocument, you get ALL 119 properties automatically.
  You don't need to configure them — they're inherited from the class hierarchy.
  
  This means: one HRDocument can be a Job Application, a Payslip, a Contract,
  or a Performance Review — the DocType property tells you which.
```

###  The "Class vs Property" Design Decision
> This is a fundamental IBM Content Services design question: **Should I create a new class, or add a property to an existing class?**
>
> **Create a new class when:**
> - The document type has fundamentally different properties
> - Different security policies apply
> - Different lifecycle/retention rules apply
> - Different workflows are triggered
>
> **Add a property when:**
> - The document type is a variant of an existing type
> - The same properties apply, just with different values
> - You want to avoid class proliferation
>
> The number of class problems in this repository are largely caused by teams choosing "create a new class" when they should have added a property.

---

## 📋 Scene 5 — "Bob, Give Me a Cleaning Roadmap"

### The Situation
You've seen the inventory, the duplicates, the legacy classes, and the inheritance model. Now you want Bob to synthesize everything into a prioritized action plan.

### 💬 Prompt to Bob

Switch to Plan Mode

```
Bob, based on everything you've seen in our repository —
the duplicates, the legacy classes, the naming inconsistencies — 
what would you recommend as a cleaning plan? 
Give me a prioritized roadmap with quick wins and longer-term actions. Create a Markdown with that plan.
```

### ✅ Expected Output from Bob

Bob should produce a structured roadmap:

```
🗺️ Repository Cleaning Roadmap
═══════════════════════════════

QUICK WINS (Week 1-2) — Low risk, high impact
──────────────────────────────────────────────
1. Remove demo classes immediately
   • DemoDocument — explicitly a demo, no business value
   • AIngelDokument — no description, no apparent owner
   Action: Verify zero documents, then delete

2. Remove user-specific classes
   • usr1_Client_Document
   • usr2_Client_document
   Action: Migrate any documents to ClientDocument, then delete

3. Document the top 10 most-used classes
   Action: Add descriptions, assign business owners

CONSOLIDATION (Week 3-6) — Medium risk, requires migration
────────────────────────────────────────────────────────────
4. Consolidate Client Document variants (4 → 1)
   • ClientDocument + usr1_ + usr2_ + welClientDocument → Client_Document
   Action: Create new class, migrate documents, deprecate old classes

5. Consolidate Invoice variants (3 → 1)
   • Invoice + Invoice_ach + JKJInvoice → Finance_Invoice
   Action: Add InvoiceType property, migrate, deprecate

6. Merge Customer classes (2 → 1)
   • Customer + CustomerDocuments → Customer_Document
   Action: Merge properties, migrate, deprecate

GOVERNANCE (Week 7-10) — Foundation for the future
────────────────────────────────────────────────────
7. Establish naming convention
   Standard: [Domain]_[Type]_[Variant]
   Examples: HR_Employee_Document, Finance_Invoice_Standard

8. Assign business owners to all remaining classes
   Target: 0 classes without a documented owner

9. Set up quarterly review process
   Metric: No class with 0 documents for >6 months

TARGET STATE: 91 classes → <50 classes
Estimated effort: 10 weeks with a small team
```

### 💡 Instructor Callout — The Governance Lesson
> Bob's roadmap mirrors what's already documented in [`Classification_and_Cleaning_Plan.md`](Classification_and_Cleaning_Plan.md) — but Bob derived it **from the live repository**, not from a static document. This is the power of AI + MCP: the recommendations are always based on the current state of the system.

---

## 🏁 Lab 1 Summary

In this lab, Bob helped you:

| What Bob Did | MCP Tool Used |
|-------------|--------------|
| Inventoried all 91 document classes | `list_root_classes` + `determine_class` |
| Identified duplicates and legacy classes | `get_class_property_descriptions` (comparative) |
| Deep-dived into HRDocument (119 properties) | `get_class_property_descriptions HRDocument` |
| Explained the inheritance model | AI reasoning on property metadata |
| Produced a prioritized cleaning roadmap | AI synthesis of all findings |

### Key Takeaways

1. **Bob can interrogate a live repository** — no need to navigate admin consoles or read static documentation
2. **91 classes is too many** — the target is <50 well-governed classes
3. **The "class vs property" design decision** is the root cause of class proliferation
4. **HRDocument is well-designed** — it uses `DocType` to differentiate document types rather than creating separate classes
5. **Governance is the long-term solution** — not just a one-time cleanup

---

## ➡️ Next Step

Proceed to **[Lab 2 — Feeding Bob: Generate Sample Content](Lab2_Generate_Sample_Content.md)**

In Lab 2, you'll generate 40 realistic HR documents and upload them to the repository using Bob — with a few deliberate mistakes that you'll fix in Lab 3.

---

## 📎 Reference

- [`Document_Class_Architecture.md`](Reference/Document_Class_Architecture.md) — Full class hierarchy diagram and catalog
- [`Document_Property_Specifications.md`](Reference/Document_Property_Specifications.md) — Complete property specifications
- [`Classification_and_Cleaning_Plan.md`](Reference/Classification_and_Cleaning_Plan.md) — Detailed cleaning plan
- [`README_Labs.md`](README_Labs.md) — Lab series overview and prerequisites