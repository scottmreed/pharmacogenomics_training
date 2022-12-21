import paramiko
import logging
import os

error_logger = logging.getLogger('test.error')
info_logger = logging.getLogger('test.info')


class Serverconnection:
    """
    Class to manage multiple different server connections
    """
    def __init__(self, host, username, password):

        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, port=22, username=username, password=password)
        self.transport = paramiko.Transport((host, 22))
        self.transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def run_command(self, command):
        _stdin, _stdout, _stderr = self.client.exec_command(command)
        stdout = _stdout.read().decode()
        stderr = _stderr.read().decode()
        success = True
        if len(stderr) > 0:
            success = False
            error_logger.error(stderr)

        return stdout, success

    def send_batch(self, path, command):
        f = self.sftp.open(f'{path}', "wb")
        f.write(f'{command}')
        f.close()

    def send_chmod(self, path):
        self.sftp.chmod(path, 0o775)

    def retreive_results(folder, sftp):
        f = sftp.get(f'{folder}/temp_bt', 'output')
        print(f)

class Pharmacogenomics(Serverconnection):
    """This is a subclass of Serverconnection
    which must be imported from server_connections
    Multiple subclassses can be prepared for different connections
    Each inherits the class functions like run_command
    but allows for a unique set of credentials to be passed."""

    def __init__(self, username, password):

        # this is for accesing from local network only
        my_ip = os.popen('curl ipinfo.io/ip').read()

        if my_ip.startswith('174.29.'):
            host = '192.168.0.20'
        else:
            host = 'pharmacogenomics.ddnsfree.com'

        super().__init__(host, username, password)


class Alderaan(Serverconnection):
    """This is a subclass of Serverconnection
    which must be imported from server_connections
    Multiple subclassses can be prepared for different connections
    Each inherits the class functions like run_command
    but allows for a unique set of credentials to be passed."""

    def __init__(self, username, password):
        # must be on VPN for this to work
        host = '10.133.30.30'
        host = 'clas-compute.ucdenver.pvt'
        super().__init__(host, username, password)

class Kenari(Serverconnection):
    """This is a subclass of Serverconnection
    which must be imported from server_connections
    Multiple subclassses can be prepared for different connections
    Each inherits the class functions like run_command
    but allows for a unique set of credentials to be passed."""

    def __init__(self, username, password):
        # must be on VPN for this to work
        host = 'clas-chem-compute.ucdenver.pvt'
        super().__init__(host, username, password)