"""
Network module defined for different network related api endpoints.
"""

""" *******************************************************************************************************************
|
|  Name        :  __networks.py
|  Module      :  risksense_api
|  Description :  A class to be used for interacting with RiskSense platform networks.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0
|
******************************************************************************************************************* """

import json
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
import csv


class Networks(Subject):

    """Class for network function definitions.

    Args:
        profile:     Profile Object

    To utlise network function:
    
    Usage:
        :obj:`self.{risksenseobjectname}.networks.{function}`

    Examples:
        To create a network using :meth:`create` function

        >>> self.{risksenseobjectname}.networks.create(args)

    """

    def __init__(self, profile:object):

        """Initialization of Networks object.

        Args:
            profile:     Profile Object

        """

        self.subject_name = "network"
        Subject.__init__(self, profile, self.subject_name)

    def list_network_filter_fields(self,client_id :int=None)->dict:

        """
        List filter endpoints.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The JSON output from the platform is returned, listing the available filters.

        Examples:
            >>> apiobj = self.{risksenseobject}.networks.list_network_filter_fields(client_id=124)
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



    def create(self, name :str, client_id :int=None, csvdump:bool=False)->int:
        """
        Create a new network.

        Args:
            name:            The name for the new network.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:         Toggle to dump data in csv

        Return:
            The new network job ID.

        Examples:
            >>> apiobj = self.{risksenseobject}.networks.create('test_aug', 'IP')

        Note:
            You can also dump the data of the network job id in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.networks.create('test_aug', 'IP',csvdump=True)  
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        body = {
            "name": name,
            "type": "MIXED"
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
        network_id = jsonified_response['id']


        try:
            if csvdump==True:
                field_names = ['id']
                try:
                    with open('groupcreate.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow({'id': network_id})
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()


        return network_id

    def update(self, network_id :int,name :str, client_id :int=None, csvdump:bool=False)->int:
        """
        Update an existing network.

        Args:
            network_id:  The network ID.
            name:        A new name for the network.
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv

        Return:
            Network job id

        Examples:
            >>> apiobj = self.{risksenseobject}.networks.update(291935, 'test_aug1')

        Note:
            You can also dump the data of the network job id in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.networks.update(291935, 'test_aug1',csvdump=True)  
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(network_id))
        body = {
            "name": name
        }


        body = self._strip_nones_from_dict(body)

        if body == {}:
            raise ValueError("Body is empty. Name and/or network_type not provided.")

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
        returned_id = jsonified_response['id']


        try:
            if csvdump==True:
                field_names = ['id']
                try:
                    with open('groupcreate.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow({'id': returned_id})
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()


        return returned_id

    def delete(self, network_id:int, client_id:int=None,csvdump:bool=False)->int:

        """
        Deletes a network.

        Args:
            network_id:  The network ID to be deleted.
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv

        Return:
            True/False indicating whether or not the operation was successful.

        Examples:
            >>> apiobj = self.{risksenseobject}.networks.delete(1234,client_id=123)

        Note:
            You can also dump the data of the network tht will be deleted in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.networks.delete(1234,client_id=123,csvdump=True)  
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(network_id))

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        if csvdump==True:
            jsonified_response=self.get_single_search_page([{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":f"{network_id}"}])
            print(jsonified_response)
            field_names = []
            for item in jsonified_response['_embedded']['networks'][0]:
                field_names.append(item)
            try:
                with open('get_networks.csv', 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response['_embedded']['networks']:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        success = True

        return success

    def get_single_search_page(self, search_filters:list, page_num:int=0, page_size:int=150,
                               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC, client_id:int=None)->dict:

        """
        Searches for and returns networks based on the provided filter(s) and other parameters.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            page_num:        Page number of results to be returned.
            page_size:       Number of results to be returned per page.
            sort_field:      Name of field to sort results on.
            sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            A paginated JSON response from the platform is returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.networks.get_single_search_page([{"field":"name","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"test"}])
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/search"

        body = {
            "filters": search_filters,
            "projection": Projection.BASIC,
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

    def search(self, search_filters : list, page_size :int=150, sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC, client_id :int=None,csvdump :bool=False)->list:

        """
        Searches for and returns networks based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            page_size:       The number of results per page to be returned.
            sort_field:      Name of field to sort results on.
            sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:         Whether retrieved search details to be dumped in a csv file or not

        Return:
            A list containing all networks returned by the search using the filter provided.

        Examples:
            >>> apiobj = self.{risksenseobject}.networks.search([{"field":"name","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"test"}])

        Note:
            You can also dump the data of the network search in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.networks.search([{"field":"name","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"test"}],csvdump=True) 
        """

        func_args = locals()
        func_args.pop('self')
        func_args.pop('csvdump')
        all_results = []

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            page_info = self._get_page_info(self.subject_name, search_filters, page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            print("There was a problem with the networks search.")
        

        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        if csvdump==True:
            field_names = []
            for item in all_results[0]:
                field_names.append(item)
            try:
                with open('get_networks.csv', 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in all_results:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        

        return all_results

    def get_model(self, client_id :int=None)->dict:

        """
        Get available projections and models for Networks.

        Args:
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Networks projections and models are returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.networks.get_model()
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

    def get_available_scanners(self, network_id :int,client_id :int=None)->dict:

        """
        Get available scanners for a network.

        Args:
            network_id:  The network ID.
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The JSON output from the platform is returned, listing the available scanners.

        Examples:
            >>> apiobj = self.{risksenseobject}.networks.get_available_scanners(networkid)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+f'/get-available-scanners-for-network/{network_id}'
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)

        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def fetch_scanner_precedence(self, network_id :int,scanner_uuid :str,scanner_type :str,client_id :int=None)->dict:

        """
        Fetch scanner precedence for a network.

        Args:
            network_id:   The network ID.
            scanner_uuid: Scanner uuid
            scanner_type: Type of scanner either "HOST" or "APPLICATION"
            client_id:    Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The JSON output from the platform is returned, listing the available scanners.

        Examples:
            >>> apiobj = self.{risksenseobject}.networks.get_available_scanners(networkid)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+f'/fetch-applicable-precedence'

        body= {"networkId":network_id,
               "scannerUuid":scanner_uuid,"ingestingScannerUuid":scanner_uuid,"assetType":scanner_type}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)

        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response



    def suggest(self, search_filters :list, suggest_filter :dict, client_id :int=None)->dict:
        """
        Suggest values for filter fields.

        Args:
            search_filters:     Active Filters input
            suggest_filter:     Suggest Filter input
            client_id:          Client ID. If an ID isn't passed, will use the profile's default Client ID.

        Return:
            Value suggestions

        Examples:
            >>> apiobj = self.{risksenseobject}.networks.suggest([],{"field":"name","exclusive":False,"operator":"WILDCARD","value":"tes*","implicitFilters":[]})
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._suggest(self.subject_name, search_filters, suggest_filter, client_id)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

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
