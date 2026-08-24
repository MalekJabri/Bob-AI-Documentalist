# IBM Content Services - Document Property Specifications

## Overview

This document provides detailed specifications for all properties in the base `Document` class and the specialized `HRDocument` class. These properties form the foundation for content management, security, versioning, and business metadata across the IBM Content Services platform.

---

## Base Document Class Properties

The `Document` class contains **79 properties** that provide comprehensive content management capabilities.

### Identity & Metadata Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| Id | ID | GUID | SINGLE | ✓ | ✓ | The unique object ID |
| Creator | Creator | STRING | SINGLE | ✓ | ✓ | The name of the user who created this object |
| DateCreated | Date Created | DATE | SINGLE | ✓ | ✓ | The date and time this object was created |
| LastModifier | Last Modifier | STRING | SINGLE | ✓ | ✓ | The name of the user who last modified this object |
| DateLastModified | Date Last Modified | DATE | SINGLE | ✓ | ✓ | The date and time when this object was last modified |
| Name | Name | STRING | SINGLE | ✗ | ✓ | Returns the value of the designated name property for the object, or its ID if there is no name property |
| DocumentTitle | Document Title | STRING | SINGLE | ✓ | ✗ | Document Title |

### Version Control Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| IsVersioningEnabled | Is Versioning Enabled | BOOLEAN | SINGLE | ✓ | ✓ | Determines if versioning is enabled for this class of object |
| MajorVersionNumber | Major Version Number | LONG | SINGLE | ✓ | ✓ | The major version number for this document version |
| MinorVersionNumber | Minor Version Number | LONG | SINGLE | ✓ | ✓ | The minor version number for this document version |
| VersionStatus | Version Status | LONG | SINGLE | ✓ | ✓ | The version status of this document version |
| IsCurrentVersion | Is Current Version | BOOLEAN | SINGLE | ✓ | ✓ | Indicates whether this is the current version in the version series |
| IsFrozenVersion | Is Frozen Version | BOOLEAN | SINGLE | ✓ | ✓ | Indicates whether user properties or content can be modified |
| IsReserved | Is Reserved | BOOLEAN | SINGLE | ✓ | ✓ | Indicates whether a user has reserved the right to check in a version following this version |
| ReservationType | Reservation Type | LONG | SINGLE | ✓ | ✓ | Indicates the type (collaborative or exclusive) of the reservation |
| DateCheckedIn | Date Checked In | DATE | SINGLE | ✓ | ✓ | The date and time this object was checked in |
| VersionSeries | Version Series | OBJECT | SINGLE | ✓ | ✓ | The version series object with which this object is associated |
| Versions | Versions | OBJECT | ENUM | ✗ | ✓ | The enumeration of versions of the document |
| CurrentVersion | Current Version | OBJECT | SINGLE | ✗ | ✓ | The current (latest) document version of this version series, whether it is a major version or a minor version |
| ReleasedVersion | Released Version | OBJECT | SINGLE | ✗ | ✓ | The latest released major version of this version series |
| Reservation | Reservation | OBJECT | SINGLE | ✗ | ✓ | The reservation of the current version series |

### Security & Permissions Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| Owner | Owner | STRING | SINGLE | ✗ | ✓ | The security owner of the object |
| Permissions | Permissions | OBJECT | LIST | ✗ | ✓ | The discretionary permissions for the object |
| SecurityPolicy | Security Policy | OBJECT | SINGLE | ✓ | ✓ | The Security Policy associated with this object |
| SecurityParent | Security Parent | OBJECT | SINGLE | ✗ | ✓ | The object from which this object inherits security |
| SecurityFolder | Security Folder | OBJECT | SINGLE | ✓ | ✓ | Partial security proxy defined for inherited access control |
| ActiveMarkings | Active Markings | OBJECT | LIST | ✗ | ✓ | The list of Active Markings currently applied to this object |
| ClbSharingController | Sharing Controller | OBJECT | SINGLE | ✓ | ✗ | Sharing Controller |
| ClbSecurityController | Security Controller | OBJECT | SINGLE | ✓ | ✗ | Security Controller |
| ClbSensitiveContent | Sensitive Content | LONG | SINGLE | ✓ | ✗ | Specifies if this document contains sensitive content |

