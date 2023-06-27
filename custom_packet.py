"""
Custom Packet Sender Script

StudentID: p2243452
Name: Seah Kwan Hock Reuben
Class: DISM/FT/1B/04
Assessment: CA1-2

Script name:
    custom_packet.py

Purpose:
    Send custom packet that allows the user to send a custom packet through the network

Usage syntax:
    Nil, intended to be used as a custom module

Input file(s):
    Nil

Output file(s):
    Nil

Python version:
    Python 3.10.9

Reference:
https://stackoverflow.com/questions/106179/regular-expression-to-match-dns-hostname-or-ip-address
https://docs.python.org/3/library/re.html#re.IGNORECASE

Library/Module:
- modules used that are installed by default in Python 3.10.9
    - os
    - re
- required external modules installed using pip: pip install <module name>  # e.g. pip install scapy
    - scapy

Known issues:
    Nil


"""

import os
import re
from scapy.all import send, IP, TCP, ICMP, UDP   


# Does not need an initializer "__init__()"
class CustomPacketSender:
    """
    A class for using a Custom Packet Sender

    Attributes:
        Nil

    Methods:
        validate_address(address):
            Validate an address using regex

        Args:
            address (str): domain address or ipv4 address to validate

        Returns:
            bool: If the entered hostname or ipv4 is valid return True, else return False


        validate_port(number):
            Check if the number is a valid port number

            Args:
                number (int): The number to validate

            Returns:
                bool: True if it is a valid port number, otherwise False


        validate_pkt_type(packet):
            Check if the packet type is one of three valid inputs,
            (T)TCP, (U)UDP, (I)ICMP echo request. Case sensitiv

            Args:
                packet (str): Packet type input to validate

            Returns:
                bool: True if packet type is valid, False otherwise


        send_packet(src_addr, src_port, dest_addr, dest_port, pkt_type, pkt_data):
            Create and send a packet based on the provided parameters

            Args:
                src_addr(str) : Source IP address
                src_port(int) : Source Port
                dest_addr(str): Destination IP address
                dest_port(int): Destination Port
                pkt_type(str) : Type of packet (T)TCP, (U)UDP, (I)ICMP echo request. Note it is case sensitive
                pkt_data(str) : Data in the packet

            Returns:
                bool: True if packets are sent successfully, False otherwise


        print_buffered_menu(menu):
            Print line by line of a buffered menu

            Args:
                menu (list): Menu to print out


        custom_packet_menu():
            Obtain inputs to create custom packet
    """

    # User-defined method
    def validate_address(self, address: str) -> bool:
        """
        Validate an address using regex

        Args:
            address (str): domain address or ipv4 address to validate

        Returns:
            bool: If the entered hostname or ipv4 is valid return True, else return False
        """
        # Check for a numbers only input within the address
        numbers_only_pattern = r"^\d+$"

        # Address regex matches a hostname. Leading HTTP/HTTPS scheme is optional.
        address_regex = r"^(http://|https://)?(([a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])\.)*([a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])$"

        # IPv4 address regex matches an IPv4 address
        ipv4_addr_regex = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$" 

        if re.match(pattern=numbers_only_pattern, string=address):
            return False

        # Ignore casing for address as it does not matter
        if re.match(pattern=address_regex, string=address, flags=re.IGNORECASE):
            return True
        elif re.match(pattern=ipv4_addr_regex, string=address):
            return True
        return False


    # User-defined method
    def validate_port(self, number: str) -> bool:
        """
        Check if the number is a valid port number

        Args:
            number (int): The number to validate

        Returns:
            bool: True if it is a valid port number, otherwise False
        """
        if number.isnumeric():
            if int(number) > 0 and int(number) < 65536:
                return True
        return False


    # User-defined method
    def validate_pkt_type(self, packet: str) -> bool:
        """
        Check if the packet type is one of three valid inputs,
        (T)TCP, (U)UDP, (I)ICMP echo request. Case sensitive

        Args:
            packet (str): Packet type input to validate

        Returns:
            bool: True if packet type is valid, False otherwise
        """
        if packet == "T":
            return True
        elif packet == "U":
            return True
        elif packet == "I":
            return True
        return False


    # User-defined method
    def send_packet(self, src_addr: str, src_port: int, dest_addr: str, 
                dest_port: int, pkt_type: str, pkt_data: str)  -> bool:
        """
        Create and send a packet based on the provided parameters

        Args:
            src_addr(str) : Source IP address
            src_port(int) : Source Port
            dest_addr(str): Destination IP address
            dest_port(int): Destination Port
            pkt_type(str) : Type of packet (T)TCP, (U)UDP, (I)ICMP echo request. Note it is case sensitive
            pkt_data(str) : Data in the packet
        Returns:
            bool: True if packets are sent successfully, False otherwise
        """    
        if pkt_type == "T":
            pkt = IP(dst=dest_addr, src=src_addr) / TCP(dport=dest_port, sport=src_port) / pkt_data
        elif pkt_type == "U":
            pkt = IP(dst=dest_addr, src=src_addr) / UDP(dport=dest_port, sport=src_port) / pkt_data
        elif pkt_type == "I":
            pkt = IP(dst=dest_addr, src=src_addr) / ICMP() / pkt_data

        try:
            send(pkt ,verbose = False)   # Hide "Send 1 packets" message on console
            return True
        except:
            return False
    

    # User-defined method
    def print_buffered_menu(self, menu: list):
        """
        Print line by line of a buffered menu

        Args:
            menu (list): Menu to print out
        """
        for line in menu:
            print(line)


    # User-defined method
    def custom_packet_menu(self):
        """
        Obtain inputs to create custom packet
        """    
        menu_buffer = [
            "************************",
            "* Custom Packet        *",
            "************************\n"
        ]
        self.print_buffered_menu(menu=menu_buffer)

        # Validate src_addr, no type casting
        src_addr = input("Enter Source address of Packet: ")
        src_addr_flag = self.validate_address(address=src_addr)
        while src_addr_flag == False:
            os.system("cls")
            self.print_buffered_menu(menu_buffer)
            print("\nPlease enter a valid source address.\n")
            src_addr = input("Enter Source address of Packet: ")
            src_addr_flag = self.validate_address(address=src_addr)
        menu_buffer.append(f"Enter Source address of Packet: {src_addr}")

        os.system("cls")
        self.print_buffered_menu(menu=menu_buffer)

        # Validate and cast src_port to int type
        src_port = input("Enter Source Port of Packet: ")
        src_port_flag = self.validate_port(number=src_port)
        while src_port_flag == False:
            os.system("cls")
            self.print_buffered_menu(menu_buffer)
            print("\nPlease enter a valid source port.\n")
            src_port = input("Enter Source Port of Packet: ")
            src_port_flag = self.validate_port(number=src_port)
        src_port = int(src_port)
        menu_buffer.append(f"Enter Source Port of Packet: {src_port}")

        os.system("cls")
        self.print_buffered_menu(menu=menu_buffer)

        # Validate dest_addr, no type casting
        dest_addr = input("Enter Destination address of Packet: ")
        dest_addr_flag = self.validate_address(address=dest_addr)
        while dest_addr_flag == False:
            os.system("cls")
            self.print_buffered_menu(menu_buffer)
            print("\nPlease enter a valid destination address.\n")
            dest_addr = input("Enter Destination address of Packet: ")
            dest_addr_flag = self.validate_address(address=dest_addr)
        menu_buffer.append(f"Enter Destination address of Packet: {dest_addr}")

        os.system("cls")
        self.print_buffered_menu(menu=menu_buffer)

        # Validate and cast dest_port to int type
        dest_port = input("Enter Destination Port of Packet: ")
        dest_port_flag = self.validate_port(number=dest_port)
        while dest_port_flag == False:
            os.system("cls")
            self.print_buffered_menu(menu_buffer)
            print("\nPlease enter a valid destination port.\n")
            dest_port = input("Enter Destination Port of Packet: ")
            dest_port_flag = self.validate_port(number=dest_port)
        dest_port = int(dest_port)
        menu_buffer.append(f"Enter Destination Port of Packet: {dest_port}")

        os.system("cls")
        self.print_buffered_menu(menu=menu_buffer)

        # Validate pkt_type, no type casting
        pkt_type = input("Enter Type (T) TCP, (U) UDP, (I) ICMP echo request (T/U/I) (case sensitive): ")
        pkt_type_flag = self.validate_pkt_type(packet=pkt_type)
        while pkt_type_flag == False:
            os.system("cls")
            self.print_buffered_menu(menu_buffer)
            print("\nPlease enter a valid packet type.\n")
            pkt_type = input("Enter Type (T) TCP, (U) UDP, (I) ICMP echo request (T/U/I) (case sensitive): ")
            pkt_type_flag = self.validate_pkt_type(packet=pkt_type)
        menu_buffer.append(f"Enter Type (T) TCP, (U) UDP, (I) ICMP echo request (T/U/I) (case sensitive): {pkt_type}")

        os.system("cls")
        self.print_buffered_menu(menu=menu_buffer)

        if pkt_type == "I":
            print("  Note: Port number for ICMP will be ignored")

        pkt_data = input("Packet RAW Data (optional, DISM-DISM-DISM-DISM left blank): ")
        menu_buffer.append(f"Packet RAW Data (optional, DISM-DISM-DISM-DISM left blank): {pkt_data}")
        if pkt_data == "":
            pkt_data = "DISM-DISM-DISM-DISM"

        # Validate and cast pkt_count to int type
        # Uses "self.validate_port" to validate the no. of packets to send as it has the same number range
        pkt_count = input("No of Packet to send (1-65535): " )
        pkt_count_flag = self.validate_port(number=pkt_count)
        while pkt_count_flag == False:
            os.system("cls")
            self.print_buffered_menu(menu_buffer)
            print("\nPlease enter a number of packets to send in the range of 1-65535.\n")
            pkt_count = input("No of Packet to send (1-65535): ")
            pkt_count_flag = self.validate_port(number=pkt_count)
        pkt_count = int(pkt_count)
        menu_buffer.append(f"No of Packet to send (1-65535): {pkt_count}")

        os.system("cls")
        self.print_buffered_menu(menu=menu_buffer)

        start_now = input("Enter Y/yes to continue, no to return to the main menu. Any other response is \"no\": ") 

        if start_now == "Y" or start_now == "y" or start_now == "Yes" or start_now == "yes": 
            count = 0

            for _ in range(pkt_count):
                if self.send_packet(src_addr, src_port, dest_addr, dest_port, pkt_type, pkt_data):
                    count  = count + 1

            print(f"{count} packet(s) sent" )
            input("Press \"Enter\" to return to the main menu.....")
            os.system("cls")
        else:
            print("\nAborted sending a custom packet.")
            input("Press \"Enter\" to return to the main menu.....")
            os.system("cls")

