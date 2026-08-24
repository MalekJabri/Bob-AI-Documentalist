# Repository Audit Tools

This folder contains utility scripts for IBM FileNet Content Repository auditing.

## Available Tools

### init_audit.py

Python script to initialize the audit folder structure before running an audit.

**Purpose:**
- Automatically creates standardized folder hierarchy for audit outputs
- Reads Object Store name from MCP configuration
- Generates audit metadata and README files
- Ensures consistent organization across multiple audits

**Usage:**

```bash
# Basic usage (reads Object Store from .bob/mcp.json)
python tools/init_audit.py

# Specify Object Store manually
python tools/init_audit.py --object-store OS2

# Specify custom date (DD-MM format)
python tools/init_audit.py --date 19-05

# Specify custom MCP config location
python tools/init_audit.py --config /path/to/mcp.json

# Full example with all options
python tools/init_audit.py --object-store OS2 --date 19-05
```

**What it creates:**

```
audits/
└── [ObjectStore]_[DD-MM]/
    ├── reports/           # Executive summary and comprehensive reports
    ├── data/             # CSV files and raw data exports
    ├── analysis/         # Detailed analysis documents
    ├── recommendations/  # Actionable recommendations and roadmaps
    ├── audit_metadata.json
    └── README.md
```

**Requirements:**
- Python 3.6+
- No external dependencies (uses only standard library)

**When to use:**
- Before starting a new audit
- When you want to pre-create the folder structure
- When running audits programmatically or in batch

**Integration with Bob:**

The Content Repository Auditor mode can also create this structure automatically, but this script is useful for:
- Pre-creating structure before Bob runs
- Batch audit preparation
- CI/CD pipeline integration
- Manual folder setup

### export_graphql_definitions.py

Python script to export IBM FileNet metadata to GraphQL mutation format.

**Purpose:**
- Export Class Definitions, Property Templates, and Choice Lists
- Generate GraphQL mutations compatible with IBM FileNet Content Services API
- Support migration, backup, and documentation workflows
- Integrate with existing GraphQL deployment tools

**Usage:**

```bash
# Export everything (choice lists, property templates, class definitions)
python tools/export_graphql_definitions.py --all

# Export only choice lists
python tools/export_graphql_definitions.py --choice-lists

# Export only property templates
python tools/export_graphql_definitions.py --property-templates

# Export only class definitions
python tools/export_graphql_definitions.py --class-definitions

# Export metadata for specific class and its dependencies
python tools/export_graphql_definitions.py --all --class-name HRDocument

# Export to custom directory
python tools/export_graphql_definitions.py --all --output-dir exports/my-export

# Use custom MCP config file
python tools/export_graphql_definitions.py --all --mcp-config /path/to/mcp.json
```

**What it creates:**

```
graphql/exports/
├── README.md                       # Export documentation
├── 01-choice-lists.graphql        # Choice list definitions
├── 02-property-templates.graphql  # Property template definitions
└── 03-class-definitions.graphql   # Class definition structures
```

**Requirements:**
- Python 3.6+
- `requests` library (`pip install requests`)
- Access to `.bob/mcp.json` with content-repository MCP server configuration
- Read permissions on target Object Store

**When to use:**
- During audits to export current repository state
- Before migrations to capture source metadata
- For backup and version control of metadata
- To generate deployment scripts for other environments

**Integration with Bob:**

The Content Repository Auditor mode can use this tool to:
- Export metadata during audit for documentation
- Create baseline snapshots for comparison
- Generate deployment artifacts
- Support migration planning

**Importing Exported Definitions:**

To import the exported GraphQL files into another repository:

1. Update `repositoryIdentifier` in each file to target Object Store
2. Update choice list references in property templates if needed
3. Execute in order using the GraphQL runner:

```bash
python graphql/run_graphql.py graphql/exports/01-choice-lists.graphql
python graphql/run_graphql.py graphql/exports/02-property-templates.graphql
python graphql/run_graphql.py graphql/exports/03-class-definitions.graphql
```

**Comparison with CS Deployment API:**

This tool is inspired by the IBM Content Services Deployment API and generates compatible GraphQL format. Key differences:

| Feature | export_graphql_definitions.py | CS Deployment API |
|---------|------------------------------|-------------------|
| Export Format | GraphQL mutations | Python API objects |
| Configuration | `.bob/mcp.json` | `config.py` |
| Dependencies | requests only | csdeploy package |
| Use Case | Quick export/audit | Full deployment automation |
| Complexity | Simple, single script | Comprehensive framework |

## Future Tools

Additional tools planned for this folder:
- `compare_audits.py` - Compare findings between two audit runs
- `export_findings.py` - Export audit findings to various formats
- `validate_structure.py` - Validate audit folder structure completeness
- `import_graphql_definitions.py` - Import GraphQL definitions with validation

## Related Resources

- **CS Deployment API Samples**: `/Users/jabrimalek/development/cs-deployment-api/ibm-content-platform-engine-samples/CS-Deployment-API/`
- **GraphQL Runner**: `graphql/run_graphql.py`
- **Content Repository Auditor Guide**: `docs/Content_Repository_Auditor_Guide.md`
- **Quick Start Guide**: `docs/Repository_Auditor_Quick_Start.md`

---

*Part of the IBM FileNet Content Repository Auditor toolkit*