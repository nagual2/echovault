"""Bridge between stdio and TCP for MCP server."""

import asyncio
import sys
import os

# TCP server settings
HOST = "127.0.0.1"
PORT = 8767


async def forward_stdin_to_tcp(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """Forward data from stdin to TCP server."""
    try:
        while True:
            # Read from stdin
            data = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.buffer.read, 4096)
            if not data:
                break
            
            # Write to TCP
            writer.write(data)
            await writer.drain()
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"Error forwarding stdin->tcp: {e}", file=sys.stderr)


async def forward_tcp_to_stdout(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """Forward data from TCP server to stdout."""
    try:
        while True:
            # Read from TCP
            data = await reader.read(4096)
            if not data:
                break
            
            # Write to stdout
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"Error forwarding tcp->stdout: {e}", file=sys.stderr)


async def main():
    """Run the bridge."""
    try:
        # Connect to TCP server
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(HOST, PORT),
            timeout=10.0
        )
    except asyncio.TimeoutError:
        print(f"Failed to connect to TCP server at {HOST}:{PORT}", file=sys.stderr)
        sys.exit(1)
    except ConnectionRefusedError:
        print(f"Connection refused to TCP server at {HOST}:{PORT}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error connecting to TCP server: {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Start bidirectional forwarding
        stdin_task = asyncio.create_task(forward_stdin_to_tcp(reader, writer))
        tcp_task = asyncio.create_task(forward_tcp_to_stdout(reader, writer))
        
        # Wait for either task to complete
        done, pending = await asyncio.wait(
            [stdin_task, tcp_task],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # Cancel remaining tasks
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"Bridge error: {e}", file=sys.stderr)
    finally:
        writer.close()
        await writer.wait_closed()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