### Content Management Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| ContentSize | Content Size | DOUBLE | SINGLE | ✓ | ✓ | The size (in bytes) of the captured content associated with this object |
| MimeType | Mime Type | STRING | SINGLE | ✓ | ✓ | The MIME type of the document |
| ContentElements | Content Elements | OBJECT | LIST | ✗ | ✓ | List of content elements contained within this object |
| ContentElementsPresent | Content Elements Present | STRING | LIST | ✗ | ✓ | List of the component types of the content elements contained within this object at the time it was last made persistent |
| StoragePolicy | Storage Policy | OBJECT | SINGLE | ✓ | ✓ | The storage policy for the document |
| StorageLocation | Storage Location | STRING | SINGLE | ✓ | ✓ | The storage location for the document |
| StorageArea | Storage Area | OBJECT | SINGLE | ✓ | ✓ | The Storage Area this object is stored in |
| DateContentLastAccessed | Date Content Last Accessed | DATE | SINGLE | ✓ | ✓ | The date and time when this content of a document was last accessed |
| ContentRetentionDate | Content Retention Date | DATE | SINGLE | ✓ | ✓ | The date until which the object must be retained, as determined by the content storage subsystem |
| CmThumbnails | Thumbnails | OBJECT | ENUM | ✗ | ✓ | Contains the set of thumbnail images corresponding to this document |

### Lifecycle Management Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| DocumentLifecyclePolicy | Document Lifecycle Policy | OBJECT | SINGLE | ✓ | ✓ | Document lifecycle policy applied to a document |
| CurrentState | Current State | STRING | SINGLE | ✓ | ✓ | The current state of a document |
| IsInExceptionState | Is In Exception State | BOOLEAN | SINGLE | ✓ | ✓ | Indicates whether the lifecycle of a document is in exception state |
| CmRetentionDate | Retention Date | DATE | SINGLE | ✓ | ✓ | Specifies the earliest date at which the object may be deleted |
| CmIsMarkedForDeletion | Is Marked For Deletion | BOOLEAN | SINGLE | ✗ | ✓ | Indicates whether this object is marked for deletion |
| ClbDocumentState | Document State | LONG | SINGLE | ✓ | ✗ | ClbDocumentState |

### Workflow & Task Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| WorkflowSubscriptions | Workflow Subscriptions | OBJECT | ENUM | ✗ | ✓ | Enumeration of workflow subscription objects whose target is this object |
| CoordinatedTasks | Coordinated Tasks | OBJECT | ENUM | ✗ | ✓ | The enumeration of tasks coordinated by the object |

### Relationship & Structure Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| FoldersFiledIn | Folders Filed In | OBJECT | ENUM | ✗ | ✓ | The list of folders where this document is filed |
| Containers | Containers | OBJECT | ENUM | ✗ | ✓ | The enumeration of referential containment relationship objects that identify the containers of this object |
| Annotations | Annotations | OBJECT | ENUM | ✗ | ✓ | The annotations associated with this object |
| CompoundDocumentState | Compound Document State | LONG | SINGLE | ✓ | ✓ | State of document, is it a standard document or a compound document |
| ChildDocuments | Child Documents | OBJECT | ENUM | ✗ | ✓ | Return, security permitting, enumeration of child component documents |
| ChildRelationships | Child Relationships | OBJECT | ENUM | ✗ | ✓ | Return enumeration of child component relationship objects |
| ParentDocuments | Parent Documents | OBJECT | ENUM | ✗ | ✓ | Return, security permitting, enumeration of parent component documents |
| ParentRelationships | Parent Relationships | OBJECT | ENUM | ✗ | ✓ | Return enumeration of parent component relationship objects |

