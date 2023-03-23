""" *******************************************************************************************************************
|
|  Name        :  import_new_tags.py
|  Description :  Mass-creation of tags in the RiskSense platform.
|  Project     :  risksense_tools
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import os
import sys
import csv
import toml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rsapi


class ImportNewTags:

    """ ImportNewTags class """

    def __init__(self):

        """ Main body of script """

        conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
        config = self.read_config_file(conf_file)

        self.rs_platform = config['platform_url']
        self.api_key = config['api_key']
        self.tag_csv_filename = config['tag_csv_filename']

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
        csv_data_dict = self.read_csv_file(self.tag_csv_filename)

        print()

        #  Attempt creation of tags
        for item in csv_data_dict:
            print(f"Attempting to create tag \"{item['name']}\" ...")

            try:
                new_tag_id = self.create_tag(item)
                print(f" - New tag {item['name']} created as tag ID {new_tag_id}.")
            except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.PageSizeError,
                    rsapi.InsufficientPrivileges, rsapi.UserUnauthorized, rsapi.NoMatchFound, ValueError) as ex:
                print(f" - Unable to create tag.")
                print(ex)

        print()
        print("Done.")

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

    def create_tag(self, tag_info):

        """
        Create a new tag.

        :param tag_info:    Dict containing variables read from the csv file row.
        :type  tag_info:    dict

        :return:    Tag ID
        :rtype:     int

        :raises:    ValueError
        :raises:    RequestFailed
        """

        if "" in tag_info:
            raise ValueError("Fields cannot be blank.")

        acceptable_types = ['COMPLIANCE', 'LOCATION', 'CUSTOM', 'REMEDIATION',
                            'PEOPLE', 'PROJECT', 'SCANNER', 'CMDB']

        if tag_info['tag_type'] not in acceptable_types:
            raise ValueError(f"Tag type is not valid.  Valid types are: {acceptable_types}")

        tag_type = tag_info['tag_type']
        tag_name = tag_info['name']
        tag_desc = tag_info['desc']
        tag_owner = tag_info['owner']
        tag_color = tag_info['color']
        tag_locked = tag_info['locked']

        try:
            tag_id = self.rs.tags.create(tag_type, tag_name, tag_desc, tag_owner, color=tag_color, locked=tag_locked)
        except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.PageSizeError,
                rsapi.InsufficientPrivileges, rsapi.UserUnauthorized, rsapi.NoMatchFound):
            raise

        return tag_id


#  Execute the script
if __name__ == "__main__":
    try:
        ImportNewTags()
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
