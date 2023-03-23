"""
**Host Findings module defined for different host findings related api endpoints.**
"""
""" *******************************************************************************************************************
|
|  Name        :  __host_findings.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating HostFindings on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

from http import client
import json
from os import listdir
from pydoc import synopsis
from sre_constants import SUCCESS
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
from ..__notifications import Notifications
from ..__exports import Exports
import sys
import zipfile
import pandas as pd
import time
import csv


class HostFindings(Subject):

    """ **Class for HostFindings function defintions**.

    To utlise Host Findings function:

    Args:
            profile:     Profile Object
    
    Usage:
        :obj:`self.{risksenseobjectname}.host_findings.{function}`
    
    Examples:
        To get model for host findings using :meth:`get_model()` function

        >>> self.{risksenseobject}.host_findings.get_model()

    """

    def __init__(self, profile:object):

        """
        Initialization of HostFindings object.

        profile:     Profile Object
        :type  profile:     _profile

        """

        self.subject_name = "hostFinding"
        Subject.__init__(self, profile, self.subject_name)

    

    def downloadfilterinexport(self,filename:str,filters:list,client_id:int=None):
        """ **Exports and Downloads a file based on the filters defined** .

        Args:
            filename: Name of the file to export as
            filters:  host findings search filters based on which the export performs
            client_id: The client id to get the data from. If not supplied, takes default client id

        **IGNORE INTERNAL FUNCTION**

        Examples:
            
            >>>  self.{risksenseobject}.host_findings.downloadfilterinexport('hostfindingsdata',[])
        """
        if client_id is None:
            client_id= self._use_default_client_id()
        exportid=self.export(filters,file_name=filename,file_type=ExportFileType.CSV)
        self.exports=Exports(self.profile)
        print("Processing the export job, kindly wait for a while")
        while(True):
                try:
                    exportstatus=self.exports.check_status(exportid)
                    print(f'Export job state is in {exportstatus}')
                    if exportstatus=='COMPLETE':
                        break
                    elif exportstatus=='ERROR':
                        print('error getting file please check the platform')
                        exit()
                    time.sleep(10)
                except (RequestFailed,MaxRetryError,StatusCodeError, ValueError) as ex:       
                    print(ex)
                    print()
                    print("Unable to export the file.")
                    sys.exit("Exiting")
        try:   
                print('Downloading the file and extracting the zip file')
                self.exports.download_export(exportid,f"{filename}.zip")
                with zipfile.ZipFile(f"{filename}.zip","r") as zip_ref:
                    zip_ref.extractall(filename)
                    print('CSV downloaded in the folder and extracted')
        except(RequestFailed,MaxRetryError,StatusCodeError, ValueError):
                    print(ex)
                    print()
                    print("Unable to retrieve file. Exiting.")
                    sys.exit(1)
  
    def create(self, host_id_list:list, assessment_id:int, severity:str, source_id:str, scanner_uuid:str,
               title:str, finding_type:str,synopsis:str, description:str,solution:str,service_name:str,service_portnumber:str,cveids:list=[],filters:list=[],csvdump:bool=False, client_id=None)->int:
        """
        Manually create a new host finding.

        Args:
            host_id_list:    List of Host IDs to associate with this finding

            assessment_id:   Assessment ID

            severity:        Severity

            source_id:       Source ID

            scanner_uuid:    Scanner UUID

            title:           Host Finding Title

            finding_type:    Host Finding Type

            synopsis:        Synopsis

            description:     Description

            solution:        Solution

            service_name:    Service name

            cveids:         Ids of cves

            service_portnumber:  Service portnumber

            filters   :        A series of filters that make up a complete filter   

            csvdump: dumps id to csv
            
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The job ID is returned.
        Example:
            Creating host finding

            >>> self.{risksenseobject}.host_findings.create([123],190805,"9","publicnew","85200f98-1ea6-4641-9d27-171dc79f693f","something",'SERVICE',"testing to work on",,'somethingto work on','something to work on','new','5',[{"field":"id","exclusive":False,"operator":"IN","value":"6371904"}])
        Note:
            You can also dump the host finding job id created in a csv using :obj:`csvdump=True`:

            >>> self.{risksenseobject}.host_findings.create([123],190805,"9","publicnew","85200f98-1ea6-4641-9d27-171dc79f693f","something",'SERVICE',"testing to work on",,'somethingto work on','something to work on','new','5',[{"field":"id","exclusive":False,"operator":"IN","value":"6371904"}],csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        body = {
            "hostId": host_id_list,
            "assessmentId": assessment_id,
            "severity": severity,
            "sourceId": source_id,
            "scannerUuid": scanner_uuid,
            "title": title,
            "type": finding_type,
            "description": description,
            "solution": solution,
            "synopsis": synopsis,
            "service": {
                'name': service_name,
                'portNumber': service_portnumber
            },
            "cveIds": cveids,
            "filterRequest": {
                "filters":filters
            }
        }

        body = self._strip_nones_from_dict(body)

        if type(csvdump)!=bool:
            print('Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        hostfinding_id = jsonified_response['id']

        if csvdump==True:
            hostfinding={'jobid':[hostfinding_id]}
            df = pd.DataFrame(hostfinding)
            df.to_csv('hostfindingcreated.csv',index=None)

        return hostfinding_id

    def update(self, hostfindingid:int, client_id:int=None,csvdump:bool=False, **kwargs)->int:
        """
        Update a new host finding.
        
        Args:

            hostfindingid:    Host finding id which you want to update
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

            csvdump: dumps id to csv
        Keyword Args:
            title(``str``):   title
            description)(``str``):   description
            synopsis(``str``):   synopsis
            solution(``str``):   solution
        Return:
            The hostfinding ID is returned.
        Example:
            To update host finding id 123's description to 'new description'
            
            >>> self.rs.host_findings.update(123,description='new description')
        Note:
            You can also dump the host finding job id updated in a csv using :obj:`csvdump=True`:
            
            >>> self.rs.host_findings.update(123,description='new description',csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/{}'.format(hostfindingid)

        title = kwargs.get("title", None)
        description = kwargs.get("description", None)
        solution = kwargs.get("solution", None)
        synopsis = kwargs.get("synopsis", None)

        body = {
            "description": description,
            "solution": solution,
            "synopsis": synopsis,
            "title": title  
            }

        body = self._strip_nones_from_dict(body)

        if type(csvdump)!=bool:
            print('Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
    
        if csvdump==True:
            hostfinding={'jobid':[hostfinding_id]}
            df = pd.DataFrame(hostfinding)
            df.to_csv('hostfindingupdated.csv',index=None)

        jsonified_response = json.loads(raw_response.text)
        hostfinding_id = jsonified_response['id']

        return hostfinding_id

    def delete_manage_observations(self,hostfindingid:int,asssessmentid:list,csvdump:bool=False,client_id:int=None)->dict:

        """
        Delete manage observations
        
        Args:
            hostfindingid:    Host finding id

            asssessmentid:     Assessment id

            csvdump:         dumps the data in csv

            client_id:        Client id of user, if none gets default client id
        
        Return:
            
            jsonified_response:    The jsonified response
        
        Example:
            
            To delete observation linked to host finding id 123 and assessment id 1234
            
            >>> self.{risksenseobject}.host_findings.delete_manage_observations(123,[1234])
        Note:
            You can also dump the host findings data before deleting the manage observation using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.host_findings.delete_manage_observations(123,[1234],csvdump=True)
        
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/{}/assessment/delete".format(hostfindingid)

        body={
                "assessmentIds": asssessmentid
                }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('deletemanageobservations',[{"field":"id","exclusive":False,"operator":"IN","value":f"{hostfindingid}"}])

        try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url=url,body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_hostfinding_history(self,vulnerableids:list,csvdump=True,client_id:int=None)->list:

        """
        Get Host findings history

        Args:
            vulnerableids:    List of vulnerable ids to get history of

            client_id:      The client id , if none, default client id is taken

            csvdump:         dumps the data in csv
        Return:
            The jsonified response
        
        Example:

            To get host finding history
        
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/history"
        body={
                "vulnIds": vulnerableids
                }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url=url,body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
      
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_groupby_hostfinding(self,client_id:int=None)->dict:

        """
        Gets all the groupby key metrics for host findings

        Args:
            client_id:      The client id , if none, default client id is taken

        Return:
            The group by key metrics

        Example:
            >>>  self.{risksenseobject}.host_findings.get_groupby_hostfinding()
        **IGNORE INTERNAL FUNCTION**
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

        hostfindinggroupbykeymetrics={}

        for i in range(len(jsonified_response['groupByFields'])):
            hostfindinggroupbykeymetrics[jsonified_response['groupByFields'][i]['key']]=[jsonified_response['groupByFields'][i]['groupMetrics'][j]['key'] for j in range(len(jsonified_response['groupByFields'][i]['groupMetrics']))]

            
        return hostfindinggroupbykeymetrics

    def groupby_hostfinding(self,filters:list=[],sortorder:str=None,client_id:int=None,csvdump:bool=False)->dict:

        """
        Get groupby values for host finding
        
        Args:
            filters:        The filters which will populate in groupby

            sortorder: The order to sort the groupby values, please choose ASC for ascending and DESC for descending

            client_id:      The client id , if none, default client id is taken

            csvdump:         dumps the data in csv
        Return:
            groupby:      Group by information
        Example:

            >>>  self.{risksenseobject}.host_findings.groupby_hostfinding({filter})
        
            The filter must be provided for the group by to be used. The groupby fields will be displayed in the `terminal` and you must choose a `group by` filter to which the data will be populated      

        Note:
            This function also has an option to dump the data in a csv by a simple argument, :obj:`csvdump=True`

            >>>  self.{risksenseobject}.host_findings.groupby_hostfinding({filter},csvdump=True)

        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/group-by"

        hostfindingslist=self.get_groupby_hostfinding()

        hostfindingskeys=list(hostfindingslist.keys())

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        for i in range(len(hostfindingskeys)):
            print(f'Index-{i},Key:{hostfindingskeys[i]}')
        try:
            keymetric=hostfindingskeys[int(input('Please enter the key for group by parameter:'))]
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
                "metricFields": hostfindingslist[keymetric],
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
                with open('hostfindinggroupby.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response['data']:
                        print(item)
                        writer.writerow(item)
            except (FileNotFoundError,Exception) as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        return jsonified_response

    def get_single_search_page(self, search_filters:list, projection:str=Projection.BASIC, page_num:int=0, page_size:int=150,
                               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC, client_id:int=None,csvdump:bool=False)->dict:

        """
        Searches for and returns hostfindings based on the provided filter(s) and other parameters.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.

            projection:      Projection to be used in API request.  Projection.BASIC or Projection.DETAIL

            page_num:        The page number of results to be returned.

            csvdump: Dumps the data in csv

            page_size:       The number of results per page to be returned.

            sort_field:      The field to be used for sorting results returned.

            sort_dir:        The direction of sorting to be used. SortDirection.ASC or SortDirection.DESC

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The JSON response from the platform is returned.
        Example:
            An example to get single search page of host findings data
            
            >>> self.{risksenseobject}.host_findings.get_single_search_page([])

            You can also try changing the other arguments to your liking to reflect the data as you suffice such as change page_size or page_num etc.

            >>> self.{risksenseobject}.host_findings.get_single_search_page([],page_num=2,page_size=10)
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

    def search(self, search_filters:list, projection:str=Projection.BASIC, page_size:int=150,
               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC,csvdump:bool=False, client_id:int=None)->list:

        """
        Searches for and returns hostfindings based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.

            projection:      Projection to be used in API request.  Projection.BASIC or Projection.DETAIL

            page_size:       The number of results per page to be returned.

            sort_field:      The field to be used for sorting results returned.

            sort_dir:        The direction of sorting to be used. SortDirection.ASC or SortDirection.DESC

            csvdump:         dumps data in csv

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            
        Return:
            A list containing all host findings returned by the search using the filter provided.
        Example:
            An example to search for host finding data is
            
            >>> self.{risksenseobject}.host_findings.search([])

        Note:
            You can also dump the search based data in a csv by simply providing :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.host_findings.search([],csvdump=True)
        """

        func_args = locals()
        func_args.pop('self')
        func_args.pop('csvdump')
        all_results = []

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
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        if csvdump==True:
            self.downloadfilterinexport('hostfindingsearchdata',search_filters)

        return all_results

    def get_count(self, search_filters:list, client_id:int=None)->int:

        """
        Gets a count of hostfindings identified using the provided filter(s).

        Args:

            search_filters:   A list of dictionaries containing filter parameters.

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The number of hostfindings identified using the provided filter(s).
        
        Example:
            An example to use get count function is as follows
            
            >>> self.{risksenseobject}.host_findings.get_count([])
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

    def add_tag(self, search_filters:list, tag_id:int,csvdump:bool=False,client_id:int=None)->int:

        """
        Adds a tag to hostfinding(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.

            tag_id:          ID of tag to tbe added to hostfinding(s).

            csvdump:         dumps the data in csv

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID is returned.
        Example:
            An example to add a tag is 
            
            >>> self.{risksenseobject}.host_findings.add_tag([],1234)

        Note:
            You can also dump the host findings from the search filters post the tag completion for more information by :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.host_findings.add_tag([],1234,csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/tag"

        if type(csvdump)!=bool:
            print('Please provide either true or false')
            exit()

        body = {
            "tagId": tag_id,
            "isRemove": False,
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
        
        if csvdump==True:
            self.downloadfilterinexport('hostfindingtagadddata',search_filters)
        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            jobid={'add_tag_jobid':[job_id]}
            df = pd.DataFrame(jobid)
            df.to_csv('add_tag.csv',index=None)
        return job_id

    def remove_tag(self, search_filters:list, tag_id:int, client_id:int=None,csvdump:bool=False)->int:

        """
        Removes a tag from hostfinding(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            tag_id:          ID of tag to tbe removed from hostfinding(s).
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:         dumps the data in csv
        Return:
            The job ID is returned.
        Example:
            An example to use remove tag is
           
            >>> self.{risksenseobject}.host_findings.remove_tag([],123)

        Note:
            You can also dump the host findings which the tags will be removed from with a :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.host_findings.remove_tag([],123,csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/tag"

        body = {
            "tagId": tag_id,
            "isRemove": True,
            "filterRequest": {
                "filters": search_filters
            }
        }

        if type(csvdump)!=bool:
            print('Please provide either true or false')
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('hostfindingtagremovedata',search_filters)

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

    def assign(self, search_filters:list, users:list,csvdump:bool=False, client_id:int=None)->int:

        """
        Assigns hostfinding(s) to a list of user IDs.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            users:           A list of user IDs to be assigned to hostfinding(s).
            csvdump:         dumps the data in csv
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID is returned.
        Example:
            
            Lets assign user `123` to host findings based on filter of patch id `123`

            >>> self.{risksenseobject}.host_findings.assign([{"field":"source_patch_ids","exclusive":False,"operator":"IN","value":"123"}],[123])
        Note:
            You can also dump the host findings data before assigning them to users using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.host_findings.assign([{"field":"source_patch_ids","exclusive":False,"operator":"IN","value":"123"}],[123],csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/assign"

        body = {
            "filters": search_filters,
            "userIds": users
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
        
        if csvdump==True:
            self.downloadfilterinexport('assign',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def unassign(self, search_filters:list, users:list,csvdump:bool=False, client_id:int=None)->int:

        """
        Unassigns hostfinding(s) from a list of user IDs.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            users:           A list of user IDs to be unassigned from hostfinding(s).
            csvdump:         dumps the data in csv
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID is returned.
        Example:
            Lets unassign user `123` from host findings based on filter of patch id `123`
            
            >>> self.{risksenseobject}.host_findings.unassign([{"field":"source_patch_ids","exclusive":False,"operator":"IN","value":"123"}],[123])
        Note:
            You can also dump the host findings data before unassigning them from users using :obj:`csvdump=True` argument
            
            >>> self.{risksenseobject}.host_findings.unassign([{"field":"source_patch_ids","exclusive":False,"operator":"IN","value":"123"}],[123],csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/unassign"

        body = {
            "filters": search_filters,
            "userIds": users
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('unassign',search_filters)
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
    
    def self_assign(self,filterfields:list,userid:list,csvdump:bool=False,client_id:int=None)->int:

        """
        The host findings fetched are assigned to the current user

        Args:
            filterfields:  A list of dictionaries containing filter parameters.
            csvdump:         dumps the data in csv
            userid:           A list of user IDs to be assigned to hostfinding(s).
            client_id:       Client ID. If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID in the platform is returned.
        Example:
            
            Lets assign user `123` to host finding `1234`
            
            >>> self.{risksenseobject}.host_findings.self_assign([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],[123])
        Note:
            You can also dump the host findings data before assigning them to users using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.host_finding.self_assign([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],[123],csvdump=True)
        """

         
        

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/self-assign"
        
        body = {
                "filters": filterfields,
                "userIds": userid
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
        
        if csvdump==True:
            self.downloadfilterinexport('selfassign',filterfields)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id
    
    def self_unassign(self,filterfields:list,userids:list,client_id:int=None,csvdump:bool=False)->int:

        """
        The host findings fetched are unassigned from the current user
        
        Args:
            filterfields:  A list of dictionaries containing filter parameters.
            userids: A list of integers of user ids
            csvdump:         dumps the data in csv
            client_id:       Client ID. If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID in the platform is returned.
        Example:
            
            To unassign user 123 from finding id 1234
            
            >>> self.{risksenseobject}.host_findings.self_unassign([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],[123])
        Note:
            You can also dump the host findings data before unassigning them from users using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.host_findings.self_unassign([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],[123],csvdump=True)
        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/self-unassign"

        body = {
                "filters": filterfields,
                "userIds":userids
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('selfunassign',filterfields)
        
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

    def list_hostfinding_filter_fields(self,client_id:int=None)->list:

        """
        List filter endpoints.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The JSON output from the platform is returned, listing the available filters.
        
        Examples:
            
            >>>  self.{risksenseobject}.host_findings.list_hostfinding_filter_fields()

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


    def getexporttemplate(self,client_id:int=None)->list:
        
        """
        Gets configurable export template for host findings.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The Exportable fields
        Example:
            An example to use getexporttemplate
                
            >>> self.{risksenseobject}.host_findings.getexporttemplate()

            This gets all the export templates for host findings

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

    def getexporttemplatebyid(self,export_id:int=None,client_id:int=None)->list:
        
        """
        Gets configurable export template for host findings.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The Exportable fields
        Example:
            An example to use getexporttemplate
                
            >>> self.{risksenseobject}.host_findings.getexporttemplate()

            This gets all the export templates for host findings

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/export/template/{export_id}"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        exportablefilter = json.loads(raw_response.text)
        return exportablefilter['exportableFields']


    def getexporttemplates(self,client_id:int=None)->list:
        
        """
        Gets created existing export template for host findings.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The Exportable fields
        Example:
            An example to use getexporttemplates
                
            >>> self.{risksenseobject}.host_findings.getexporttemplates()

            This gets all the export templates for host findings

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/export/templates"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        exportablefilter = json.loads(raw_response.text)
        return exportablefilter



    def export(self, search_filters:list, file_name:str, row_count:str=ExportRowNumbers.ROW_ALL,file_type:str=ExportFileType.CSV,export_id:int=None, client_id:int=None)->int:

        """
        Initiates an export job on the platform for host finding(s) based on the
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

            exportable_filter:       Exportable filter
            file_type:       File type to export. ExportFileType.CSV, ExportFileType.JSON,  or ExportFileType.XLSX
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            export_id:       If present, an export template id of the template to use to export.
        Return:
            The job ID in the platform from is returned.
        Example:
            An example to use export is
            
            >>> self.{risksenseobject}.host_findings.export([],'testingexport')
            
            You can change the filetype to any of the names above or even the other positional arguments as mentioned

            >>> self.{risksenseobject}.host_findings.export([],'testingexport',file_type=ExportFileType.JSON)
        """
        func_args = locals()
        if export_id==None:
            func_args['exportable_filter']=self.getexporttemplate()
        elif export_id!=None:
            func_args['exportable_filter']=self.getexporttemplatebyid(export_id)
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

    def update_due_date(self, search_filters:list, new_due_date:str,csvdump:bool=False, client_id:int=None)->int:

        """
        Updates the due date assigned to hostfinding(s) based on the provided filter(s)

        Args:
            search_filters:  A list of dictionaries containing filter parameters.

            new_due_date:    The new due date in the "YYYY-MM-DD" format.

            csvdump:         dumps the data in csv

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID is returned.
        Example:
            
            Lets update an host finding id 1234 to due date 2022-08-11
            
            >>> self.{risksenseobject}.host_findings.update_due_date([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],'2022-08-11')
        Note:
            You can also dump the host findings data after updating their due date using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.host_findings.update_due_date([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],'2022-08-11',csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update-due-date"

        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "dueDate": new_due_date
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        if csvdump==True:
            self.downloadfilterinexport('update due date',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def add_note(self, search_filters:list, new_note:str,csvdump:bool=False, client_id:int=None)->int:

        """
        Adds a note to hostfinding(s) based on the filter(s) provided.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            new_note:        The note to be added to the hostfinding(s).  String.
            csvdump:         dumps the data in csv
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID is returned.
        Example:
            
            To add a note 'testing' to host finding id 123
            
            >>> self.{risksenseobject}.host_findings.add_note([{"field":"id","exclusive":False,"operator":"IN","value":"123"}],'testing')
        Note:
            You can also dump the host findings data post adding a note using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.host_findings.add_note([{"field":"id","exclusive":False,"operator":"IN","value":"123"}],'testing',csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/note"

        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "note": new_note
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
        
        if csvdump==True:
            self.downloadfilterinexport('addnote',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id


    def delete(self, search_filters:list,csvdump:bool=False, client_id:int=None)->int:

        """
        Deletes hostfinding(s) based on the provided filter(s)

        Args:
            search_filters:   A list of dictionaries containing filter parameters.

            csvdump:         dumps the data in csv

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID is returned.
        Example:
            
            To delete host finding by id 12345
            
            >>> self.{risksenseobject}.host_findings.delete([{"field":"id","exclusive":False,"operator":"IN","value":"12345"}])
        Note:
            You can also dump the host findings data before deleting the host findings using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.host_findings.delete([{"field":"id","exclusive":False,"operator":"IN","value":"12345"}],csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/delete"

        body = {
            "filterRequest": {
                "filters": search_filters
            }
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('deletedhostfindings',search_filters)

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

    def subscribe_new_open_ransomware_findings(self,client_id:int=None)->dict:

        """
        Subscribes the user to new open ransomware findings

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The response to the subscription that was performed

        Example:

            An example to use subscribe_new_open_ransomware_findings()
                
            >>> self.{risksenseobject}.host_findings.subscribe_new_open_ransomware_findings()
            
            This helps the user subscrive to new open ransomware findings

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=4,subscribe=True)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def unsubscribe_new_open_ransomware_findings(self,client_id:int=None)->dict:

        """
        Unsubscribes the user from new open ransomware findings

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The response to the unsubscription that was performed

        Example:

            An example to use unsubscribe_new_open_ransomware_findings()
                
            >>> self.{risksenseobject}.host_findings.unsubscribe_new_open_ransomware_findings()
            
            This helps the user unsubscribe from new open ransomware findings

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=4)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def subscribe_new_open_critical_findings_vrr(self,client_id:int=None)->dict:

        """
        Subscribes the user to new open critical findings based on vrr

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The response to the subscription that was performed

        Example:

            An example to use subscribe_new_open_critical_findings_vrr()
                
            >>> self.{risksenseobject}.host_findings.subscribe_new_open_critical_findings_vrr()
            
            This helps the user subscribe to new open critical findings based on vrr.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=5,subscribe=True)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def unsubscribe_new_open_critical_findings_vrr(self,client_id:int=None)->dict:

        """
        Unsubscribes the user from new open critical findings based on vrr

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The response to the subscription that was performed

        Example:

            An example to use unsubscribe_new_open_critical_findings_vrr()
                
            >>> self.{risksenseobject}.host_findings.unsubscribe_new_open_critical_findings_vrr()
            
            This helps the user to unsubscribe from new open critical findings based on vrr.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=5)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def subscribe_new_open_critical_findings_severity(self,client_id:int=None)->dict:

        """
        Subscribes the user to new open critical findings based on severity

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The response to the subscription that was performed

        Example:

            An example to use subscribe_new_open_critical_findings_severity()
                
            >>> self.{risksenseobject}.host_findings.subscribe_new_open_critical_findings_severity()
            
            This helps the user subscribe to new open critical findings based on severity.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(self,notificationtypeid=6,subscribe=True)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def unsubscribe_new_open_critical_findings_severity(self,client_id:int=None)->dict:

        """
        Unsubscribes the user from new open critical findings based on severity

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The response to the subscription that was performed

        Example:

            An example to use unsubscribe_new_open_critical_findings_severity()
                
            >>> self.{risksenseobject}.host_findings.unsubscribe_new_open_critical_findings_severity()
            
            This helps the user unsubscribe from new open critical findings based on severity.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=6)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def subscribe_new_open_high_findings_vrr(self,client_id:int=None)->dict:

        """
        Subscribes the user to new open high findings based on vrr

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The response to the subscription that was performed

        Example:

            An example to use subscribe_new_open_high_findings_vrr()
                
            >>> self.{risksenseobject}.host_findings.subscribe_new_open_high_findings_vrr()
            
            This helps the user subscribe to new open high findings based on vrr.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=7,subscribe=True)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def unsubscribe_new_open_high_findings_vrr(self,client_id:int=None)->dict:

        """
        Unsubscribe the user from new open high findings based on vrr

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The response to the subscription that was performed

        Example:

            An example to use unsubscribe_new_open_high_findings_vrr()
                
            >>> self.{risksenseobject}.host_findings.unsubscribe_new_open_high_findings_vrr()
            
            This helps the user unsubscribe from new open high findings based on vrr.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=7)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def subscribe_new_open_high_findings_severity(self,client_id:int=None)->dict:

        """
        Subscribes the user to new open high findings based on severity

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The response to the subscription that was performed

        Example:

            An example to use subscribe_new_open_high_findings_severity()
                
            >>> self.{risksenseobject}.host_findings.subscribe_new_open_high_findings_severity()
            
            This helps the user subscribe to new open high findings based on severity.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=8,subscribe=True)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def unsubscribe_new_open_high_findings_severity(self,client_id:int=None)->dict:

        """
        Unsubscribes the user from new open high findings based on severity

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The response to the subscription that was performed

        Example:

            An example to use unsubscribe_new_open_high_findings_severity()
                
            >>> self.{risksenseobject}.host_findings.unsubscribe_new_open_high_findings_severity()
            
            This helps the user unsubscribe from new open high findings based on severity.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.subscribe_notifications(self,notificationtypeid=8,subscribe=False)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def map_findings(self, filter_request:list,workflowtype:str,workflowuuid:str,csvdump:bool=False,client_id:int=None)->bool:

        """
        Map hostfindings to a workflow .

        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            workflowtype:      Type of workflow, either falsePositive,remediation,acceptance,severityChange. Please use the exact names as above for workflow type

            workflowuuid:      workflow uuid

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The success flag.
        Example:
            
            To map a workflow 'st1234' to finding by id '123' of type severitychange
            
            >>> self.{risksenseobject}.host_findings.map_findings([{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"123"}],'severityChange','st1234')
        Note:
            You can also dump the host findings data post mapping the findings using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.host_findings.map_findings([{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"123"}],'severityChange','st1234',csvdump=True)

        """


        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        body = {"subject":"hostFinding","filterRequest":{"filters":filter_request}}

        try:
            url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/map'.format(str(client_id),workflowtype,workflowuuid)


        except Exception as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        if csvdump==True:
            self.downloadfilterinexport('mapfindings',filter_request)

        success=True
        return success

    def add_ticket_tag(self,search_filters:list,tag_id:int,client_id:int=None)->int:

        """
        Adds a ticket tag to the host findings based on a search filter

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            tag_id:         The tag id 
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID in the platform is returned.
        
        Example:
            To add a ticket tag to host findings

            >>> self.{risksenseobject}.host_findings.add_ticket_tag([],123)

        """
        

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/search/hostFinding/job/tag'
        print(url)

        body = {"tagId":tag_id,"isRemove":False,"filterRequest":{"filters":search_filters},"publishTicketStats":False}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response



    def unmap_findings(self, filter_request:list,workflowtype:str,workflowuuid:str,csvdump:bool=False, client_id:int=None)->bool:

        """
        Unmap findings from workflow.

        Args:
            filter_request:      A list of dictionaries containing filter parameters.
            workflowtype:      Type of workflow, either falsePositive,remediation,acceptance,severityChange. Please use the exact names as above for workflow type
            workflowuuid:      workflow uuid
            csvdump:         dumps the data in csv
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The success flag.
        Example:
            
            To unmap a workflow 'st1234' from finding by id '123' of type severitychange
            
            >>> self.{risksenseobject}.host_findings.unmap_findings([{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"123"}],'severityChange','st1234')
        Note:
            You can also dump the host findings data before unmapping the findings using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.host_findings.unmap_findings([{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"123"}],'severityChange','st1234',csvdump=True)
        """


        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/unmap'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":"hostFinding","filterRequest":{"filters":filter_request}}

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
        
        if csvdump==True:
            self.downloadfilterinexport('unmapfindings',filter_request)
        
        success=True

        return success

    def get_model(self, client_id:int=None)->dict:

        """
        Get available projections and models for Host Findings.

        Args:
            client_id:   Client ID  
        Return:
            Host Finding projections and models are returned.
        Example:
            An example to use get_model is
           
            >>> self.{risksenseobject}.host_findings.get_model()
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

    def suggest(self, search_filter_1:list, search_filter_2:dict, client_id:int=None):

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

            >>> self.{risksenseobject}.host_findings.suggest([],{})

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

### PRIVATE FUNCTIONS

    def apply_system_filters(self, csvdump:bool=False,client_id:int=None)->list:

        """
        Get data from system filters for host findings.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if it's not needed.
        Return:
            The data of the system filter based host findings values are returned
        
        Example:
            An example to use apply_system_filters is
           
            >>> self.{risksenseobject}.host_findings.apply_system_filters()

            The system filters will be displayed in the terminal to which you must provide a key value and the data returned will reflect based on the system filter chosen

        Note:
            You can also dump the host findings from the system filters search by :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.host_findings.apply_system_filters(csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        url= self.profile.platform_url + "/api/v1/search/systemFilter"

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
            for hostFindingsystemfilter in filter['subjectFilters']:
                if hostFindingsystemfilter['subject']=="hostFinding":
                    systemfilters[filter['name']]=hostFindingsystemfilter["filterRequest"]
        try:
            systemfilterkeys=list(systemfilters.keys())
            i=0
            for key in systemfilterkeys:
                print(f'Index-{i},Key:{key}')
                i=i+1

            actualfilter=systemfilters[ systemfilterkeys[int(input('Please enter the key for system filter parameter:'))]]

            response=self.search(actualfilter['filters'])

            if csvdump==True:
                self.downloadfilterinexport('hostfindingdataofsystemfilter',actualfilter['filters'])
            print(response)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()



"""
   Copyright 2022 RiskSense, Inc.
   
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
