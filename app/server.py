import asyncio

MAX_CHUNK_SIZE = 1024 # 1 KB read buffer
CRLF = b"\r\n"

async def connection_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    """Manages lifecycle of a TCP connection

    Reads the raw binary streams from the socket buffer and then hands them off to the RESP parser,
    and then routes the resulting commands to an in-memory store. 

    Args:
        reader (asyncio.StreamReader): Async stream reader for incoming bytes.
        writer (asyncio.StreamWriter): Async stream writer for outbound bytes.

    Raises:
        ConnectionResetError: If the socket connection with the client is abruptly terminated.
    """

    addr = writer.get_extra_info("peername")
    print(f"Connection accepted from {addr}")
    try:
        while True:
            # read the chunks from TCP stream
            data = await reader.read(MAX_CHUNK_SIZE)
            if not data:
                break
            # log raw bytes
            print(f"{addr} Raw bytes received: {data!r}")
            writer.write(b"+PONG\r\n")
            await writer.drain()

    except ConnectionResetError:
        pass # client drops connection
    finally:
        print(f"Connection closed from {addr}")
        writer.close()
        await writer.wait_closed()

async def start_server(host="127.0.0.1", port = 6379):
    """Initializes and runs async TCP server.
    
    Args:
        host (str): IP address to bind the server to. Defaults to "127.0.0.1".
        port (int): TCP port to listen on. Defaults to 6379.
    """
    server = await asyncio.start_server(connection_handler, host, port)
    print(f"async engine bound to {host}: {port}")

    async with server:
        await server.serve_forever()