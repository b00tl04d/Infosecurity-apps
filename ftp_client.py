"""
FTP Client Script 

StudentID: p2243452 
Name: Seah Kwan Hock Reuben
Class: DISM/FT/1B/04
Assessment: CA1-2

Script name:
    ftp_client.py

Purpose:
    FTP client script that allows the user to upload/download files to/from an FTP server

Usage syntax:
    Nil, intended to be used as a custom module

Input file(s):
    Nil

Output file(s):
    Nil

Python version:
    Python 3.10.9

Reference:
https://pythonspot.com/ftp-client-in-python/
https://stackoverflow.com/questions/17438096/ftp-upload-files-python
https://github.com/julian-r/python-magic
https://docs.python.org/3/library/ftplib.html#ftplib.FTP.dir
https://docs.python.org/3/library/ftplib.html#ftplib.FTP.pwd
https://www.geeksforgeeks.org/python-os-path-isfile-method/
https://www.geeksforgeeks.org/how-to-download-and-upload-files-in-ftp-server-using-python/

Library/Module:
- modules used that are installed by default in Python 3.10.9
    - socket
    - ftplib
    - os
    - re
- required external modules installed using pip on the command line: pip install <module name>  # e.g. pip install python-magic-bin
    - python-magic-bin


Known issues:
    If the external module "python-magic" is installed it has to be uninstalled first with the command "pip uninstall python-magic",
    this is due to the conflicting import name of "magic"

    "python-magic-bin" was used as there is a compatibility error with "python-magic" using Python 3.10.9


"""

import socket  # For handling the "socket.gaierror"
import ftplib
import os
import re
import magic


