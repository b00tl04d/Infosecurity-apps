"""
Nmap Scanner Script

StudentID: p2243452
Name: Seah Kwan Hock Reuben
Class: DISM/FT/1B/04
Assessment: CA1-2

Script name:
    nmap_scanner.py

Purpose:
    Nmap scanner module script that allows the user to perform a selected port scan option on a network target

Usage syntax:
    Nil, intended to be used as a custom module

Input file(s):
    Nil

Output file(s):
    Nil

Python version:
    Python 3.10.9

Reference:
https://geektechstuff.com/2020/06/03/python-and-nmap-scanning-for-hosts-python/
https://rich.readthedocs.io/en/stable/tables.html
https://rich.readthedocs.io/en/stable/reference/table.html#rich.table.Table.add_row
https://rich.readthedocs.io/en/stable/appendix/box.html#appendix-box
https://rich.readthedocs.io/en/stable/live.html
https://nmap.org/book/man-misc-options.html
https://pypi.org/project/python-nmap/

Library/Module:
- modules used that are installed by default in Python 3.10.9
    - os
    - re
- required external modules installed using pip: pip install <module name>  # e.g. pip install rich
    - python-nmap
    - rich

Known issues:
    Nil


"""

import os
import re
import nmap
from rich import box
from rich.table import Table
from rich.console import Console


class CustomNmapScanner():
    """
    A class for using a Custom Nmap Scanner

    Attributes:
        Nil

    Methods:
        __init__():
            Initialize and get all the required variables such as the scan results

        
        perform_scan():
            Execute an nmap scan

            Args:
                ip (str): IP address(es) or hostnames to scan

        
        validate_host(hosts)
            Use regex to validate host(s) that is entered

            Args:
                host (list): list of hostnames or ipv4 addresses to validate

            Returns:
                bool: If a hostname or ipv4 address is invalid return False, else return True


        display_scan_output():
            Display type of nmap scan, the host(s) scanned, type of scan results, and scan results in a table
    """

    # Initializer
    def __init__(self) -> None:
        """
        Initialize and get all the required variables such as the scan results
        """
        self.nmScan = nmap.PortScanner()
        self.hosts = input("Targets to scan (space separated for multiple hosts): ")
        self.host_ls = self.hosts.split()
        self.validation_flag = self.validate_host(hosts=self.host_ls)

        while True:
            if self.validation_flag:
                print("Scanning.....")
                self.perform_scan(ip=self.hosts)
                break

            os.system("cls")
            print("Please enter valid hostnames or IPv4 addresses that are separated by a space")
            self.hosts = self.get_hosts()
            self.host_ls = self.hosts.split()
            self.validation_flag = self.validate_host(hosts=self.host_ls)


    # User-defined method
    def perform_scan(self, ip: str):
        """
        Execute an nmap scan

        Args:
            ip (str): IP address(es) or hostnames to scan
        """
        # Aggressive scan option "-A" includes OS and version detection along with script scanning and traceroute
        options = "-sTU -T5 -A --top-ports 10 --reason -vv -Pn"  
        self.nmScan.scan(hosts=ip, arguments=options)


    # User-defined method
    def validate_host(self, hosts: list) -> bool:
        """
        Use regex to validate host(s) that is entered

        Args:
            host (list): list of hostnames or ipv4 addresses to validate

        Returns:
            bool: If a hostname or ipv4 address is invalid return False, else return True
        """
        numbers_only_pattern = r"^\d+$"
        hostname_pattern = r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
        ipv4_addr_pattern = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$" 

        if len(hosts) < 1:
            return False

        for host in hosts:
            if re.match(pattern=numbers_only_pattern, string=host):
                return False
            elif re.match(pattern=hostname_pattern, string=host) == False and re.match(pattern=ipv4_addr_pattern, string=host) == False:
                return False
        return True 


    # User-defined method
    def display_scan_output(self):
        """
        Display type of nmap scan, the host(s) scanned, type of scan results, and scan results in a table
        """
        # Initialize rich table
        table = Table(box=box.SQUARE, show_lines=True)

        # Add rich table columns
        table.add_column(header="Host", no_wrap=True)
        table.add_column(header="Hostname", no_wrap=True)
        table.add_column(header="Protocol", no_wrap=True)
        table.add_column(header="Port ID", no_wrap=True)
        table.add_column(header="State", no_wrap=True)
        table.add_column(header="Product", no_wrap=True)
        table.add_column(header="Extrainfo", no_wrap=True)
        table.add_column(header="Reason", no_wrap=True)
        table.add_column(header="CPE", no_wrap=True)

        # Extract information for the table
        for host in self.nmScan.all_hosts():
            for protocol in self.nmScan[host].all_protocols():
                for port in self.nmScan[host][protocol]:
                    hostname = self.nmScan[host].hostname()
                    state = self.nmScan[host][protocol][port]["state"]
                    product = self.nmScan[host][protocol][port]["product"]
                    extrainfo = self.nmScan[host][protocol][port]["extrainfo"]
                    reason = self.nmScan[host][protocol][port]["reason"]
                    cpe = self.nmScan[host][protocol][port]["cpe"]

                    # Unable to use named arguments for the "add_row" function as it uses the unpacking operator "*" 
                    # Add table rows with each component of the nmap scan result to the respective columns, i.e. hostname to the Hostname column
                    table.add_row(host, hostname, protocol, str(port), state, product, extrainfo, reason, cpe)
        
        # Display nmap scan details
        print(f"Type of nmScan: {type(self.nmScan)}")
        print(f"Scanning Ports: {self.hosts}")
        print(f"Type of results: {type(self.nmScan._scan_result)}")

        # Display nmap scan results using the rich table
        console = Console()
        console.print(table)
