import paramiko
import logging
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
error_logger = logging.getLogger('test.error')
info_logger = logging.getLogger('test.info')


class Serverconnection:

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