#!/usr/bin/env python3
"""Test script to verify create_unified_adapter fix"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now test import
try:
    from memory.unified_adapter import create_unified_adapter
    import inspect
    
    # Check function signature
    sig = inspect.signature(create_unified_adapter)
    params = list(sig.parameters.keys())
    
    print(f"✓ Function found: create_unified_adapter")
    print(f"  Parameters: {params}")
    
    if 'existing' in params:
        print(f"✓ SUCCESS: 'existing' parameter is present")
    else:
        print(f"✗ FAIL: 'existing' parameter is MISSING")
        
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
