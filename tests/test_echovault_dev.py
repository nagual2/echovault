#!/usr/bin/env python3
"""
EchoVault-DEV MCP Server Test Suite
Tests all methods of echovault-dev MCP server

Usage:
    python test_echovault_dev.py [options]

Options:
    --verbose        Enable verbose output
"""

import sys
import os

# Setup paths - adjust as needed for your installation
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
os.environ.setdefault('MEMORY_HOME', os.path.expanduser('~/.memory.dev'))

import asyncio
import json
from memory.core import MemoryService


async def test_all_methods():
    """Test all echovault-dev methods directly"""
    print("=" * 60)
    print("EchoVault-DEV MCP Server Test Suite")
    print("=" * 60)
    
    service = MemoryService()
    results = {}
    
    # Test 1: memory_save
    print("\n[1/9] Testing memory_save...")
    try:
        from memory.mcp_server import handle_memory_save
        result = handle_memory_save(
            service,
            title="[TEST] Echovault Dev Test Entry",
            what="Testing echovault-dev MCP server save functionality",
            category="test",
            tags=["test", "echovault-dev"],
            project="test-project"
        )
        data = json.loads(result)
        print(f"  [OK] Saved: {data.get('id', 'N/A')[:8]}...")
        results['memory_save'] = 'PASS'
    except Exception as e:
        print(f"  [ER] {e}")
        results['memory_save'] = 'FAIL'
    
    # Test 2: memory_search
    print("\n[2/9] Testing memory_search...")
    try:
        from memory.mcp_server import handle_memory_search
        result = handle_memory_search(service, query="test", limit=3)
        data = json.loads(result)
        print(f"  [OK] Found {len(data)} results")
        results['memory_search'] = 'PASS'
    except Exception as e:
        print(f"  [ER] {e}")
        results['memory_search'] = 'FAIL'
    
    # Test 3: memory_context
    print("\n[3/9] Testing memory_context...")
    try:
        from memory.mcp_server import handle_memory_context
        result = handle_memory_context(service, limit=5)
        data = json.loads(result)
        count = len(data.get('memories', [])) if isinstance(data, dict) else len(data)
        print(f"  [OK] Got {count} context entries")
        results['memory_context'] = 'PASS'
    except Exception as e:
        print(f"  [ER] {e}")
        results['memory_context'] = 'FAIL'
    
    # Test 4: memory_record_usage
    print("\n[4/9] Testing memory_record_usage...")
    try:
        from memory.mcp_server import handle_memory_record_usage
        result = handle_memory_record_usage(service, memory_id="test-id-123", usage_type="main")
        print(f"  [OK] Recorded usage")
        results['memory_record_usage'] = 'PASS'
    except Exception as e:
        print(f"  [ER] {e}")
        results['memory_record_usage'] = 'FAIL'
    
    # Test 5: memory_governor
    print("\n[5/9] Testing memory_governor...")
    try:
        from memory.mcp_server import handle_memory_governor
        result = handle_memory_governor(service)
        data = json.loads(result)
        print(f"  [OK] Governor returned {len(data.get('actions', []))} actions")
        results['memory_governor'] = 'PASS'
    except Exception as e:
        print(f"  [ER] {e}")
        results['memory_governor'] = 'FAIL'
    
    # Test 6: memory_rollback_status
    print("\n[6/9] Testing memory_rollback_status...")
    try:
        from memory.rollback import RollbackManager
        mgr = RollbackManager(memory_home=service.memory_home)
        result = mgr.get_status()
        print(f"  [OK] Rollback status: {result.get('enabled', 'N/A')}")
        results['memory_rollback_status'] = 'PASS'
    except Exception as e:
        print(f"  [ER] {e}")
        results['memory_rollback_status'] = 'FAIL'
    
    # Test 7: memory_rollback_enable
    print("\n[7/9] Testing memory_rollback_enable (shadow mode)...")
    try:
        from memory.rollback import enable_shadow_mode
        enable_shadow_mode(service.memory_home)
        print(f"  [OK] Shadow mode enabled")
        results['memory_rollback_enable'] = 'PASS'
    except Exception as e:
        print(f"  [ER] {e}")
        results['memory_rollback_enable'] = 'FAIL'
    
    # Test 8: memory_unified_search
    print("\n[8/9] Testing memory_unified_search...")
    try:
        from memory.mcp_server import _get_unified_service
        unified = _get_unified_service(service.memory_home)
        entries = unified.search_sync(query="test", limit=3)
        print(f"  [OK] Unified search: {len(entries)} entries")
        results['memory_unified_search'] = 'PASS'
    except Exception as e:
        print(f"  [ER] {e}")
        results['memory_unified_search'] = 'FAIL'
    
    # Test 9: memory_unified_context
    print("\n[9/9] Testing memory_unified_context...")
    try:
        entries = unified.get_context(limit=5)
        print(f"  [OK] Unified context: {len(entries)} entries")
        results['memory_unified_context'] = 'PASS'
    except Exception as e:
        print(f"  [ER] {e}")
        results['memory_unified_context'] = 'FAIL'
    
    service.close()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(1 for v in results.values() if v == 'PASS')
    failed = sum(1 for v in results.values() if v == 'FAIL')
    
    for method, status in results.items():
        icon = "[OK]" if status == 'PASS' else "[ER]"
        print(f"  {icon} {method}")
    
    print(f"\n  Total: {len(results)}, Passed: {passed}, Failed: {failed}")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(test_all_methods())
    sys.exit(0 if success else 1)
