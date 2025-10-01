# WhatsFuse Automation Scripts

Automation tools for maintaining WhatsFuse's unified API.

## Scripts

### `validate_api.py`
Validates that code matches the API specification.

```bash
python scripts/validate_api.py
```

**Checks:**
- BaseClient has all methods from `api_spec.json`
- WhatsFuse has all methods from `api_spec.json`
- All providers have all methods
- All parameters match exactly

### `generate_docs.py`
Automatically generates documentation from API specification.

```bash
python scripts/generate_docs.py
```

**Generates:** `docs/FEATURE_MATRIX.md`

## Workflow

When adding new methods or parameters:

1. Edit `api_spec.json`
2. Update code (BaseClient, WhatsFuse, Providers)
3. Run `python scripts/validate_api.py`
4. Run `python scripts/generate_docs.py`
5. Commit all changes

See [Automation System](../docs/development/automation-system.md) for details.

