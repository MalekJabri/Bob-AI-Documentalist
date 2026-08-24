# HR Document Class - Complete Description

## Class Overview
- **Display Name**: HR Document
- **Symbolic Name**: HRDocument
- **Description**: HR Document
- **Parent Class**: Document

## Custom HR-Specific Properties

### Employee Information
| Property | Display Name | Data Type | Searchable | Description |
|----------|--------------|-----------|------------|-------------|
| FirstName | First Name | STRING | Yes | Employee's first name |
| LastName | Last Name | STRING | Yes | Employee's last name |
| PersonalID | Personal ID | STRING | Yes | Personal identification number |
| Birthdate | Birthdate | DATE | Yes | Employee's date of birth |
| EmployeeID | Employee ID | STRING | Yes | Internal employee identifier |

### Employment Details
| Property | Display Name | Data Type | Searchable | Description |
|----------|--------------|-----------|------------|-------------|
| JobRole | Job Role | STRING | Yes | Employee's job role |
| JobFunction | Job Function | STRING | Yes | Employee's job function |
| JobCode | Job Code | STRING | Yes | Job classification code |
| JobLevel | Job Level | STRING | Yes | Employee's job level |
| JobStatus | Job Status | STRING | Yes | Current job status |
| EmploymentType | Employment Type | STRING | Yes | Type of employment |
| CurrentStatus | Current Status | STRING | Yes | Current employment status |

### Organizational Structure
| Property | Display Name | Data Type | Searchable | Description |
|----------|--------------|-----------|------------|-------------|
| Company | Company | STRING | Yes | Company name |
| CompanyCode | Company Code | STRING | Yes | Company identification code |
| BusinessUnit | Business Unit | STRING | Yes | Business unit assignment |
| Division | Division | STRING | Yes | Division or Department |
| Department | Department | STRING | Yes | Department assignment |
| CostCenter | Cost Center | STRING | Yes | Cost center code |
| Location | Location | STRING | Yes | Work location |

### Dates
| Property | Display Name | Data Type | Searchable | Description |
|----------|--------------|-----------|------------|-------------|
| StartDate | Start Date | DATE | Yes | Employment start date |
| TerminationDate | Termination Date | DATE | Yes | Employment termination date |

### Integration Properties - SAP
| Property | Display Name | Data Type | Searchable | Description |
|----------|--------------|-----------|------------|-------------|
| SAPEmployeeID | SAP Employee ID | STRING | Yes | SAP system employee identifier |
| SapLinkTrigger | SapLinkTrigger | BOOLEAN | Yes | Trigger for SAP linking |
| sapLinked | sapLinked | STRING | Yes | SAP link status |
| SAPDocId | SAPDocId | STRING | Yes | SAP document identifier |
| SAPDocProt | SAPDocProt | STRING | Yes | SAP document protocol |
| SAPComps | SAPComps | STRING | Yes | SAP components |
| SAPContType | SAPContType | STRING | Yes | SAP content type |
| SAPCompVersion | SAPCompVersion | STRING | Yes | SAP component version |

### Integration Properties - Salesforce
| Property | Display Name | Data Type | Searchable | Description |
|----------|--------------|-----------|------------|-------------|
| SFLinkTrigger | SFLinkTrigger | BOOLEAN | Yes | Trigger for Salesforce linking |
| SfSalesforceRelationships | Salesforce Relationships | OBJECT | No | Salesforce relationships |

### Integration Properties - DocuFlow
| Property | Display Name | Data Type | Searchable | Description |
|----------|--------------|-----------|------------|-------------|
| docuflowTimestamp | docuflowTimestamp | DATE | Yes | DocuFlow processing timestamp |
| docuflowUsername | docuflowUsername | STRING | Yes | DocuFlow user identifier |

### Document Classification
| Property | Display Name | Data Type | Searchable | Description |
|----------|--------------|-----------|------------|-------------|
| DocType | DocType | STRING | Yes | Document type |
| DocumentCategory | Document Category | STRING | Yes | Document category classification |
| ClassDocType | ClassDocType | STRING | Yes | Classification document type |

**Note**: While the repository doesn't expose formal choice lists through the API, the following values are commonly used in practice based on the document generation scripts:

