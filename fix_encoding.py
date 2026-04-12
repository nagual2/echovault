#!/usr/bin/env python3
"""
Script to check and fix encoding issues in EchoVault memory files.
Converts non-UTF-8 files to UTF-8 encoding.
"""

import os
import sys
from pathlib import Path
from chardet import detect


def detect_encoding(file_path: str) -> tuple[str, float]:
    """Detect file encoding and confidence."""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = detect(raw_data)
    return result.get('encoding', 'unknown'), result.get('confidence', 0.0)


def convert_to_utf8(file_path: str, source_encoding: str) -> bool:
    """Convert file to UTF-8 encoding."""
    try:
        with open(file_path, 'r', encoding=source_encoding, errors='replace') as f:
            content = f.read()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"  Error converting {file_path}: {e}")
        return False


def scan_and_fix_memory_files(memory_home: str = None) -> dict:
    """Scan all memory files and fix encoding issues."""
    if memory_home is None:
        memory_home = os.environ.get('MEMORY_HOME', os.path.expanduser('~/.memory'))
    
    vault_path = Path(memory_home) / 'vault'
    
    if not vault_path.exists():
        print(f"Vault directory not found: {vault_path}")
        return {'scanned': 0, 'fixed': 0, 'errors': 0}
    
    stats = {'scanned': 0, 'fixed': 0, 'errors': 0, 'utf8': 0, 'non_utf8': 0}
    
    print(f"Scanning memory files in: {vault_path}\n")
    
    for md_file in vault_path.rglob('*.md'):
        stats['scanned'] += 1
        rel_path = md_file.relative_to(vault_path)
        
        encoding, confidence = detect_encoding(str(md_file))
        
        if encoding and encoding.lower() in ['utf-8', 'utf8']:
            stats['utf8'] += 1
            print(f"✓ {rel_path}: UTF-8 (confidence: {confidence:.2%})")
        else:
            stats['non_utf8'] += 1
            print(f"⚠ {rel_path}: {encoding} (confidence: {confidence:.2%}) - CONVERTING...")
            
            if convert_to_utf8(str(md_file), encoding or 'latin-1'):
                stats['fixed'] += 1
                print(f"  → Converted to UTF-8")
            else:
                stats['errors'] += 1
    
    return stats


def main():
    """Main entry point."""
    print("=" * 60)
    print("EchoVault Memory Encoding Fixer")
    print("=" * 60)
    
    # Check if chardet is installed
    try:
        import chardet
    except ImportError:
        print("\nError: 'chardet' module not installed.")
        print("Install it with: pip install chardet")
        sys.exit(1)
    
    memory_home = sys.argv[1] if len(sys.argv) > 1 else None
    
    stats = scan_and_fix_memory_files(memory_home)
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  Files scanned: {stats['scanned']}")
    print(f"  Already UTF-8: {stats['utf8']}")
    print(f"  Non-UTF-8: {stats['non_utf8']}")
    print(f"  Fixed: {stats['fixed']}")
    print(f"  Errors: {stats['errors']}")
    print("=" * 60)


if __name__ == '__main__':
    main()
