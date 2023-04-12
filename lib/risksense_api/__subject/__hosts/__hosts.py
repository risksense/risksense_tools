"""
**Hosts module defined for different hosts related api endpoints.**
"""
""" *******************************************************************************************************************
|
|  Name        :  __hosts.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating Hosts on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

from email.quoprimime import body_length
import json
from re import I

from risksense_api import FilterSubject
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
from ..__filters import Filters
from ..__exports import Exports
import zipfile
import sys
import csv
import pandas as pd



class Hosts(Subject):

    """ **Class for Hosts function defintions**.

    To utlise Hosts function:

    Args:
            profile:     Profile Object
    
    Usage:
        :obj:`self.{risksenseobjectname}.hosts.{function}`
    
    Examples:
        To get dynamic columns using :meth:`getdynamiccolumns` function

        >>> self.rs.hosts.getdynamiccolumns()

    """

    def __init__(self, profile:object):

        """**Initialization of Hosts Object** .

        Args:
            profile:     Profile Object

        """

        self.subject_name = "host"
        Subject.__init__(self, profile, self.subject_name)
        self.alt_base_api_url=self.profile.platform_url + "/api/v1/client/{}/search/{}"

    def downloadfilterinexport(self,filename:str,filters:list,client_id:int=None):
        
        """ **Exports and Downloads a file based on the filters defined** .


        Args:
            filename: Name of the file to export as
            filters:  Host search filters based on which the export performs
            client_id: The client id to get the data from. If not supplied, takes default client id
        
        **IGNORE INTERNAL FUNCTION**

        Examples:
            >>>  self.{risksenseobject}.hosts.downloadfilterinexport('hostdata',[])
        """
        if client_id is None:
            client_id= self._use_default_client_id()
        exportid=self.export(filters,file_name=filename)
        self.exports=Exports(self.profile)
        while(True):
                try:
                    exportstatus=self.exports.check_status(exportid)
                    if exportstatus=='COMPLETE':
                        break
                    elif exportstatus=='ERROR':
                        print('error getting zip file please check ')
                        exit()
                except (RequestFailed,MaxRetryError,StatusCodeError, ValueError) as ex:       
                    print(ex)
                    print()
                    print("Unable to export the file.")
                    sys.exit("Exiting")
        try:   
                self.exports.download_export(exportid,f"{filename}.csv")
        except(RequestFailed,MaxRetryError,StatusCodeError, ValueError):
                    print(ex)
                    print()
                    print("Unable to retrieve file. Exiting.")
                    sys.exit(1)
  


    def create(self, group_id:int,group_ids:list, assessment_id:int, network_id:int, ip_address:str, hostname:str, subnet:str, disc_date:str, client_id:int=None,scannerFirstDiscoveredOn:str=None,scannerlastDiscoveredOn:str=None,services:list=None,criticality:int=None,os_scanner:int=None,createcmdb:dict=None,lockCmdb:dict=None)->int:

        """
        Creates a host based on the data provided by the user.

        Args:
            
            group_id:        Group ID
            group_ids:       Group IDs
            assessment_id:   Assessment ID 
            network_id:      Network ID
            ip_address:      IP Address of host
            hostname:        Hostname
            subnet:          Subnet host belongs to
            disc_date:       Discovered Date (Date formatted as "YYYY-MM-DDTHH:MM:SS")
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Keyword Args:
            scanner_first_discovered_on(``str``): Scanner First Discovered On 
            scanner_last_discovered_on(``str``): Scanner Last Discovered On       
            criticality(``int``):       int     1-5
            services(``list``):          list    A list of dicts, each dict containing :obj:`portNumber(int)`, and :obj:`name (str)`
            os_scanner(`str`):        dict    A dict containing 
                                                :obj:`name (str)`, :obj:`family(str)`,  :obj: `class(str)`,
                                                 :obj:`vendor(str)`, :obj:`product (str)`, and :obj:`certainty (int)`
            createcmdb(`dict`): dict
            lockCmdb(`dict`): dict


        Return:
                The host ID on the platform is returned.

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))
        body = {
            "groupId": group_id,
            "groupIds": group_ids,
            "assessmentId": assessment_id,
            "networkId": network_id,
            "ipAddress": ip_address,
            "subnet": subnet,
            "hostName": hostname,
            "discoveredDate": disc_date,
            "scannerFirstDiscoveredOn":scannerFirstDiscoveredOn,
            "scannerLastDiscoveredOn":scannerlastDiscoveredOn,
            "services": services,
            "criticality": criticality,
            "operatingSystemScanner": os_scanner,
            "createCmdb": createcmdb,
            "lockCmdb":lockCmdb
        }


        body = self._strip_nones_from_dict(body)
        body['createCmdb'] = self._strip_nones_from_dict(body['createCmdb'])
        print(body)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']



        return job_id
    

    def getdynamiccolumns(self,client_id:int=None)->list:
        
        """
        Gets Dynamic columns for the hosts.

        Args:
            client_id: If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The Dynamic columns

        Examples:
            >>>  self.{risksenseobject}.hosts.getdynamiccolumns()
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.alt_base_api_url.format(str(client_id),self.subject_name) + "/dynamic-columns"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error in getting dynamic columns')
            print(e)
            exit()
        jsonified_response = json.loads(raw_response.text)
             
        return jsonified_response


    def list_host_filter_fields(self,client_id:int=None)->list:

        """
        Lists all the host filter data from the platform

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The JSON output from the platform is returned, listing the available filters.

        Examples:
            >>>  self.{risksenseobject}.hosts.list_host_filter_fields()            
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/filter'
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)

        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_host_trend_information(self,assetids:list,fields:list,includemonthlytrend:bool=True,includeweeklytrend:bool=True,client_id:int=None)->list:

        """
        Search for trend informatin for host

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            assetids:        List of assetids to get trend information
            fields:          Status fields list , open,closed or both in list
            includemonthlytrend: Include monthly trend, true to include, false to not
            includeweeklytrend   Include weekly trend, true to include, false to not

        Return:
            The JSON output from the platform is returned, listing the jsonified response.

        Examples:
            >>>  self.{risksenseobject}.hosts.get_host_trend_information(assetids,fields)            
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/trend'

        body={
                "assetIds": assetids,
                "includeWeeklyTrend": includemonthlytrend,
                "includeMonthlyTrend": includeweeklytrend,
                "fields": fields
                }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)

        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response


    def delete(self, search_filters:list,csvdump:bool=False, client_id:int=None)->int:

        """
        Delete hosts based on provided filters.

        Args:
            search_filters:      A list of dictionaries containing filter parameters.

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The delete Job ID
        
        Examples:
            To delete a host:

            >>>  self.{risksenseobject}.hosts.delete([])
        
        Note:
            You can also dump the data of the hosts that are going to be deleted in a csv file using :obj:`csvdump=True` argument:
            
            >>>  self.{risksenseobject}.hosts.delete([],csvdump=True)

        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/delete"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        body = {
            "filterRequest": {
                "filters": search_filters
            }
        }
        if csvdump==True:
            self.downloadfilterinexport('hostexportbeforedeletion',search_filters) 
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def get_groupby_host(self,client_id:int=None)->dict:

        """
        Gets all the groupby fields for hosts

        Args:
            client_id:      The client id , if none, default client id is taken

        Return:
            The group by key metrics
        **IGNORE INTERNAL FUNCTION**
        Example:
            >>>  self.{risksenseobject}.hosts.get_groupby_host()
        
        Note:
            This function just returns the groupbyfields
        
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/group-by"

        try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        jsonified_response = json.loads(raw_response.text)

        hostgroupbykeymetrics={}

        for i in range(len(jsonified_response['groupByFields'])):
            hostgroupbykeymetrics[jsonified_response['groupByFields'][i]['key']]=[jsonified_response['groupByFields'][i]['groupMetrics'][j]['key'] for j in range(len(jsonified_response['groupByFields'][i]['groupMetrics']))]

            
        return hostgroupbykeymetrics


    def post_groupby_host(self,filters:list=[],sortorder:str=None,csvdump:bool=False,client_id:int=None)->dict:

        """
        Gets the groupby values for hosts based on the filter provided

        Args:  
            filters:        The filters which will populate in groupby
            sortorder: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
            csvdump:         dumps the data in csv
            client_id:      The client id , if none, default client id is taken
        
        Return:
            The hosts data grouped based on the particular field provided
        
        Example:

            >>>  self.{risksenseobject}.hosts.post_groupby_host({filter})
        
            The filter must be provided for the group by to be used. The groupby fields will be displayed in the `terminal` and you must choose a `group by` filter to which the data will be populated      

        Note:
            This function also has an option to dump the data in a csv by a simple argument, :obj:`csvdump=True`

            >>>  self.{risksenseobject}.hosts.post_groupby_host({filter},csvdump=True)
        
        """
        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/group-by"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        hostslist=self.get_groupby_host()

        hostskeys=list(hostslist.keys())
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            for i in range(len(hostskeys)):
                print(f'Index-{i},Key:{hostskeys[i]}')
            keymetric=hostskeys[int(input('Please enter the key for group by parameter:'))]
        except IndexError as ex:
                print()
                print('There was an error fetching group by data')
                print('Please enter an index number from the above list')
                print(ex)
                exit()
        except (Exception) as e:
                print('There was an error fetching group by data')
                print(e)
                exit()
        if sortorder is None:
            sortorder=[{"field":keymetric,"direction":"ASC"}]

        body = {
                "key": keymetric,
                "metricFields": hostslist[keymetric],
                "filters": filters,
                "sortOrder": sortorder
                }
        try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)
            
        
        if csvdump==True:
            field_names = []
            for item in jsonified_response['data'][0]:
                field_names.append(item)

            try:
                with open('hostgroupby.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response['data']:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)    
        return jsonified_response

    def update_hosts_attrs(self, search_filters:list,csvdump:bool=False, client_id:int=None, **kwargs)->int:

        """
        This function updates hosts attributes based on search filters

        Args:
            search_filters:      A list of dictionaries containing filter parameters.
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:         dumps the data in csv

        Keyword Args:
                ip_address(``str``):  IP Address of host
                hostname(``str``):    Hostname
                subnet(``str``):      Subnet host belongs to
                discovered_date(``str``): Date formatted as "YYYY-MM-DD"
                criticality(``int``):      1-5
                services(``int``):        A list of dicts, each dict containing :obj:`portNumber(int)`, and :obj:`name (str)`
                os_scanner(``dict``):    A dict containing :obj:`name(str)`, :obj:`family (str)`, :obj:`class(str)`, :obj:`vendor(str)`, :obj:`product(str)`, and :obj:`certainty(int)`
        
        Return:
                The host ID on the platform is returned.
        
        Example:

            >>> self.{risksenseobject}.hosts.update_hosts_attrs([],criticality=2)

            An example to change the host attributes based on ip address

        Note:
            
            You can also dump the job id data in a csv by simply using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.hosts.update_hosts_attrs([],criticality=3,csvdump=True)

        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update"

        ip_address = kwargs.get("ip_address", None)
        hostname = kwargs.get("hostname", None)
        subnet = kwargs.get("subnet", None)
        discovered_date = kwargs.get("discovered_date", None)
        criticality = kwargs.get("criticality", None)
        services = kwargs.get("services", None)
        os_scanner = kwargs.get("os_scanner", None)
        edit_cmdb= kwargs.get('edit_cmdb',None)


        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "ipAddress": ip_address,
            "hostname": hostname,
            "subnet": subnet,
            "discoveredDate": discovered_date,
            "criticality": criticality,
            "services": services,
            "operatingSystemScanner": os_scanner,
            "editCmdb": edit_cmdb
             
            }
        body = self._strip_nones_from_dict(body)
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            hostid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(hostid)
            df.to_csv('hostupdated.csv',index=False)

        return job_id

    def update_hosts_cmdb(self, search_filters:list, client_id:int=None, **kwargs)->int:

        """
        Updates host cmdb
        
        Args:

            search_filters:      A list of dictionaries containing filter parameters.
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Keyword Args:

            manufacturer(``str``):   Manufacturer
            model_id(``str``):    Model id
            mac_address(``str``):       Mac Address
            location(``str``):          Location
            managed_by(``str``):        Managed By
            owned_by(``str``):          Owned By
            supported_by(``str``):      Supported By
            support_group(``str``):     Support Group
            sys_id(``str``):            Sys id
            os(``str``):                Operating System
            last_scan_date(``str``):    Date formatted as "YYYY-MM-DD"
            asset_tag(``str``):                 Asset Tag
            ferpa(``bool``):             Ferpa
            hipaa(``bool``):             Hipaa
            pci(``bool``):               PCI
            cf_1(``str``):              Custom field_1
            cf_2(``str``):              Custom field_2
            cf_3(``str``):              Custom field_3
            cf_4(``str``):              Custom field_4
            cf_5(``str``):              Custom field_5
            cf_6(``str``):              Custom field_6
            cf_7(``str``):              Custom field_7
            cf_8(``str``):              Custom field_8
            cf_9(``str``):              Custom field_9
            cf_10(``str``):             Custom field_10
            am_1(``str``):              Asset Matching field_1
            am_2(``str``):              Asset Matching field_2
            am_3(``str``):              Asset Matching field_3
        
        Return:
              The job ID

        Example:
            An example to update hosts cmdb with manufacturer name or model id
            
            >>> self.{risksenseobject}.hosts.update_hosts_cmdb([],manufacturer='manufacturername',model_id='R1234')

            Use the keyword arguments depending on what cmdb data you need to update

        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update"

        o_s = kwargs.get("os", None)
        manufacturer = kwargs.get("manufacturer", None)
        model_id = kwargs.get("model_id", None)
        location = kwargs.get("location", None)
        managed_by = kwargs.get("managed_by", None)
        owned_by = kwargs.get("owned_by", None)
        supported_by = kwargs.get("supported_by", None)
        support_group = kwargs.get("support_group", None)
        sys_id = kwargs.get('sys_id', None)
        mac_address = kwargs.get("mac_address", None)
        last_scan_date = kwargs.get("last_scan_date", None)
        asset_tag = kwargs.get("asset_tags", None)
        ferpa = kwargs.get("ferpa", None)
        hipaa = kwargs.get("hipaa", None)
        pci = kwargs.get("pci", None)
        cf_1 = kwargs.get("cf_1", None)
        cf_2 = kwargs.get("cf_2", None)
        cf_3 = kwargs.get("cf_3", None)
        cf_4 = kwargs.get("cf_4", None)
        cf_5 = kwargs.get("cf_5", None)
        cf_6 = kwargs.get("cf_6", None)
        cf_7 = kwargs.get("cf_7", None)
        cf_8 = kwargs.get("cf_8", None)
        cf_9 = kwargs.get("cf_9", None)
        cf_10 = kwargs.get("cf_10", None)
        am_1 = kwargs.get("am_1", None)
        am_2 = kwargs.get("am_2", None)
        am_3 = kwargs.get("am_3", None)   

        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "editCmdb": {
                "manufacturer": manufacturer,
                "model_id": model_id,
                "location": location,
                "managed_by": managed_by,
                "owned_by": owned_by,
                "supported_by": supported_by,
                "support_group": support_group,
                "sys_id": sys_id,
                "mac_address": mac_address,
                "os": o_s,
                "sys_updated_on": last_scan_date,
                "asset_tag": asset_tag,
                "ferpa": ferpa,
                "hipaa": hipaa,
                "pci": pci,
                "cf_1": cf_1,
                "cf_2": cf_2,
                "cf_3": cf_3,
                "cf_4": cf_4,
                "cf_5": cf_5,
                "cf_6": cf_6,
                "cf_7": cf_7,
                "cf_8": cf_8,
                "cf_9": cf_9,
                "cf_10": cf_10,
                "am_1": am_1,
                "am_2": am_2,
                "am_3": am_3 
            }
        }

        body['editCmdb'] = self._strip_nones_from_dict(body['editCmdb'])

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            
            jsonified_response = json.loads(raw_response.text)
            job_id = jsonified_response['id']

            return job_id
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        raise
       

    def lock_hosts_cmdb(self, search_filters:list, client_id:int=None, **kwargs):

        """
        Locks The hosts cmdb data

        Args:
            search_filters:      A list of dictionaries containing filter parameters.
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Keyword Args:
            manufacturer(``str``):   Manufacturer
            business_criticality(``int``): business criticality
            model_id(``str``):    Model id
            mac_address(``str``):       Mac Address
            location(``str``):          Location
            managed_by(``str``):        Managed By
            owned_by(``str``):          Owned By
            supported_by(``str``):      Supported By
            support_group(``str``):     Support Group
            sys_id(``str``):            Sys id
            os(``str``):                Operating System
            last_scan_date(``str``):    Date formatted as "YYYY-MM-DD"
            asset_tag(``str``):                 Asset Tag
            ferpa(``bool``):             Ferpa
            hipaa(``bool``):             Hipaa
            pci(``bool``):               PCI
            cf_1(``str``):              Custom field_1
            cf_2(``str``):              Custom field_2
            cf_3(``str``):              Custom field_3
            cf_4(``str``):              Custom field_4
            cf_5(``str``):              Custom field_5
            cf_6(``str``):              Custom field_6
            cf_7(``str``):              Custom field_7
            cf_8(``str``):              Custom field_8
            cf_9(``str``):              Custom field_9
            cf_10(``str``):             Custom field_10
            am_1(``str``):              Asset Matching field_1
            am_2(``str``):              Asset Matching field_2
            am_3(``str``):              Asset Matching field_3

        Return:
            The job ID

        Example:
            An example to lock hosts cmdb with manufacturer name or model id
            
            >>> self.{risksenseobject}.hosts.lock_hosts_cmdb([],business_criticality=437)

            Use the keyword arguments depending on what cmdb data you need to lock
    
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update"

        os = kwargs.get("os", None)
        manufacturer = kwargs.get("manufacturer", None)
        model_id = kwargs.get("model_id", None)
        location = kwargs.get("location", None)
        managed_by = kwargs.get("managed_by", None)
        owned_by = kwargs.get("owned_by", None)
        supported_by = kwargs.get("supported_by", None)
        support_group = kwargs.get("support_group", None)
        sys_id = kwargs.get('sys_id', None)
        mac_address = kwargs.get("mac_address", None)
        last_scan_date = kwargs.get("last_scan_date", None)
        asset_tag = kwargs.get("asset_tags", None)
        ferpa = kwargs.get("ferpa", None)
        hipaa = kwargs.get("hipaa", None)
        pci = kwargs.get("pci", None)
        cf_1 = kwargs.get("cf_1", None)
        cf_2 = kwargs.get("cf_2", None)
        cf_3 = kwargs.get("cf_3", None)
        cf_4 = kwargs.get("cf_4", None)
        cf_5 = kwargs.get("cf_5", None)
        cf_6 = kwargs.get("cf_6", None)
        cf_7 = kwargs.get("cf_7", None)
        cf_8 = kwargs.get("cf_8", None)
        cf_9 = kwargs.get("cf_9", None)
        cf_10 = kwargs.get("cf_10", None)
        am_1 = kwargs.get("am_1", None)
        am_2 = kwargs.get("am_2", None)
        am_3 = kwargs.get("am_3", None)   
        business_criticality=kwargs.get("business_criticality",None)
        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "lockCmdb": {
                "manufacturer": manufacturer,
                "model_id": model_id,
                "location": location,
                "managed_by": managed_by,
                "owned_by": owned_by,
                "supported_by": supported_by,
                "support_group": support_group,
                "sys_id": sys_id,
                "mac_address": mac_address,
                "os": os,
                "sys_updated_on": last_scan_date,
                "asset_tag": asset_tag,
                "ferpa": ferpa,
                "hipaa": hipaa,
                "pci": pci,
                "cf_1": cf_1,
                "cf_2": cf_2,
                "cf_3": cf_3,
                "cf_4": cf_4,
                "cf_5": cf_5,
                "cf_6": cf_6,
                "cf_7": cf_7,
                "cf_8": cf_8,
                "cf_9": cf_9,
                "cf_10": cf_10,
                "am_1": am_1,
                "am_2": am_2,
                "am_3": am_3,
                "busines_criticality":business_criticality 
            }
        }

        body['lockCmdb'] = self._strip_nones_from_dict(body['lockCmdb'])

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def get_single_search_page(self, search_filters:list, projection:str=Projection.BASIC, page_num:int=0, page_size:int=150,
                               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC, client_id:int=None)->dict:

        """
        Searches for and returns hosts based on the provided filter(s) and other parameters.
        This gets paginated results data

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            projection:      Projection to be used in API request.  Projection.BASIC or Projection.DETAIL
            page_num:        The page number of results to be returned.
            page_size:       The number of results per page to be returned.
            sort_field:      The field to be used for sorting results returned.
            sort_dir:        The direction of sorting to be used. SortDirection.ASC or SortDirection.DESC
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:    
            The JSON response from the platform is returned.
        
        Example:
            An example to get single search page of hosts data
            
            >>> self.{risksenseobject}.hosts.get_single_search_page([])

            You can also try changing the other arguments to your liking to reflect the data as you suffice such as change page_size or page_num etc.

            >>> self.{risksenseobject}.hosts.get_single_search_page([],page_num=2,page_size=10)
        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/search"

        body = {
            "filters": search_filters,
            "projection": projection,
            "sort": [
                {
                    "field": sort_field,
                    "direction": sort_dir
                }
            ],
            "page": page_num,
            "size": page_size
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def search(self, search_filters:list, projection:str=Projection.BASIC, page_size:int=150,sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC, csvdump:bool=False,client_id:int=None)->list:

        """
        Searches for and returns hosts based on the provided filter(s) and other parameters.  Rather than returning paginated results, this function cycles through all pages of results and returns them all in a single list.
        
        Args:

            search_filters:  A list of dictionaries containing filter parameters.
            projection:      Projection to be used in API request.  Projection.BASIC or Projection.DETAIL
            page_size:       The number of results per page to be returned.
            sort_field:      The field to be used for sorting results returned.
            sort_dir:        The direction of sorting to be used. SortDirection.ASC or SortDirection.DESC
            csvdump:         dumps the data in csv
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
                A list containing all hosts returned by the search using the filter provided.
        
        Example:
            An example to search for host data is
            
            >>> self.{risksenseobject}.hosts.search([])

            Where :obj:`[]` is the search filter for all hosts, you can provide your search filter there.

        Note:
            You can also dump the search based data in a csv by simply providing :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.hosts.search([],csvdump=True)

        """

        func_args = locals()
        func_args.pop('self')
        func_args.pop('csvdump')

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        try:
            page_info = self._get_page_info(self.subject_name, search_filters, page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed, Exception):
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        if csvdump==True:
            self.downloadfilterinexport('hostdata',search_filters) 

        return all_results

    def get_count(self, search_filters:list, client_id:int=None)->int:

        """
        Gets a count of hosts identified using the provided filter(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
                The number of hosts identified using the provided filter(s).
        
        Example:
            An example to use get count function is as follows
            
            >>> self.{risksenseobject}.hosts.get_count([])

            Where :obj:`[]` is the search filter for all hosts, you can provide your search filter there.

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            page_info = self._get_page_info(self.subject_name, search_filters=search_filters, client_id=client_id)
            count = page_info[0]
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return count
    
    def add_tag(self, search_filters:list, tag_id:int,csvdump:bool=False, client_id:int=None)->int:

        """
        Adds a tag to host(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            tag_id:          ID of tag to tbe added to host(s).
            csvdump:         dumps the data in csv
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
                The job ID is returned.
        Example:
            An example to add a tag is 
            
            >>> self.{risksenseobject}.hosts.add_tag([],1234)

            Where 
            
            :obj:`[]` is the search filter for all hosts, you can provide your search filter there.

            :obj:`1234` is the tag id

        Note:
            You can also dump the hosts from the search filters post the tag completion for more information by :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.hosts.add_tag([],1234,csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/tag"

        body = {
            "tagId": tag_id,
            "isRemove": False,
            "filterRequest": {
                "filters": search_filters
            }
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
                self.downloadfilterinexport('addtag',search_filters) 
        return job_id

    def remove_tag(self, search_filters:list, tag_id:int,csvdump:bool=False, client_id:int=None)->int:

        """
        Removes a tag from host(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            tag_id:          ID of tag to be removed from host(s).
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:         dumps the data in csv

        Return:    
            The job ID is returned.
        
        Example:
            An example to use remove tag is
            
            >>> self.{risksenseobject}.hosts.remove_tag([],123)

            Where 
            
            :obj:`[]` is the search filter for all hosts, you can provide your search filter there.
            
            :obj:`123` is the tag id

        Note:
            You can also dump the hosts which the tags will be removed from with a :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.hosts.remove_tag([],123,csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        url = self.api_base_url.format(str(client_id)) + "/tag"

        if csvdump==True:
            self.downloadfilterinexport('hostremovetag',search_filters) 

        body = {
            "tagId": tag_id,
            "isRemove": True,
            "filterRequest": {
                "filters": search_filters
            }
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id


    def getexporttemplate(self,client_id:int=None)->list:
        
        """
        Gets configurable export template for Hosts.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The Exportable fields

        Example:
            An example to use getexporttemplate
                
                >>> self.{risksenseobject}.hosts.getexporttemplate()

            This gets all the export templates for hosts
    
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/export/template"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        exportablefilter = json.loads(raw_response.text)

        for i in range(len(exportablefilter['exportableFields'])):
            for j in range(len(exportablefilter['exportableFields'][i]['fields'])):
                if exportablefilter['exportableFields'][i]['fields'][j]['selected']==False:
                    exportablefilter['exportableFields'][i]['fields'][j]['selected']=True

        return exportablefilter['exportableFields']

    def merge_host(self, search_filter:list,host_id_to_merge_to:int,csvdump:bool=False, client_id:int=None)->int:

        """
        Merges host(s).

        Args:
            search_filter:  A list of dictionaries containing filter parameters.
            host_id_to_merge_to:  The host id to which the hosts based on the filter will be merged to
            csvdump:         dumps the data in csv
            client_id:       Client ID.  If an ID isn't passed, it will use the profile's default Client ID.
        Return:
            The job ID is returned.
        Example:
            An example to use merge_host is
            
                >>> self.{risksenseobject}.hosts.merge_host([],123)

            Where
            
                :obj:`[]` is the search filter for all hosts, you can provide your search filter there.
                
                :obj:`123` is the host id to which the hosts will be merged to.

        Note:
                You can also dump the hosts that are going to be merged before merging them by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.hosts.merge_host([],123,csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/search/host/job/merge'.format(str(client_id))

        body = {"filterRequest":{"filters":search_filter},"sourceId":host_id_to_merge_to}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('hostmerge',search_filter) 

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def set_asset_criticality(self, filter:list,assetcriticality:int, csvdump:bool=False,client_id:int=None)->int:

        """
        Sets asset criticality of the host.

        Args:
            filter:  Search filters
            assetcriticality:  The asset criticality to provide.
            csvdump:  Dump the csv data.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID is returned.
        Example:
            An example to use set_asset_criticality is
            
                >>> self.{risksenseobject}.hosts.set_asset_criticality([],4)

            Where
            
            :obj:`[]` is the search filter for all hosts, you can provide your search filter there.
            
            :obj:`4` is the criticality of the asset to set to

        Note:
                You can also dump the hosts to which asset criticality should be changed by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.hosts.set_asset_criticality([],4,csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update"

        body = {"filterRequest":{"filters":filter},"criticality":assetcriticality}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        
        if csvdump==True:
            self.downloadfilterinexport('assetcriticalityhost',filter) 

        return job_id

    def set_address_type(self, filter:list,addresstype:str,csvdump:bool=False, client_id:int=None)->int:

        """
        Sets address type of the host.

        Args:
            filter:  Search filters
            addresstype:  Provide external for external address and internal for internal
            csvdump:  Dump the csv data.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The job ID is returned.

        Example:
            An example to use set_address_type is
            
                >>> self.{risksenseobject}.hosts.set_address_type([],'external')

            Where
            
                :obj:`[]` is the search filter for all hosts, you can provide your search filter there.
                
                :obj:`external` is to set the address type as external address.
        Note:
                You can also dump the hosts which the address type will be set by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.hosts.set_address_type([],'external',csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update"

        if addresstype.lower()=='internal':
            setaddresstype=False
        if addresstype.lower()=='external':
            setaddresstype=True
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        body = {"filterRequest":{"filters":filter},"isExternal":setaddresstype}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        
        if csvdump==True:
            self.downloadfilterinexport('addresstypessethost',filter) 
        
        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def export(self, search_filters:list, file_name:str, row_count:str=ExportRowNumbers.ROW_ALL,file_type:str=ExportFileType.CSV, client_id:int=None)->int:

        """
        Initiates an export job on the platform for host(s) based on the
        provided filter(s).

        Args:
            
            search_filters:  A list of dictionaries containing filter parameters.
            
            file_name:       The name to be used for the exported file.
            
            row_count:      No of rows to be exported. Available options
                            ExportRowNumbers.ROW_10000,
                            ExportRowNumbers.ROW_25000,
                            ExportRowNumbers.ROW_50000,
                            ExportRowNumbers.ROW_100000,
                            ExportRowNumbers.ROW_ALL
            file_type:      File type to export. ExportFileType.CSV, ExportFileType.JSON,  or ExportFileType.XLSX
            
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
             The job ID in the platform from is returned.
        Example:
            An example to use export is
            
                >>> self.{risksenseobject}.hosts.export([],'testingexport')

            Where

                :obj:`[]` is the search filter for all hosts, you can provide your search filter there.

                :obj:`testingexport` is the filename to export the file to
            
            You can change the filetype to any of the names above or even the other positional arguments as mentioned

                >>> self.{risksenseobject}.hosts.export([],'testingexport',file_type=ExportFileType.JSON)

        """
        func_args = locals()
        func_args['exportable_filter']=self.getexporttemplate()
        func_args.pop('self')
        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]
        try:
            export_id = self._export(self.subject_name, **func_args)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return export_id

    def network_move(self, search_filters:list, network_identifier:int, is_force_merge:bool=False, csvdump:bool=False,client_id:int=None)->int:

        """
        Moves host(s) into a new network as specified.

        Args:
            search_filters:      A list of dictionaries containing filter parameters.
            network_identifier:  Network ID to move the hosts to
            is_force_merge:      Force merge of hosts?
            csvdump:             Dump the csv data.
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
              The job ID is returned.
        Example:
            An example to use network_move is
            
                >>> self.{risksenseobject}.hosts.network_move([],12345,False)

            Where
            
                :obj:`[]` is the search filter for all hosts, you can provide your search filter there.

                :obj:`12345` is the network id to which the hosts will move to

                :obj:`False` is to not force merge the hosts

        Note:
                You can also dump the hosts that are going to be moved before moving them by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.hosts.network_move([],12345,False,csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/network/move"

        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "targetNetworkId": network_identifier,
            "isForceMerge": is_force_merge
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('hostnetworkmove',search_filters) 

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def run_urba(self, search_filters:list,csvdump:bool=False, client_id:int=None)->int:

        """
        Initiates the update of remediation by assessment for hosts specified in filter(s).

        Args:
            search_filters:      A list of dictionaries containing filter parameters.
            
            csvdump: Dump the data in csv

            client_id:           Client ID.  If an ID isn't passed, it will use the profile's default Client ID.
        Return:
                The job ID is returned.
        Example:
            An example to use run_urba is
           
                >>> self.{risksenseobject}.hosts.run_urba([])

                Where
           
                :obj:`[]` is the search filter for all hosts, you can provide your search filter there.

                This will run the urba for all the hosts fetched from the search filter
        Note:
                You can also dump the hosts to which urba is being run by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.hosts.run_urba([],csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update-remediation-by-assessment"

        body = {
            "filterRequest": {
                "filters": search_filters
            }
        }
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('hostrunurba',search_filters) 
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def add_note(self, search_filters:list, new_note:str,csvdump:bool=False, client_id:int=None)->int:

        """
        Adds a note to host(s) based on the filter(s) provided.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            new_note:        The note to be added to the host(s).
            csvdump:             Dump the csv data.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
                The job ID is returned.
        Example:
            An example to use add_note is
           
                >>> self.{risksenseobject}.hosts.add_note([],'test')

            Where
        
                :obj:`[]` is the search filter for all hosts, you can provide your search filter there.

                :obj:`test` is the note which will be given to the hosts
        Note:
                You can also dump the hosts to which notes will be added post adding the note by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.hosts.add_note([],'test',csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/note"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "note": new_note
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            self.downloadfilterinexport('hostnotesadded',search_filters) 

        return job_id

    def get_model(self, client_id:int=None)->dict:

        """
        Get available projections and models for Hosts.
        
        Args:
            client_id:   Client ID

        Return:
            Hosts projections and models are returned.
        
        Example:
            An example to use get_model is
           
                >>> self.{risksenseobject}.hosts.get_model()

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return response

    def suggest(self, search_filter_1:list, search_filter_2:dict, client_id:int=None)->list:

        """
        Suggest values for filter fields.

        Args:
            search_filter_1:     Search Filter 1
            search_filter_2:     Search Filter 2
            client_id:           Client ID
        Return:
           Value suggestions
        
        Example:
            To use suggest function is

            >>> self.{risksenseobject}.hosts.suggest([],{})

            Where 

                :obj:`[]` is the first search filter 

                :obj:`{}` is the seconf search filter

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._suggest(self.subject_name, search_filter_1, search_filter_2, client_id)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return response

    def add_group(self, search_filter:list, group_ids:list,csvdump:bool=False, client_id:int=None)->int:

        """
        Add host(s) to one or more groups.

        Args:
            search_filter:   Search filter
            group_ids:       List of Group IDs to add to host(s).
            csvdump:         dumps the data in csv
            client_id:       Client ID
        Return:
            Job ID of group add job
        Example:
            An example to use add_group is
           
                >>> self.{risksenseobject}.hosts.add_group([],[2,3,4])

            Where
           
                :obj:`[]` is the search filter for all hosts, you can provide your search filter there.

                :obj:`[2,3,4]` are the group ids to add the hosts to .
        Note:
                You can also dump the hosts which will be addedd to the groups by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.hosts.add_group([],[2,3,4],csvdump=True)


        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            response = self._add_group(self.subject_name, search_filter, group_ids, client_id)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        if csvdump==True:
            self.downloadfilterinexport('hostgroupadd',search_filter) 

        return response

    def remove_group(self, search_filter:list, group_ids:list,csvdump:bool=False, client_id:int=None)->int:

        """
        Remove host(s) from one or more groups.

        Args:

            search_filter:   Search filter
            group_ids:       List of Group IDs to add to host(s).
            csvdump:         dumps the data in csv
            client_id:       Client ID
        Return:
            Job ID of group remove job
        Example:
            An example to use remove_group is
           
                >>> self.{risksenseobject}.hosts.remove_group([],[2,3,4])

            Where
           
                :obj:`[]` is the search filter for all hosts, you can provide your search filter there.

                :obj:`[2,3,4]` are the group ids to remove the hosts from .
        Note:
                You can also dump the hosts which will be removed from the groups by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.hosts.remove_group([],[2,3,4],csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
        
        if csvdump==True:
            self.downloadfilterinexport('removegrouphost',search_filter) 

        try:
            response = self._remove_group(self.subject_name, search_filter, group_ids, client_id)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()


        return response

### PRIVATE FUNCTIONS

def apply_system_filters(self, csvdump:bool=False,client_id:int=None)->list:

        """
        Get data of the hosts based on system filter.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:         dumps the data in csv   

        Return:
            The data of the system filter based host values are returned
        
        Example:
            An example to use apply_system_filters is
            
            >>> self.{risksenseobject}.hosts.apply_system_filters()

            Where 
            
            :obj:`[]` is the search filter for all hosts, you can provide your search filter there.

            The system filters will be displayed in the terminal to which you must provide a key value and the data returned will reflect based on the system filter chosrn

        Note:
            You can also dump the hosts from the system filters search by :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.hosts.apply_system_filters(csvdump=True)
        

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        url= self.profile.platform_url + "/api/v1/search/systemFilter"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            systemfilter = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        
        systemfilter=json.loads(systemfilter.text)

        systemfilters={}

        for filter in systemfilter:
            for hostsystemfilter in filter['subjectFilters']:
                if hostsystemfilter['subject']=="host":
                    systemfilters[filter['name']]=hostsystemfilter["filterRequest"]
    
        systemfilterkeys=list(systemfilters.keys())
        i=0
        for key in systemfilterkeys:
            print(f'Index-{i},Key:{key}')
            i=i+1
        try:
            actualfilter=systemfilters[ systemfilterkeys[int(input('Please enter the key for group by parameter:'))]]
        except IndexError as ex:
                print()
                print('Please enter an index number from the above list')
                print(ex)
                exit()
        except (Exception) as e:
                print('There was an error fetching group by data')
                print(e)
                exit()


        response=self.search(actualfilter['filters'])

        if csvdump==False:
            self.downloadfilterinexport('hostsystemfilter',actualfilter['filters']) 

        return response

"""
   Copyright 2021 RiskSense, Inc.
   
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
