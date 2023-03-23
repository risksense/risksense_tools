from http import client
import os
import sys
import toml
import requests
import json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rsapi

class gbexport:

    def __init__(self):
        conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'conf.toml')
        config = self.read_config_file(conf_file)
        self.rs_platform = config['platform_url']
        self.api_key = config['api_key']
        self.client_id=config['client_id']
        self.vrrcriticalmax=config['vrrCriticalMax']
        self.vrrhighmax=config['vrrHighMax']
        self.vrrmediummax=config['vrrMediumMax']
        self.vrrlowmax=config['vrrLowMax']
        self.findingcount=config['findingCount']
        self.assettype=config['assetType']
        self.assetcriticality=config['assetCriticality']
        self.assetcategory=config['assetCategory']
        rs3simulateurl=f'{self.rs_platform}/api/v1/client/{self.client_id}/simulate/rs3'
        
        rs3body={
                 "vrrCriticalMax": self.vrrcriticalmax,
                "vrrHighMax": self.vrrhighmax,
                "vrrMediumMax": self.vrrmediummax,
                "vrrLowMax": self.vrrlowmax,
                "findingCount": self.findingcount,
                "assetType": f"{self.assettype}",
                "assetCriticality": self.assetcriticality,
                "assetCategory": f"{self.assetcategory}"
                }
        header={"accept":"application/json","x-api-key":f"{self.api_key}","Content-Type":"application/json"}
        try:
            rs3score=(requests.post(url=rs3simulateurl,headers=header,data=json.dumps(rs3body))).json()
            print('your rs3 score is ',int(rs3score['rs3']))
        except(rsapi.RequestFailed, rsapi.MaxRetryError, rsapi.StatusCodeError, ValueError) as ex:
                print(ex)
                print()
                print("Unable to simulate rs3 score.")
                sys.exit("Exiting")

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
        gbexport()
    except KeyboardInterrupt:
        print()
        print("KeyboardInterrupt detected.  Exiting...")
        print()
        sys.exit(0)
