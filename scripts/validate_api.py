#!/usr/bin/env python3
"""Validate that code matches API specification."""

import json
import inspect
import sys
from pathlib import Path


def load_spec():
    """Load API specification."""
    spec_path = Path(__file__).parent.parent / 'api_spec.json'
    with open(spec_path, encoding='utf-8') as f:
        return json.load(f)


def validate_base_client(spec):
    """Validate BaseClient matches spec."""
    print("\nנ” Validating BaseClient...")
    errors = []
    
    try:
        # Import BaseClient
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from whatsfuse.core.base_client import BaseClient
        
        for method_name, method_spec in spec['methods'].items():
            # Check method exists
            if not hasattr(BaseClient, method_name):
                errors.append(f"ג Missing method: {method_name} in BaseClient")
                continue
            
            # Get method signature
            method = getattr(BaseClient, method_name)
            sig = inspect.signature(method)
            
            # Expected parameters (excluding self and kwargs)
            spec_params = {p['name'] for p in method_spec['parameters']}
            actual_params = {name for name in sig.parameters.keys() 
                           if name not in ('self', 'kwargs')}
            
            # Check parameters match
            if spec_params != actual_params:
                missing = spec_params - actual_params
                extra = actual_params - spec_params
                
                error_msg = f"ג {method_name}: Parameter mismatch"
                if missing:
                    error_msg += f"\n   Missing: {missing}"
                if extra:
                    error_msg += f"\n   Extra: {extra}"
                errors.append(error_msg)
            else:
                print(f"   ג… {method_name}: OK")
        
    except Exception as e:
        errors.append(f"ג Error validating BaseClient: {e}")
    
    return errors


def validate_whatsfuse(spec):
    """Validate WhatsFuse main class matches spec."""
    print("\nנ” Validating WhatsFuse...")
    errors = []
    
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from whatsfuse.main import WhatsFuse
        
        for method_name, method_spec in spec['methods'].items():
            if not hasattr(WhatsFuse, method_name):
                errors.append(f"ג Missing method: {method_name} in WhatsFuse")
                continue
            
            method = getattr(WhatsFuse, method_name)
            sig = inspect.signature(method)
            
            spec_params = {p['name'] for p in method_spec['parameters']}
            actual_params = {name for name in sig.parameters.keys() 
                           if name not in ('self', 'kwargs')}
            
            if spec_params != actual_params:
                missing = spec_params - actual_params
                extra = actual_params - spec_params
                
                error_msg = f"ג {method_name}: Parameter mismatch"
                if missing:
                    error_msg += f"\n   Missing: {missing}"
                if extra:
                    error_msg += f"\n   Extra: {extra}"
                errors.append(error_msg)
            else:
                print(f"   ג… {method_name}: OK")
        
    except Exception as e:
        errors.append(f"ג Error validating WhatsFuse: {e}")
    
    return errors


def validate_providers(spec):
    """Validate provider implementations match spec."""
    print("\nנ” Validating Providers...")
    errors = []
    
    providers = [
        ('WAHA', 'whatsfuse.providers.waha.client', 'WAHAClient'),
        ('Green API', 'whatsfuse.providers.green_api.client', 'GreenAPIClient')
    ]
    
    for provider_name, module_path, class_name in providers:
        try:
            module = __import__(module_path, fromlist=[class_name])
            provider_class = getattr(module, class_name)
            
            print(f"\n   Checking {provider_name}...")
            
            for method_name, method_spec in spec['methods'].items():
                if not hasattr(provider_class, method_name):
                    errors.append(f"ג {provider_name}: Missing method {method_name}")
                    continue
                
                method = getattr(provider_class, method_name)
                sig = inspect.signature(method)
                
                spec_params = {p['name'] for p in method_spec['parameters']}
                actual_params = {name for name in sig.parameters.keys() 
                               if name not in ('self', 'kwargs')}
                
                if spec_params != actual_params:
                    missing = spec_params - actual_params
                    extra = actual_params - spec_params
                    
                    error_msg = f"ג {provider_name}.{method_name}: Parameter mismatch"
                    if missing:
                        error_msg += f"\n      Missing: {missing}"
                    if extra:
                        error_msg += f"\n      Extra: {extra}"
                    errors.append(error_msg)
                else:
                    print(f"      ג… {method_name}: OK")
            
        except Exception as e:
            errors.append(f"ג Error validating {provider_name}: {e}")
    
    return errors


def main():
    """Main validation function."""
    print("=" * 60)
    print("נ” WhatsFuse API Validation")
    print("=" * 60)
    
    try:
        spec = load_spec()
        print(f"\nנ“‹ Loaded spec version {spec['version']}")
        print(f"נ“ Validating {len(spec['methods'])} methods...")
        
        all_errors = []
        
        # Validate BaseClient
        all_errors.extend(validate_base_client(spec))
        
        # Validate WhatsFuse
        all_errors.extend(validate_whatsfuse(spec))
        
        # Validate Providers
        all_errors.extend(validate_providers(spec))
        
        print("\n" + "=" * 60)
        
        if all_errors:
            print("ג VALIDATION FAILED\n")
            for error in all_errors:
                print(error)
            print("\n" + "=" * 60)
            sys.exit(1)
        else:
            print("ג… ALL VALIDATIONS PASSED!")
            print("=" * 60)
            sys.exit(0)
            
    except Exception as e:
        print(f"\nג Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