class CustomFTPClient:
    """
    A class for setting up a Custom FTP Client

    Attributes:
        Nil

    Methods:
        __init__():
            Instantiate FTP client with the current working directory and an instance of the ftplib client


        connection():
            Initiate connection to the ftp server

            Returns:
                bool: True if there is a successful connection to the ftp server, False otherwise 

        
        determine_transfer_mode(file):
            Determine whether ascii or binary mode should be used for ftp uploads

            Args:
                file (str): Name of the file in the current directory

            Returns:
                str: Whether the ascii or binary mode should be used depending on the file's mimetype 


        list_directory(filesystem):
            List the current working directory of the ftp client or the server, depends on the argument value

            Args:
                filesystem (str): Used to specify if its the client's current working directory or the remote ftp server's current working directory

        
        specify_home_directory():
            Allow user to specify the home directory of the ftp client, where files are uploaded from/ downloaded to


        upload_file():
            Uploads a file from the ftp client to the ftp server and closes the FTP session afterwards


        download_file():
            Downloads a file from an ftp server and closes the FTP session afterwards
    """

    # Initializer
    def __init__(self) -> None:
        """
        Instantiate FTP client with the current working directory and an instance of the ftplib client
        """
        self.ftp_client = ftplib.FTP()
        self.initial_path = os.getcwd()


    # User-defined method
    def connection(self) -> bool:
        """
        Initiate connection to the ftp server

        Returns:
            bool: True if there is a successful connection to the ftp server, False otherwise 
        """
        try:
            # As per assignment's details, use "127.0.0.1" for the interface and port "2121"
            self.ftp_client.connect("127.0.0.1", 2121)
            self.ftp_client.login()
            return True
        except ConnectionRefusedError:
            return False
        except socket.gaierror:
            return False


    # User-defined method
    def determine_transfer_mode(self, file: str) -> str:
        """
        Determine whether ascii or binary mode should be used for ftp uploads

        Args:
            file (str): Name of the file in the current directory

        Returns:
            str: Whether the ascii or binary mode should be used depending on the file's mimetype 
        """
        try:
            content_type = magic.from_file(file, mime=True)

            if content_type.startswith("text/"):
                return "ascii"
            return "binary"
        except magic.MagicException:
            # Default to binary mode if the mime type of the file is unknown
            return "binary"


    # User-defined method
    def list_directory(self, filesystem: str):
        """
        List the current working directory of the ftp client or the server, depends on the argument value

        Args:
            filesystem (str): Used to specify if its the client's current working directory or the remote ftp server's current working directory
        """
        if filesystem == "client":
            print("[Current Directory] - .")
            print("[Parent Directory] - ..")
            for entry in os.listdir():
                if os.path.isfile(entry):
                    print(f"[file] - {entry}")
                elif os.path.isdir(entry):
                    print(f"[Directory] - {entry}")
            print()
        elif filesystem == "server":
            print(f"FTP server directory path: \"{self.ftp_client.pwd()}\"")
            print("FTP server directory listing: ")
            self.ftp_client.dir()
            print()


    # User-defined method
    def specify_home_directory(self):
        """
        Allow user to specify the home directory of the ftp client, where files are uploaded from/ downloaded to
        """
        error_msg = ""
        while True:
            try:
                print(f"Use relative paths to go to a parent directory or to use the current directory.") 
                print(f"Current working directory path: {os.getcwd()}")
                print(f"Current directory listing: ")
                self.list_directory(filesystem="client")

                if error_msg != "":
                    print(f"{error_msg}\n")
                
                current_directory = input("Specify home directory of FTP client: ")

                # Ensure usage of relative paths. Prevent change directory to the root path of a drive
                if re.match(r"^[A-Za-z]:\\+|^[A-Za-z]:/+|^\\|^/", current_directory):
                    error_msg = "Error - Please use a relative path for changing directories or using the current directory"
                    os.system("cls")
                    continue

                # Case insensitive as only one directory with its exact naming can exist
                os.chdir(current_directory)

                confirmation = input("Confirm home direcory selection (Y/yes to confirm, no to change directory. Any other response is \"no\"): ")
                error_msg = ""
                os.system("cls")

                if confirmation == "Y" or confirmation == "y" or confirmation == "Yes" or confirmation == "yes":
                    os.system("cls")
                    break
            except FileNotFoundError:
                os.system("cls")
                error_msg = "Error - Directory does not exist, please select a valid directory"
            except NotADirectoryError:
                os.system("cls")
                error_msg = "Error - Directory does not exist, please select a valid directory"
            except OSError:
                os.system("cls")
                error_msg = "Error - Directory does not exist, please select a valid directory"


    # User-defined method
    def upload_file(self):
        """
        Uploads a file from the ftp client to the ftp server and closes the FTP session afterwards
        """
        error_msg = ""
        while True:
            print("Choose a file to upload.")
            print("Home directory listing:")
            self.list_directory(filesystem="client")

            if error_msg != "":
                print(f"{error_msg}\n")

            selected_file = input("Select a file: ")

            if not os.path.isfile(selected_file):
                os.system("cls")
                error_msg = "Error - Please select an existing file."
            else:
                filetype = self.determine_transfer_mode(file=selected_file)

                try:
                    if filetype == "ascii":
                        with open(selected_file, "rb") as file:
                            self.ftp_client.storlines(f"STOR {selected_file}", file)
                    elif filetype == "binary":
                        with open(selected_file, "rb") as file:
                            self.ftp_client.storbinary(f"STOR {selected_file}", file)
                except:
                    print(f"Error in uploading: {selected_file}")
                    err_qns = input("Would you like to try again? (Y/yes to try again, default response is \"no\"): ")

                    if err_qns == "Y" or err_qns == "y" or err_qns == "Yes" or err_qns == "yes":
                        error_msg = ''
                        os.system("cls")
                        continue
                    else:
                        print("\nEnding FTP client session....")
                        self.ftp_client.close()
                        input("Press \"enter\" to return to the Info Security Apps menu....")
                        os.system("cls")
                        break

                print(f"\nUploaded file: {selected_file}.")
                print("Ending FTP client session....")

                self.ftp_client.close()
                os.chdir(self.initial_path)  # Revert local directory to where the menu script was executed

                input("Press \"enter\" to return to the Info Security Apps menu....")
                os.system("cls")
                break


    # User-defined method
    def download_file(self):
        """
        Downloads a file from an ftp server and closes the FTP session afterwards
        """
        error_msg = ""
        while True:
            print("Choose a file to download.")
            self.list_directory(filesystem="server")

            if error_msg != "":
                print(f"{error_msg}\n")

            selected_file = input("Select a file (Use \"/cwd <directory>\" to change FTP server directory): ")

            try:
                if re.match(pattern=r"^/cwd\b.*", string=selected_file):
                    error_msg = ''
                    directory = re.search(pattern=r"^/cwd\b(.*)", string=selected_file).group(1).strip()
                    self.ftp_client.cwd(directory)
                    os.system("cls")
                    continue
            except:
                error_msg = "Error in changing directory, please select a valid directory."
                os.system("cls")
                continue

            try:
                # No need to determine FTP download transfer mode as binary mode + Python write in binary mode handles most filetypes properly
                with open(selected_file, "wb") as file:
                    self.ftp_client.retrbinary(f"RETR {selected_file}", file.write)
            except:
                print(f"Error in downloading: {selected_file}")
                os.remove(selected_file)

                err_qns = input("Would you like to try again? (Y/yes to try again, default response is \"no\"): ")

                if err_qns == "Y" or err_qns == "y" or err_qns == "Yes" or err_qns == "yes":
                    error_msg = ''
                    os.system("cls")
                    continue
                else:
                    print("\nEnding FTP client session....")
                    self.ftp_client.close()
                    input("Press \"enter\" to return to the Info Security Apps menu....")
                    os.system("cls")
                    break

            print(f"\nDownloaded file: {selected_file}")
            print("Ending FTP client session....")

            self.ftp_client.close()
            os.chdir(self.initial_path)  # Revert local directory to where the menu script was executed

            input("Press \"enter\" to return to the Info Security Apps menu....")
            os.system("cls")
            break
