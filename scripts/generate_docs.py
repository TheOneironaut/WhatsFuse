#!/usr/bin/env python3
"""Generate documentation automatically from API spec."""

import json
from pathlib import Path
from datetime import datetime


def load_spec():
    """Load API specification."""
    spec_path = Path(__file__).parent.parent / 'api_spec.json'
    with open(spec_path, encoding='utf-8') as f:
        return json.load(f)


def status_emoji(status):
    """Get emoji for status."""
    return {
        'complete': 'ג…',
        'in_progress': 'נ§',
        'planned': 'נ“‹',
        'deprecated': 'ג ן¸'
    }.get(status, 'ג“')


def support_emoji(support):
    """Get emoji for support level."""
    return {
        'full': 'ג…',
        'partial': 'ג ן¸',
        'none': 'ג',
        'planned': 'נ“‹'
    }.get(support, 'ג“')


def generate_method_table(method_name, method_spec):
    """Generate parameter table for a method."""
    md = f"### {method_name}()\n\n"
    md += f"**Status**: {status_emoji(method_spec['status'])} {method_spec['status'].replace('_', ' ').title()}\n\n"
    md += f"**Purpose**: {method_spec['description']}\n\n"
    md += f"**Returns**: `{method_spec['returns']}`\n\n"
    
    # Parameters table
    md += "#### Parameters\n\n"
    md += "| Parameter | Type | Required | Default | WAHA | Green API | Description |\n"
    md += "|-----------|------|----------|---------|------|-----------|-------------|\n"
    
    for param in method_spec['parameters']:
        required = "ג… Yes" if param['required'] else "ג No"
        default = f"`{param.get('default', '-')}`" if not param['required'] else "-"
        waha_support = support_emoji(param['waha']['support'])
        green_support = support_emoji(param['green_api']['support'])
        
        md += f"| `{param['name']}` | `{param['type']}` | {required} | {default} | "
        md += f"{waha_support} | {green_support} | {param['description']} |\n"
    
    md += "\n"
    
    # Provider mapping details
    md += "#### Provider Mapping\n\n"
    
    # WAHA
    md += "**WAHA Provider:**\n```python\n{\n"
    for param in method_spec['parameters']:
        if param['required'] or param.get('default') is not None:
            waha_name = param['waha']['name']
            md += f'    "{waha_name}": {param["name"]}'
            if 'notes' in param['waha']:
                md += f"  # {param['waha']['notes']}"
            md += ",\n"
    md += "}\n```\n"
    md += f"**Support**: {support_emoji('full')} "
    partial_params = [p for p in method_spec['parameters'] if p['waha']['support'] == 'partial']
    if partial_params:
        md += f"Most features, ג ן¸ {', '.join(p['name'] for p in partial_params)} partial\n\n"
    else:
        md += "All features fully supported\n\n"
    
    # Green API
    md += "**Green API Provider:**\n```python\n{\n"
    for param in method_spec['parameters']:
        if param['required'] or param.get('default') is not None:
            green_name = param['green_api']['name']
            md += f'    "{green_name}": {param["name"]}'
            if 'notes' in param['green_api']:
                md += f"  # {param['green_api']['notes']}"
            md += ",\n"
    md += "}\n```\n"
    md += f"**Support**: {support_emoji('full')} "
    partial_params = [p for p in method_spec['parameters'] if p['green_api']['support'] == 'partial']
    if partial_params:
        md += f"Most features, ג ן¸ {', '.join(p['name'] for p in partial_params)} partial\n\n"
    else:
        md += "All features fully supported\n\n"
    
    md += "---\n\n"
    return md


def generate_feature_matrix(spec):
    """Generate complete feature matrix documentation."""
    md = "# WhatsFuse Feature Matrix\n\n"
    md += "> **Auto-generated** from `api_spec.json` - Do not edit manually!\n\n"
    md += f"**Version**: {spec['version']}  \n"
    md += f"**Last Updated**: {spec['updated']}  \n"
    md += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    md += "---\n\n"
    
    # Table of contents
    md += "## נ“‹ Table of Contents\n\n"
    for method_name in spec['methods'].keys():
        md += f"- [{method_name}()](#user-content-{method_name.replace('_', '')})\n"
    md += "\n---\n\n"
    
    # Legend
    md += "## נ“ Legend\n\n"
    md += "### Support Status\n"
    md += "- ג… **Fully Supported** - Works as documented\n"
    md += "- ג ן¸ **Partial Support** - Works with limitations\n"
    md += "- נ§ **In Progress** - Currently being implemented\n"
    md += "- ג **Not Supported** - Feature unavailable\n"
    md += "- נ“‹ **Planned** - Scheduled for future\n\n"
    
    md += "---\n\n"
    
    # Group by category
    categories = {}
    for method_name, method_spec in spec['methods'].items():
        category = method_spec.get('category', 'other')
        if category not in categories:
            categories[category] = []
        categories[category].append((method_name, method_spec))
    
    # Generate sections by category
    category_names = {
        'messaging': 'נ“¬ Message Sending',
        'chat': 'נ’¬ Chat Management',
        'contact': 'נ‘¥ Contact Management',
        'session': 'נ” Session Management'
    }
    
    for category, methods in categories.items():
        md += f"## {category_names.get(category, category.title())}\n\n"
        for method_name, method_spec in methods:
            md += generate_method_table(method_name, method_spec)
    
    # Summary table
    md += "## נ“ˆ Summary\n\n"
    md += "### Methods Overview\n\n"
    md += "| Method | Category | Status | WAHA | Green API |\n"
    md += "|--------|----------|--------|------|-----------|\n"
    
    for method_name, method_spec in spec['methods'].items():
        status = status_emoji(method_spec['status'])
        
        # Check overall provider support
        waha_full = all(p['waha']['support'] == 'full' for p in method_spec['parameters'])
        green_full = all(p['green_api']['support'] == 'full' for p in method_spec['parameters'])
        
        waha = support_emoji('full' if waha_full else 'partial')
        green = support_emoji('full' if green_full else 'partial')
        
        md += f"| `{method_name}` | {method_spec['category']} | {status} | {waha} | {green} |\n"
    
    md += "\n---\n\n"
    
    # Footer
    md += "## נ”„ Maintenance\n\n"
    md += "This document is **automatically generated** from `api_spec.json`.\n\n"
    md += "**To update this documentation:**\n"
    md += "1. Edit `api_spec.json`\n"
    md += "2. Run `python scripts/generate_docs.py`\n"
    md += "3. Commit both files\n\n"
    md += "**Do not edit this file manually!**\n\n"
    
    md += "---\n\n"
    md += f"*Generated by WhatsFuse docs generator v{spec['version']}*\n"
    
    return md


def main():
    """Main function."""
    print("נ”„ Loading API specification...")
    spec = load_spec()
    
    print("נ“ Generating feature matrix...")
    docs = generate_feature_matrix(spec)
    
    output_path = Path(__file__).parent.parent / 'docs' / 'FEATURE_MATRIX.md'
    output_path.parent.mkdir(exist_ok=True)
    
    print(f"נ’¾ Writing to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(docs)
    
    print("ג… Documentation generated successfully!")
    print(f"נ“„ Output: {output_path}")


if __name__ == "__main__":
    main()
