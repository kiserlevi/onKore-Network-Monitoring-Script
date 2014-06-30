import paramiko

class Server(object):

    def __init__(self, sftpusername, sftppassword, host, port):

        self.transport = paramiko.Transport((host, port))
        self.transport.connect(username = sftpusername, password = sftppassword)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def upload(self, local, remote):
        self.sftp.put(local, remote)

    def close(self):
        """
        Close the connection if it's active
        """

        if self.transport.is_active():
            self.sftp.close()
            self.transport.close()

    # with-statement support
    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()
