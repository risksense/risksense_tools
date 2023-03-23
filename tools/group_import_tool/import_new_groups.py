""" *******************************************************************************************************************
|
|  Name        :  import_new_groups.py
|  Description :  Mass creation of groups in the RiskSense platform.
|  Project     :  risksense_tools
|  Copyright   :  (c) RiskSense, Inc. 
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import os
import sys
import toml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rsapi


class ImportNewGroups:

    """ ImportNewGroups class """

    def __init__(self):

        """ Main body of script """

        conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
        config = self.read_config_file(conf_file)

        self.rs_platform = config['platform_url']
        self.api_key = config['api_key']
        self.group_text_filename = config['group_text_filename']

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
        print(f"Reading text file...")
        file_lines = self.read_text_file(self.group_text_filename)

        #  Submit group creation for each item from .csv file
        for item in file_lines:
            try:
                group_id = self.create_group(item['group_name'])
                print(f"New group \"{item['group_name']}\" created as group ID {group_id}")
            except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.InsufficientPrivileges,
                    rsapi.UserUnauthorized, ValueError) as ex:
                print(f"There was an error trying to create new group \"{item['group_name']}\".")
                print(ex)

        print()
        print("Done.  Exiting.")

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
    def read_text_file(filename):

        """
        Read the text file, and return a list of lines.

        :param filename:    Path to text file to be read.
        :type  filename:    str

        :return:    The data contained in the text file, in list format.
        :rtype:     list
        """

        return_data = []

        input_file = open(filename, 'r')
        all_lines = input_file.readlines()

        for line in all_lines:
            return_data.append(line.strip())

        return return_data

    def create_group(self, group_name):

        """
        Create a new group.

        :param group_name:          Group Name
        :type  group_name:          str

        :return:    Group ID
        :rtype:     int

        :raises:    ValueError
        :raises:    RequestFailed
        """

        if group_name == "" or group_name is None:
            raise ValueError("Group Name required.")

        try:
            group_id = self.rs.groups.create(group_name)
        except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.UserUnauthorized, rsapi.InsufficientPrivileges, Exception):
            raise

        return group_id


#
#  Execute the script
if __name__ == "__main__":
    try:
        ImportNewGroups()
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
