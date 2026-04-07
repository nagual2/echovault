"""TCP MCP Server for echovault - reliable transport for Windows."""

import asyncio
import json
import sys
import os

# Setup paths
os.environ['MEMORY_HOME'] = r'C:\Git\.memory'
sys.path.insert(0, r'c:\Git\MCP\echovault\src')

from memory.core import MemoryService
from memory.mcp_server import _create_server
from mcp.types import ListToolsRequest, CallToolRequest

HOST = "127.0.0.1"
PORT = 8767


class MCPTCPServer:
    def __init__(self):
        self.service = MemoryService()
        self.server = _create_server(self.service)
        print(f"echovault TCP server ready on {HOST}:{PORT}", file=sys.stderr)
    
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle single MCP client connection."""
        buffer = b""
        
        while True:
            try:
                # Read data
                data = await reader.read(4096)
                if not data:
                    break
                
                buffer += data
                
                # Process complete messages
                while True:
                    header_end = buffer.find(b'\r\n\r\n')
                    if header_end == -1:
                        break
                    
                    header = buffer[:header_end].decode('utf-8')
                    body_start = header_end + 4
                    
                    # Get content length
                    content_length = 0
                    for line in header.split('\r\n'):
                        if line.lower().startswith('content-length:'):
                            try:
                                content_length = int(line.split(':')[1].strip())
                            except:
                                pass
                            break
                    
                    # Check full message received
                    if len(buffer) < body_start + content_length:
                        break
                    
                    # Extract and process body
                    body = buffer[body_start:body_start + content_length]
                    buffer = buffer[body_start + content_length:]
                    
                    await self.process_message(body, writer)
                    
            except Exception as e:
                print(f"Client error: {e}", file=sys.stderr)
                break
        
        writer.close()
        await writer.wait_closed()
    
    async def process_message(self, body: bytes, writer: asyncio.StreamWriter):
        """Process single MCP message."""
        try:
            msg = json.loads(body.decode('utf-8'))
            method = msg.get('method')
            msg_id = msg.get('id')
            
            response = None
            
            # Handle initialize
            if method == 'initialize':
                response = {
                    'jsonrpc': '2.0',
                    'id': msg_id,
                    'result': {
                        'protocolVersion': '2024-11-05',
                        'capabilities': {'tools': {'listChanged': False}},
                        'serverInfo': {'name': 'echovault', 'version': '1.27.0'}
                    }
                }
            
            # Handle tools/list
            elif method == 'tools/list':
                handler = self.server.request_handlers[ListToolsRequest]
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
            
            # Handle tools/call
            elif method == 'tools/call':
                handler = self.server.request_handlers[CallToolRequest]
                result = await handler(msg.get('params', {}))
                response = {
                    'jsonrpc': '2.0',
                    'id': msg_id,
                    'result': result
                }
            
            # Send response
            if response:
                resp_json = json.dumps(response)
                output = f'Content-Length: {len(resp_json)}\r\n\r\n{resp_json}'.encode()
                writer.write(output)
                await writer.drain()
                
        except Exception as e:
            # Send error
            error = {
                'jsonrpc': '2.0',
                'id': msg.get('id') if isinstance(msg, dict) else None,
                'error': {'code': -32603, 'message': str(e)}
            }
            err_json = json.dumps(error)
            output = f'Content-Length: {len(err_json)}\r\n\r\n{err_json}'.encode()
            writer.write(output)
            await writer.drain()
    
    async def run(self):
        """Run TCP server."""
        srv = await asyncio.start_server(
            self.handle_client,
            HOST,
            PORT
        )
        
        async with srv:
            print(f"Server listening on {HOST}:{PORT}", file=sys.stderr)
            await srv.serve_forever()


if __name__ == '__main__':
    server = MCPTCPServer()
    asyncio.run(server.run())
