CRLF = b"\r\n"

def parse_response(data: bytes) -> tuple[list[str], int]:
    """
    Deserializes raw RESP-encoded byte string into a python list

    Args:
        data (bytes): The raw binary stream from the TCP socket.

    Returns:
        tuple[list[str], int]: A tuple containing the extracted command arguments as a list of strings,
        and the total bytes consumed from the buffer.   
    """
    if not data:
        return [], 0
    
    if data[0:1] != b'*': # client should always send a RESP array which starts with `*`
        raise ValueError(f"Invalid payload. Expected RESP array got: {data!r}")
    
    first_crlf = data.find(CRLF) # first instance of CRLF
    if first_crlf == -1:
        return [], 0 # incomplete, wait for more data

    # extracts num elements ('*3' -> 3)
    try:
        num_elements = int(data[1:first_crlf])
    except ValueError:
        raise ValueError("Invalid array length indicator")
    # added try catch loop since someone can send something like b"*XyZ\r\n" which would then crash the parser due to the ValueError
    elements = []

    pointer = first_crlf + 2 # move the pointer to where the start of the first element is

    for _ in range(num_elements):
        # read the bulk string length indicator which starts with '$'
        if data[pointer:pointer+1] != b'$':
            raise ValueError("Expected bulk string")
        
        next_crlf = data.find(CRLF, pointer)
        if next_crlf == -1:
            return [], 0
        
        # extract string length
        str_length = int(data[pointer+1:next_crlf])

        # calculate the boundaries of the string
        str_start = next_crlf + 2
        str_end = str_start + str_length

        if len(data) < str_end + 2:
            return [], 0
        
        if data[str_end:str_end+2] != CRLF:
            raise ValueError("Bulk string not terminated by CRLF")
        
        # extracts, decodes, and then appends the actual payload as a string
        payload = data[str_start:str_end].decode("utf-8")
        elements.append(payload)

        pointer = str_end + 2

    return elements, pointer