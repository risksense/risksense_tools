import os
import sys
import toml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rsapi

class hclappscancreate:

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

    def __init__(self):
        print(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
        conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'conf.toml')
        config = self.read_config_file(conf_file)
        self.rs_platform = config['platform_url']
        self.api_key = config['api_key']
        self.client_id=config['client_id']
        self.rs = rsapi.RiskSenseApi(self.rs_platform,self.api_key)
        self.access_key=config['username']
        self.secret_key=config['password']
        self.connector_name=config['connector_name']
        self.networkid=config['networkId']
        self.connectorurl=config['connector_url']
        self.scheduletype=config['schedule_type']
        self.hourofday=config['hourOfDay']
        self.rs.set_default_client_id(self.client_id)
            
        try:
            connector_details=self.rs.connectors.create_hclappscan(self.connector_name,self.connectorurl,self.scheduletype,self.networkid,self.access_key,self.secret_key,auto_urba=False,hour_of_day=self.hourofday)
        except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.InsufficientPrivileges, rsapi.UserUnauthorized, ValueError) as ex:
            print(ex)
            print()
            print("An exception has occurred. Unable to create connector. Please check your configuration parameters and also your internet connection. Exiting.")
            sys.exit(1)
        print(connector_details)


if __name__ == "__main__":
    try:
        hclappscancreate()
    except KeyboardInterrupt:
        print()
        print("KeyboardInterrupt detected.  Exiting...")
        print()
        sys.exit(0)


        

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

