import json
import os
from platform import platform
import sys
import toml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'lib'))
import risksense_api as rsapi
import zipfile


class slapriority:
    def __init__(self):
            conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'conf.toml')
            config = self.read_config_file(conf_file)
            self.rs_platform = config['platform_url']
            self.api_key = config['api_key']
            self.client_id=config['client_id']
            self.playbookuuid=config['playbookuuid']
            self.rs = rsapi.RiskSenseApi(self.rs_platform,self.api_key)   
            slarequest=self.rs.sla.getslarules(self.client_id,self.playbookuuid)
            groupspecificpriorities= []
            defaultspecific=''
            for i in range(len(slarequest['content'])):
                a=json.loads(slarequest['content'][i]['actionConfig'])
                if a['isDefaultSLA']==False:
                    groupspecificpriorities.append(str(slarequest['content'][i]['priority']))
                if a['isDefaultSLA']==True:
                    defaultspecific=slarequest['content'][i]['priority']
            print('the group specific sla priority numbers are '+ ','.join(groupspecificpriorities))
            print('the default specific sla priority number is '+str(defaultspecific))

        
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
        slapriority()
    except KeyboardInterrupt:
        print()
        print("KeyboardInterrupt detected.  Exiting...")
        print()
        sys.exit(0)
