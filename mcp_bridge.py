"""STDIO to TCP bridge for echovault MCP server."""

import sys
import socket
import threading

TCP_HOST = "127.0.0.1"
TCP_PORT = 8767


def forward_stdin_to_tcp(sock):
    """Forward stdin to TCP server."""
    while True:
        try:
            data = sys.stdin.buffer.read(4096)
            if not data:
                break
            sock.sendall(data)
        except:
            break


def forward_tcp_to_stdout(sock):
    """Forward TCP server responses to stdout."""
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()
        except:
            break


def main():
    # Connect to TCP server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_HOST, TCP_PORT))
    
    # Start forwarding threads
    stdin_thread = threading.Thread(target=forward_stdin_to_tcp, args=(sock,), daemon=True)
    stdout_thread = threading.Thread(target=forward_tcp_to_stdout, args=(sock,), daemon=True)
    
    stdin_thread.start()
    stdout_thread.start()
    
    # Wait for threads
    stdin_thread.join()
    stdout_thread.join()


if __name__ == '__main__':
    main()