### Indexing & Search Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| IndexationId | Indexation Id | GUID | SINGLE | ✓ | ✓ | The object ID of the verity collection an object is stored into, or null for objects that were full text indexed prior to the 4.0 release |
| CmIndexingFailureCode | Indexing Failure Code | LONG | SINGLE | ✓ | ✓ | Bitmask of well known reasons for indexing of content to fail |
| ClassificationStatus | Classification Status | LONG | SINGLE | ✓ | ✓ | The auto-classification status for the document |

### Records Management Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| CmHoldRelationships | Hold Relationships | OBJECT | ENUM | ✗ | ✓ | An enumeration of CmHoldRelationship objects associated with this object |
| RecordInformation | Record Information | OBJECT | SINGLE | ✓ | ✗ | RMSystem |
| CanDeclare | Can Declare | BOOLEAN | SINGLE | ✗ | ✗ | RMSystem |

### Integration Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| SfSalesforceRelationships | Salesforce Relationships | OBJECT | ENUM | ✗ | ✗ | Association property with reflective property set to SfDocument on the SfSalesforceRelationship class. Deletion of the document version object will result in the deletion of all associated Salesforce relationships |

### Digital Signature Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| DSSignatureStatus | Signature Status | LONG | SINGLE | ✓ | ✗ | Signature Status |
| DSEnvelopeID | Envelope ID | STRING | SINGLE | ✓ | ✗ | Envelope ID |

### AI & Analytics Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| GenaiDateIndexed | Gen AI Date Indexed | DATE | SINGLE | ✓ | ✗ | (empty description) |
| GenaiWatsonxSummary | Watsonx Summary | STRING | SINGLE | ✓ | ✗ | (empty description) |

### Entry Template Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| EntryTemplateId | Entry Template Id | GUID | SINGLE | ✓ | ✗ | Entry Template Id |
| EntryTemplateObjectStoreName | Entry Template Object Store Name | STRING | SINGLE | ✓ | ✗ | Entry Template Object Store Name |
| EntryTemplateLaunchedWorkflowNumber | Entry Template Launched Workflow Number | STRING | SINGLE | ✓ | ✗ | Entry Template Launched Workflow Number |

### WebDAV Lock Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| LockToken | Lock Token | GUID | SINGLE | ✓ | ✓ | The token used by a WebDAV client to signal a lock on this resource |
| LockTimeout | Lock Timeout | LONG | SINGLE | ✓ | ✓ | The number of seconds beyond the last modified date that the server will retain a lock |
| LockOwner | Lock Owner | STRING | SINGLE | ✓ | ✓ | A string supplied by the WebDAV client when a lock is applied that describes the owner of the lock |

### Replication Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| ReplicationGroup | Replication Group | OBJECT | SINGLE | ✓ | ✓ | A reference to the replication group to which the object is affiliated |
| ExternalReplicaIdentities | External Replica Identities | OBJECT | LIST | ✓ | ✓ | A list of the identities of replicas of the object in external repositories |

### System Internal Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| ClassDescription | Class Description | OBJECT | SINGLE | ✓ | ✓ | Describes an object's class |
| This | This | OBJECT | SINGLE | ✓ | ✓ | Enables the expression of relationships among objects in DMA queries and selects candidate objects in query results |
| AuditedEvents | Audited Events | OBJECT | ENUM | ✗ | ✓ | A collection of event objects audited for the object |
| ComponentBindingLabel | Component Binding Label | STRING | SINGLE | ✓ | ✗ | Component Binding Label |
| IgnoreRedirect | Ignore Redirect | BOOLEAN | SINGLE | ✓ | ✗ | Ignore Redirect |

---

## HRDocument Class Properties

The `HRDocument` class extends the base `Document` class with **40 additional HR-specific properties**.

### Personal Information Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| FirstName | First Name | STRING | SINGLE | ✓ | ✗ | First Name |
| LastName | Last Name | STRING | SINGLE | ✓ | ✗ | Last Name |
| PersonalID | Personal ID | STRING | SINGLE | ✓ | ✗ | Personal ID |
| Birthdate | Birthdate | DATE | SINGLE | ✓ | ✗ | Birthdate |

