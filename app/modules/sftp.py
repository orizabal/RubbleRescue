import pysftp
from pysftp import Connection

class Sftp:
    connection: Connection
    host: str
    username: str
    dir: str
    password: str = None
    
    def __init__(self, host: str, username: str, dir: str, password: str = None):
        self.host = host
        self.username = username
        self.dir = dir
        self.password = password

    # Called when entering the context
    # Establishes a connection with the Pi and returns a connection
    def __enter__(self) -> Connection:
        self.connection = pysftp.Connection(host=self.host, username=self.username, password=self.password)
        # cd to the directory that contains the audio files
        self.connection.cd(self.dir)
        return self.connection
    
    # Called when exiting the context
    def __exit__(self):
        self.connection.close()
