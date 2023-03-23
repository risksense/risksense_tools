"""
****Clients module defined for different clients related api endpoints.****
"""
""" *******************************************************************************************************************
|
|  Name        :  __clients.py
|  Module      :  risksense_api
|  Description :  A class to be used for retrieving client information from the RiskSense Platform.
|  Copyright   : (c) RiskSense, Inc.
|  License     : Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
from ...__subject import Subject
from ..._api_request_handler import *
import csv
import pandas as pd


class Clients(Subject):

    """
        **Class for Clients function defintions**.

        To utlise clients function:

        Args:
                profile:     Profile Object
        
        Usage:
            :obj:`self.{risksenseobjectname}.clients.{function}`
        
        Examples:
            To get subjects using :meth:`get_subject()` function

            >>> self.{risksenseobject}.clients.get_subjects()

    """

    def __init__(self, profile:object):

        """
        Initialization of Clients object.

        Args:
            profile:     Profile Object
        """
        self.subject_name = "client"
        Subject.__init__(self, profile, self.subject_name)
        self.api_base_url = self.profile.platform_url + "/api/v1/client"

    def get_clients(self, page_size:int=500, page_number:int=0)->dict:

        """
        Gets all clients associated with the API key.

        Args:
            page_size:       Number of results to be returned on each page.

            page_number:     The page number to be returned.
        
        Return:
          The JSON response from the platform is returned.
        
        Example:

            To use get_clients method

            >>> self.{risksenseobject}.get_clients()

        

        """
        url = self.api_base_url

        params = {
            "size": page_size,
            "page": page_number
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed,Exception) as e:
            print('Error in getting clients')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_client_info(self, client_id:int=None)->dict:

        """
        Gets the details for a specific client ID.

        Args:
            client_id:   Client ID
        
        Return:
           The JSON response from the platform is returned.

        Example:
            To get client info of 123

            >>> self.{risksenseobject}.geT_client_info(123)
        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "/" + str(client_id)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
            jsonified_response = json.loads(raw_response.text)
        except (RequestFailed,Exception) as e:
            print('Error in getting client info')
            print(e)
            exit()
        if jsonified_response!={}:
            for key,value in jsonified_response.items():
                print(key,':',value)  
                print('---')          
        return jsonified_response

    def get_subjects(self, client_id:int=None)->list:

        """
        List out all of the available subjects for a specific client.

        Args:
            client_id:   Client ID

        Return:
          The JSON from the platform is returned.

        Example:
            To try out get_subjects
                
            >>> self.{risksenseobject}.get_subjects(1234)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "/" + str(client_id) + "/subject"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting subjects')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response


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
