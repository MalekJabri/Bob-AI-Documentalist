# AI Documentalist

An AI-powered document management and classification system for HR documents using IBM FileNet Content Manager, driven by Bob — an AI assistant connected to a live content repository via the IBM Content Services MCP server.

## Project Overview

This project demonstrates how to use AI (Bob) to manage, classify, and organize HR documents in a content repository. It includes automated document generation, classification, and repository management capabilities across a 3-lab hands-on series.

## Features

- **Automated HR Document Generation**: Generate sample HR documents for testing
- **Document Classification**: Automatically classify documents using the HRDocument class
- **Repository Management**: Organize documents in a structured folder hierarchy
- **Metadata Management**: Properly tag documents with employee information, department, job role, etc.
- **AI-driven Auditing**: Let Bob inspect, compare, and recommend governance actions on live repository classes

## Project Structure

```
AIDocumentalist/
├── Lab1_Bob_as_Documentalist.md    # Introduction to Bob as a documentalist
├── Lab2_Generate_Sample_Content.md # Guide for generating sample HR documents
├── Lab3_Review_and_Reclassify.md   # Document review and reclassification guide
├── HR_Document_Class_Description.md # Full HRDocument class & property reference
├── generate_hr_documents.py         # Python script to generate HR documents
├── bulk_upload_employees.py         # Bulk upload helper script
├── .bob/
│   └── mcp.json                     # MCP server configuration (credentials)
├── Reference/                       # Reference documentation and images
│   ├── Classification_and_Cleaning_Plan.md
│   ├── Document_Class_Architecture.md
│   └── Document_Property_Specifications.md
└── Completed Lab/                   # Completed lab exercises
```

---

## Prerequisites

Before running any lab you need the following components installed and accessible.

### 1. Bob AI Assistant

Bob is the AI assistant that orchestrates all interactions with the content repository. It must be installed and running locally.

