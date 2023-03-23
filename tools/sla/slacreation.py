import os
from platform import platform
import sys
import toml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'lib'))
import risksense_api as rsapi


class getslaoverdue:
        def __init__(self):
            conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'conf.toml')
            config = self.read_config_file(conf_file)
            self.rs_platform = config['platform_url']
            self.api_key = config['api_key']
            self.client_id=config['client_id']
            self.slaname=config['slaname']
            self.description=config['sladescription']
            self.defaultpriority=config['defaultpriority']
            self.grouppriority=config['grouppriority']
            self.actionType=config['actionType']
            self.isdefaultsla=config['isdefaultSLA']
            self.inputdata=config['inputdata']
            self.servicelevelmatrix=config['slamatrix']
            self.updateslavrr=config['updateSLAIfVRRUpdates']
            self.timereference=config['timeReference']
            self.offsetbasis=config['offsetbasis']
            self.sladataoperator=config['sladataoperator']
            self.rs = rsapi.RiskSenseApi(self.rs_platform,self.api_key)   
            self.affectonlynewfindings=config['affectOnlyNewFindings'] 
            self.targetgroupids=config['Targetgroupids']
            self.slamatrixtype=config['slaMatrixProfileType']
            self.slaid= self.getslaname()
            self.targetgroupidslist=[]
            self.targetgroupidslist=[int(x) for x in self.targetgroupids.split(',')]
            self.rs.set_default_client_id(self.client_id)
            if self.isdefaultsla==False:
                print('groupslacreation')
                groupslacreation= self.rs.sla.add_group_sla_rule(self.slaid,self.slaname,self.description,self.grouppriority,self.targetgroupidslist)
            elif self.isdefaultsla==True:
                print('default creation')
                defaultslacreation= self.rs.sla.add_default_sla_rule(self.slaid,self.slaname,self.description,self.defaultpriority,self.actionType,self.timereference,self.servicelevelmatrix,self.slamatrixtype,self.offsetbasis,self.affectonlynewfindings,self.updateslavrr,self.inputdata,self.client_id)
        
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
        def getslaname(self):
                a=self.rs.sla.getslas(self.client_id)
                slaid=a['content'][0]['uuid']
                return slaid


if __name__ == "__main__":
    try:
        getslaoverdue()
    except KeyboardInterrupt:
        print()
        print("KeyboardInterrupt detected.  Exiting...")
        print()
        sys.exit(0)
