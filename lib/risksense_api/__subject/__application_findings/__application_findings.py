"""
**Application Findings module defined for different application findings related api endpoints.**
"""
""" *******************************************************************************************************************
|
|  Name        :  __application_findings.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating Application Findings on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

from cmath import e
import json
import datetime
from pickle import LIST
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
from ..__notifications import Notifications
from ..__exports import Exports
import csv
import zipfile
import sys
import pandas as pd


class ApplicationFindings(Subject):

    """ **Class for Application Findings function defintions**.

    To utlise Application Findings function:

    Args:
            profile:     Profile Object
    
    Usage:
        :obj:`self.{risksenseobjectname}.application_findings.{function}`
    
    Examples:
        To get model for application findings using :meth:`get_model()` function

        >>> self.{risksenseobject}.application_findings.get_model()

    """

    def __init__(self, profile:object):

        """**Initialization of Application Findings Object** .

        Args:
            profile:     Profile Object

        """
        self.subject_name = 'applicationFinding'
        Subject.__init__(self, profile, self.subject_name)
        self.alt_base_api_url=self.profile.platform_url + "/api/v1/client/{}/search/{}"

    def create(self,applicationids:list,assessmentid:int, synopsis:str,description:str,severity:str,sourceid:str,scanneruuid:str,title:str,solution:str,parameter:str,payload:str,request:str,response:str,filterrequests:list,cweids:list,applicationurl:str,isSelectedAll:bool=False,csvdump:bool=False,client_id:int=None)->json:

        """
        Creates application finding.

        Args:

            applicationids:  A list containing application ids the findings are part of
            assessmentid:    Assessment id of the finding
            synopsis:       Synopsis for the application finding
            description:       description for the application finding
            severity:       Application severity 
            sourceid:       Sourceid of the application
            scanneruuid:      scanneruuid of the application
            title:      title for the application
            solution:      solution for the application
            parameter:      parameter for the application
            payload:      payload for the application
            request:      request for the application
            response:      request for the application
            filterrequests:      filterrequests for the application as a list
            cweids:      cwe ids  for the application as a list
            applicationurl:      applicationurl  for the application as a list
            isSelectedAll:      whether isselectedall
            csvdump: dumps id to csv
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:

            Jsonified response.

        Example:

            To create an application finding

            >>> self.{risksenseobject}.application_findings.create([123],123,"Application/Environment information being disclosed","[p]Any part of the application which reveals details","8","public_key_pinning","aaaabbbb-cccc-ddd","vulnerability test 4","[p]Applications should not reveal any debug or","","","","",[{"field":"id","exclusive":False,"operator":"IN","value":""}],[1,2],"/webpage.html")

        Note:
            You can also dump the application finding job id created in a csv using :obj:`csvdump=True`:
            
            >>> self.{risksenseobject}.application_findings.create([123],123,"Application/Environment information being disclosed","[p]Any part of the application which reveals details","8","public_key_pinning","aaaabbbb-cccc-ddd","vulnerability test 4","[p]Applications should not reveal any debug or","","","","",[{"field":"id","exclusive":False,"operator":"IN","value":""}],[1,2],"/webpage.html",csvdump=True)

        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))
        body = {
            "applicationIds":applicationids,"assessmentId":assessmentid,
            "synopsis":synopsis,"description":description,
            "severity":severity,
            "sourceId":sourceid,"scannerUuid":scanneruuid,
            "title":title,
            "solution":solution,
            "parameter":parameter,
            "payload":payload,
            "request":request,
            "response":response,
            "isSelectedAll":isSelectedAll,
            "filterRequest":{"filters":filterrequests},
            "cweIds":cweids,
            "applicationUrl":applicationurl}
        print(body)
        if type(csvdump)!=bool:
            print('Error in csvdumpvalue,Please provide either true or false')
            exit()
        
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            jsonified_response = json.loads(raw_response.text)

        except (RequestFailed,Exception) as e:
            print('There was an error creating application finding')
            print(e)
            exit()
       
        if csvdump==True:
            applicationfinding={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(applicationfinding)
            df.to_csv('applicationfindingcreated.csv',index=False)
        return jsonified_response

    def update(self,applicationfindingid:int,applicationids:int,assessmentid:int,applicationurl:str,severity:int,sourceid:int,title:str,description:str,solution:str,synopsis:str,notes:str,cweids:int,request:str,response:str,parameter:str,payload:str,vulnrequestid:int,csvdump:bool=False,client_id:int=None)->dict:

        """
        Update application finding.

        Args:
            applicationfindingid:  An id of the application finding to update
            applicationids:  A list containing application ids the findings are part of
            assessmentid:    Assessment id of the finding
            applicationurl:  Url of the application
            severity:       Application severity 
            sourceid:       Sourceid of the application           
            title:      title for the application
            description:       description for the application finding
            solution:      solution for the application
            synopsis:       Synopsis for the application finding
            notes:       notes for application finding
            cweids:       cwe id
            request:      request for the application
            response:      request for the application
            parameter:      parameter for the application
            payload:      payload for the application
            vulnrequestid:      payload for the application
            csvdump:         dumps the data in csv
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            Jsonified response.
        
        Example:
            To Update the application findings 

            >>> self.{risksenseobject}.application_findings.update(applicationfindingid=3205739,applicationids=11519,assessmentid=107556,applicationurl="/webpage.html",severity=9,sourceid=1234,title='vulnerability test 8',description="[p]Any part of the application which reveals details",solution='something to work on etc',synopsis='something to work on etc',notes='something to work on etc',cweids=79,request='',response='',parameter='',payload='',vulnrequestid=1234)

        Note:
            You can also dump the job id of the application findings using :obj:`csvdump=True` argument:
            
            >>> self.{risksenseobject}.application_findings.update(applicationfindingid=3205739,applicationids=11519,assessmentid=107556,applicationurl="/webpage.html",severity=9,sourceid=1234,title='vulnerability test 8',description="[p]Any part of the application which reveals details",solution='something to work on etc',synopsis='something to work on etc',notes='something to work on etc',cweids=79,request='',response='',parameter='',payload='',vulnrequestid=1234,csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/{}'.format(str(applicationfindingid))
        body = {
                "applicationId": applicationids,
                "assessmentId": assessmentid,
                "applicationUrl": applicationurl,
                "severity": severity,
                "sourceId": sourceid,
                "title": title,
                "description": description,
                "solution": solution,
                "synopsis": synopsis,
                "notes":    notes,
                "cweId": cweids,
                "request": request,
                "response": response,
                "parameter": parameter,
                "payload": payload,
                "vulnRequestId": vulnrequestid
                }
        
        if type(csvdump)!=bool:
            print('Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
            jsonified_response = json.loads(raw_response.text)
            
        except (RequestFailed,Exception) as e:
            print('There was an error updating application finding')
            print(e)
            exit()
    
        if csvdump==True:
            appfinding={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(appfinding)
            df.to_csv('applicationfindingupdates.csv',index=None)
        
        return jsonified_response
        

    def get_model(self, client_id:int=None)->dict:

        """
        Get available projections and models for application findings.
        
        Args:
            client_id:   Client ID

        Return:
            Application findings projections and models are returned.
        
        Example:
            An example to use get_model is
           
                >>> self.{risksenseobject}.application_findings.get_model()

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
            
        except (RequestFailed,Exception) as e:
            print('There was an error getting available projection models for application findings')
            print(e)
            exit()

        return response

    def list_applicationfinding_filter_fields(self,client_id:int=None)->list:

        """
        Lists application finding filter fields.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The JSON output from the platform is returned, listing the available filter fields.

        Examples:
            >>>  self.{risksenseobject}.application_findings.list_applicationfinding_filter_fields()
        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/filter'
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url) 
            jsonified_response = json.loads(raw_response.text)
            return jsonified_response

        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()


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

            >>> self.{risksenseobject}.application_findings.suggest([],{})

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._suggest(self.subject_name, search_filter_1, search_filter_2, client_id)
            
        except (RequestFailed,Exception) as e:
            print('There was an error getting suggest values for filter fields')
            print(e)
            exit()
        return response
        

    def search(self, search_filters:list, projection:str=Projection.BASIC, page_size:int=150,
               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC,csvdump:bool=False, client_id:int=None)->list:

        """
        Searches for and returns application findings based on the provided filter(s) and other parameters.
        Rather than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            projection:      Projection to be used in API request.  Projection.BASIC or Projection.DETAIL
            page_size:       The number of results per page to be returned.
            sort_field:      The field to be used for sorting results returned.
            sort_dir:        The direction of sorting to be used. SortDirection.ASC or SortDirection.DESC
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        
        Return:
            A list containing all application findings returned by the search using the filter provided.
        
        Example:
            An example to search for application finding data is
            
            >>> self.{risksenseobject}.application_findings.search([])

        Note:
            You can also dump the search based data in a csv by simply providing :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.application_findings.search([],csvdump=True)
        

        """

        func_args = locals()
        func_args.pop('self')
        all_results = []
        func_args.pop('csvdump')
        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            page_info = self._get_page_info(subject_name=self.subject_name, search_filters=search_filters,
            page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print(e)
            exit()

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()
        
        
        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed,Exception) as e:
            print('There was an error searching application finding data')
            print(e)
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationfindingdatasearch',search_filters)
        return all_results


    def downloadfilterinexport(self,filename:str,filters:list,client_id:int=None):

        """ **Exports and Downloads a file based on the filters defined** .

        Args:
            filename: Name of the file to export as
            filters:  Application findings search filters based on which the export performs
            client_id: The client id to get the data from. If not supplied, takes default client id
        **IGNORE INTERNAL FUNCTION*

        Examples:
            >>>  self.{risksenseobject}.application_findings.downloadfilterinexport('applicationfindingsdata',[])
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
            self.exports.download_export(exportid,f"{filename}.zip")
            with zipfile.ZipFile(f"{filename}.zip","r") as zip_ref:
                zip_ref.extractall(filename)
        except(RequestFailed,MaxRetryError,StatusCodeError, ValueError) as ex:
                    print(ex)
                    print()
                    print("Unable to retrieve file. Exiting.")
                    sys.exit(1)


    def get_single_search_page(self, search_filters:list, projection:str=Projection.BASIC, page_num:int=0, page_size:int=150,
                               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC, client_id:int=None)->dict:

        """
        Searches for and returns application findings based on the provided filter(s) and other parameters.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            projection:      The projection to use for API call.  Projection.BASIC or Projection.DETAIL
            page_num:        Page number of results to be returned.
            page_size:       Number of results to be returned per page.
            sort_field:      Name of field to sort results on.
            sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The paginated JSON response from the platform is returned.
        
        Example:
            An example to get single search page of application findings data
            
            >>> self.{risksenseobject}.application_findings.get_single_search_page([])

            You can also try changing the other arguments to your liking to reflect the data as you suffice such as change page_size or page_num etc.

            >>> self.{risksenseobject}.application_findings.get_single_search_page([],page_num=2,page_size=10)
        """
        try:
            func_args = locals()
            func_args.pop('self')

            if client_id is None:
                client_id, func_args['client_id'] = self._use_default_client_id()

            try:
                response = self._get_single_search_page(self.subject_name, **func_args)
            except (RequestFailed,Exception) as e:
                print('Error finding application findings data')
                print()
                print(e)

            return response
        except (Exception) as e:
                print('There was an error in getting single search page')
                print(e)
                exit()

    def apply_system_filters(self, csvdump:bool=False,client_id:int=None)->list:

        """
        Get data from system filters for application findings.

        Args:

            client_id:       Client ID.  If an ID isn't passed, it will use the profile's default Client ID.
            csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if it's not needed.

        Return:
            The data of the system filter based application findings values are returned
       
        Example:
            An example to use apply_system_filters is
           
            >>> self.{risksenseobject}.application_findings.apply_system_filters()

            The system filters will be displayed in the terminal to which you must provide a key value and the data returned will reflect based on the system filter chosen

        Note:
            You can also dump the application findings from the system filters search by :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.application_findings.apply_system_filters(csvdump=True)
        """

        try:
            if client_id is None:
                client_id = self._use_default_client_id()[0]
            
            url= self.profile.platform_url + "/api/v1/search/systemFilter"

            try:
                systemfilter = self.request_handler.make_request(ApiRequestHandler.GET, url)
            except (RequestFailed,Exception) as e:
                print('There was an error fetching system filters data')
                print(e)
                exit()
            
            systemfilter=json.loads(systemfilter.text)

            systemfilters={}

            for filter in systemfilter:
                for applicationFindingsystemfilter in filter['subjectFilters']:
                    if applicationFindingsystemfilter['subject']=="applicationFinding":
                        systemfilters[filter['name']]=applicationFindingsystemfilter["filterRequest"]
        
            systemfilterkeys=list(systemfilters.keys())
            i=0
            try:
                for key in systemfilterkeys:
                    print(f'Index-{i},Key:{key}')
                    i=i+1
                actualfilter=systemfilters[ systemfilterkeys[int(input('Please enter the key for the system filter to add:'))]]
            except IndexError as ex:
                print()
                print('There was an error fetching system filters data')
                print('Please enter an index number from the above list')
                exit()
            except (Exception) as e:
                print('There was an error fetching system filters data')
                print(e)
                exit()

            try:
                response=self.search(actualfilter['filters'])
            except (Exception) as e:
                print('There was an error fetching search data')
                print(e)
                exit()
            

            if csvdump==True:
                self.downloadfilterinexport('applicationfindingdataofsystemfilter',actualfilter['filters'])
            return response
        except (Exception) as e:
                print('There was an error in apply system filters function')
                print(e)
                exit()


    def get_groupby_appfinding(self,client_id:int=None)->dict:

        """
        Gets all the groupby key metrics for application findings

        Args:
            client_id:      The client id , if none, default client id is taken

        Return:
            The group by key metrics
        **IGNORE INTERNAL FUNCTION*
        Example:
            >>>  self.{risksenseobject}.application_findings.get_groupby_appfinding()
        
        Note:
            This function just returns the groupbyfields
        
        """
        try:
            if client_id is None:
                    client_id = self._use_default_client_id()[0]

            url = url = self.api_base_url.format(str(client_id)) + "/group-by"

            try:
                    raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
            except (RequestFailed,Exception) as e:
                print('There was an error fetching groupby fields data')
                print(e)
                exit()

            jsonified_response = json.loads(raw_response.text)

            appfindinggroupbykeymetrics={}

            for i in range(len(jsonified_response['groupByFields'])):
                appfindinggroupbykeymetrics[jsonified_response['groupByFields'][i]['key']]=[jsonified_response['groupByFields'][i]['groupMetrics'][j]['key'] for j in range(len(jsonified_response['groupByFields'][i]['groupMetrics']))]

                
            return appfindinggroupbykeymetrics
        except (Exception) as e:
                print('There was an error in returning group by key metrics function')
                print(e)
                exit()
        

    def groupby_appfinding(self,filters:list=[],sortorder:str=None,csvdump:bool=False,client_id:int=None)->dict:

        """
        Gets groupby data for all application finding
        
        Args:
            filters:        The filters which will be used for groupby
            sortorder: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
            csvdump:      Whether to export the data populated, if false will not export
            client_id:      The client id , if none, default client id is taken

        Return:
            Jsonified response

        Example:

            >>>  self.{risksenseobject}.application_findings.groupby_appfinding({filter})
        
            The filter must be provided for the group by to be used. The groupby fields will be displayed in the `terminal` and you must choose a `group by` filter to which the data will be populated      

        Note:
            This function also has an option to dump the data in a csv by a simple argument, :obj:`csvdump=True`

            >>>  self.{risksenseobject}.application_findings.groupby_appfinding({filter},csvdump=True)

        
        """
        try:
            if client_id is None:
                    client_id = self._use_default_client_id()[0]

            url = url = self.api_base_url.format(str(client_id)) + "/group-by"
            print(url)

            appfindingslist=self.get_groupby_appfinding()

            appfindingskeys=list(appfindingslist.keys())

            try:
                for i in range(len(appfindingskeys)):
                    print(f'Index-{i},Key:{appfindingskeys[i]}')
                keymetric=appfindingskeys[int(input('Please enter the key for group by parameter:'))]
            except IndexError as ex:
                print()
                print('There was an error fetching group by data')
                print('Please enter an index number from the above list')
                exit()
            except (Exception) as e:
                print('There was an error fetching group by data')
                print(e)
                exit()
            
            if sortorder is None:
                sortorder=[{"field":keymetric,"direction":"ASC"}]

            body = {
                    "key": keymetric,
                    "metricFields": appfindingslist[keymetric],
                    "filters": filters,
                    "sortOrder": sortorder
                    }
            try:
                    raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
                    jsonified_response = json.loads(raw_response.text)
            except (RequestFailed,Exception) as e:
                print('There was an error fetching groupby data')
                print(e)
                exit()
            try:
                if csvdump==True:
                    field_names = []
                    for item in jsonified_response['data'][0]:
                        field_names.append(item)

                    try:
                        with open('applicationfindinggroupby.csv', 'w') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=field_names)
                            writer.writeheader()
                            for item in jsonified_response['data']:
                                writer.writerow(item)
                    except FileNotFoundError as fnfe:
                        print("An exception has occurred while attempting to write the .csv file.")
                        print()
                        print(fnfe)
            except Exception as e:
                    print('There seems to be an exception')
                    print(e)
                    exit()
            return jsonified_response
        except (Exception) as e:
                print('There was an error getting all group by data')
                print(e)
                exit()

    def get_count(self, search_filters:list, client_id:int=None)->int:

        """
        Gets a count of application findings identified using the provided filter(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
                The number of application findings identified using the provided filter(s).
        
        Example:
            An example to use get count function is as follows
            
            >>> self.{risksenseobject}.application_findings.get_count([])

        """
        try:
            if client_id is None:
                client_id = self._use_default_client_id()[0]

            try:
                page_info = self._get_page_info(self.subject_name, search_filters, client_id=client_id)
                count = page_info[0]
            except (RequestFailed,Exception) as e:
                print('There was an error getting count data')
                print(e)
                exit()

            return count
        except (Exception) as e:
                print('There was an error completing the get count function')
                print(e)
                exit()

    def add_tag(self, search_filters:list, tag_id:int, csvdump:bool=False,client_id:int=None)->int:

        """
        Add a tag to application finding(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            tag_id:          ID of tag to tbe added to application findings(s).
            csvdump:         dumps the data in csv
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
                The job ID is returned.
        Example:
            An example to add a tag is 
            
            >>> self.{risksenseobject}.application_findings.add_tag([],1234)

        Note:
            You can also dump the application findings from the search filters post the tag completion for more information by :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.application_findings.add_tag([],1234,csvdump=True)
        """
        try:
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
                print('Please provide either true or false')
                exit()


            try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            except (RequestFailed,Exception) as e:
                print('There was an error adding tag')
                print(e)
                exit()
            
            if csvdump==True:
                self.downloadfilterinexport('applicationfindingtagadd',search_filters)

            jsonified_response = json.loads(raw_response.text)
            job_id = jsonified_response['id']

            return job_id
        except (Exception) as e:
                print('There was an error completing the tag addition function')
                print(e)
                exit()
        
    def remove_tag(self, search_filters:list, tag_id:int,csvdump:bool=False, client_id:int=None)->int:

        """
        Remove a tag to application finding(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            tag_id:          ID of tag to be removed from application findings(s).
            client_id:       Client ID.  If an ID isn't passed, it will use the profile's default Client ID.
            csvdump:         dumps the data in csv

        Return:    
            The job ID is returned.
       
        Example:
            An example to use remove tag is
           
            >>> self.{risksenseobject}.application_findings.remove_tag([],123)

        Note:
            You can also dump the application findings which the tags will be removed from with a :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.application_findings.remove_tag([],123,csvdump=True)

        """
        try:
            if client_id is None:
                client_id = self._use_default_client_id()[0]
            
            if csvdump==True:
                self.downloadfilterinexport('applicationfindingtowhichtagisremoved',search_filters)

            url = self.api_base_url.format(str(client_id)) + "/tag"
            
            body = {"tagId":tag_id,"isRemove":True,"filterRequest":{"filters":search_filters},"publishTicketStats":False}

            try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url=url, body=body)
            except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
            jsonified_response = json.loads(raw_response.text)
            job_id = jsonified_response['id']

            return job_id
        except (Exception) as e:
                print('There was an error completing the tag removal function')
                print(e)
                exit()
        
    def assign(self, search_filters:list, user_ids:list,csvdump:bool=False, client_id:int=None)->int:

        """
        Assign user(s) to application findings.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            user_ids:        A list of user IDs.
            csvdump:       Dumps data in csv  
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The job ID in the platform is returned.
        
        Example:
            
            Lets assign user `123` to application findings based on filter of patch id `123`
                >>> self.{risksenseobject}.application_findings.assign([{"field":"source_patch_ids","exclusive":False,"operator":"IN","value":"123"}],[123])
        Note:
            You can also dump the application findings data before assigning them to users using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.application_findings.assign([{"field":"source_patch_ids","exclusive":False,"operator":"IN","value":"123"}],[123],csvdump=True)
            
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/assign"

        body = {
            "filters": search_filters,
            "userIds": user_ids
        }


        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationfindingtagisassigned',search_filters)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error assigning tag')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def unassign(self, search_filters:list, user_ids:list,csvdump:bool=False, client_id:int=None)->int:

        """
        Unassigns user(s) from application findings.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            user_ids:        A list of user IDs to which application findings to be unassigned.
            csvdump:         Dumps data in csv  
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The job ID in the platform is returned.
        
        Example:
            
            Lets unassign user `123` from application findings based on filter of patch id `123`
            
            >>> self.{risksenseobject}.application_findings.unassign([{"field":"source_patch_ids","exclusive":False,"operator":"IN","value":"123"}],[123])
        Note:
            You can also dump the application findings data before unassigning them from users using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.application_findings.unassign([{"field":"source_patch_ids","exclusive":False,"operator":"IN","value":"123"}],[123],csvdump=True)
            
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/unassign"

        body = {
            "filters": search_filters,
            "userIds": user_ids
        }
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error unassigning tag')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport(f'applicationfindingtagisunassigned',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def getdynamiccolumns(self,client_id:int=None)->list:

        """
        Gets Dynamic columns for the application findings.

        Args:
            client_id: If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The Dynamic columns

        Examples:
            >>>  self.{risksenseobject}.application_findings.getdynamiccolumns()
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
        
    def getexporttemplate(self,client_id:int=None)->list:

        """
        Gets configurable export template for application findings.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The Exportable fields

        Example:
            An example to use getexporttemplate
                
            >>> self.{risksenseobject}.application_findings.getexporttemplate()

            This gets all the export templates for application findings
    
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/export/template"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error getting export template')
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
        Gets configurable export template by id for application findings.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The Exportable fields
        Example:
            An example to use getexporttemplate
                
            >>> self.{risksenseobject}.application_findings.getexporttemplatebyid(id)

            This gets the export template of the id for application findings

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
        Gets created existing export template for application findings.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The Exportable fields
        Example:
            An example to use getexporttemplates
                
            >>> self.{risksenseobject}.application_findings.getexporttemplates()

            This gets all the export templates for application findings

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
        Initiates an export job on the platform for application finding(s) based on the
        provided filter(s), by default fetches all the columns data.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.

            file_name:       The name to be used for the exported file.

            row_count:      No of rows to be exported. Available options
                            ExportRowNumbers.ROW_10000,
                            ExportRowNumbers.ROW_25000,
                            ExportRowNumbers.ROW_50000,
                            ExportRowNumbers.ROW_100000,
                            ExportRowNumbers.ROW_ALL

            file_type:       File type to export. ExportFileType.CSV, ExportFileType.JSON,  or ExportFileType.XLSX

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

            export_id: The export id of an existing export template to use

        Return:
            The job ID in the platform from is returned.

        Example:
            An example to use export is
            
                >>> self.{risksenseobject}.application_findings.export([],'testingexport')
            
            You can change the filetype to any of the names above or even the other positional arguments as mentioned

                >>> self.{risksenseobject}.application_findings.export([],'testingexport',file_type=ExportFileType.JSON)
        """
        func_args = locals()
        func_args['exportable_filter']=self.getexporttemplate()
        func_args.pop('self')
        if export_id==None:
            func_args['exportable_filter']=self.getexporttemplate()
        elif export_id!=None:
            func_args['exportable_filter']=self.getexporttemplatebyid(export_id)
        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]
        try:
            export_id = self._export(self.subject_name, **func_args)

        except (RequestFailed,Exception) as e:
            print('There was an error performing export job')
            print(e)
            exit()
        return export_id
  

    def subscribe_new_open_ransomware_findings(self,client_id:int=None)->dict:

        """
        Subscribes the user to new open ransomware findings

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The response to the subscription that was performed

        Example:

            An example to use subscribe_new_open_ransomware_findings()
                
                >>> self.{risksenseobject}.application_findings.subscribe_new_open_ransomware_findings()
            
            This helps the user subscrive to new open ransomware findings

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=4,subscribe=True)
        except (RequestFailed,Exception) as e:
            print('There was an error subscribing new open ransomware findings')
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
                
                >>> self.{risksenseobject}.application_findings.unsubscribe_new_open_ransomware_findings()
            
            This helps the user unsubscribe from new open ransomware findings

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=4)
        except (RequestFailed,Exception) as e:
            print('There was an error unsubscribing new open ransomware findings')
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
                
                >>> self.{risksenseobject}.application_findings.subscribe_new_open_critical_findings_vrr()
            
            This helps the user subscribe to new open critical findings based on vrr.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=5,subscribe=True)
        except (RequestFailed,Exception) as e:
            print('There was an error subscribing new open critical findings vrr')
            print(e)
            exit()

        return subscribe

    def unsubscribe_new_open_critical_findings_vrr(self,client_id:int=None)->dict:

        """
        Unsubscribes the user from new open critical findings

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The response to the subscription that was performed

        Example:

            An example to use unsubscribe_new_open_critical_findings_vrr()
                
                >>> self.{risksenseobject}.application_findings.unsubscribe_new_open_critical_findings_vrr()
            
            This helps the user to unsubscribe from new open critical findings based on vrr.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=6,subscribe=True)
        except (RequestFailed,Exception) as e:
            print('There was an error unsubscribing new open critical findings severity')
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
                
                >>> self.{risksenseobject}.application_findings.subscribe_new_open_critical_findings_severity()
            
            This helps the user subscribe to new open critical findings based on severity.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=6)
        except (RequestFailed,Exception) as e:
            print('There was an error unsubscribing new open critical findings severity')
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
                
                >>> self.{risksenseobject}.application_findings.unsubscribe_new_open_critical_findings_severity()
            
            This helps the user unsubscribe from new open critical findings based on severity.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=6)
        except (RequestFailed,Exception) as e:
            print('There was an error unsubscribing new open critical findings severity')
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
                
                >>> self.{risksenseobject}.application_findings.subscribe_new_open_high_findings_vrr()
            
            This helps the user subscribe to new open high findings based on vrr.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=7,subscribe=True)
        except (RequestFailed,Exception) as e:
            print('There was an error subscribing new open high findings vrr')
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
                
                >>> self.{risksenseobject}.application_findings.unsubscribe_new_open_high_findings_vrr()
            
            This helps the user unsubscribe from new open high findings based on vrr.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=7)
        except (RequestFailed,Exception) as e:
            print('There was an error unsubscribing new open high findings vrr')
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
                
                >>> self.{risksenseobject}.application_findings.subscribe_new_open_high_findings_severity()
            
            This helps the user subscribe to new open high findings based on severity.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=8,subscribe=True)
        except (RequestFailed,Exception) as e:
            print('There was an error subscribing new open high findings severity')
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
                
                >>> self.{risksenseobject}.application_findings.unsubscribe_new_open_high_findings_severity()
            
            This helps the user unsubscribe from new open high findings based on severity.

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=8)
        except (RequestFailed,Exception) as e:
            print('There was an error unsubscribing to new open high findings severity')
            print(e)
            exit()

        return subscribe

    def update_due_date(self, search_filters:list, due_date:str,csvdump:bool=False, client_id:int=None)->int:

        """
        Update the due date for remediation of an application finding.

        Args:

            search_filters:  A list of dictionaries containing filter parameters.
            due_date:        The due date to assign.  Must be in "YYYY-MM-DD" format.
            csvdump:         Dumps the data in csv
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID in the platform is returned.
        
        Example:
            
            Lets update an application finding id 1234 to due date 2022-08-11
            
            >>> self.{risksenseobject}.application_findings.update_due_date([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],'2022-08-11')
        Note:
            You can also dump the application findings data after updating their due date using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.application_findings.update_due_date([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],'2022-08-11',csvdump=True)

        """




        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        url = self.api_base_url.format(str(client_id)) + "/update-due-date"
        
        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "dueDate": due_date
        }
        
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error updating due date')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('applicationfindingsduedateupdated',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id
    
    def self_assign(self,filterfields:list,userid:list,csvdump:bool=False,client_id:int=None)->int:

        """
        The application findings fetched are assigned to the current user

        Args:
            filterfields:  A list of dictionaries containing filter parameters.
            userid:           A list of user IDs to be assigned to application findings(s).
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:         dumps the data in csv
        Return:
            The job ID in the platform is returned.

        Example:
            
            Lets assign user `123` to application finding `1234`
            
            >>> self.{risksenseobject}.application_finding.self_assign([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],[123])
        Note:
            You can also dump the application findings data before assigning them to users using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.application_finding.self_assign([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],[123],csvdump=True)
        """

        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/self-assign"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()
 
        if csvdump==True:
            self.downloadfilterinexport('applicationfindingsselfassign',filterfields)

        body = {
                "filters": filterfields,
                "userIds": userid
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error performing self assignment')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id
    
    def self_unassign(self,filterfields:list,userid:list,csvdump:bool=False,client_id:int=None)->int:

        """
        The application findings fetched are unassigned from users

        Args:
            filterfields:  A list of dictionaries containing filter parameters.
            userid:           A list of user IDs to be assigned to Application Findings(s).
            csvdump:         dumps the data in csv
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID in the platform is returned.
        Example:
            
            To unassign user 123 from finding id 1234
            
            >>> self.{risksenseobject}.application_findings.self_unassign([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],[123])
        Note:
            You can also dump the application findings data before unassigning them from users using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.application_findings.self_unassign([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],[123],csvdump=True)

        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/self-unassign"

        if csvdump==True:
            self.downloadfilterinexport('applicationfindingsselfunassign',filterfields)

        body = {
                "filters": filterfields,
                "userIds": userid
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error performing self unassignment')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def add_note(self, search_filters:list, note:str,csvdump:bool=False, client_id:int=None)->int:

        """
        Add a note to application finding(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            note:            A note to assign to the application findings.
            csvdump:         dumps the data in csv
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID in the platform is returned.
        Example:
            
            To add a note 'testing' to application finding id 123
            
            >>> self.{risksenseobject}.application_findings.add_note([{"field":"id","exclusive":False,"operator":"IN","value":"123"}],'testing')
        Note:
            You can also dump the application findings data post adding a note using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.application_findings.add_note([{"field":"id","exclusive":False,"operator":"IN","value":"123"}],'testing',csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/note"

        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "note": note
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error adding notes')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('addnote',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def add_ticket_tag(self,search_filters:list,tag_id:int,client_id:int=None)->int:

        """
        Adds a ticket tag to the application findings based on a search filter

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            tag_id:         The tag id
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID in the platform is returned.
        
        Example:
            To add a ticket tag to application findings

            >>> self.{risksenseobject}.application_findings.add_ticket_tag([],123)

        """
        

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/search/applicationFinding/job/tag'

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

    def delete_manage_observations(self,applicationfindingid:int,vulnrequestid:int,csvdump:bool=False,client_id:int=None)->bool:

        """
        Delete manage observations

        Args:
            applicationfindingid:    Application finding id
            vulnrequestid:     Vulnerability request id
            csvdump:         dumps the data in csv
            client_id:        Client id of user, if none gets default client id

        Return:
            Success response 
        
        Example:
            
            To delete observation linked to application finding id 123 and vulnrequest id 1234
            
            >>> self.{risksenseobject}.application_findings.delete_manage_observations(123,1234)
        Note:
            You can also dump the application findings data before deleting the manage observation using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.application_findings.delete_manage_observations(123,1234,csvdump=True)

        
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/{}/request/{}".format(applicationfindingid,vulnrequestid)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('deletemanageobservations',[{"field":"id","exclusive":False,"operator":"IN","value":f"{applicationfindingid}"}])

        try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url=url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        success=True
        return success
        
    def delete(self, search_filters:list, csvdump:bool=False,client_id:int=None)->int:

        """
        Delete application findings based on filter(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID from the platform is returned.
        Example:
            
            To delete application finding by id 12345
            
            >>> self.{risksenseobject}.application_findings.delete([{"field":"id","exclusive":False,"operator":"IN","value":"12345"}])
        Note:
            You can also dump the application findings data before deleting the application findings using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.application_findings.delete([{"field":"id","exclusive":False,"operator":"IN","value":"12345"}],csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationfindingsthataredeleted',search_filters)
        
        url = self.api_base_url.format(str(client_id)) + "/delete"

        body = {
            "filterRequest": {
                "filters": search_filters
            }
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error delete application findings')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def _tag(self, search_filters:list, tag_id:int, is_remove:bool=False,client_id:int=None)->int:

        """
        Add/Remove a tag to application findings.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            tag_id:          The tag ID to apply.
            is_remove:       remove tag? Mention true if need to be removed or false if to add       
            client_id:       Client ID.
        Return:
            The job ID is returned.
        
        Example:
            
            To add a tag 
            
            >>> self.{risksenseobject}.application_findings._tag([{"field":"id","exclusive":False,"operator":"IN","value":"12345"}],123,is_remove=False)

            To delete a tag

            >>> self.rs.application_findings._tag([{"field":"id","exclusive":False,"operator":"IN","value":"12345"}],123,is_remove=True)
            
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/tag"

        body = {
            "tagId": tag_id,
            "isRemove": is_remove,
            "filterRequest": {
                "filters": search_filters
            }
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching adding or removing tag for application findings')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def map_findings(self, filter_request:list,workflowtype:str,workflowuuid:str,csvdump:bool=False, client_id:int=None)->bool:

        """
        Maps findings to a worklow request based on workflow uuid.

        Args:
            filter_request:      A list of dictionaries containing filter parameters.
            workflowtype:         Type of workflow, either falsePositive,remediation,acceptance,severityChange. Please use the exact names as above for workflow type.
            workflowuuid:        Uuid of the workflow.
            csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            Whether success or not.
        Example:
            
            To map a workflow 'st1234' to finding by id '123' of type severitychange
            
            >>> self.{risksenseobject}.application_findings.map_findings([{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"123"}],'severityChange','st1234')
        Note:
            You can also dump the application findings data post mapping the findings using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.application_findings.map_findings([{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"123"}],'severityChange','st1234',csvdump=True)

        """


        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/map'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":"applicationFinding","filterRequest":{"filters":filter_request}}

        
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error mapping application findings data')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('applicationfindingsmappedtotheworkflow',filter_request)

        success=True
        
        return success

    def unmap_findings(self, filter_request:list,workflowtype:str,workflowuuid:str,csvdump:bool=False,client_id:int=None)->bool:

        """
        Unmaps findings from worklow request based on workflow uuid.

        Args:
            filter_request:      A list of dictionaries containing filter parameters.
            workflowtype:         Type of workflow, either falsePositive,remediation,acceptance,severityChange. Please use the exact names as above for workflow type.
            workflowuuid:        Uuid of the workflow.
            csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            Whether success or not.
        Example:
            
            To unmap a workflow 'st1234' from finding by id '123' of type severitychange
            
            >>> self.{risksenseobject}.application_findings.unmap_findings([{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"123"}],'severityChange','st1234')
        Note:
            You can also dump the application findings data before unmapping the findings using :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.application_findings.unmap_findings([{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"123"}],'severityChange','st1234',csvdump=True)

        """


        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/unmap'.format(str(client_id),workflowtype.lower(),workflowuuid)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        if csvdump==True:
            self.downloadfilterinexport('applicationfindingsunmappedfromkworkflow',filter_request)

        body = {"subject":"applicationFinding","filterRequest":{"filters":filter_request}}



        try:

            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error performing unmap of application findings')
            print(e)
            exit()
        success= True

        return success



    ##### BEGIN PRIVATE FUNCTIONS #####################################################

 


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
