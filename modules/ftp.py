""" FTP Uploader using ftplib """
from socket import error
import logging
from ftplib import FTP, error_perm
from yaml import safe_load


class FTPUploader:
    """
    It uploads files to an FTP server

    :param config_path: str = 'ftp_config.yml', defaults to ftp_config.yml
    :type config_path: str (optional)
    """

    def __init__(self, config_path: str = 'ftp_config.yml') -> None:
        with open(config_path, mode='r', encoding='utf8') as config_file:
            self.config = safe_load(config_file)

        logging.info(f'Connect to FTP server: {self.config["ftp_host"]}')

    def upload_files(self, files_to_upload: list[str] = None):
        """
        It uploads files to an FTP server.

        :param files_to_upload: list[str] = None
        :type files_to_upload: list[str]
        :return: None
        """
        if files_to_upload is None:
            return False
        try:
            with FTP(self.config['ftp_host'],
                    self.config['ftp_user'],
                    self.config['ftp_password']) as ftp:

                ftp.cwd(self.config['ftp_upload_dir'])

                for zip_file in files_to_upload:
                    with open(zip_file, mode='rb') as zip_file_handler:
                        ftp.storbinary(f'STOR {zip_file}', zip_file_handler)
                return None
        except error_perm:
            logging.error('Incorrect login datas')
        except error as e:
            logging.error(f'Problems with FTP connection: {str(e)[12:]}')
