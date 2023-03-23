import os
import sys
import toml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rsapi

class sonatype:

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
        
        "Main body of script"

        conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'conf.toml')
        config = self.read_config_file(conf_file)
        self.rs_platform = config['platform_url']
        self.api_key = config['api_key']
        self.client_id=config['client_id']
        self.rs = rsapi.RiskSenseApi(self.rs_platform,self.api_key)
        self.sonatypename=config['connector_name']
        self.networkid=config['networkId']
        self.sonatypeusername=config['sonatype_username']
        self.sonatypepassword=config['sonatype_password']
        self.taginfopull=config['Taginfotobepulled']
        self.createassetifzerovulnfound=config['createAssetsIfZeroVulnFoundInFile']
        self.nexusapitopullapplicationfilter=config['nexusAPIToPullApplicationFilter']
        self.nexustopullstagefilter=config['nexusAPIToPullStageFilter']
        self.sonatypeurl=config['connector_url']
        self.scheduletype=config['schedule_type']
        self.schedulestatus=config['schedule_enabled']
        self.hourofday=config.get('hourOfDay',None)
        self.dayofmonth=config.get('dayofmonth',None)
        self.dayofweek=config.get('dayofweek',None)
        self.autourba=config['autoUrba']
        self.rs.set_default_client_id(self.client_id)

        try:
            connector_details=self.rs.connectors.create_sonatype_connector(self.sonatypename,self.networkid,self.sonatypeurl,self.sonatypeusername,self.sonatypepassword,self.schedulestatus,self.scheduletype,self.taginfopull,self.createassetifzerovulnfound,self.nexusapitopullapplicationfilter,self.nexustopullstagefilter,self.autourba,hour_of_day=self.hourofday,day_of_week=self.dayofweek,day_of_month=self.dayofmonth)
        except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.InsufficientPrivileges, rsapi.UserUnauthorized, ValueError) as ex:
            print(ex)
            print()
            print("An exception has occurred.  Unable to retrieve hostfindings. Exiting.")
            sys.exit(1)

        print(connector_details)
            


if __name__ == "__main__":
    try:
        sonatype()
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

