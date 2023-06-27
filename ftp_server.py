"""
FTP Server Script

StudentID: p2243452
Name: Seah Kwan Hock Reuben
Class: DISM/FT/1B/04
Assessment: CA1-2

Script name:
    ftp_server.py

Purpose:
    FTP server script that allows the user to host an FTP server

Usage syntax:
    This script must run on a new/separate terminal to start the FTP server
    Run with command line in the directory where this script is located, e.g. python ftp_server.py

Input file(s):
    Nil

Output file(s):
    Nil

Python version:
    Python 3.10.9

Reference:
https://pyftpdlib.readthedocs.io/en/latest/api.html#pyftpdlib.authorizers.DummyAuthorizer
https://pyftpdlib.readthedocs.io/en/latest/tutorial.html
https://pyftpdlib.readthedocs.io/en/latest/api.html
https://github.com/giampaolo/pyftpdlib/commit/553e8f7c52b8b2fa9d8ccfb368c3d88441fd46e7

Library/Module:
- modules used that are installed by default in Python 3.10.9
    - os
    - re
- required external modules installed using pip: pip install <module name>  # e.g. pip install pyftpdlib
    - pyftpdlib

Known issues:


"""

import os
import re
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class CustomFTPServer:
    """
    A class for setting up a Custom FTP Server

    Attributes:
        Nil

    Methods:
        __init__():
            Initialize with the FTP server settings


        list_directory():
            Lists the entries of the current working directory

        
        get_home_directory():
            Allow user to specify the home directory of the ftp server 

            Returns:
                str: The home directory of the ftp server that the user has specified


        start_server():
            Start the ftp server
    """

    # Initializer
    def __init__(self) -> None:
        """
        Initialize with the FTP server settings
        """
        # Instantiate a dummy authorizer for managing 'virtual' users
        self.authorizer = DummyAuthorizer() # handle permission and user
        self.server_home_directory = self.get_home_directory()

        # Define an anonymous user and home directory having read-write permissions
        # Use full path that is specified by the user
        self.authorizer.add_anonymous(self.server_home_directory, perm='elrw')  # read-write permissions for upload/download

        # Instantiate FTP handler class
        self.handler = FTPHandler #  understand FTP protocol
        self.handler.authorizer = self.authorizer

        # FTP server to listen on the address 127.0.0.1 and port 2121
        self.address = ('127.0.0.1', 2121)
        self.ftp_server = FTPServer(self.address, self.handler)


    # User-defined method
    def list_directory(self):
        """
        Lists the entries of the current working directory
        """
        print("[Current Directory] - .")
        print("[Parent Directory] - ..")
        for entry in os.listdir():
            if os.path.isfile(entry):
                print(f"[file] - {entry}")
            elif os.path.isdir(entry):
                print(f"[Directory] - {entry}")
        print()


    # User-defined method
    def get_home_directory(self) -> str:
        """
        Allow user to specify the home directory of the ftp server, where files are uploaded to/downloaded from 

        Returns:
            str: The home directory of the ftp server that the user has specified
        """
        error_msg = ""
        while True:
            try:
                print(f"Use relative paths to go to a parent directory or to use the current directory.") 
                print(f"Current working directory path: {os.getcwd()}")
                print(f"Current directory listing: ")
                self.list_directory()

                if error_msg != "":
                    print(f"{error_msg}\n")
                
                current_directory = input("Specify home directory of FTP server: ")

                # Ensure usage of relative paths. Prevent change directory to the root path of a drive
                if re.match(r"^[A-Za-z]:\\+|^[A-Za-z]:/+|^\\|^/", current_directory):
                    error_msg = "Error - Please use a relative path for changing directories or using the current directory"
                    os.system("cls")
                    continue

                os.chdir(current_directory)

                confirmation = input("Confirm home direcory selection (Y/yes to confirm, no to change directory. Any other response is \"no\"): ")
                error_msg = ""
                os.system("cls")

                if confirmation == "Y" or confirmation == "y" or confirmation == "Yes" or confirmation == "yes":
                    os.system("cls")
                    return os.getcwd() + "/"
            except FileNotFoundError:
                os.system("cls")
                error_msg = "Error directory does not exist, please select a valid directory"
            except NotADirectoryError:
                os.system("cls")
                error_msg = "Error directory does not exist, please select a valid directory"
            except OSError:
                os.system("cls")
                error_msg = "Error directory does not exist, please select a valid directory"

    # User-defined method
    def start_server(self):
        """
        Start the ftp server
        """
        # start ftp server
        # Follow github commit where a timeout was added so that "ctrl + c" exits the FTP server on Windows OS
        self.ftp_server.serve_forever(timeout=2 if os.name == 'nt' else None)


# Main program
if __name__ == "__main__":
    server = CustomFTPServer()
    server.start_server()
