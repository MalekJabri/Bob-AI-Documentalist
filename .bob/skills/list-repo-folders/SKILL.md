---
name: list-repo-folders
description: Use when the user wants to list all folders in the content repository, get a folder tree summary, browse the MCP Content Services folder structure, or produce a repository folder report.
---

# List Repository Folders

Connect to the IBM FileNet Content Services MCP server, discover all folders across the entire
repository, and write a structured Markdown summary report.

## Steps

### 1. Read MCP config to identify the server key

Use `read_file` to read `.bob/mcp.json`. Extract:
- The server key name (e.g. `core-cs-mcp-server`)
- The `USERNAME` from the `env` block — used to label the report

### 2. Scan all folders via MCP

Because the repository may have many folders and a single unfiltered query is truncated, use the
`repository_object_search` MCP tool in **parallel batches** — one call per letter/prefix — to
retrieve all `Folder` objects.

Run these 33 prefix batches in parallel (split into two `function_calls` blocks of ~16 each to
avoid timeouts):

**Batch A — letters:**
`A B C D E F G H I J K L M N O P Q R S T U V W X Y Z`

**Batch B — numeric prefixes (employee subfolders):**
`01 02 03 04 05 06 07 08`

For each batch call, use:
```
search_class: "Folder"
search_properties: [{ operator: "STARTS", property_name: "FolderName", property_value: "<prefix>" }]
```

### 3. Aggregate results

From all batch responses, collect every folder object's `PathName` property value. Deduplicate.
Sort alphabetically.

Build a folder tree by grouping paths by their depth level:
- **Root folders** — paths with exactly one `/` segment (e.g. `/BOB_LAB`)
- **Level 2** — two segments (e.g. `/BOB_LAB/PENN`)
- **Level 3+** — deeper paths

### 4. Write the report

Use `write_file` to write the report. The output path is:
```
reports/folder-tree-<YYYYMMDD_HHmmss>.md
```
where the timestamp is the current UTC date and time at the moment of generation.

The report must include:

```markdown
# Repository Folder Report

**Server:** <server-key>
**Username:** <USERNAME from env>
**Generated:** <ISO timestamp>

## Summary

| Metric | Count |
|--------|-------|
| Total folders | N |
| Root-level folders | N |
| Hidden system folders | N |

## Folder Tree

<sorted, indented tree of all PathName values>

## Root Folders

<flat list of root-level folders only>
```

Mark any folder where `IsHiddenContainer` is `true` with a `[HIDDEN]` suffix.

### 5. Confirm to the user

Report back:
- Total folder count discovered
- Output file path
- A short inline summary (root folders listed by name)

Do NOT print credentials or passwords in the chat response.