**DocType Common Values**:
- JobApplication
- InterviewNotes
- EmploymentContract
- IDDocument
- PersonalInfo
- Payslip
- SalaryInfo
- PerformanceReview
- TrainingRecord
- DisciplinaryRecord
- ExitDocument

**Department Common Values** (from _DEPARTMENTS):
- IT
- Marketing
- Human Resources
- Sales
- Finance

**Position/JobRole Common Values**:
- Senior Developer
- Marketing Manager
- HR Specialist
- Sales Representative
- Financial Analyst

**Location Common Values**:
- Paris, France
- Lyon, France
- Bordeaux, France
- Marseille, France
- Lille, France

### AI Properties
| Property | Display Name | Data Type | Searchable | Description |
|----------|--------------|-----------|------------|-------------|
| GenaiDateIndexed | Gen AI Date Indexed | DATE | Yes | Date indexed by GenAI |
| GenaiWatsonxSummary | Watsonx Summary | STRING | Yes | AI-generated summary |

## Standard Document Properties

### Core Metadata
- DocumentTitle - Document Title
- MimeType - MIME type of the document
- ContentSize - Size in bytes

### Version Control
- IsCurrentVersion - Current version indicator
- IsReserved - Document checkout status
- IsFrozenVersion - Version frozen status
- MajorVersionNumber - Major version number
- MinorVersionNumber - Minor version number
- VersionStatus - Version status code
- IsVersioningEnabled - Versioning enabled flag

### Audit Properties
- Creator - User who created the document
- DateCreated - Creation date and time
- LastModifier - User who last modified
- DateLastModified - Last modification date
- DateCheckedIn - Check-in date and time
- Owner - Security owner
- Id - Unique object ID

### Content Management
- ClassificationStatus - Auto-classification status
- IndexationId - Verity collection ID
- CmIndexingFailureCode - Indexing failure reasons
- DateContentLastAccessed - Last content access date

### Records Management
- CmRetentionDate - Earliest deletion date
- ContentRetentionDate - Content retention date
- CmIsMarkedForDeletion - Deletion marker
- RecordInformation - Records management info
- CanDeclare - Can be declared as record

### Lifecycle
- DocumentLifecyclePolicy - Applied lifecycle policy
- CurrentState - Current lifecycle state
- IsInExceptionState - Exception state indicator
- WorkflowSubscriptions - Associated workflows

### Compound Documents
- CompoundDocumentState - Compound document state
- ChildDocuments - Child component documents
- ChildRelationships - Child relationships
- ParentDocuments - Parent documents
- ParentRelationships - Parent relationships

### Storage
- StoragePolicy - Storage policy
- StorageLocation - Storage location
- StorageArea - Storage area
- FoldersFiledIn - Folders containing document
- Containers - Referential containment relationships

### Digital Signatures
- DSSignatureStatus - Signature status
- DSEnvelopeID - Envelope ID

### Collaboration
- ClbSharingController - Sharing controller
- ClbSecurityController - Security controller
- ClbSensitiveContent - Sensitive content indicator
- ClbDocumentState - Document state

### Other System Properties
- Annotations - Associated annotations
- CmHoldRelationships - Hold relationships
- CmThumbnails - Thumbnail images
- ActiveMarkings - Active security markings
- SecurityPolicy - Security policy
- CoordinatedTasks - Coordinated tasks

## Property Statistics

- Total Properties: 109
- Custom HR Properties: 44
- System Properties: 65
- Searchable Properties: 82
- Hidden Properties: 35
- User-Modifiable Properties: 44

## Key Features

1. Comprehensive Employee Data - Complete employee information
2. Multi-System Integration - SAP, Salesforce, and DocuFlow support
3. AI-Ready - GenAI properties for AI-powered processing
4. Full Version Control - Complete document versioning
5. Records Management - Retention policies and records declaration
6. Digital Signatures - DocuSign integration
7. Collaboration Features - Sharing and security controls
8. Flexible Classification - Multiple document type fields

## Usage Notes

- All custom HR properties are searchable
- Supports SAP and Salesforce integration triggers
- GenAI properties enable AI-powered summarization
- Standard document lifecycle capabilities supported
- Inherits all standard document security features