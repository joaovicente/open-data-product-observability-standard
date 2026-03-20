import json
import os

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema", "odps-observability-json-schema-v0.0.1.json")
DOCS_DIR = r"c:\Users\Joao\code\open-data-product-observability-standard\docs"
EXAMPLES_DIR = os.path.join(DOCS_DIR, "examples")

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(EXAMPLES_DIR, exist_ok=True)

with open(SCHEMA_PATH, "r") as f:
    schema = json.load(f)

def resolve_ref(ref_str, root_schema):
    parts = ref_str.lstrip("#/").split("/")
    curr = root_schema
    for p in parts:
        curr = curr.get(p, {})
    return curr

def get_type_str(prop, root_schema=None):
    if "$ref" in prop and root_schema:
        prop = resolve_ref(prop["$ref"], root_schema)
    if "type" in prop:
        t = prop["type"]
        if isinstance(t, list):
            return " | ".join(t)
        return t
    return "any"

def get_req_str(name, required_list):
    return "**Required**" if name in required_list else "Optional"

def render_properties(properties, required_list, level=2, root_schema=None):
    md = ""
    for name, prop in properties.items():
        if "$ref" in prop and root_schema:
            resolved = resolve_ref(prop["$ref"], root_schema)
            new_prop = resolved.copy()
            new_prop.update(prop)
            prop = new_prop
            
        type_str = get_type_str(prop, root_schema)
        req_str = get_req_str(name, required_list)
        desc = prop.get("description", "")
        
        md += f"{'#' * level} `{name}`\n\n"
        md += f"**Type:** `{type_str}` | {req_str}\n\n"
        if desc:
            md += f"{desc}\n\n"
        
        if "enum" in prop:
            md += "**Allowed Values:**\n"
            for e in prop["enum"]:
                md += f"- `{e}`\n"
            md += "\n"
            
        if "examples" in prop:
            md += "**Examples:**\n"
            for e in prop["examples"]:
                md += f"- `{e}`\n"
            md += "\n"
            
        if "pattern" in prop:
            md += f"**Pattern:** `{prop['pattern']}`\n\n"
        
        if "items" in prop and "properties" in prop["items"]:
            md += f"This is an array of objects with the following properties:\n\n"
            item_req = prop["items"].get("required", [])
            md += render_properties(prop["items"]["properties"], item_req, level + 1, root_schema)
        elif "properties" in prop:
            md += render_properties(prop["properties"], prop.get("required", []), level + 1, root_schema)
            
    return md

readme = f"""# Data Product Observability Standard

## Executive Summary

{schema.get('description', '')}

## Schema Details

**Schema Version:** `0.0.1`
**Schema File:** [`../schema/odps-observability-json-schema-v0.0.1.json`](../schema/odps-observability-json-schema-v0.0.1.json)
**Schema ID:** `{schema.get('$id', '')}`

## Properties

"""

readme += render_properties(schema.get("properties", {}), schema.get("required", []), 3, schema)

with open(os.path.join(DOCS_DIR, "README.md"), "w") as f:
    f.write(readme)

examples = schema.get("examples", [])
if examples:
    ex_md = "# Examples\n\n"
    for i, ex in enumerate(examples):
        ex_md += f"## Example {i+1}\n\n```json\n{json.dumps(ex, indent=2)}\n```\n\n"
        
    with open(os.path.join(EXAMPLES_DIR, "README.md"), "w") as f:
        f.write(ex_md)
else:
    with open(os.path.join(EXAMPLES_DIR, "README.md"), "w") as f:
        f.write("# Examples\n\nNo examples provided in the schema.\n")

print("Generated docs successfully.")
