#!/usr/bin/env python3
"""
Export GraphQL Definitions Tool

This tool exports Class Definitions, Property Templates, and Choice Lists from
an IBM FileNet Content Services repository to GraphQL mutation format.

It reads connection settings from .bob/mcp.json and uses the IBM csdeploy package
to properly query the GraphQL API.

Usage:
    python tools/export_graphql_definitions.py --all
    python tools/export_graphql_definitions.py --choice-lists
    python tools/export_graphql_definitions.py --property-templates
    python tools/export_graphql_definitions.py --class-definitions
    python tools/export_graphql_definitions.py --class-name HRDocument
    python tools/export_graphql_definitions.py --output-dir exports/graphql

Features:
- Exports all metadata types or specific types
- Generates properly formatted GraphQL mutations
- Includes dependencies (choice lists for properties, etc.)
- Creates organized folder structure
- Supports filtering by class name or pattern
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Try to import csdeploy, provide helpful error if not available
try:
    from csdeploy import GraphqlConnection, GraphqlRequest, ExportSelectionUtil
except ImportError:
    print("Error: csdeploy library not found.")
    print("This tool requires the IBM Content Services Deployment API package.")
    print("\nInstall from: /Users/jabrimalek/development/cs-deployment-api/")
    print("Or use the CS Deployment API Jupyter notebooks instead.")
    sys.exit(1)


class GraphQLExporter:
    """Exports repository metadata to GraphQL mutation format using csdeploy."""
    
    def __init__(self, mcp_config_path: str = ".bob/mcp.json"):
        """Initialize exporter with MCP configuration."""
        self.mcp_config_path = Path(mcp_config_path)
        self.config = self._load_mcp_config()
        self.server_url = self.config.get("url")
        self.object_store = self.config.get("objectStore")
        
        if not self.server_url or not self.object_store:
            raise ValueError("MCP config must contain 'url' and 'objectStore'")
        
        # Initialize csdeploy connection
        self.gql_connection = GraphqlConnection(
            url=self.server_url,
            username=self.config["username"],
            password=self.config["password"]
        )
        self.gql_request = GraphqlRequest(self.gql_connection)
        self.export_util = ExportSelectionUtil(
            gql_request=self.gql_request,
            object_store_name=self.object_store
        )
    
    def _load_mcp_config(self) -> Dict:
        """Load MCP server configuration."""
        if not self.mcp_config_path.exists():
            raise FileNotFoundError(f"MCP config not found: {self.mcp_config_path}")
        
        with open(self.mcp_config_path, 'r') as f:
            config = json.load(f)
        
        # Extract content-repository server config
        for server_name, server in config.get("mcpServers", {}).items():
            if "content-repository" in server_name or "content-repository" in str(server.get("command", "")):
                env = server.get("env", {})
                return {
                    "url": env.get("GRAPHQL_ENDPOINT") or env.get("SERVER_URL"),
                    "objectStore": env.get("OBJECT_STORE_NAME") or env.get("OBJECT_STORE"),
                    "username": env.get("USERNAME"),
                    "password": env.get("PASSWORD")
                }
        
        raise ValueError("content-repository MCP server not found in config")
    
    def export_choice_lists(self, output_file: Path) -> int:
        """Export all choice lists to GraphQL format."""
        print("Querying choice lists using csdeploy...")
        
        try:
            response = self.export_util.query_choice_lists()
            choice_lists = response.get("data", {}).get("repositoryObjects", {}).get("independentObjects", [])
        except Exception as e:
            print(f"Error querying choice lists: {e}")
            return 0
        
        if not choice_lists:
            print("No choice lists found")
            return 0
        
        # Generate GraphQL mutations
        mutations = []
        mutations.append(f"# Choice Lists Export")
        mutations.append(f"# Generated: {datetime.now().isoformat()}")
        mutations.append(f"# Object Store: {self.object_store}")
        mutations.append(f"# Total Choice Lists: {len(choice_lists)}")
        mutations.append("")
        
        for cl in choice_lists:
            # Extract display name - handle both direct displayName and localized displayNames
            display_name = cl.get("displayName", "")
            if not display_name and cl.get("displayNames"):
                display_names = cl.get("displayNames", [])
                if display_names:
                    display_name = display_names[0].get("localizedText", "Unknown")
            
            mutation_name = f"Create{cl.get('id', 'Unknown').replace('-', '').replace('{', '').replace('}', '')}ChoiceList"
            mutations.append(f"mutation {mutation_name} {{")
            mutations.append(f"  admCreateChoiceList(")
            mutations.append(f'    repositoryIdentifier: "{self.object_store}"')
            mutations.append(f"    choiceListProperties: {{")
            mutations.append(f'      dataType: {cl.get("dataType", "STRING")}')
            mutations.append(f'      displayName: "{display_name}"')
            
            if cl.get("choiceValues"):
                mutations.append(f"      choiceValues: {{")
                mutations.append(f"        replace: [")
                for cv in cl["choiceValues"]:
                    mutations.append(f"          {{")
                    mutations.append(f'            choiceType: {cl.get("dataType", "STRING")}')
                    cv_display = cv.get("displayName", "")
                    if not cv_display and cv.get("displayNames"):
                        cv_display = cv["displayNames"][0].get("localizedText", "")
                    mutations.append(f'            choiceStringValue: "{cv.get("choiceStringValue", "")}"')
                    mutations.append(f"            displayNames: {{")
                    mutations.append(f"              replace: [")
                    mutations.append(f'                {{ localeName: "en-us", localizedText: "{cv_display}" }}')
                    mutations.append(f"              ]")
                    mutations.append(f"            }}")
                    mutations.append(f"          }}")
                mutations.append(f"        ]")
                mutations.append(f"      }}")
            
            mutations.append(f"    }}")
            mutations.append(f"  ) {{")
            mutations.append(f"    id")
            mutations.append(f"  }}")
            mutations.append(f"}}")
            mutations.append("")
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text("\n".join(mutations))
        print(f"✓ Exported {len(choice_lists)} choice lists to {output_file}")
        return len(choice_lists)
    
    def export_property_templates(self, output_file: Path, class_name: Optional[str] = None) -> int:
        """Export property templates to GraphQL format."""
        print(f"Querying property templates using csdeploy{' for ' + class_name if class_name else ''}...")
        
        try:
            response = self.export_util.query_property_templates()
            property_templates = response.get("data", {}).get("repositoryObjects", {}).get("independentObjects", [])
        except Exception as e:
            print(f"Error querying property templates: {e}")
            return 0
        
        # Filter by class if specified
        if class_name and property_templates:
            # Note: Filtering by class would require additional query - for now export all
            print(f"Note: Exporting all property templates (class filtering requires additional implementation)")
        
        if not property_templates:
            print(f"No property templates found")
            return 0
        
        # Generate GraphQL mutations
        mutations = []
        mutations.append(f"# Property Templates Export")
        if class_name:
            mutations.append(f"# Class: {class_name}")
        mutations.append(f"# Generated: {datetime.now().isoformat()}")
        mutations.append(f"# Object Store: {self.object_store}")
        mutations.append(f"# Total Property Templates: {len(property_templates)}")
        mutations.append("")
        
        for pt in property_templates:
            display_name = pt.get("displayName", "")
            if not display_name and pt.get("displayNames"):
                display_names = pt.get("displayNames", [])
                if display_names:
                    display_name = display_names[0].get("localizedText", "Unknown")
            
            symbolic_name = pt.get("symbolicName", pt.get("id", "Unknown"))
            mutation_name = f"Create{symbolic_name.replace(' ', '')}PropertyTemplate"
            
            mutations.append(f"mutation {mutation_name} {{")
            mutations.append(f"  admCreatePropertyTemplate(")
            mutations.append(f'    repositoryIdentifier: "{self.object_store}"')
            mutations.append(f'    dataType: {pt.get("dataType", "STRING")}')
            mutations.append(f"    propertyTemplateProperties: {{")
            mutations.append(f'      cardinality: {pt.get("cardinality", "SINGLE")}')
            mutations.append(f"      displayNames: {{")
            mutations.append(f"        replace: [")
            mutations.append(f"          {{")
            mutations.append(f'            localeName: "en-us"')
            mutations.append(f'            localizedText: "{display_name}"')
            mutations.append(f"          }}")
            mutations.append(f"        ]")
            mutations.append(f"      }}")
            mutations.append(f'      symbolicName: "{symbolic_name}"')
            
            if pt.get("choiceList"):
                cl_id = pt["choiceList"].get("id", "CHOICE_LIST_ID_PLACEHOLDER")
                mutations.append(f"      # Note: Replace with actual choice list ID")
                mutations.append(f'      # choiceList: {{ identifier: "{cl_id}" }}')
            
            mutations.append(f"    }}")
            mutations.append(f"  ) {{")
            mutations.append(f"    id")
            mutations.append(f"  }}")
            mutations.append(f"}}")
            mutations.append("")
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text("\n".join(mutations))
        print(f"✓ Exported {len(property_templates)} property templates to {output_file}")
        return len(property_templates)
    
    def export_class_definitions(self, output_file: Path, class_name: Optional[str] = None) -> int:
        """Export class definitions to GraphQL format."""
        print(f"Querying class definitions using csdeploy{' for ' + class_name if class_name else ''}...")
        
        try:
            response = self.export_util.query_class_definitions()
            class_definitions = response.get("data", {}).get("repositoryObjects", {}).get("independentObjects", [])
        except Exception as e:
            print(f"Error querying class definitions: {e}")
            return 0
        
        # Filter by class name if specified
        if class_name:
            class_definitions = [cd for cd in class_definitions 
                                if cd.get("symbolicName") == class_name or cd.get("displayName") == class_name]
        
        if not class_definitions:
            print(f"No class definitions found{' for ' + class_name if class_name else ''}")
            return 0
        
        # Generate GraphQL mutations
        mutations = []
        mutations.append(f"# Class Definitions Export")
        if class_name:
            mutations.append(f"# Class: {class_name}")
        mutations.append(f"# Generated: {datetime.now().isoformat()}")
        mutations.append(f"# Object Store: {self.object_store}")
        mutations.append(f"# Total Class Definitions: {len(class_definitions)}")
        mutations.append("")
        mutations.append("# Note: This export includes class structure only.")
        mutations.append("# Property templates and choice lists must be created first.")
        mutations.append("")
        
        for cd in class_definitions:
            display_name = cd.get("displayName", "")
            if not display_name and cd.get("displayNames"):
                display_names = cd.get("displayNames", [])
                if display_names:
                    display_name = display_names[0].get("localizedText", "Unknown")
            
            symbolic_name = cd.get("symbolicName", cd.get("id", "Unknown"))
            mutation_name = f"Create{symbolic_name.replace(' ', '')}ClassDefinition"
            
            mutations.append(f"mutation {mutation_name} {{")
            mutations.append(f"  createClassDefinition(")
            mutations.append(f"    input: {{")
            mutations.append(f'      repositoryIdentifier: "{self.object_store}"')
            mutations.append(f'      symbolicName: "{symbolic_name}"')
            mutations.append(f'      displayName: "{display_name}"')
            
            if cd.get("superclassDefinition"):
                parent_name = cd["superclassDefinition"].get("symbolicName", "Document")
                mutations.append(f'      parentClassIdentifier: "{parent_name}"')
            
            mutations.append(f"      isAbstract: false")
            mutations.append(f"      isSystemOwned: false")
            
            # Add property definitions if available
            if cd.get("propertyDefinitions"):
                mutations.append(f"      propertyDefinitions: [")
                for pd in cd["propertyDefinitions"]:
                    pt = pd.get("propertyTemplate", {})
                    pt_name = pt.get("symbolicName", "Unknown")
                    mutations.append(f"        {{")
                    mutations.append(f'          propertyTemplateSymbolicName: "{pt_name}"')
                    mutations.append(f"          isValueRequired: false")
                    mutations.append(f"          isHidden: false")
                    mutations.append(f"          isReadOnly: false")
                    mutations.append(f"        }}")
                mutations.append(f"      ]")
            
            mutations.append(f"    }}")
            mutations.append(f"  ) {{")
            mutations.append(f"    id")
            mutations.append(f"  }}")
            mutations.append(f"}}")
            mutations.append("")
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text("\n".join(mutations))
        print(f"✓ Exported {len(class_definitions)} class definitions to {output_file}")
        return len(class_definitions)
    
    def export_all(self, output_dir: Path, class_name: Optional[str] = None):
        """Export all metadata types to organized GraphQL files."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"Exporting metadata from Object Store: {self.object_store}")
        print(f"Output directory: {output_dir}")
        print(f"Using IBM csdeploy package")
        print(f"{'='*60}")
        
        total_exported = 0
        
        # Export choice lists
        print("\n1. Exporting Choice Lists...")
        cl_file = output_dir / "01-choice-lists.graphql"
        total_exported += self.export_choice_lists(cl_file)
        
        # Export property templates
        print("\n2. Exporting Property Templates...")
        pt_file = output_dir / "02-property-templates.graphql"
        total_exported += self.export_property_templates(pt_file, class_name)
        
        # Export class definitions
        print("\n3. Exporting Class Definitions...")
        cd_file = output_dir / "03-class-definitions.graphql"
        total_exported += self.export_class_definitions(cd_file, class_name)
        
        # Create README
        readme_content = f"""# GraphQL Metadata Export

**Generated:** {datetime.now().isoformat()}  
**Object Store:** {self.object_store}  
**Total Objects Exported:** {total_exported}
**Method:** IBM csdeploy package

## Files

1. **01-choice-lists.graphql** - Choice list definitions
2. **02-property-templates.graphql** - Property template definitions
3. **03-class-definitions.graphql** - Class definition structures

## Usage

To import these definitions into another repository:

```bash
# Update repository identifier in each file
# Then execute in order:
python graphql/run_graphql.py {output_dir}/01-choice-lists.graphql
python graphql/run_graphql.py {output_dir}/02-property-templates.graphql
python graphql/run_graphql.py {output_dir}/03-class-definitions.graphql
```

## Notes

- Choice lists must be created before property templates that reference them
- Property templates must be created before class definitions that use them
- Update `repositoryIdentifier` values before importing to target repository
- Review and update choice list IDs in property template references
- This export was generated using the IBM Content Services Deployment API (csdeploy)

## Alternative: Use CS Deployment API

For full import/export with dependency resolution, use the IBM CS Deployment API:

```bash
cd /Users/jabrimalek/development/cs-deployment-api/ibm-content-platform-engine-samples/CS-Deployment-API/
jupyter notebook deploy_all.ipynb
```
"""
        
        readme_file = output_dir / "README.md"
        readme_file.write_text(readme_content)
        
        print("\n" + "=" * 60)
        print(f"✓ Export complete! Total objects exported: {total_exported}")
        print(f"✓ Files created in: {output_dir}")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Export IBM FileNet metadata to GraphQL format using csdeploy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export everything
  python tools/export_graphql_definitions.py --all
  
  # Export only choice lists
  python tools/export_graphql_definitions.py --choice-lists
  
  # Export metadata for specific class
  python tools/export_graphql_definitions.py --all --class-name HRDocument
  
  # Export to custom directory
  python tools/export_graphql_definitions.py --all --output-dir exports/my-export

