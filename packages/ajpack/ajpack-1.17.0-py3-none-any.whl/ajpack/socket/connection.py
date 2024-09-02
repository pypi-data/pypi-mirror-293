import socket
import time

def send(serverSocket: socket.socket, msg: str, endIndicator: str = "/end/", chunkSize: int = 1000, delay: float = 0) -> None:
    """
    Sends a message to the server.

    :param serverSocket (socket.socket): The socket object.
    :param msg (str): The message to send.
    :param endIndicator (str): The end str to be sent, to indicate that the message is done.
    :param chunkSize (int): The size of each chunk to send.
    :param delay (float): The time to wait before sending a new chunk.
    """
    try:
        # Split the message into chunks
        chunks = [msg[i:i+chunkSize] for i in range(0, len(msg), chunkSize)]

        for chunk in chunks:
            if chunk:
                # Send chunk
                serverSocket.send(chunk.encode())
                # Wait to prevent bugs
                time.sleep(delay)
        
        # Send end indicator
        serverSocket.send(endIndicator.encode())
    except Exception as e:
        raise Exception(f"There was an unexpected error while sending the message to the server. --> {e}")

def rcv(serverSocket: socket.socket, endIndicator: str = "/end/", bufSize: int = 1024) -> str:
    """
    Receives a message of the server.

    :param serverSocket (socket.socket): The socket object.
    :param endIndicator (str): The end str to be received, to indicate that the message is done. (must be the same of sending)
    :param bufSize (int): The buf size of the socket object.
    """
    try:
        feedback: str = ""

        while True:
            feedbackTmp: str = serverSocket.recv(bufSize).decode()
            if feedbackTmp:
                if feedbackTmp != endIndicator:
                    feedbackTmp += feedbackTmp
                else:
                    break
            
        return feedback
    except Exception as e:
        raise Exception(f"There was an unexpected error while receiving the data from the server. --> {e}")


#ToDo Finish
def send_rsa() -> None:
    from ..settings import code_missing
    code_missing()

#ToDo Finish
def rcv_rsa() -> None:
    from ..settings import code_missing
    code_missing()