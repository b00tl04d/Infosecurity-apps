"""
Main Menu Script

StudentID: p2243452
Name: Seah Kwan Hock Reuben
Class: DISM/FT/1B/04
Assessment: CA1-2

Script name:
    menu.py

Purpose:
    Main Menu script that allows the user to select one of the info security apps and to use it

Usage syntax:
    Run with command line in the directory where this script is located, e.g. python menu.py

Input file(s):
    Nil

Output file(s):
    Nil

Python version:
    Python 3.10.9

Reference:
    Nil

Library/Module:
- modules used that are installed by default in Python 3.10.9
    - os
- custom module(s) from python scripts in the same directory
    - nmap_scanner
    - ftp_client
    - custom_packet

Known issues:
    Nil


"""

import os
import nmap_scanner
import ftp_client
import custom_packet


# User-defined function
def validate_option(user_option: str, first_option: int, last_option: int) -> int | bool:
    """
    Check if a user's number input is within a numeric range of options

    Args:
        user_option (str): User's input
        first_option (int): The first option in the range of numeric options
        last_option (int): The last option in the range of numeric options

    Returns:
        int | bool: int if the user's option is numeric and is within the specified range, False otherwise
    """
    if user_option.isnumeric():
        if int(user_option) >= first_option and int(user_option) <= last_option:
            return int(user_option)
    return False


# User-defined function
def main_menu():
    """
    Main menu interface
    """
    initial_path = os.getcwd()

    error_msg = ""
    while True:
        print("** PSEC Info Security Apps **")
        print("1) Scan network")
        print("2) Upload/download file using FTP")
        print("3) Send custom packet")
        print("4) Quit\n")

        if error_msg != "":
            print(error_msg)

        opt = input("Choose an Info Security App: ")
        opt_result = validate_option(user_option=opt, first_option=1, last_option=4)

        match opt_result:
            case 1:
                os.system("cls")
                error_msg = ""
                scanner = nmap_scanner.CustomNmapScanner()
                os.system("cls")
                scanner.display_scan_output()
                print()
                input("Scan results displayed, press \"enter\" to return to the main menu....")
                os.system("cls")
            case 2:
                os.system("cls")
                error_msg = ""

                print("** FTP Menu **")
                print("1) Upload file to FTP Server")
                print("2) Download file from FTP Server")
                print("3) Return to main menu\n")

                if error_msg != "":
                    print(error_msg)

                ftp_opt = input("Choose an FTP option: ")
                ftp_opt_result = validate_option(user_option=ftp_opt, first_option=1, last_option=4)

                match ftp_opt_result:
                    case 1:
                        error_msg = ""
                        client = ftp_client.CustomFTPClient()
                        client.specify_home_directory()
                        while True:
                            if client.connection() == False:
                                reconnect = input("Connection to FTP server failed, try again? (Y/yes to try again, default is \"no\"): ")
                                if reconnect == "Y" or reconnect == "y" or reconnect == "Yes" or reconnect == "yes":
                                    os.system("cls")
                                    continue
                                else:
                                    input("Press \"enter\" to return to the Info Security Apps menu....")
                                    os.chdir(initial_path)  # Revert working directory to where the menu script was executed
                                    os.system("cls")
                                    break
                            else:
                                client.upload_file()
                                break
                    case 2:
                        error_msg = ""
                        client = ftp_client.CustomFTPClient()
                        client.specify_home_directory()
                        while True:
                            if client.connection() == False:
                                reconnect = input("Connection to FTP server failed, try again? (Y/yes to try again, default is \"no\"): ")
                                if reconnect == "Y" or reconnect == "y" or reconnect == "Yes" or reconnect == "yes":
                                    os.system("cls")
                                    continue
                                else:
                                    input("Press \"enter\" to return to the Info Security Apps menu....")
                                    os.chdir(initial_path)  # Revert working directory to where the menu script was executed
                                    os.system("cls")
                                    break
                            else:
                                client.download_file()
                                break
                    case 3:
                        os.system("cls")
                        pass
                    case False:
                        error_msg = "Please select a valid option from the FTP menu.\n"
                        os.system("cls")
            case 3:
                os.system("cls")
                error_msg = ""
                packet_sender = custom_packet.CustomPacketSender()
                packet_sender.custom_packet_menu()
            case 4:
                break
            case False:
                error_msg = "Please select a valid option from the menu.\n"
                os.system("cls")


# Main program
if __name__ == "__main__":
    main_menu()
