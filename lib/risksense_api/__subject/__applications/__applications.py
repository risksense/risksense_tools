"""
****Application module defined for different application related api endpoints.****
"""
""" *******************************************************************************************************************
|
|  Name        :  __applications.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating Applications on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

from ast import Delete
from cmath import e
import json
from json.encoder import INFINITY
from sqlite3 import IntegrityError

from risksense_api import SearchFilter
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
from ..__exports import Exports
import csv
import zipfile
import sys
import pandas as pd


class Applications(Subject):

    """ **Class for Applications function defintions**.

    To utlise Applications function:

    Args:
            profile:     Profile Object
    
    Usage:
        :obj:`self.{risksenseobjectname}.applications.{function}`
    
    Examples:
        To delete application using :meth:`delete()` function

        >>> self.{risksenseobject}.applications.delete({applicationfilter})

    """

    def __init__(self, profile):

        """**Initialization of Applications Object** .

        Args:
            profile:     Profile Object

        """

        

        self.subject_name = "application"
        Subject.__init__(self, profile, self.subject_name)

    def create(self, name:str,groupids:list,networkid:int,applicationurl:str,criticality:int,externality:bool=False,csvdump:bool=False, client_id:int=None)->dict:

        """
        Create an application

        Args:
             name:  Name of the application .

             groupids:  ids of the groups you want it to be assigned to

             networkid:       network id. Id of network the application to be a part of

             applicationurl:       url of the application.

             criticality:  the application criticality

             externality: the application whether external or internal. Externality is true if application is external , false if internal

             csvdump:         dumps the data in csv

             client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Jsonified response.
        Examples:
            To create an application:

            >>>  self.{risksenseobject}.applications.create('applicationname',[1,2,3],123,'webpagetest.org',5,False)
        
        Note:
            You can also dump the job id of the created application using :obj:`csvdump=True` argument:
            
            >>>  self.{risksenseobject}.applications.create('applicationname',[1,2,3],123,'webpagetest.org',5,False,csvdump=True)

        """


        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        body =  {"name":name,"groupIds":groupids,"networkId":networkid,"url":applicationurl,"criticality":criticality,"externality":externality}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in creating application')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            jobid={'applicationid':[jsonified_response['id']]}
            df=pd.DataFrame(jobid)
            df.to_csv('applicationid.csv')

        return jsonified_response

    def delete(self, filterrequest:list,csvdump:bool=False, client_id:int=None)->dict:

        """
        Deletes an application

        Args:

         filterrequest:  Search filters .

         csvdump:         dumps the data in csv

         client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
         

        Return:
            The Jsonified response.
        
        Examples:
            To delete an application:

            >>>  self.{risksenseobject}.applications.delete([])
        
        Note:
            You can also dump the application data that is going to be deleted by adding a :obj:`csvdump=True` argument:
            
            >>>  self.{risksenseobject}.applications.delete([],csvdump=True)
        


        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/delete'

        body =  {"filterRequest":{"filters":filterrequest}}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('deletedapplications',filterrequest)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in creating application')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response



    def downloadfilterinexport(self,filename:str,filters:dict,client_id:int=None):

        """ **Exports and Downloads a file based on the filters defined** .


        Args:
            filename: Name of the file to export as
            filters:  Application search filters based on which the export performs
            client_id: The client id to get the data from. If not supplied, takes default client id

        *IGNORE Internal function*

        Examples:
            >>>  self.{risksenseobject}.applications.downloadfilterinexport('applicationdata',[])
        """

        if client_id is None:
            client_id= self._use_default_client_id()
        exportid=self.export(filters,file_name=filename)
        self.exports=Exports(self.profile)
        while(True):
                try:
                    exportstatus=self.exports.check_status(exportid)
                    print(exportstatus)
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
        except(RequestFailed,MaxRetryError,StatusCodeError, ValueError) as e:
                    print(e)
                    print()
                    print("Unable to retrieve file. Exiting.")
                    sys.exit(1)

    def list_application_filter_fields(self,client_id:int=None)->list:

        """
        Lists application filter fields.

        Args:

            client_id:  Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The JSON output from the platform is returned, listing the available filters.
        
        Example:
            >>>  self.{risksenseobject}.applications.list_application_filter_fields()

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

    def get_single_search_page(self, search_filters:list, page_num:int=0, page_size:int=150,
                               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC, client_id:int=None)->dict:

        """
        Searches for and returns applications based on the provided filter(s) and other parameters for a single page.

        Args:
            search_filters:  List of dictionaries containing filter parameters.
            page_num:        Page number of results to be returned.
            page_size:       Number of results to be returned per page.
            sort_field:      Name of field to sort results on.
            sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The paginated JSON response from the platform is returned.
        
        Example:
            An example to get single search page of applications data
            
            >>> self.{risksenseobject}.applications.get_single_search_page([])

            You can also try changing the other arguments to your liking to reflect the data as you suffice such as 'change page_size` or `page_num` etc.

            >>> self.{risksenseobject}.applications([],page_num=2,page_size=10)
        """

        func_args = locals()
        func_args.pop('self')

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()
        try:
            response = self._get_single_search_page(self.subject_name, **func_args)
        except (RequestFailed,Exception) as e:
            print('Error finding application data')
            print(e)
            exit()

        return response

    def get_groupby_application(self,client_id:int=None)->dict:

        """
        Get groupby keymetrics for applications

        Args:
            client_id:      The client id , if none, default client id is taken
        Return:
            The keymetrics for groupby
        
        Example:
            >>>  self.{risksenseobject}.applications.get_groupby_application()
        **IGNORE INTERNAL FUNCTION**
        Note:
            This function just returns the groupby key metrics
        
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/group-by"

        try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error getting group by application data')
            print(e)
            exit()


        jsonified_response = json.loads(raw_response.text)

        applicationgroupbykeymetrics={}
        
        for i in range(len(jsonified_response['groupByFields'])):
            applicationgroupbykeymetrics[jsonified_response['groupByFields'][i]['key']]=[jsonified_response['groupByFields'][i]['groupMetrics'][j]['key'] for j in range(len(jsonified_response['groupByFields'][i]['groupMetrics']))]
            
        return applicationgroupbykeymetrics


    def groupby_application(self,filters:list=[],sortorder:str=None,csvdump:bool=False,client_id:bool=None)->dict:

        """
        Get groupby values for applications

        Args:

            filters:        The filters which will populate in groupby
            sortorder: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
            csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
            client_id:      The client id , if none, default client id is taken
        
        Return:
            The groupby values of the application.
        
        Example:

            >>>  self.{risksenseobject}.applications.groupby_application({filter})
        
            The filter must be provided for the group by to be used. The groupby fields will be displayed in the `terminal` and you must choose a `group by` filter to which the data will be populated      

        Note:
            This function also has an option to dump the data in a csv by a simple argument, :obj:`csvdump=True`

            >>>  self.{risksenseobject}.applications.groupby_application({filter},csvdump=True)
        
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/group-by"

        applicationslist=self.get_groupby_application()

        applicationskeys=list(applicationslist.keys())

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()
        try:
            for i in range(len(applicationskeys)):
                print(f'Index-{i},Key:{applicationskeys[i]}')
            keymetric=applicationskeys[int(input('Please enter the key for group by parameter:'))]
        except IndexError as ex:
            print()
            print('There was an error fetching group by data')
            print(ex)
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
                "metricFields": applicationslist[keymetric],
                "filters": filters,
                "sortOrder": sortorder
                }
        try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching group by data')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        try:
            if csvdump==True:
                field_names = []
                for item in jsonified_response['data'][0]:
                    field_names.append(item)
                try:
                    with open('applicationgroupby.csv', 'w') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        for item in jsonified_response['data']:
                            writer.writerow(item)
                except (FileNotFoundError,Exception) as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
                    exit()
                else:
                    return jsonified_response
        except (Exception,RequestFailed) as e:
            print('Error dumping data in csv')
            print()
            print(e)
            exit()

        return jsonified_response


    def search(self, search_filters:list, page_size:int=150, sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC, csvdump:bool=False,client_id:int=None)->list:

        """
        Searches for and returns applications based on the provided filter(s) and other parameters.  Rather than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        Args:

            search_filters:  A list of dictionaries containing filter parameters.

            page_size:       The number of results per page to be returned.

            sort_field:      The field to be used for sorting results returned.

            sort_dir:        The direction of sorting to be used. SortDirection.ASC or SortDirection.DESC

            csvdump:         dumps the data in csv

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            A list containing all applications returned by the search using the filter provided.

         Example:
            An example to search for application data is
            
            >>> self.{risksenseobject}.applications.search([])

        Note:
            You can also dump the search based data in a csv by simply providing :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.applications.search([],csvdump=True)
        """

        func_args = locals()
        func_args.pop('self')
        func_args.pop('csvdump')
        all_results = []

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            page_info = self._get_page_info(subject_name=self.subject_name, search_filters=search_filters,
                                            page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except (RequestFailed,Exception) as e:
            print('Error fetching application data')
            print(e)
            exit()


        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed,Exception) as e:
            print('Error fetching application data')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('applcationsearch',search_filters)

        return all_results

    def get_count(self, search_filters:list, client_id:int=None)->int:

        """
        Gets a count of applications identified using the provided filter(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The number of applications identified using the filter(s).
        Example:
            
            To get count of the appplications

            >>> self.{risksenseobject}.applications.get_count([])

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self.get_single_search_page(search_filters, client_id=client_id)
        except (RequestFailed,Exception) as e:
            print('Error fetching application data')
            print(e)
            exit()


        count = response['page']['totalElements']

        return count

    def merge_application(self, searchfilters:list,application_id_to_merge_to:int, csvdump:bool=False,client_id:int=None)->int:

        """
        Merges applications based on search filters to the application id provided.

        Args:
            searchfilters:  A list of dictionaries containing filter parameters.
            application_id_to_merge_to: Application id to merge to.

            csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID is returned.

        Example:
            An example to use merge_application is
            
                >>> self.{risksenseobject}.applications.merge_application([],123)

        Note:
                You can also dump the applications that are going to be merged before merging them by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.applications.merge_application([],123,csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationsmerged',searchfilters)

        url = self.profile.platform_url+'/api/v1/client/{}/search/application/job/merge'.format(str(client_id))

        body = {"filterRequest":{"filters":searchfilters},"sourceId":application_id_to_merge_to}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in merging applications')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def set_asset_criticality(self, filter:list,assetcriticality:int, csvdump:bool=False,client_id:int=None)->int:

        """
        Set asset criticality for the application.

        Args:
            filter:  A list of dictionaries containing filter parameters.

            assetcriticality:  The asset criticality to set the filter specified applications to.

            csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID is returned.
        
        Example:
            To set asset criticality based on id

            >>> self.{risksenseobject}.applications.set_asset_criticality([{"field":"id","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"1234"}],3)
        
        Note:
                You can also dump the applications to which asset criticality should be changed by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.applications.set_asset_criticality([{"field":"id","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"1234"}],3,csvdump=True)


        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        body = {"filterRequest":{"filters":filter},"criticality":assetcriticality}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in setting asset criticality')
            print(e)
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationssetassetcriticality',filter)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def set_address_type(self, filter:list,addresstype:str, csvdump:bool=False,client_id:int=None)->int:

        """
        Set address type for the application.

        Args:
            filter:  A list of dictionaries containing filter parameters.

            addresstype:    The address type whether external or internal, provide string external for external and internal for internal 

            csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The job ID is returned.
        
        Example:
            
            To set address type based on id
            
            >>> self.{risksenseobject}.applications.set_address_type([{"field":"id","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"1234"}],"EXTERNAL")

        Note:
                You can also dump the applications which the address type will be set by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.applications.set_address_type([{"field":"id","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"1234"}],"EXTERNAL",csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update"

        if addresstype.lower()=='internal':
            addresstypes=False
        if addresstype.lower()=='external':
            addresstypes=True

        body = {"filterRequest":{"filters":filter},"isExternal":addresstypes}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in setting address type')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('applicationssetaddresstype',filter)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def edit_application(self,filter:list,name:str,url:str,csvdump:bool=True,client_id:int=None)->int:

        """
        Edit an application.

        Args:
            filter:  A list of dictionaries containing filter parameters.

            name:    Name of the application

            url:    Url of the application

            csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The job ID is returned.
        
        Example:
            To edit an application based on an id :obj:`1234` from platform
           
            >>> self.{risksenseobject}.applications.edit_application([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],name='test1',url='10.1.1.1/app')

        Note:
                You can also dump the applications which are edited by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.applications.edit_application([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],name='test1',url='10.1.1.1/app',csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update"

        body = {"filterRequest":{"filters":filter,"sort":[],"projection":"basic","page":0,"size":10},"name":name,"url":url}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in setting address type')
            print(e)
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationupdates',filter)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id


    def add_tag(self, search_filters:list, tag_id:int,csvdump:bool=False, client_id:int=None)->int:

        """ 
        Add a tag to application(s).

        Args:
            
            search_filters:  A list of dictionaries containing filter parameters.
            
            tag_id:          The tag ID to add to the application(s).
            
            csvdump:         dumps the data in csv
            
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The job ID is returned.

        Example:
            To add a tag for an application id :obj:`1234` to tag :obj:`123`

            >>> self.rs.applications.add_tag([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],123)
        
        Note:
                You can also dump the applications to which tags are added post tag addition by :obj:`csvdump=True` argument

                >>> self.rs.applications.add_tag([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],123,csvdump=True)
        
                
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
            print('Please provide either true or false')
            exit()
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in adding tag')
            print(e)
            exit()

        if csvdump==True:
            self.downloadfilterinexport('appfindingtagadddata',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def remove_tag(self, search_filters:list, tag_id:int, csvdump:bool=False,client_id:int=None)->int:

        """
        Remove a tag from application(s).
    
        Args:
            search_filters:  A list of dictionaries containing filter parameters.

            tag_id:          The tag ID to remove from the application(s).

            csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The job ID is returned.
        
        Example:
            To remove a tag from an application id :obj:`1234` from tag :obj:`123`

            >>> self.rs.applications.remove_tag([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],123)
        
        Note:
                You can also dump the applications to which tags are removed before tag removal by :obj:`csvdump=True` argument

                >>> self.rs.applications.remove_tag([{"field":"id","exclusive":False,"operator":"IN","value":"1234"}],123,csvdump=True)
        
        


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
            self.downloadfilterinexport('applicationsremovetag',search_filters)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in removing tag')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def getexporttemplate(self,client_id:int=None)->list:

        """
        Gets configurable export template for Applications.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The Exportable fields

        Example:
            An example to use getexporttemplate
                
                >>> self.{risksenseobject}.applications.getexporttemplate()

            This gets all the export templates for applications
    
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/export/template"
        print(url)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting export template')
            print(e)
            exit()

        exportablefilter = json.loads(raw_response.text)

        for i in range(len(exportablefilter['exportableFields'])):
            for j in range(len(exportablefilter['exportableFields'][i]['fields'])):
                if exportablefilter['exportableFields'][i]['fields'][j]['selected']==False:
                    exportablefilter['exportableFields'][i]['fields'][j]['selected']=True

        return exportablefilter['exportableFields']


    def export(self, search_filters:list, file_name:str, row_count:str=ExportRowNumbers.ROW_ALL,file_type:str=ExportFileType.CSV, client_id:int=None)->int:

        """
        Initiates an export job on the platform for application(s) based on the
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
        
            file_type:       File type to export.  ExportFileType.CSV, ExportFileType.JSON, or ExportFileType.XLSX

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The job ID in the platform from is returned.
        
        Example:
            An example to use export is
            
                >>> self.{risksenseobject}.applications.export([],'testingexport')
            
            You can change the filetype to any of the names above or even the other positional arguments as mentioned

                >>> self.{risksenseobject}.applications.export([],'testingexport',filetype=ExportFileType.JSON)

        """
        func_args = locals()
        func_args['exportable_filter']=self.getexporttemplate()
        func_args.pop('self')
        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]
        try:
            export_id = self._export(self.subject_name, **func_args)
        except (RequestFailed,Exception) as e:
            print('Error in exporting application data')
            print(e)
            exit()

        return export_id


    def network_move(self, search_filters:list, network_id:int, force_merge:bool=False,csvdump:bool=False, client_id:int=None)->int:

        """
        Move an application to a different network.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.

            network_id:      The ID of the network the application should be moved to.

            force_merge:     Boolean indicating whether or not a merge should be forced.

            csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The job ID is returned.
        
        Example:
            
            To move an application in id :obj:`123` to network :obj:`1234`
   
            >>> self.{risksenseobject}.applications.network_move([{"field":"id","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"123"}],1234)

        Note:
                You can also dump the applications that are being moved by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.applications.network_move([{"field":"id","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"123"}],1234,csvdump=True)



        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/network/move"

        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "targetNetworkId": network_id,
            "isForceMerge": force_merge
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in moving application across network')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('applicationsnetworkmove',search_filters)


        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id
    

    def run_urba(self, search_filters:list,csvdump:bool=False, client_id:int=None)->int:

        """
        Initiates the update of remediation by assessment for application(s) specified in filter(s).

        Args:

            search_filters:  A list of dictionaries containing filter parameters.

            csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The job ID is returned.
        
        Example:
            An example to use run_urba for an application 123 is
           
                >>> self.{risksenseobject}.applications.run_urba([{"field":"id","exclusive":False,"operator":"IN","value":"123"}])
        Note:
                You can also dump the applications to which urba is being run by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.applications.run_urba([{"field":"id","exclusive":False,"operator":"IN","value":"123"}],csvdump=True)

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
            self.downloadfilterinexport('applicationsrunurba',search_filters)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in running urba')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id


    def add_note(self, search_filters:list, note:str,csvdump:bool=False, client_id:int=None)->int:

        """
        Add a note to applications based on search filters.

        Args:
            
            search_filters:  A list of dictionaries containing filter parameters.
            
            note:            A note to be added to the application(s).
            
            csvdump:         dumps the data in csv
           
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The job ID is returned.

        Example:

            An example to use add_note is
           
                >>> self.{risksenseobject}.applications.add_note([],'test')

        Note:
                You can also dump the applications to which notes will be added post adding the note by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.applications.add_note([],'test',csvdump=True)
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
            print('Error in adding note')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('addnote',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def get_model(self, client_id:int=None)->dict:

        """
        Get available projections and models for Applications.

        Args:
            client_id:   Client ID

        Return:    
            Application projections and models are returned.

        Example:
            An example to use get_model is
           
                >>> self.{risksenseobject}.applications.get_model()
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
        except (RequestFailed,Exception) as e:
            print('Error in getting model')
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

            An example to use suggest for assessment labels is
           
                >>> self.{risksenseobject}.applications.suggest([],{"field":"assessment_labels","exclusive":False,"operator":"WILDCARD","value":"","implicitFilters":[]})
            

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._suggest(self.subject_name, search_filter_1, search_filter_2, client_id)
        except (RequestFailed,Exception) as e:
            print('Error in suggesting value for filter fields')
            print(e)
            exit()

        return response

    def add_group(self, search_filter:list, group_ids:list,csvdump:bool=False, client_id:int=None)->int:

        """
        Add application(s) to one or more groups.

        Args:
            search_filter:   Search filter
            group_ids:       List of Group IDs to add to application(s).
            csvdump:         dumps the data in csv
            client_id:       Client ID

        Return:
            Job ID of group add job
        
        Example:
            An example to use add_group is
           
                >>> self.{risksenseobject}.applications.add_group([],[2,3,4])

        Note:
                You can also dump the applications which will be addedd to the groups by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.applications.add_group([],[2,3,4],csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        try:
            response = self._add_group(self.subject_name, search_filter, group_ids, client_id)
        except (RequestFailed,Exception) as e:
            print('Error in adding applications to group')
            print(e)
            exit()

                
        if csvdump==True:
            self.downloadfilterinexport('addgroup',search_filter)

        return response

    def remove_group(self, search_filter:list, group_ids:list,csvdump:bool=False,client_id:int=None)->int:

        """
        Remove application(s) from one or more groups.

        Args:
            search_filter:   Search filter
            group_ids:       List of Group IDs to add to application(s).
            csvdump:         dumps the data in csv
            client_id:       Client ID

        Return:
            Job ID of group remove job
        
        Example:
            
            An example to use remove_group is
           
                >>> self.{risksenseobject}.applications.remove_group([],[2,3,4])

        Note:
                You can also dump the applications which will be removed from the groups by :obj:`csvdump=True` argument

                >>> self.{risksenseobject}.applications.remove_group([],[2,3,4],csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            response = self._remove_group(self.subject_name, search_filter, group_ids, client_id)
        except (RequestFailed,Exception) as e:
            print('Error in removing from group')
            print(e)
            exit()

        if csvdump==True:
            self.downloadfilterinexport('removegroup',search_filter)

        return response

### Private Functions

    def apply_system_filters(self, csvdump:bool=False,client_id:int=None)->list:

        """
        Get data from system filters for applications.

        Args:

            csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The data of the application findings based on the system filter chosen.
        
        Example:
            An example to use apply_system_filters is
            
            >>> self.{risksenseobject}.applications.apply_system_filters()

            The system filters will be displayed in the terminal to which you must provide a key value and the data returned will reflect based on the system filter chosrn

        Note:
            You can also dump the applications from the system filters search by :obj:`csvdump=True` argument

             >>> self.{risksenseobject}.applications.apply_system_filters(csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        url= self.profile.platform_url + "/api/v1/search/systemFilter"

        try:
            systemfilter = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error getting data')
            print()
            print(e)
            exit()
        
        systemfilter=json.loads(systemfilter.text)

        systemfilters={}

        for filter in systemfilter:
            for applicationsystemfilter in filter['subjectFilters']:
                if applicationsystemfilter['subject']=="application":
                    systemfilters[filter['name']]=applicationsystemfilter["filterRequest"]
    
        systemfilterkeys=list(systemfilters.keys())
        i=0
        try:
            for key in systemfilterkeys:
                print(f'Index-{i},Key:{key}')
                i=i+1
            actualfilter=systemfilters[ systemfilterkeys[int(input('Please enter the key for system filter parameter:'))]]
        except (IndexError) as ex:
            print()
            print('There was an error fetching system filters data')
            print('Please enter an index number from the above list')
            print(ex)
            exit()
        except (Exception) as e:
            print('There was an error fetching system filters data')
            print(e)
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationsystemfilterdata',actualfilter['filters'])

        response=self.search(actualfilter['filters'])

        return response



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
