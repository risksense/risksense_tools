"""
Weakness module defined for different weakness related api endpoints.
"""

""" *******************************************************************************************************************
|
|  Name        :  __weaknesses.py
|  Project     :  risksense_api
|  Copyright   :  2022 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
from ...__subject import Subject
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ..._params import *
from ..._api_request_handler import *
import csv
from ..__exports import Exports
import zipfile
import csv
import sys


class Weaknesses(Subject):

    """Class for weakness function definitions.

    Args:
        profile:     Profile Object

    To utlise weakness function:
    
    Usage:
        :obj:`self.{risksenseobjectname}.weaknesses.{function}`
    
    Examples:
        To get model for weakness using :meth:`get_model` function

        >>> self.{risksenseobjectname}.weaknesses.get_model()
    """

    def __init__(self, profile:object):

        """
        Initialization of Weaknesses object.

        Args:
            profile:     Profile Object
        """

        self.subject_name = "weakness"
        Subject.__init__(self, profile, self.subject_name)

    def downloadfilterinexport(self,filename:str,filters:list,client_id:int=None):
        """
        Download weakness data based on search filters.

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
   

    def search(self, search_filters:list, projection:str=Projection.BASIC, page_size:int=150,
               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC,csvdump:bool=False, client_id:int=None)->list:
        """
        Searches for and returns weaknesses based on the provided filter(s) and other parameters. Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            projection:      Projection to be used in API request.  Projection.BASIC or Projection.DETAIL
            page_size:       The number of results per page to be returned.
            sort_field:      The field to be used for sorting results returned.
            sort_dir:        The direction of sorting to be used. SortDirection.ASC or SortDirection.DESC
            csvdump:         dumps the data in csv
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            A list containing all weaknesses returned by the search using the filter provided.

        Examples:
            >>> apiobj = self.{risksenseobject}.weaknesses.search([{"field":"vulnId","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"CWE-918"}])

        Note:
            You can also dump the data of the vulnerability search in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.weaknesses.search([{"field":"vulnId","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"CWE-918"}],csvdump=True) 
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
            print('There was an exception')
            print(e)
            exit()
        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed,Exception) as e:
            print('There was an exception')
            print(e)
            exit()
        if csvdump==True:
            self.downloadfilterinexport('weaknesses',search_filters)
        return all_results

    def list_weakness_filter_fields(self,client_id:int=None)->dict:
        """
        List filter endpoints.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The JSON output from the platform is returned, listing the available filters.

        Examples:
            >>> apiobj = self.{risksenseobject}.weaknesses.list_weakness_filter_fields()
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



    def get_single_search_page(self, search_filters:list, projection:str=Projection.BASIC, page_num:int=0, page_size:int=150,
                               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC, client_id:int=None)->dict:
        """
        Searches for and returns weaknesses based on the provided filter(s) and other parameters.

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

        Examples:
            >>> apiobj = self.{risksenseobject}.weaknesses.get_single_search_page([{"field":"vulnId","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"CWE-918"}])
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
            print('There was an exception')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_model(self, client_id:int=None)->dict:

        """
        Get available projections and models for weaknesses.

        Args:
            client_id:   Client ID
        
        Return:
            Weaknesses projections and models are returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.weaknesses.get_model()
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
        except RequestFailed:
            raise

        return response

    def suggest(self, search_filter:list, suggest_filter:dict, client_id:int=None)->dict:

        """
        Suggest values for filter fields.

        Args:
            search_filter:     Search Filter
            suggest_filter:     Suggest Filter
            client_id:           Client ID
        
        Return:
            Value suggestions

        Examples:
            >>> apiobj = self.{risksenseobject}.weaknesses.suggest([],{"field":"vulnId","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"CWE*"})
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._suggest(self.subject_name, search_filter, suggest_filter, client_id)
        except RequestFailed:
            raise

        return response

    def get_export_template(self, client_id:int=None)->list:
        """
        Get all fields that are part of configurable export

        Args:
            client_id:   Client ID
        
        Return:
            Fields that can be configured for export

        Examples:
            >>> apiobj = self.{risksenseobject}.weaknesses.get_export_template()
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + '/export/template'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed:
            raise

        exportablefilter = json.loads(raw_response.text)

        for i in range(len(exportablefilter['exportableFields'])):
            for j in range(len(exportablefilter['exportableFields'][i]['fields'])):
                if exportablefilter['exportableFields'][i]['fields'][j]['selected']==False:
                    exportablefilter['exportableFields'][i]['fields'][j]['selected']=True

        return exportablefilter['exportableFields']

    def export(self, search_filters:list, file_name:str, file_type=ExportFileType.CSV,row_count=ExportRowNumbers.ROW_ALL, comment="", client_id:int=None)->int:
        """
        Initiates an export job on the platform for weaknesses based on the provided filter(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            file_name:       The file name to be assigned to the export.
            file_type:       The file type for the export.  Options are ExportFileType.CSV,
                                ExportFileType.JSON, and ExportFileType.XLSX
            comment:         Any comment wished to be associated with the export.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The job ID is returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.weaknesses.export([{"field":"vulnId","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"CWE-918"}],'test')
        """

        func_args = locals()
        func_args['exportable_filter']=self.get_export_template()
        func_args.pop('self')

        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]

        try:
            export_id = self._export(self.subject_name, **func_args)
            return export_id
        except (RequestFailed,Exception) as e:
            print('There was an exception')
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