- **Download**: [IBM Bob](https://www.ibm.com/products/bob) *(or your internal distribution)*
- Bob uses a workspace folder — open this repository folder as your Bob workspace.

### 2. Python 3.9+

Required only for the document generation scripts (`generate_hr_documents.py`, `bulk_upload_employees.py`).

```bash
python --version   # must be 3.9 or later
```

No external packages are required — the scripts use the Python standard library only.

### 3. `uv` — Python package runner

The MCP server is launched by Bob via `uvx`, which ships with [uv](https://github.com/astral-sh/uv). Install it once:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify:
```bash
uvx --version
```

### 4. IBM Content Services access

You need credentials for an IBM FileNet / IBM Content Services GraphQL endpoint:

| Item | Description |
|------|-------------|
| `SERVER_URL` | The GraphQL endpoint URL of your Content Services deployment |
| `USERNAME` | Your service account username (format: `user.fid@tenantID`) |
| `PASSWORD` | Your service account password / API key |
| `OBJECT_STORE` | The symbolic name of the target Object Store (e.g. `OS1`) |

> **Lab environment**: If you are attending an instructor-led session, these credentials will be provided to you. Use your assigned tenant credentials in the configuration step below.

---

## MCP Server Configuration

Bob connects to the content repository through the **IBM Content Services MCP server**. This is configured in `.bob/mcp.json` at the root of the workspace.

### How it works

When Bob starts, it reads `.bob/mcp.json` and launches the MCP server as a background process using `uvx`. The server is pulled directly from GitHub — no manual installation step is needed beyond having `uv` on your PATH.

### Configuration file — `.bob/mcp.json`

Open `.bob/mcp.json` and fill in your credentials:

```json
{
  "mcpServers": {
    "core-cs-mcp-server": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/ibm-ecm/ibm-content-services-mcp-server",
        "core-cs-mcp-server"
      ],
      "env": {
        "USERNAME": "<your-username>",
        "PASSWORD": "<your-password>",
        "SERVER_URL": "<your-graphql-endpoint>",
        "OBJECT_STORE": "<your-object-store>"
      }
    }
  }
}
```

#### Field reference

| Field | Example value | Notes |
|-------|---------------|-------|
| `USERNAME` | `jdoe.fid@t2122` | Provided by your IBM Cloud / CP4BA admin |
| `PASSWORD` | `abc123...` | Treat as a secret — do not commit to git |
| `SERVER_URL` | `https://my-tenant.automationcloud.ibm.com/dba/run/content-services-graphql/graphql` | Must end in `/graphql` |
| `OBJECT_STORE` | `OS1` | Case-sensitive symbolic name of the object store |

> **Security note**: `.bob/mcp.json` is listed in `.gitignore`. Never commit credentials to source control. If you need to share the configuration, strip the `env` block and share the template only.

### Connecting to a CP4BA on-premises deployment

If your environment is an on-premises IBM Cloud Pak for Business Automation instance (instead of IBM Automation Cloud), the `SERVER_URL` pattern is slightly different and may also require an XSRF token:

```json
"env": {
  "USERNAME": "cpmanager",
  "PASSWORD": "<password>",
  "SERVER_URL": "https://<cpd-host>/content-services-graphql/graphql",
  "OBJECT_STORE": "CONTENT",
  "ECM_CS_XSRF_TOKEN": "<token>",
  "COOKIE": "ECM-CS-XSRF-Token=<token>"
}
```

### Verifying the connection

Once `.bob/mcp.json` is configured and Bob is open on this workspace, ask Bob:

```
Bob, list all root classes in the repository.
```

If the MCP server is connected, Bob will respond with the available root class types (Document, Folder, etc.). If you see a connection error, double-check `SERVER_URL`, credentials, and that `uvx` is on your PATH.

---

## Getting Started

### Setup steps

1. **Clone this repository**
   ```bash
   git clone <repo-url>
   cd AIDocumentalist
   ```

2. **Install `uv`** (if not already installed — see Prerequisites above)

3. **Configure the MCP server** — edit `.bob/mcp.json` with your credentials (see section above)

4. **Open the folder in Bob** — Bob auto-detects `.bob/mcp.json` and connects to the MCP server on startup

5. **Verify the connection** — ask Bob to list root classes (see above)

6. **Generate sample documents** *(Lab 2 only)*
   ```bash
   python generate_hr_documents.py
   ```

7. **Follow the lab guides in sequence**: Lab 1 → Lab 2 → Lab 3

---

## Usage

### Generating Sample HR Documents

```bash
# Interactive — prompts for your last name (used as namespace)
python generate_hr_documents.py

# Non-interactive — specify your last name directly
python generate_hr_documents.py --user DUPONT

# Add deliberate misclassification errors (required for Lab 3)
python generate_hr_documents.py --seed-misclassifications

# Preview without writing any files
python generate_hr_documents.py --dry-run

# Generate for a single employee only
python generate_hr_documents.py --employee 1
```

Your last name is used as both a **namespace** and a **random seed**, so every participant gets a unique but reproducible set of 5 fictional employees, and no two participants ever collide in the repository.

### Repository Structure

Documents are organized in the repository under:
```
/BOB_LAB/[YOUR_NAME]/[EmployeeID_Name]/[Category]/[Documents]
```

Example for user `DUPONT`:
```
/BOB_LAB/DUPONT/JAB001_Jade Robin/
├── 01_Recruitment/
├── 02_Employment_Contract/
├── 03_Personal_Administration/
├── 04_Payroll/
├── 05_Performance/
├── 06_Training/
├── 07_Disciplinary/
└── 08_Exit/
```

---

## HR Document Categories

The system manages documents across 8 categories:

| # | Category | Document Types |
|---|----------|---------------|
| 1 | **Recruitment** | Job Application, Interview Notes |
| 2 | **Employment Contract** | Employment Agreement |
| 3 | **Personal Administration** | Personal Info, ID Document |
| 4 | **Payroll** | Payslip, Salary Info |
| 5 | **Performance** | Performance Review |
| 6 | **Training** | Training Record |
| 7 | **Disciplinary** | Disciplinary Record |
| 8 | **Exit** | Exit Document |

---

## Document Metadata

Each HR document is stored under the `HRDocument` class and includes standardized metadata:

| Property | Description |
|----------|-------------|
| `EmployeeID` | Internal employee identifier |
| `FirstName` / `LastName` | Employee name |
| `DocType` | Discriminator: `JobApplication`, `Payslip`, `PerformanceReview`, etc. |
| `Department` | IT, Marketing, HR, Sales, Finance |
| `JobRole` | Employee's job title |
| `Company` / `CompanyCode` | Company name and code |
| `CostCenter` | Cost center code |
| `Location` | Work location |
| `StartDate` | Employment start date |

See [`HR_Document_Class_Description.md`](HR_Document_Class_Description.md) for the full property specification (40 custom HR properties + 79 inherited system properties).

---

## Labs

| Lab | Title | Duration | What You Do |
|-----|-------|----------|-------------|
| [Lab 1](Lab1_Bob_as_Documentalist.md) | Meet Bob, Your AI Documentalist | ~30 min | Inventory all document classes, identify legacy/duplicate classes, deep-dive HRDocument, get a cleaning roadmap |
| [Lab 2](Lab2_Generate_Sample_Content.md) | Feeding Bob: Generate Sample Content | ~45 min | Generate 40 realistic HR documents with deliberate errors and upload them to the repository |
| [Lab 3](Lab3_Review_and_Reclassify.md) | Bob the Classifier: Review & Reclassify | ~30 min | Run a classification audit, read document content, detect and fix misclassified documents |

---

## Reference

- [`Reference/Document_Class_Architecture.md`](Reference/Document_Class_Architecture.md) — Full class hierarchy diagram and catalog
- [`Reference/Document_Property_Specifications.md`](Reference/Document_Property_Specifications.md) — Complete property specifications
- [`Reference/Classification_and_Cleaning_Plan.md`](Reference/Classification_and_Cleaning_Plan.md) — Detailed cleaning plan

---

## Contributing

This is a demonstration project for learning purposes.

## License

[Specify your license here]
