import asyncio
from app.protocol import (
    parse_response,
    serialize_simple_string,
    serialize_bulk_string,
    serialize_error
)
from app.store import db # global datastore

MAX_CHUNK_SIZE = 1024 # 1 KB read buffer
CRLF = b"\r\n"

def handle_command(command_args: list[str]) -> bytes:
    """Routes a RESP command to the corresponding datastore operation and returns the serialized reponse.

    Args:
        command_args (list[str]): input RESP commands

    Returns:
        bytes: serialized RESP response
    """

    if not command_args:
        return serialize_error("Empty command")
    
    cmd = command_args[0].upper() # redis commands are case insensitive

    if cmd == "PING":
        return serialize_simple_string("PONG")
    
    elif cmd == "COMMAND":
        return b"*0\r\n"
    
    elif cmd == "SET":
        if len(command_args) < 3:
            return(serialize_error("ERR wrong number of args for set command"))
        key,value = command_args[1], command_args[2]
        db.set(key,value)
        return(serialize_simple_string("OK"))
    
    elif cmd == "GET":
        if len(command_args) != 2:
            return(serialize_error("ERR wrong number of args for get command"))
        key = command_args[1]
        val = db.get(key)
        return serialize_bulk_string(val)
    return serialize_error(f"ERR unknown command {cmd}")

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
            try:
                command_args, _ = parse_response(data)

                if command_args:
                    print(f"Parsed command: {command_args} from {addr}")
                    response_bytes = handle_command(command_args)
                    writer.write(response_bytes)
                    await writer.drain()
                else:
                    print(f"waiting for more data from {addr}...")
                    continue

            except ValueError as e:
                print(f"Protocol error: {e}")
                writer.write(b"-ERR Protocol error\r\n")
                await writer.drain()
                continue

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