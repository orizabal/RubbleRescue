import os
import paramiko
from paramiko import SFTPClient

class Paramiko:
    sftpClient: SFTPClient
    host: str
    port: str
    user: str
    dir: str
    password: str = None

    print(os.getcwd())
    paramiko.util.log_to_file('./metrics/log/paramiko.log')
    paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))

    def __init__(self, host: str, port: str, user: str, dir: str, password: str):
        self.host = host
        self.port = port
        self.user = user
        self.dir = dir
        self.password = password


    # Called when entering the context
    # Establishes a connection with the Pi and returns a connection
    def __enter__(self) -> SFTPClient:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.host, port=self.port, username=self.user)
            self.sftpClient = self.ssh.open_sftp()
            return self.sftpClient
        except Exception as e:
            print(e)
            pass
    
    # Called when exiting the context
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        # self.sftpClient.close()