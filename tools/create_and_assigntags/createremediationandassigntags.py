from http import client
import os
import sys
import toml
import requests
import json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rsapi

class createandassigntags:

    def __init__(self):
        conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'conf.toml')
        config = self.read_config_file(conf_file)
        self.rs_platform = config['platform_url']
        self.api_key = config['api_key']
        self.client_id=config['client_id']
        self.tagname=config['name']
        self.description=config['description']
        self.owner= config['owner']
        self.filter=config['filters']
        self.pathtofile=os.getcwd()
        self.rs = rsapi.RiskSenseApi(self.rs_platform,self.api_key)   
        self.rs.set_default_client_id(self.client_id)
        try:
            remediation_Tag = self.rs.tags.create_remediation_tag(self.tagname,self.description,self.owner)
        except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.InsufficientPrivileges, rsapi.UserUnauthorized, ValueError) as ex:
            print(ex)
            print()
            print("An exception has occurred.  Unable to create remediation tags. Exiting.")
            sys.exit(1)
        print(remediation_Tag)
        try:
            assign_tags=self.rs.application_findings.add_tag(self.filter,remediation_Tag)
        except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.InsufficientPrivileges, rsapi.UserUnauthorized, ValueError) as ex:
            print(ex)
            print()
            print("An exception has occurred.  Unable to retrieve hostfindings. Exiting.")
            sys.exit(1)
        print(assign_tags)





    def read_config_file(self,filename):
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
                exit(1)

if __name__ == "__main__":
    try:
        createandassigntags()
    except KeyboardInterrupt:
        print()
        print("KeyboardInterrupt detected.  Exiting...")
        print()
        sys.exit(0)
