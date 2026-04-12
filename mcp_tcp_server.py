"""TCP MCP server for echovault."""

import asyncio
import json
import os
import sys
from pathlib import Path

# Set up paths
base_dir = Path(__file__).parent
sys.path.insert(0, str(base_dir / "src"))

# Set MEMORY_HOME if not set
if "MEMORY_HOME" not in os.environ:
    os.environ["MEMORY_HOME"] = r"C:\Git\.memory"

from memory.core import MemoryService
from memory.mcp_server import _create_server
from mcp.server import Server

# TCP server settings
HOST = "127.0.0.1"
PORT = 8767


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, server: Server):
    """Handle a single client connection."""
    buffer = b""
    
    while True:
        try:
            # Read data
            chunk = await reader.read(4096)
            if not chunk:
                break
            
            buffer += chunk
            
            # Process complete messages
            while True:
                # Find Content-Length header
                header_end = buffer.find(b'\r\n\r\n')
                if header_end == -1:
                    break
                
                header = buffer[:header_end].decode('utf-8')
                body_start = header_end + 4
                
                # Parse Content-Length
                content_length = 0
                for line in header.split('\r\n'):
                    if line.lower().startswith('content-length:'):
                        content_length = int(line.split(':')[1].strip())
                        break
                
                # Wait for full body
                if len(buffer) < body_start + content_length:
                    break
                
                # Extract and parse body
                body = buffer[body_start:body_start + content_length]
                buffer = buffer[body_start + content_length:]
                
                try:
                    msg = json.loads(body.decode('utf-8'))
                except json.JSONDecodeError:
                    continue
                
                # Handle the message through MCP server
                method = msg.get('method', '')
                msg_id = msg.get('id')
                
                if method == 'initialize':
                    response = {
                        'jsonrpc': '2.0',
                        'id': msg_id,
                        'result': {
                            'protocolVersion': '2024-11-05',
                            'capabilities': {},
                            'serverInfo': {'name': 'echovault', 'version': '0.4.0'}
                        }
                    }
                elif method == 'tools/list':
                    # Get tools from server
                    from mcp.types import ListToolsRequest
                    handler = server.request_handlers.get(ListToolsRequest)
                    if handler:
                        result = await handler(msg.get('params', {}))
                        tools_data = []
                        for tool in result.root.tools:
                            tools_data.append({
                                'name': tool.name,
                                'description': tool.description,
                                'inputSchema': tool.inputSchema
                            })
                        response = {
                            'jsonrpc': '2.0',
                            'id': msg_id,
                            'result': {'tools': tools_data}
                        }
                    else:
                        response = {
                            'jsonrpc': '2.0',
                            'id': msg_id,
                            'error': {'code': -32601, 'message': 'Method not found'}
                        }
                elif method == 'tools/call':
                    # Call tool through server
                    from mcp.types import CallToolRequest
                    handler = server.request_handlers.get(CallToolRequest)
                    if handler:
                        result = await handler(msg.get('params', {}))
                        content = []
                        for item in result.root.content:
                            content.append({
                                'type': item.type,
                                'text': item.text
                            })
                        response = {
                            'jsonrpc': '2.0',
                            'id': msg_id,
                            'result': {'content': content}
                        }
                    else:
                        response = {
                            'jsonrpc': '2.0',
                            'id': msg_id,
                            'error': {'code': -32601, 'message': 'Method not found'}
                        }
                else:
                    response = {
                        'jsonrpc': '2.0',
                        'id': msg_id,
                        'error': {'code': -32601, 'message': f'Method not found: {method}'}
                    }
                
                # Send response
                resp_json = json.dumps(response)
                output = f'Content-Length: {len(resp_json)}\r\n\r\n{resp_json}'
                writer.write(output.encode('utf-8'))
                await writer.drain()
                
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error handling client: {e}", file=sys.stderr)
            break
    
    writer.close()
    await writer.wait_closed()


async def main():
    """Run TCP MCP server."""
    # Initialize memory service
    service = MemoryService()
    
    # Create MCP server
    server = _create_server(service)
    
    # Start TCP server
    srv = await asyncio.start_server(
        lambda r, w: handle_client(r, w, server),
        HOST, PORT
    )
    
    print(f"MCP TCP Server running on {HOST}:{PORT}", file=sys.stderr)
    
    async with srv:
        try:
            await srv.serve_forever()
        except asyncio.CancelledError:
            pass
    
    service.close()
    print("MCP TCP Server stopped", file=sys.stderr)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