### Employment Identification Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| EmployeeID | Employee ID | STRING | SINGLE | ✓ | ✗ | Employee ID |
| SAPEmployeeID | SAP Employee ID | STRING | SINGLE | ✓ | ✗ | SAP Employee ID |

### Job Details Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| JobRole | Job Role | STRING | SINGLE | ✓ | ✗ | Job Role |
| JobFunction | Job Function | STRING | SINGLE | ✓ | ✗ | Job Function |
| JobCode | Job Code | STRING | SINGLE | ✓ | ✗ | Job Code |
| JobLevel | Job Level | STRING | SINGLE | ✓ | ✗ | Job Level |
| JobStatus | Job Status | STRING | SINGLE | ✓ | ✗ | Job Status |
| EmploymentType | Employment Type | STRING | SINGLE | ✓ | ✗ | Employment Type |
| CurrentStatus | Current Status | STRING | SINGLE | ✓ | ✗ | Current Status |

### Employment Dates Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| StartDate | Start Date | DATE | SINGLE | ✓ | ✗ | Start Date |
| TerminationDate | Termination Date | DATE | SINGLE | ✓ | ✗ | Termination Date |

### Organizational Structure Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| Company | Company | STRING | SINGLE | ✓ | ✗ | Company |
| CompanyCode | Company Code | STRING | SINGLE | ✓ | ✗ | Company Code |
| BusinessUnit | Business Unit | STRING | SINGLE | ✓ | ✗ | Business Unit |
| Department | Department | STRING | SINGLE | ✓ | ✗ | Department |
| Division | Division | STRING | SINGLE | ✓ | ✗ | Division or Department |
| CostCenter | Cost Center | STRING | SINGLE | ✓ | ✗ | Cost Center |
| Location | Location | STRING | SINGLE | ✓ | ✗ | Location |

### Document Classification Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| DocType | DocType | STRING | SINGLE | ✓ | ✗ | DocType |
| DocumentCategory | Document Category | STRING | SINGLE | ✓ | ✗ | Document Category |
| ClassDocType | ClassDocType | STRING | SINGLE | ✓ | ✗ | ClassDocType |

### SAP Integration Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| SAPDocId | SAPDocId | STRING | SINGLE | ✓ | ✗ | SAPDocId |
| SAPDocProt | SAPDocProt | STRING | SINGLE | ✓ | ✗ | SAPDocProt |
| SAPComps | SAPComps | STRING | SINGLE | ✓ | ✗ | SAPComps |
| SAPContType | SAPContType | STRING | SINGLE | ✓ | ✗ | SAPContType |
| SAPCompVersion | SAPCompVersion | STRING | SINGLE | ✓ | ✗ | SAPCompVersion |
| SapLinkTrigger | SapLinkTrigger | BOOLEAN | SINGLE | ✓ | ✗ | SapLinkTrigger |
| sapLinked | sapLinked | STRING | SINGLE | ✓ | ✗ | sapLinked |

### Salesforce Integration Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| SFLinkTrigger | SFLinkTrigger | BOOLEAN | SINGLE | ✓ | ✗ | SFLinkTrigger |

### Workflow Integration Properties

| Property | Display Name | Data Type | Cardinality | Searchable | System Owned | Description |
|----------|--------------|-----------|-------------|------------|--------------|-------------|
| docuflowTimestamp | docuflowTimestamp | DATE | SINGLE | ✓ | ✗ | docuflowTimestamp |
| docuflowUsername | docuflowUsername | STRING | SINGLE | ✓ | ✗ | docuflowUsername |

---

## Property Usage Guidelines

### Searchable Properties
Properties marked as **Searchable** can be used in search queries and filters. Use these properties for:
- Building search interfaces
- Creating saved searches
- Filtering document lists
- Generating reports

### System-Owned Properties
Properties marked as **System Owned** are managed by the system and typically:
- Cannot be directly modified by users
- Are automatically updated by system processes
- Should not be included in custom forms (except for display)

### Custom Properties
Properties **not** marked as System Owned are custom business properties that:
- Can be modified by authorized users
- Should be included in data entry forms
- Represent business-specific metadata
- Can be used for business rules and workflows

