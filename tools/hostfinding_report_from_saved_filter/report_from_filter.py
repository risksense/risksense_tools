""" *******************************************************************************************************************
|
|  Name        :  report_from_filter.py
|  Description :  Generate a report as a csv file, based upon a saved hostfinding filter.
|  Project     :  risksense_tools
|  Copyright   :  2020 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import os
import sys
import csv
import toml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rsapi


class HfReportFromFilter:

    """ HfReportFromFilter """

    def __init__(self):

        """ Main body of script """

        #  Read configuration and assign variables based up on config settings.
        conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
        config = self.read_config_file(conf_file)

        self.rs_platform = config['platform_url']
        self.api_key = config['api_key']
        self.saved_filter_name = config['saved_filter_name']
        self.csv_output_filename = config['csv_output_filename']

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

        #  Get filter definition
        try:
            filter_defn = self.get_filter_defn(self.saved_filter_name)
        except (rsapi.RequestFailed, rsapi.MaxRetryError, rsapi.StatusCodeError, ValueError) as ex:
            print(ex)
            print()
            print("Unable to retrieve saved filter definition. Exiting.")
            sys.exit(1)

        #  Get hostfinding details, based on saved filter definition.
        try:
            returned_findings = self.rs.host_findings.search(filter_defn, projection=rsapi.Projection.DETAIL, page_size=1000)
        except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.PageSizeError,
                rsapi.InsufficientPrivileges, rsapi.UserUnauthorized, rsapi.NoMatchFound, ValueError) as ex:
            print(ex)
            print()
            print("An exception has occurred.  Unable to retrieve hostfindings. Exiting.")
            sys.exit(1)

        #  Write findings to .csv file
        self.write_csv_file(returned_findings, self.csv_output_filename)

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

    def get_filter_defn(self, filter_name):

        """
        Get saved filter definition.

        :param filter_name:     Name of filter to find
        :type  filter_name:     str

        :return:    Filter definition
        :rtype:     list

        :raises rsapi.RequestFailed:
        :raises rsapi.MaxRetryError:
        :raises rsapi.StatusCodeError:
        :raises ValueError:
        """

        try:
            returned_filters = self.rs.filters.list_hostfinding_filters()
        except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.PageSizeError,
                rsapi.InsufficientPrivileges, rsapi.UserUnauthorized, rsapi.NoMatchFound):
            raise

        for item in returned_filters:
            if item['name'] == filter_name:
                return item['filters']

        raise ValueError(f"{filter_name} not found.")

    @staticmethod
    def write_csv_file(hf_data, output_filename):

        """
        Write report data to csv file.

        :param hf_data:             HostFinding data
        :type  hf_data:             list

        :param output_filename:     filename to write to
        :type  output_filename:     str

        :return:
        :rtype:
        """

        field_names = []

        for item in hf_data[0]:
            field_names.append(item)

        try:
            with open(output_filename, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=field_names)
                writer.writeheader()
                for item in hf_data:
                    writer.writerow(item)
        except FileNotFoundError as fnfe:
            print("An exception has occurred while attempting to write the .csv file.")
            print()
            print(fnfe)


#  Execute the script
if __name__ == "__main__":
    try:
        HfReportFromFilter()
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
