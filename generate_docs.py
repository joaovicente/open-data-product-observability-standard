import json
import os
import re
import yaml

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema", "odps-observability-json-schema-v0.1.0.json")
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

def flatten_properties(properties, required_list, root_schema, prefix=""):
    rows = []
    for name, prop in properties.items():
        if "$ref" in prop and root_schema:
            resolved = resolve_ref(prop["$ref"], root_schema)
            new_prop = resolved.copy()
            new_prop.update(prop)
            prop = new_prop
            
        full_key = f"{prefix}{name}"
        req_str = "Yes" if name in required_list else "No"
        desc = prop.get("description", "").replace("\n", " ").replace("|", "\\|")
        
        # Determine ux label
        ux_label = name
        ux_label = re.sub('([a-z0-9])([A-Z])', r'\1 \2', ux_label).title()
        
        # Determine example
        ex_val = ""
        if "examples" in prop and prop["examples"]:
            ex_val = str(prop["examples"][0])
        elif "enum" in prop:
            ex_val = str(prop["enum"][0])
        
        if ex_val:
            ex_val = f"`{ex_val}`"
            
        if "items" in prop and "properties" in prop["items"]:
            # Array of objects
            desc = f"Array of objects. {desc}"
            rows.append((full_key + "[]", ux_label, req_str, desc, ex_val))
            sub_req = prop["items"].get("required", [])
            rows.extend(flatten_properties(prop["items"]["properties"], sub_req, root_schema, full_key + "[]."))
        elif "properties" in prop:
            # Object
            desc = f"Object. {desc}"
            rows.append((full_key, ux_label, req_str, desc, ex_val))
            sub_req = prop.get("required", [])
            rows.extend(flatten_properties(prop["properties"], sub_req, root_schema, full_key + "."))
        else:
            rows.append((full_key, ux_label, req_str, desc, ex_val))
            
    return rows

groups = {
    "Fundamentals": ["schemaVersion", "kind", "productId", "asOf", "period", "status"],
    "Physical Metrics": ["physical"],
    "Static Metrics": ["static"],
    "Dynamic Metrics": ["dynamic", "slo"],
    "Output Ports": ["outputPorts"],
    "Lineage": ["lineage"],
    "Usage": ["usage", "contractUsage"],
    "Custom Properties": ["customProperties"]
}

full_example = schema.get("examples", [{}])[0]

def get_example_subset(keys, full_ex):
    sub = {}
    for k in keys:
        if k in full_ex:
            sub[k] = full_ex[k]
    return sub

readme = f"""# Data Product Observability Standard

## Executive Summary

{schema.get('description', '')}

## Schema Details

**Schema Version:** `0.1.0`
**Schema File:** [`../schema/odps-observability-json-schema-v0.1.0.json`](../schema/odps-observability-json-schema-v0.1.0.json)
**Schema ID:** `{schema.get('$id', '')}`

"""

all_props = schema.get("properties", {})
root_req = schema.get("required", [])

for group_name, keys in groups.items():
    readme += f"## {group_name}\n\n"
    
    ex_sub = get_example_subset(keys, full_example)
    if ex_sub:
        readme += f"### Example\n\n```yaml\n"
        readme += yaml.dump(ex_sub, sort_keys=False, default_flow_style=False)
        readme += "```\n\n"
        
    readme += "### Field Descriptions\n\n"
    readme += "| Key | UX label | Required | Description | Example |\n"
    readme += "|---|---|---|---|---|\n"
    
    group_props = {k: all_props[k] for k in keys if k in all_props}
    rows = flatten_properties(group_props, root_req, schema)
    for r in rows:
        key, ux, req, desc, ex = r
        readme += f"| `{key}` | {ux} | {req} | {desc} | {ex} |\n"
    
    readme += "\n"

with open(os.path.join(DOCS_DIR, "README.md"), "w") as f:
    f.write(readme)

print("Docs generated with new layout successfully.")

examples = schema.get("examples", [])
if examples:
    ex_md = "# Examples\n\n"
    for i, ex in enumerate(examples):
        ex_md += f"## Example {i+1}\n\n```yaml\n{yaml.dump(ex, sort_keys=False, default_flow_style=False)}\n```\n\n"
    with open(os.path.join(EXAMPLES_DIR, "README.md"), "w") as f:
        f.write(ex_md)

