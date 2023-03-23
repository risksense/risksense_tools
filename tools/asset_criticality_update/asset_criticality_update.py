""" *******************************************************************************************************************
|
|  Name        :  asset_criticality_update.py
|  Project     :  Asset Criticality Update
|  Description :  A tool to update Asset Criticality values based on values designated in a CSV file.
|  Copyright   :  2021 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import logging
import os
import sys
import csv
import progressbar
import toml
from rich import print
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rs_api


class AssetCriticalityUpdate:

    """ AssetCriticalityUpdate class """

    def __init__(self, config):

        """
        Main body of script.

        :param config:      Configuration
        :type  config:      dict
        """

        logging.info("***** SCRIPT START ***************************************************")

        #  Set variables
        self._rs_platform_url = config['platform_url']
        api_key = config['api_key']
        self.__client_id = config['client_id']
        self.file_to_read = config['file_to_read']
        self.network_type = config['network_type']

        try:
            print()
            print(f"Attempting to talk to RiskSense platform {self._rs_platform_url}")
            self.rs = rs_api.RiskSenseApi(self._rs_platform_url, api_key)
            self.rs.set_default_client_id(self.__client_id)
            print("[green] - Success[/green]")
        except (rs_api.UserUnauthorized, rs_api.InsufficientPrivileges,
                rs_api.MaxRetryError, rs_api.StatusCodeError) as ex:
            message = "An error has occurred while trying to verify RiskSense credentials and connection"
            logging.error(message)
            logging.error(ex)
            print()
            print(f"[red bold]{message}. Exiting.[/red bold]")
            exit(1)

        #  Read the CSV file.
        print()
        print("Attempting to read CSV file")
        self._csv_file_contents = self.read_csv_file()
        print(f" - {len(self._csv_file_contents)} found")

        #  If there are no rows in the CSV file found, exit.
        if len(self._csv_file_contents) == 0:
            print("Exiting.")
            exit(0)

        #  Begin sending updates to RiskSense for each host in the CSV file
        print()
        print("Sending update to RiskSense")
        prog_counter = 0
        row = 1
        prog_bar = progressbar.ProgressBar(max_value=len(self._csv_file_contents))

        for host in self._csv_file_contents:
            self.set_asset_criticality(host['ec2_identifier'], host['netbios'], host['ip_address'], host['hostname'], host['fqdn'], host['dns'], host['mac_addr'], host['scanner_specific_unique_id'], host['criticality'], row)
            row+=1
            prog_counter += 1          
            prog_bar.update(prog_counter)

        prog_bar.finish()

        print()
        print("Done.")
        print()

        logging.info("***** SCRIPT COMPLETE*************************************************")

# ---------------------------------------------------------------------------------------------------------------------

    def set_asset_criticality(self, ec2_identifier, netbios, ip_address, hostname, fqdn, dns, mac_addr, scanner_uuid, criticality, row):
        """
        :keyword ip_address:            IP Address.             (str)
        :keyword hostname:              Hostname.               (str)
        :keyword fqdn:                  FQDN.                   (str)
        :keyword netbios:               Netbios.                (str)
        :keyword ec2_identifier:        EC2 Identifier.         (str)
        :keyword dns:                   DNS.                    (str)
        :keyword mac_id:                MAC Address.            (str)
        :keyword scanner_uuid:          Scanner UUID.           (str)
        :keyword criticality:           Criticality             (str)
        
        """        
        search_filter = []
        empty_string = ''

        if self.network_type.upper() == 'IP':
            filter_ip_network = {
                    "field": "ipAddress",
                    "exclusive": False,
                    "operator": "EXACT",
                    "value": ip_address
            }
            search_filter.append(filter_ip_network)
            if ip_address != empty_string and ip_address is not None: 
                try:
                    job_id = self.rs.hosts.update_hosts_attrs(search_filter, criticality=int(criticality))
                    message = f"Successfully submitted update of criticality to {criticality} for host \"{ip_address}\" as job {job_id}"
                    logging.info(message)
                except (rs_api.UserUnauthorized, rs_api.InsufficientPrivileges,
                        rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.NoMatchFound) as known_ex:
                    message = f"An error has occurred while trying to set criticality to {criticality} for host \"{ip_address}\""
                    logging.error(message)
                    logging.error(known_ex)
                except Exception as ex:
                    message = f"An unexpected error has occurred while trying to set criticality to {criticality} for host \"{ip_address}\""
                    logging.error(message)
                    logging.error(ex)            
        elif self.network_type.upper() == 'HOSTNAME':
            filter_hostname_network = {
                    "field": "hostname",
                    "exclusive": False,
                    "operator": "EXACT",
                    "value": hostname
            }
            search_filter.append(filter_hostname_network)  
            if hostname != empty_string and hostname is not None:   
                try:
                    job_id = self.rs.hosts.update_hosts_attrs(search_filter, criticality=int(criticality))
                    message = f"Successfully submitted update of criticality to {criticality} for host \"{hostname}\" as job {job_id}"
                    logging.info(message)
                except (rs_api.UserUnauthorized, rs_api.InsufficientPrivileges,
                        rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.NoMatchFound) as known_ex:
                    message = f"An error has occurred while trying to set criticality to {criticality} for host \"{hostname}\""
                    logging.error(message)
                    logging.error(known_ex)
                except Exception as ex:
                    message = f"An unexpected error has occurred while trying to set criticality to {criticality} for host \"{hostname}\""
                    logging.error(message)
                    logging.error(ex)                             
        elif self.network_type.upper() == 'MIXED':
            mixed_type_asset_presence = False
            if ip_address != '':
                mixed_type_asset_presence = True
                filter_ip = {
                        "field": "ipAddress",
                        "exclusive": False,
                        "operator": "EXACT",
                        "value": ip_address                
                }
                search_filter.append(filter_ip)

            if hostname != '':
                mixed_type_asset_presence = True
                filter_hostname = {
                        "field": "hostname",
                        "exclusive": False,
                        "operator": "EXACT",
                        "value": hostname                
                }
                search_filter.append(filter_hostname)

            if fqdn != '':
                mixed_type_asset_presence = True
                filter_fqdn = {
                        "field": "fqdn",
                        "exclusive": False,
                        "operator": "EXACT",
                        "value": fqdn                   
                }
                search_filter.append(filter_fqdn)

            if netbios != '':
                mixed_type_asset_presence = True
                filter_netbios = {
                        "field": "netbios",
                        "exclusive": False,
                        "operator": "EXACT",
                        "value": netbios                 
                }
                search_filter.append(filter_netbios)

            if ec2_identifier != '':
                mixed_type_asset_presence = True
                filter_ec2_identifier = {
                        "field": "ec2Identifier",
                        "exclusive": False,
                        "operator": "EXACT",
                        "value": ec2_identifier                 
                }
                search_filter.append(filter_ec2_identifier)

            if dns != '':
                mixed_type_asset_presence = True
                filter_dns = {
                        "field": "dns",
                        "exclusive": False,
                        "operator": "EXACT",
                        "value": dns                 
                }
                search_filter.append(filter_dns)

            if mac_addr != '':
                mixed_type_asset_presence = True
                filter_mac_id = {
                        "field": "macAddress",
                        "exclusive": False,
                        "operator": "EXACT",
                        "value": mac_addr                 
                }
                search_filter.append(filter_mac_id)

            if scanner_uuid != '':
                mixed_type_asset_presence = True
                filter_scanner_uuid = {
                        "field": "source",
                        "exclusive": False,
                        "operator": "EXACT",
                        "value": scanner_uuid                 
                }
                search_filter.append(filter_scanner_uuid) 
            if mixed_type_asset_presence == True:
                try:
                    job_id = self.rs.hosts.update_hosts_attrs(search_filter, criticality=int(criticality))
                    message = f"Successfully submitted update of criticality to {criticality} for row - {row} as job {job_id}"
                    logging.info(message)
                except (rs_api.UserUnauthorized, rs_api.InsufficientPrivileges,
                        rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.NoMatchFound) as known_ex:
                    message = f"An error has occurred while trying to set criticality to {criticality} for row - {row}"
                    logging.error(message)
                    logging.error(known_ex)
                except Exception as ex:
                    message = f"An unexpected error has occurred while trying to set criticality to {criticality} for row - {row}"
                    logging.error(message)
                    logging.error(ex)                        
              


    def read_csv_file(self):

        """
        Read the CSV file, and return a list of dicts representing each row's contents

        :return:    A list of dicts representing each row's contents
        :rtype:     list
        """

        file_contents = []

        try:
            with open(self.file_to_read, 'r') as data:
                for line in csv.DictReader(data):
                    file_contents.append(dict(line))
        except FileNotFoundError as fnfe:
            message = "CSV file not found. Exiting."
            logging.error(message)
            logging.error(fnfe)
            print()
            print(f"[bold red]{message}[/bold red]")
            exit(1)
        except Exception as ex:
            message = "An exception has occurred while trying to read the CSV file. Exiting."
            logging.error(message)
            logging.error(ex)
            print()
            print(f"[bold red]{message}[/bold red]")
            exit(1)

        return file_contents

# ---------------------------------------------------------------------------------------------------------------------


def read_config_file(filename):

    """
    Reads a TOML-formatted configuration file.

    :param filename:    Path to the TOML-formatted file to be read.
    :type  filename:    str

    :return:  Values contained in config file.
    :rtype:   dict
    """

    try:
        data = toml.loads(open(filename).read())
        logging.info("Successfully read config file %s", filename)
        return data
    except (FileNotFoundError, toml.TomlDecodeError) as ex:
        print("Error reading configuration file.")
        print(ex)
        print()
        exit(1)


#  Execute the script
if __name__ == "__main__":

    #  Specify settings For the log
    log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs', f"AssetCriticalityUpdate.log")
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(levelname)s:  %(asctime)s > %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    #  Set config file path, and read the configuration.
    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
    config_contents = read_config_file(conf_file)

    try:
        AssetCriticalityUpdate(config_contents)

    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt detected.  Exiting...")
        print()
        print("KeyboardInterrupt detected.  Exiting...")
        print()
        sys.exit(0)


"""
   Copyright 2021 RiskSense, Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at:

   http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
