"""
Group module defined for different group related api endpoints.
"""

""" *******************************************************************************************************************
|
|  Name        :  __groups.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating groups on the RiskSense Platform.
|  Copyright   : (c) RiskSense, Inc.
|  License     : Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """


import json
import profile
from ...__subject import Subject
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ..__notifications import Notifications
from ..._params import *
from ..._api_request_handler import *
from ..__exports import Exports
import zipfile
import sys
import csv


class Groups(Subject):

    """Class for group function definitions.

    Args:
        profile:     Profile Object

    To utlise group function:
    
    Usage:
        :obj:`self.{risksenseobjectname}.groups.{function}`
    
    Examples:
        To create a group using :meth:`create` function

        >>> self.{risksenseobjectname}.groups.create(args)

    """

    def __init__(self, profile:object):

        """
        Initialization of Groups object.

        Args:
            profile:     Profile Object

        """
        self.profile=profile
        self.subject_name = "group"
        Subject.__init__(self, profile, self.subject_name)

    def downloadfilterinexport(self,filename:str,filters:list,client_id:int=None):
        """
        Download group data based on search filters.

        Args:
            filename: Name of the file
            filters: A list of dictionaries containing filter parameters
            client_id: Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Note:
            **IGNORE** - Internal funtion for csv dump

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
        except(RequestFailed,MaxRetryError,StatusCodeError, ValueError) as ex:
                    print(ex)
                    print()
                    print("Unable to retrieve file. Exiting.")
                    sys.exit(1)

    def list_group_filter_fields(self,client_id:int=None)->dict:

        """
        List filter endpoints.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The JSON output from the platform is returned, listing the available filters.

        Examples:
            >>> apiobj = self.{risksenseobject}.groups.list_group_filter_fields()
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

    def edit_group_properties(self,groupids,groupproperty1=False,groupproperty2=False,groupproperty3=False,groupproperty4=False,groupproperty5=False,client_id:int=None)->dict:

        """
        Edit group properties

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            Group_id:        Group IDs
            Group_property1: Edit Group Property 1, bool
            Group_property2: Edit Group Property 2, bool
            Group_property3: Edit Group Property 3, bool
            Group_property4: Edit Group Property 4, bool
            Group_property5: Edit Group Property 5, bool

        
        Return:
            A bool is returned indicating success or fail , if success, its true else false

        Examples:
            >>> apiobj = self.{risksenseobject}.groups.edit_group_properties(groupproperty1=True,groupproperty=2)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/properties'
        properties=[]
        if groupproperty1==True:
              value=input('Please provide value for group property 1')
              properties.append({"key":"GROUP_PROPERTY_1","value":value})
        if groupproperty2==True:
              value=input('Please provide value for group property 2')
              properties.append({"key":"GROUP_PROPERTY_2","value":value})
        if groupproperty3==True:
              value=input('Please provide value for group property 3')
              properties.append({"key":"GROUP_PROPERTY_3","value":value})
        if groupproperty4==True:
              value=input('Please provide value for group property 4')
              properties.append({"key":"GROUP_PROPERTY_4","value":value})
        if groupproperty5==True:
              value=input('Please provide value for group property 5')
              properties.append({"key":"GROUP_PROPERTY_5","value":value})

        body={"groupIds":groupids,"properties":properties}
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url,body=body)
            if raw_response.status_code==200:
                success=True

        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return success
    



    def get_single_search_page(self, search_filters:list, projection:str=Projection.BASIC, page_num:int=0, page_size:int=150,
                               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC, client_id:int=None,csvdump:bool=False)->dict:

        """
        Searches for and returns groups based on the provided filter(s) and other parameters.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            projection:      Projection to use
            page_num:        The page number of results to be returned.
            page_size:       The number of results per page to be returned.
            sort_field:      The field to be used for sorting the results returned.
            sort_dir:        The direction of sorting to be used. (SortDirection.ASC or SortDirection.DESC)
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:        Toggle to dump data in csv
        
        Return:
            The JSON response from the platform is returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.groups.get_single_search_page([{"field":"name","exclusive":False,"operator":"WILDCARD","value":"test*","implicitFilters":[]}])

        Note:
            You can also dump the data of the group search in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.groups.get_single_search_page([{"field":"name","exclusive":False,"operator":"WILDCARD","value":"test*","implicitFilters":[]}],csvdump=True) 
        """

        func_args = locals()
        func_args.pop('self')

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            response = self._get_single_search_page(self.subject_name, **func_args)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit() 

        if csvdump==True:
            self.downloadfilterinexport('groupsearchdata',search_filters)            
        
        
        return response

    def search(self, search_filters:list, projection:str=Projection.DETAIL, page_size:int=150,
               sort_field:int=SortField.ID, sort_dir:int=SortDirection.ASC, client_id:int=None,csvdump:bool=False)->list:
        """
        Searches for and returns groups based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            projection:      Projection to use
            page_size:       The number of results per page to be returned.
            sort_field:      The field to be used for sorting the results returned.
            sort_dir:        The direction of sorting to be used. (SortDirection.ASC or SortDirection.DESC)
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv

        Return:
            A list containing all host findings returned by the search using the filter provided.

        Examples:
            >>> apiobj = self.{risksenseobject}.groups.search([{"field":"name","exclusive":False,"operator":"WILDCARD","value":"test*","implicitFilters":[]}])

        Note:
            You can also dump the data of the group search in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.groups.search([{"field":"name","exclusive":False,"operator":"WILDCARD","value":"test*","implicitFilters":[]}],csvdump=True) 
        """

        func_args = locals()
        func_args.pop('self')
        all_results = []
        func_args.pop('csvdump')

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
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
            self.downloadfilterinexport('groupsearchdata',search_filters)      

        return all_results


    def create(self, name:str,description:str, client_id:int=None, csvdump:bool=False)->int:

        """
        Creates a new group.

        Args:
            name:                The name to be used for the new group.
            description:    Group creation description
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv
        
        Return:
            The new group ID is returned.
        
        Examples:
            >>> apiobj = self.{risksenseobject}.groups.create('test','test')

        Note:
            You can also dump the data of the group job id in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.groups.create('test','test',csvdump=True)         
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        body = {
            "name": name,
            "description":description
        }
        
        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        
        jsonified_response = json.loads(raw_response.text)
        new_group_id = jsonified_response['id']

        try:
            if csvdump==True:
                field_names = ['id']
                try:
                    with open('groupcreate.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow({'id': new_group_id})
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()

        return new_group_id

    def history(self, groupid:int, client_id:int=None,csvdump:bool=False)->dict:

        """
        Get group history.

        Args:
            groupid:             The id to be used to fetch group history.
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv
        
        Return:
            The history of group id.
        
        Examples:
            >>> apiobj = self.{risksenseobject}.groups.history(1234)

        Note:
            You can also dump the data of the group history in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.groups.history(1234,csvdump=True) 
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+f'/{groupid}/history'

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()               

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        jsonified_response = json.loads(raw_response.text)
        
        if csvdump==True:
            field_names = []
            for item in jsonified_response:
                for key in item.keys():
                    if key not in field_names:
                        field_names.append(item)
            try:
                with open('grouphistory.csv', 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response

    def delete(self, search_filters:list, client_id:int=None,csvdump:bool=False)->int:

        """
        Deletes groups as specified in search_filters.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv
        
        Return:
            Job Id
        
        Examples:
            >>> apiobj = self.{risksenseobject}.groups.delete([{"field":"name","exclusive":False,"operator":"WILDCARD","value":"test*","implicitFilters":[]}])

        Note:
            You can also dump the data of the group to be deleted in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.groups.get_single_search_page([{"field":"name","exclusive":False,"operator":"WILDCARD","value":"test*","implicitFilters":[]}],csvdump=True) 
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/delete"

        body = {
            "filterRequest": {
                "filters": search_filters
            }
        }

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('groupexportbeforedeleting',search_filters)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        if raw_response.status_code == 200:   
            jsonified_response = json.loads(raw_response.text)
            deleted_groups = jsonified_response['id']

        return deleted_groups

    def update_single_group(self, group_id:int, client_id:int=None, csvdump:bool=False, **kwargs)->int:
        """
        Updates a group name and/or asset criticality.

        Args:
            group_id:    The group ID.
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv
        
        Keyword Args:
        name (`str`):     The new name.
        description (`str`):     The new Description

        Return:
            The job ID is returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.groups.update_single_group(1234)

        Note:
            You can also dump the data of the group job id in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.groups.update_single_group(1234,csvdump=True) 
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        name = kwargs.get('name', None)
        description = kwargs.get('description', None)

        url = self.api_base_url.format(str(client_id)) + "/" + str(group_id)

        body = {}

        if name is not None:
            body.update(name=name)

        if description is not None:
            body.update(description=description)

        if body == {}:
             ValueError("Body is empty. Please provide name and/or description")

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        try:
            if csvdump==True:
                field_names = ['id']
                try:
                    with open('groupupdate.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow({'id': job_id})
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()

        return job_id

    def assign(self, search_filters:list, user_ids:list, client_id:int=None, csvdump:bool=False)->int:
        """
        Assign group(s) to user IDs, based on specified filter(s)

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            user_ids:        A list of user IDs.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:       Toggle to dump data in csv
        
        Return:
            The job ID is returned.
        
        Examples:
            >>> apiobj = self.{risksenseobject}.groups.assign([{"field":"name","exclusive":False,"operator":"EXACT","value":"test","implicitFilters":[]}],[1234])

        Note:
            You can also dump the data of the group job id in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.groups.assign([{"field":"name","exclusive":False,"operator":"EXACT","value":"test","implicitFilters":[]}],[1234],csvdump=True)         
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/assign"

        body = {
            "filters": search_filters,
            "userIds": user_ids
        }

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
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

        try:
            if csvdump==True:
                field_names = ['id']
                try:
                    with open('groupassign.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow({'id': job_id})
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()

        return job_id

    def unassign(self, search_filters:list, user_ids:list, client_id:int=None,csvdump:bool=False)->int:

        """
        Unassign group(s) from user IDs, based on specified filter(s)

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            user_ids:        A list of user IDs.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:       Toggle to dump data in csv
        
        Return:
            The job ID is returned.
        
        Examples:
            >>> apiobj = self.{risksenseobject}.groups.unassign([{"field":"name","exclusive":False,"operator":"EXACT","value":"test","implicitFilters":[]}],[1234])

        Note:
            You can also dump the data of the group job id in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.groups.unassign([{"field":"name","exclusive":False,"operator":"EXACT","value":"test","implicitFilters":[]}],[1234],csvdump=True)         
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/unassign"

        if csvdump==True:
            self.downloadfilterinexport('groupexportbeforeunassigning',search_filters)

        body = {
            "filters": search_filters,
            "userIds": user_ids
        }

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
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

        try:
            if csvdump==True:
                field_names = ['id']
                try:
                    with open('groupunassign.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow({'id': job_id})
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()


        return job_id

    def get_model(self, client_id:int=None)->dict:

        """
        Get available projections and models for Groups.

        Args:
            client_id:   Client ID
        
        Return:
            Group projections and models are returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.groups.get_model()
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

    def suggest(self, search_filter:list, suggest_filter:dict, client_id:int=None)->dict:

        """
        Suggest values for filter fields.

        Args:
            search_filter:     Search Filter
            suggest_filter:     Suggest Filter
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Value suggestions
        
        Examples:
            >>> apiobj = self.{risksenseobject}.groups.suggest([{"field":"name","exclusive":False,"operator":"WILDCARD","value":"test*","implicitFilters":[]}])
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._suggest(self.subject_name, search_filter, suggest_filter, client_id)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        return response
    
    def getexporttemplate(self,client_id:int=None)->list:
        """
        Gets configurable export template for application findings.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The Exportable fields

        Examples:
            >>> apiobj = self.{risksenseobject}.groups.getexporttemplate()
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

    def export(self, search_filters:list, file_name:str, row_count:str=ExportRowNumbers.ROW_ALL,file_type:str=ExportFileType.CSV, client_id:int=None, csvdump:bool=False)->int:
        """
        Initiates an export job on the platform for group(s) based on the
        provided filter(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            file_name:       The name to be used for the exported file.
            row_count:       No of rows to be exported. Possible options : 
                ExportRowNumbers.ROW_5000,
                ExportRowNumbers.ROW_10000,
                ExportRowNumbers.ROW_25000,
                ExportRowNumbers.ROW_50000",
                ExportRowNumbers.ROW_100000",
                ExportRowNumbers.ROW_ALL
            file_type:       File type to export.  ExportFileType.CSV, ExportFileType.XML, or ExportFileType.XLSX
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv
        
        Return:
            The Export job ID in the platform from is returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.groups.export([{"field":"name","exclusive":False,"operator":"WILDCARD","value":"test*","implicitFilters":[]}],'test')

        Note:
            You can also dump the data of the group in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.groups.export([{"field":"name","exclusive":False,"operator":"WILDCARD","value":"test*","implicitFilters":[]}],csvdump=True) 
        """
        func_args = locals()
        func_args['exportable_filter']=self.getexporttemplate()
        func_args.pop('self')

        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            export_id = self._export(self.subject_name, **func_args)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()


        try:
            if csvdump==True:
                field_names = ['id']
                try:
                    with open('groupexport.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow({'id': export_id})
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()

        
        return export_id


    ##  PRIVATE FUNCTIONS  ##


    def subscribe_change_in_grouprs3(self,client_id:int=None)->dict:
        """
        Subscribe change in group rs3 notification

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Jsonified response

        Examples:
            >>> apiobj = self.{risksenseobject}.groups.subscribe_change_in_grouprs3()
        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=3,subscribe=True)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        return subscribe

    def unsubscribe_change_in_grouprs3(self,client_id:int=None)->dict:

        """
        Unsubscribe change in group rs3 notification

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Jsonified response

        Examples:
            >>> apiobj = self.{risksenseobject}.groups.unsubscribe_change_in_grouprs3()
        """

        if client_id is None:
            client_id = self._use_default_client_id()

        try:
            print(client_id)
            subscribe = self.notifications.subscribe_notifications(self,notificationtypeid=3,subscribe=False)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        return subscribe




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
