"""Direct stdio MCP server for echovault - no TCP needed."""

import sys
import os

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Set up paths
base_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(base_dir, 'src')
venv_packages = os.path.join(base_dir, '.venv', 'Lib', 'site-packages')
pywin32_path = os.path.join(venv_packages, 'pywin32_system32')

# Add to sys.path
sys.path.insert(0, src_path)
sys.path.insert(0, venv_packages)

# Add pywin32 to PATH
if pywin32_path not in os.environ.get('PATH', ''):
    os.environ['PATH'] = pywin32_path + os.pathsep + os.environ.get('PATH', '')

# Suppress warnings
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['PYTHONWARNINGS'] = 'ignore'

# Set default MEMORY_HOME
if 'MEMORY_HOME' not in os.environ:
    os.environ['MEMORY_HOME'] = r'C:\Git\.memory'

# Run MCP server
import asyncio
from memory.mcp_server import run_server

if __name__ == '__main__':
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
