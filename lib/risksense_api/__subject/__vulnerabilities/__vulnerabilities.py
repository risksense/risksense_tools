"""
Vulnerability module defined for different vulnerability related api endpoints.
"""

""" *******************************************************************************************************************
|
|  Name        :  __vulnerabilities.py
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
from ..__exports import Exports
import sys
import zipfile


class Vulnerabilities(Subject):

    """Class for vulnerability function definitions.

    Args:
        profile:     Profile Object

    To utlise vulnerability function:
    
    Usage:
        :obj:`self.{risksenseobjectname}.vulnerabilities.{function}`
    
    Examples:
        To get model for vulnerability using :meth:`get_model` function

        >>> self.{risksenseobjectname}.vulnerabilities.get_model()
    """

    def __init__(self, profile:object):

        """
        Initialization of Vulnerabilities object.

        Args:
            profile:     Profile Object
        """

        self.subject_name = "vulnerability"
        Subject.__init__(self, profile, self.subject_name)
    def downloadfilterinexport(self,filename,filters,client_id=None):
        
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
   

    def search(self, search_filters:list, projection=Projection.BASIC, page_size:int=150,
               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC,csvdump:bool=False, client_id:int=None)->list:
        """
        Searches for and returns vulnerabilities based on the provided filter(s) and other parameters. Rather
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
            A list containing all vulnerability returned by the search using the filter provided.

        Examples:
            >>> apiobj = self.{risksenseobject}.vulnerabilities.search([{"field":"vrrGroup","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}])

        Note:
            You can also dump the data of the vulnerability search in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.vulnerabilities.search([{"field":"vrrGroup","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}],csvdump=True) 
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
        except RequestFailed:
            raise

        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed, Exception):
            raise

        if csvdump==True:
            self.downloadfilterinexport('vulnerabilitiessearch',search_filters)
        return all_results

    def list_vulnerability_filter_fields(self,client_id:int=None)->dict:
        """
        List filter endpoints.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The JSON output from the platform is returned, listing the available filters.

        Examples:
            >>> apiobj = self.{risksenseobject}.vulnerabilities.list_vulnerability_filter_fields(client_id=123)
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
        Searches for and returns vulnerabilities based on the provided filter(s) and other parameters.

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
            >>> apiobj = self.{risksenseobject}.vulnerabilities.get_single_search_page([{"field":"vrrGroup","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}])
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
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_model(self, client_id:int=None)->dict:
        """
        Get available projections and models for Vulnerabilities.

        Args:
            client_id:   Client ID
        
        Return:
            Vulnerability projections and models are returned.
        
        Examples:
            >>> apiobj = self.{risksenseobject}.vulnerabilities.get_model()
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
            >>> apiobj = self.{risksenseobject}.vulnerabilities.suggest([],{"field":"vrrGroup","exclusive":False,"operator":"WILDCARD","orWithPrevious":False,"implicitFilters":[],"value":"Critic*"})
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._suggest(self.subject_name, search_filter, suggest_filter, client_id)
        except RequestFailed:
            raise

        return response

    def getexporttemplate(self,client_id:int=None)->list:   
        """
        Gets configurable export template for Vulnerabilities.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The Exportable fields
        
        Examples:
            >>> apiobj = self.{risksenseobject}.vulnerabilities.getexporttemplate()
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/export/template"

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


    def export(self, search_filters:list, file_name:str, row_count:str=ExportRowNumbers.ROW_ALL,file_type:str=ExportFileType.CSV, client_id:int=None)->int:
        """
        Initiates an export job on the platform for Vulnerabilities based on the
        provided filter(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            file_name:       The name to be used for the exported file.
            row_count:       No of rows to be exported. Possible options : 
                ExportRowNumbers.ROW_5000,ExportRowNumbers.ROW_10000,
                ExportRowNumbers.ROW_25000,
                ExportRowNumbers.ROW_50000,
                ExportRowNumbers.ROW_100000,
                ExportRowNumbers.ROW_ALL
            file_type:       File type to export.  ExportFileType.CSV, ExportFileType.JSON, or ExportFileType.XLSX
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The job ID in the platform from is returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.vulnerabilities.export([{"field":"vrrGroup","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}],'test')
        """
        func_args = locals()
        func_args['exportable_filter']=self.getexporttemplate()
        func_args.pop('self')
        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]
        try:
            export_id = self._export(self.subject_name, **func_args)
        except RequestFailed:
            raise

        return export_id




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
