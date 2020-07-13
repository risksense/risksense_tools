""" *******************************************************************************************************************
|
|  Name        :  update_cmdb.py
|  Description :  Mass-update CMDB fields for hosts based on values in a .csv file.
|  Project     :  risksense_tools
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import os
import sys
import csv
import toml
import risksense_api as rsapi


class CmdbUpdateTool:

    """ CmdbUpdateTool class """

    @staticmethod
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
            return data
        except (Exception, FileNotFoundError, toml.TomlDecodeError) as ex:
            print("Error reading configuration file.")
            print(ex)
            print()
            input("Please press ENTER to close.")
            exit(1)

    def validate_client_id(self, submitted_client_id):

        """
        Validate the supplied CLIENT_ID variable

        :param submitted_client_id:     Client ID to validate
        :type  submitted_client_id:     int

        :raises:    ValueError
        """
        my_client_ids = []

        for client in self.rs.my_clients:
            my_client_ids.append(client['id'])

        if submitted_client_id in my_client_ids:
            pass
        else:
            raise ValueError("User not assigned to the submitted client ID.")

    def get_client_id(self):

        """
        Get the client ID associated with this API key.

        :return:    Client ID
        :rtype:     int

        """

        return self.rs.my_clients[0]['id']

    @staticmethod
    def read_csv_file(filename):

        """
        Read the CSV file, and convert it to a dict.

        :param filename:    Path to csv file to be read.
        :type  filename:    str

        :return:    The data contained in the csv file, in dict format.
        :rtype:     dict
        """

        return_data = []

        input_file = csv.DictReader(open(filename))

        for row in input_file:
            new_row = {}
            for item in row:
                new_row[item] = row[item]
            return_data.append(new_row)

        return return_data

    def send_update_request(self, **kwargs):

        """
        :keyword host:                  Host                (str)
        :keyword os:                    Operating System.   (str)
        :keyword manufacturer:          Manufacturer.       (str)
        :keyword model_id:              Model.              (str)
        :keyword location:              Location.           (str)
        :keyword managed_by:            Managed By.         (str)
        :keyword owned_by:              Owned By.           (str)
        :keyword supported_by:          Supported By.       (str)
        :keyword support_group:         Support Group.      (str)
        :keyword sys_updated_on:        Last Scanned On.    (str)
        :keyword asset_tag:             Asset Tag.          (str)
        :keyword mac_address:           MAC Address.        (str)
        :keyword ferpa:                 FERPA Compliance    (str)
        :keyword hippa:                 HIPPA Compliance    (str)
        :keyword pci:                   PCI Compliance      (str)
        :keyword sys_id:                System ID           (str)
        :keyword cf_1:                  Custom Field 1      (str)
        :keyword cf_2:                  Custom Field 2      (str)
        :keyword cf_3:                  Custom Field 3      (str)
        :keyword cf_4:                  Custom Field 4      (str)
        :keyword cf_5:                  Custom Field 5      (str)
        :keyword cf_6:                  Custom Field 6      (str)
        :keyword cf_7:                  Custom Field 7      (str)
        :keyword cf_8:                  Custom Field 8      (str)
        :keyword cf_9:                  Custom Field 9      (str)
        :keyword cf_10:                 Custom Field 10     (str)
        :keyword asset_criticality:     Asset Criticality   (int)

        :return:    Job ID
        :rtype:     int

        :raises:    RequestFailed
        :raises:    ValueError
        """

        # store the host info in a new variable, and pop it from the kwargs dict
        host = kwargs.get('host', None)
        kwargs.pop('host')

        # Create a new dict for the fields to update
        update_dict = {}

        empty_string = ""

        # Populate the new dict using only the columns that are populated for this host
        for item in kwargs:
            if kwargs[item] != empty_string:
                update_dict[item] = kwargs[item]

        if self.network_type.upper() == 'HOSTNAME':
            search_filter = [
                {
                    "field": "hostname",
                    "exclusive": False,
                    "operator": "EXACT",
                    "value": host
                }
            ]
        else:
            search_filter = [
                {
                    "field": "ipAddress",
                    "exclusive": False,
                    "operator": "EXACT",
                    "value": host
                }
            ]

        # If host isn't blank, build the body, and make the API update request
        if host != empty_string and host is not None:
            # Send API update request
            try:
                job_id = self.rs.hosts.update_hosts_cmdb(search_filter, **update_dict)
            except (rsapi.StatusCodeError, rsapi.MaxRetryError, rsapi.RequestFailed) as ex:
                print(ex)
                raise
        else:
            raise ValueError("There was no host provided for this row.")

        return job_id

    def __init__(self):

        """ Main body of script """

        conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
        config = self.read_config_file(conf_file)

        self.rs_platform = config['platform_url']
        self.api_key = config['api_key']
        self.cmdb_csv_filename = config['cmdb_csv_filename']
        self.network_type = config['network_type']

        #  Instantiate RiskSenseApi
        self.rs = rsapi.RiskSenseApi(self.rs_platform, self.api_key)

        #  Get client id, or validate supplied client ID
        if 'client_id' not in config:
            client_id = self.get_client_id()
        else:
            client_id = config['client_id']
            try:
                self.validate_client_id(client_id)
            except ValueError:
                print(f"Unable to validate that you belong to client ID {client_id}.")
                print("Exiting.")
                sys.exit(1)

        #  Set default client ID
        self.rs.set_default_client_id(client_id)

        #  Read CSV file, and convert data to a dict.
        print(f"Reading csv file...")
        csv_data_dict = self.read_csv_file(self.cmdb_csv_filename)
        total_items = len(csv_data_dict)

        print(f" - {total_items} items found in the .csv file.")
        if total_items == 0:
            print("Exiting...")
            exit(1)

        success_counter = 0
        failure_counter = 0

        print()

        # Loop through each row in the csv data and request an update for each one.
        for item in csv_data_dict:
            # Submit update request to RiskSense Platform
            try:
                job_id = self.send_update_request(**item)
                print(f"Update request for {item['host']} successfully submitted as job {job_id}.")
                success_counter += 1
            except (rsapi.RequestFailed, rsapi.MaxRetryError, rsapi.StatusCodeError, ValueError) as ex:
                print(ex)
                failure_counter += 1

        print()
        print("** DONE **")
        print(f" -- {success_counter}/{total_items} items processed reported successful submission.")
        print(f" -- {failure_counter}/{total_items} items processed did *NOT* report successful submission.")


#
#
#  Execute the script
if __name__ == "__main__":
    try:
        CmdbUpdateTool()
    except KeyboardInterrupt:
        print()
        print("KeyboardInterrupt detected.  Exiting...")
        print()
        sys.exit(0)


"""
   Copyright 2020 RiskSense, Inc.
   
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
