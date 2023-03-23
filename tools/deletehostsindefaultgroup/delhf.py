import os
import sys
import toml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rsapi

class delete_hostfindings:

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
        "Main body of the script"

        conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'conf.toml')
        config = self.read_config_file(conf_file)
        self.rs_platform = config['platform_url']
        self.api_key = config['api_key']
        self.client_id=config['client_id']
        self.rs = rsapi.RiskSenseApi(self.rs_platform,self.api_key)
        self.rs.set_default_client_id(self.client_id)
        filterlist=[{"field":"group_names","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"Default Group,"}]
        try:
            self.rs.hosts.remove_group(filterlist,7193)
        except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.PageSizeError,
                rsapi.InsufficientPrivileges, rsapi.UserUnauthorized, rsapi.NoMatchFound, ValueError) as ex:
            print(ex)
            print()
            print("Unable to remove hosts from group. Exiting.")
            sys.exit(1)


if __name__ == "__main__":
    try:
        delete_hostfindings()
    except KeyboardInterrupt:
        print()
        print("KeyboardInterrupt detected.  Exiting...")
        print()
        sys.exit(0)