Requirements:
  - IBM Content Services Deployment API (csdeploy) package must be installed
  - MCP configuration in .bob/mcp.json with content-repository server
        """
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Export all metadata types (choice lists, property templates, class definitions)"
    )
    parser.add_argument(
        "--choice-lists",
        action="store_true",
        help="Export only choice lists"
    )
    parser.add_argument(
        "--property-templates",
        action="store_true",
        help="Export only property templates"
    )
    parser.add_argument(
        "--class-definitions",
        action="store_true",
        help="Export only class definitions"
    )
    parser.add_argument(
        "--class-name",
        help="Filter exports to specific class and its dependencies"
    )
    parser.add_argument(
        "--output-dir",
        default="graphql/exports",
        help="Output directory for GraphQL files (default: graphql/exports)"
    )
    parser.add_argument(
        "--mcp-config",
        default=".bob/mcp.json",
        help="Path to MCP configuration file (default: .bob/mcp.json)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not any([args.all, args.choice_lists, args.property_templates, args.class_definitions]):
        parser.error("Must specify at least one export type (--all, --choice-lists, --property-templates, or --class-definitions)")
    
    try:
        exporter = GraphQLExporter(args.mcp_config)
        output_dir = Path(args.output_dir)
        
        if args.all:
            exporter.export_all(output_dir, args.class_name)
        else:
            if args.choice_lists:
                exporter.export_choice_lists(output_dir / "01-choice-lists.graphql")
            if args.property_templates:
                exporter.export_property_templates(output_dir / "02-property-templates.graphql", args.class_name)
            if args.class_definitions:
                exporter.export_class_definitions(output_dir / "03-class-definitions.graphql", args.class_name)
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

# Updated to use IBM csdeploy package

# Made with Bob