### Hidden Properties
Some properties are marked as **Hidden** and are:
- Used internally by the system
- Not displayed in standard user interfaces
- Available for advanced queries and system operations

---

## Property Cardinality Explained

### SINGLE
- Contains exactly one value
- Most common cardinality type
- Examples: FirstName, EmployeeID, DateCreated

### LIST
- Contains an ordered list of values
- Maintains insertion order
- Examples: Permissions, ContentElementsPresent

### ENUM
- Contains an enumeration (collection) of objects
- Used for relationships and collections
- Examples: Versions, ChildDocuments, WorkflowSubscriptions

---

## Data Type Specifications

### STRING
- Text values of variable length
- Used for names, descriptions, identifiers
- Searchable with text operators (contains, starts with, etc.)

### DATE
- Date and time values
- Stored in ISO 8601 format
- Searchable with date range operators

### LONG
- 64-bit integer values
- Used for counters, status codes, flags
- Searchable with numeric operators

### DOUBLE
- 64-bit floating-point values
- Used for sizes, measurements
- Searchable with numeric operators

### BOOLEAN
- True/false values
- Used for flags and toggles
- Searchable with equality operators

### GUID
- Globally Unique Identifiers
- 128-bit values
- Used for object references and IDs

### OBJECT
- References to other objects
- Used for relationships and complex types
- Can be navigated in queries

---

## Integration Property Patterns

### SAP Integration Pattern
```
SAPEmployeeID → Links to SAP HR system
SAPDocId → SAP document identifier
SapLinkTrigger → Triggers SAP synchronization
sapLinked → Status of SAP linkage
```

### Salesforce Integration Pattern
```
SfSalesforceRelationships → Collection of SF relationships
SFLinkTrigger → Triggers Salesforce synchronization
```

### Workflow Integration Pattern
```
WorkflowSubscriptions → Active workflow subscriptions
DocumentLifecyclePolicy → Applied lifecycle policy
CurrentState → Current lifecycle state
```

---

## Best Practices for Property Management

### 1. Required Properties
Always populate these essential properties:
- **DocumentTitle**: For user-friendly identification
- **MimeType**: For proper content handling
- **Creator/DateCreated**: Automatically set by system

### 2. HR Document Properties
For HR documents, ensure these are populated:
- **EmployeeID** or **SAPEmployeeID**: For employee linkage
- **FirstName** and **LastName**: For identification
- **Department** and **Company**: For organizational context
- **DocumentCategory**: For classification

### 3. Security Properties
Configure security appropriately:
- **Owner**: Set to appropriate user or group
- **Permissions**: Define access control lists
- **SecurityPolicy**: Apply organizational policies
- **ClbSensitiveContent**: Flag sensitive documents

### 4. Lifecycle Properties
Manage document lifecycle:
- **DocumentLifecyclePolicy**: Apply retention policies
- **CmRetentionDate**: Set retention requirements
- **CurrentState**: Track lifecycle state

### 5. Integration Properties
For integrated systems:
- Set trigger flags (**SapLinkTrigger**, **SFLinkTrigger**) to initiate sync
- Populate system-specific IDs for cross-reference
- Maintain consistent identifiers across systems

---

## Property Validation Rules

### String Properties
- Maximum length varies by property
- Some properties may have format requirements
- Case sensitivity depends on configuration

### Date Properties
- Must be valid dates
- Time zone handling per system configuration
- Range validation may apply (e.g., StartDate < TerminationDate)

### Numeric Properties
- Must be within valid ranges
- Some properties have specific value sets (enumerations)

### Boolean Properties
- Only true/false values accepted
- Null may be allowed depending on property

---

## Conclusion

This comprehensive property specification provides the foundation for effective document management in IBM Content Services. Understanding these properties enables:

- **Proper document classification and organization**
- **Effective search and retrieval**
- **Compliance with retention and security requirements**
- **Integration with enterprise systems**
- **Automated lifecycle management**

Use this reference when designing forms, building integrations, creating search interfaces, and implementing business rules.