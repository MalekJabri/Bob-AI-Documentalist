# Export GraphQL Definitions Tool - Analysis & Fix

## Problem Summary

The [`export_graphql_definitions.py`](export_graphql_definitions.py) tool fails with GraphQL validation errors because it manually constructs GraphQL queries that don't match your IBM FileNet Content Services GraphQL API schema.

## Root Cause

**Current Approach (❌ Broken):**
- Tool manually constructs raw GraphQL query strings
- Uses syntax like `repositoryObjects(objectTypes: [CHOICE_LIST])`
- Queries for fields like `symbolicName` that don't exist in your schema
- No abstraction layer for API differences

**Correct Approach (✅ Working):**
- Use the **`csdeploy`** Python package (already installed on your system)
- Provides proper abstractions: `ExportSelectionUtil`, `GraphqlRequest`, `GraphqlConnection`
- Handles API schema differences automatically
- Used by IBM's official CS Deployment API samples

## What's Missing

The tool needs to be rewritten to use `csdeploy` package methods:

### Available `csdeploy` Methods:

```python
from csdeploy import ExportSelectionUtil, GraphqlRequest, GraphqlConnection

# Methods available:
- query_choice_lists()       # Query all choice lists
- query_property_templates()  # Query all property templates  
- query_class_definitions()   # Query all class definitions
- get_selection_objects()     # Get specific objects
```

### Current Tool Structure (Lines 97-381):

```python
# ❌ BROKEN: Manual GraphQL query construction
def export_choice_lists(self, output_file: Path) -> int:
    query = f"""
    query GetChoiceLists {{
        repositoryObjects(
            repositoryIdentifier: "{self.object_store}"
            objectTypes: [CHOICE_LIST]  # ❌ Not supported
        ) {{
            independentObjects {{
                ... on ChoiceList {{
                    symbolicName  # ❌ Field doesn't exist
                }}
            }}
        }}
    }}
    """
```

### Required Tool Structure:

```python
# ✅ CORRECT: Use csdeploy package
from csdeploy import ExportSelectionUtil, GraphqlRequest, GraphqlConnection

def export_choice_lists(self, output_file: Path) -> int:
    # Create connection
    gql_connection = GraphqlConnection(
        url=self.server_url,
        username=self.config["username"],
        password=self.config["password"]
    )
    
    # Use ExportSelectionUtil
    gql_request = GraphqlRequest(gql_connection)
    util = ExportSelectionUtil(
        gql_request=gql_request,
        object_store_name=self.object_store
    )
    
    # Query using proper API
    response = util.query_choice_lists()
    choice_lists = response["data"]["repositoryObjects"]["independentObjects"]
    
    # Generate mutations...
```

## Comparison with CS Deployment API

### Your Tool vs. IBM Samples:

| Aspect | export_graphql_definitions.py | CS Deployment API Samples |
|--------|------------------------------|---------------------------|
| **Package** | ❌ Manual `requests` | ✅ `csdeploy` package |
| **Queries** | ❌ Hand-written GraphQL | ✅ `ExportSelectionUtil` methods |
| **Schema** | ❌ Hardcoded assumptions | ✅ API handles differences |
| **Auth** | ✅ Basic auth (works) | ✅ OAuth + Basic auth |
| **Export** | ✅ GraphQL mutations | ✅ Python objects + GraphQL |
| **Import** | ❌ Not implemented | ✅ Full import support |

## Reference Implementation

See: `/Users/jabrimalek/development/cs-deployment-api/ibm-content-platform-engine-samples/CS-Deployment-API/demoutil.py`

```python
# Lines 37-41 from demoutil.py
gql_request = GraphqlRequest(self.gqlConnection)
classes_response = ExportSelectionUtil(
    gql_request=gql_request, 
    object_store_name=self.os_name
).query_class_definitions()
```

## Fix Options

### Option 1: Rewrite Tool to Use `csdeploy` (Recommended)

**Pros:**
- ✅ Will work with your API
- ✅ Future-proof (handles schema changes)
- ✅ Matches IBM best practices
- ✅ Can leverage full `csdeploy` features

**Cons:**
- ⚠️ Requires significant rewrite (lines 46-381)
- ⚠️ Adds `csdeploy` as dependency

**Effort:** ~2-3 hours of development

### Option 2: Use CS Deployment API Notebooks Directly

**Pros:**
- ✅ Already working
- ✅ Full featured (export + import)
- ✅ IBM supported

**Cons:**
- ⚠️ Requires Jupyter
- ⚠️ Different workflow than standalone script

**Effort:** ~30 minutes to configure

### Option 3: Use MCP Tools for Queries

**Pros:**
- ✅ Already configured
- ✅ No code changes needed
- ✅ Works through Bob interface

**Cons:**
- ⚠️ Manual process
- ⚠️ No automated export to GraphQL format

**Effort:** Immediate (no development)

## Recommended Action Plan

### Short Term (Immediate):
1. **Document the limitation** in tool README
2. **Use MCP tools** for metadata queries via Bob
3. **Use CS Deployment API notebooks** for full export/import

### Long Term (Future Enhancement):
1. **Rewrite tool** to use `csdeploy` package
2. **Add import functionality** (not just export)
3. **Add filtering options** (by date, by pattern, etc.)
4. **Integrate with audit workflow**

## Quick Fix for Current Tool

Add dependency check and helpful error message:

```python
# At top of file
try:
    from csdeploy import ExportSelectionUtil, GraphqlRequest, GraphqlConnection
    HAS_CSDEPLOY = True
except ImportError:
    HAS_CSDEPLOY = False

# In __init__
if not HAS_CSDEPLOY:
    raise ImportError(
        "This tool requires the 'csdeploy' package. "
        "Install from IBM CS Deployment API samples or use MCP tools instead."
    )
```

## Related Files

- **CS Deployment API**: `/Users/jabrimalek/development/cs-deployment-api/ibm-content-platform-engine-samples/CS-Deployment-API/`
- **Sample notebooks**: `deploy_select_cd.ipynb`, `deploy_all_cd.ipynb`, `deploy_all.ipynb`
- **Config template**: `config.py`
- **Utility functions**: `demoutil.py`

## Conclusion

The `export_graphql_definitions.py` tool is **not compatible** with your GraphQL API because it doesn't use the `csdeploy` package. The tool needs a complete rewrite to use `ExportSelectionUtil` methods instead of manual GraphQL query construction.

**Immediate workaround:** Use the CS Deployment API Jupyter notebooks or Bob's MCP tools for metadata queries.