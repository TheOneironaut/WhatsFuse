# WhatsFuse Automation Scripts

This directory contains automation tools for maintaining WhatsFuse's unified API.

## Scripts

### 1. generate_docs.py
**Purpose**: Automatically generate documentation from API specification

**Usage**:
```bash
python scripts/generate_docs.py
```

**Output**: `docs/FEATURE_MATRIX.md`

**When to use**:
- After updating `api_spec.json`
- Before committing changes
- To ensure docs are up-to-date

---

### 2. validate_api.py
**Purpose**: Validate that code matches the API specification

**Usage**:
```bash
python scripts/validate_api.py
```

**What it checks**:
- BaseClient has all methods from spec
- WhatsFuse has all methods from spec
- All providers have all methods from spec
- All parameters match exactly

**When to use**:
- Before committing code
- In CI/CD pipeline
- After adding new parameters
- After modifying method signatures

---

## Workflow

### Adding a New Parameter

1. **Edit api_spec.json**
   ```json
   {
     "name": "new_param",
     "type": "Optional[str]",
     "required": false,
     "default": null,
     "description": "Description of parameter",
     "waha": {"support": "full", "name": "wahaParamName"},
     "green_api": {"support": "full", "name": "greenApiParamName"}
   }
   ```

2. **Update code** (BaseClient, WhatsFuse, Providers)

3. **Validate**
   ```bash
   python scripts/validate_api.py
   ```

4. **Generate docs**
   ```bash
   python scripts/generate_docs.py
   ```

5. **Commit**
   ```bash
   git add api_spec.json docs/FEATURE_MATRIX.md whatsfuse/
   git commit -m "feat: add new_param parameter"
   ```

---

### Adding a New Method

1. **Add to api_spec.json**
   ```json
   "new_method": {
     "category": "messaging",
     "description": "Method description",
     "status": "in_progress",
     "returns": "ReturnType",
     "parameters": [...]
   }
   ```

2. **Implement in BaseClient**

3. **Implement in WhatsFuse**

4. **Implement in all providers**

5. **Validate & generate docs**
   ```bash
   python scripts/validate_api.py
   python scripts/generate_docs.py
   ```

---

## CI/CD Integration

Add to your CI pipeline (`.github/workflows/test.yml`):

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -e .
      
      - name: Validate API
        run: python scripts/validate_api.py
      
      - name: Check docs are up to date
        run: |
          python scripts/generate_docs.py
          git diff --exit-code docs/FEATURE_MATRIX.md
```

---

## Files

- `api_spec.json` - Single source of truth for API
- `generate_docs.py` - Documentation generator
- `validate_api.py` - API validator
- `README.md` - This file

---

## Benefits

ג… **Single source of truth** - api_spec.json  
ג… **Always up-to-date docs** - Generated automatically  
ג… **Consistency guaranteed** - Validation catches errors  
ג… **Easy to maintain** - One place to update  
ג… **Version controlled** - Track changes in git

---

For more information, see:
- [PARAMETER_MAPPING.md](../docs/PARAMETER_MAPPING.md)
- [UNIFIED_INTERFACE_UPDATE.md](../UNIFIED_INTERFACE_UPDATE.md)