import os
import sys
import toml
import requests
import json
import zipfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rsapi

class gbexport:

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
        conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'conf.toml')
        config = self.read_config_file(conf_file)
        self.rs_platform = config['platform_url']
        self.api_key = config['api_key']
        self.client_id=config['client_id']
        self.filename=config['filename']
        self.groupby=config['groupbyfield']
        self.rs = rsapi.RiskSenseApi(self.rs_platform,self.api_key)
        self.filter={"fileName":f'{self.filename}',"fileType":"CSV","noOfRows":"All","filterRequest":{"filters":[]},"exportableFields":[],"groupByField":f"{self.groupby}"}
        header={"accept":"application/json","x-api-key":f"{self.api_key}","Content-Type":"application/json"}  
        try:
            jobid=(requests.post(url=f'{self.rs_platform}/api/v1/client/{self.client_id}/hostFinding/export',
            headers=header,data=json.dumps(self.filter))).json()
            jobid=jobid['id']
        except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.PageSizeError,
                rsapi.InsufficientPrivileges, rsapi.UserUnauthorized, rsapi.NoMatchFound, ValueError) as ex:
            print(ex)
            print()
            print("Unable to create export job. Exiting")
            sys.exit(1)
                        
        while(True):
                try:
                    exportstatus=self.rs.exports.check_status(self.jobid,self.client_id)
                    print(exportstatus)
                    if exportstatus=='COMPLETE':
                        break
                    elif exportstatus=='ERROR':
                        print('error getting zip file please check ')
                        exit()
                except (rsapi.RequestFailed, rsapi.MaxRetryError, rsapi.StatusCodeError, ValueError) as ex:       
                    print(ex)
                    print()
                    print("Unable to export the file.")
                    sys.exit("Exiting")
        try:   
                self.rs.exports.download_export(self.jobid,f"{self.filename}.zip",self.client_id)
                with zipfile.ZipFile(f"{self.filename}.zip","r") as zip_ref:
                    zip_ref.extractall("findingsdata")
        except(rsapi.RequestFailed, rsapi.MaxRetryError, rsapi.StatusCodeError, ValueError):
                    print(ex)
                    print()
                    print("Unable to retrieve file. Exiting.")
                    sys.exit(1)
            


if __name__ == "__main__":
    try:
        gbexport()
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

