""" *******************************************************************************************************************
|
|  Name        :  __quickfilters.py
|  Description :  QuickFilters
|  Project     :  risksense_api
|  Copyright   :  2021 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

from inspect import getclosurevars
import json
from platform import platform
from re import L
from ..__subject import Subject
from ..._params import *
from ..._api_request_handler import *

class Quickfilters(Subject):
    def __init__(self, profile):

        """
        Initialization of quickfilters object.

        :param profile:     Profile Object
        :type  profile:     _profile
        """

        self.subject_name = "quick-filters"
        Subject.__init__(self, profile, self.subject_name)

    def get_vulnerability_quickfilters(self,quickfilters,clientid=None):

        """
        Get vulnerability quickfilters based on filters in the search endpoint

        :param quickfilters : Filters that need to get quick filters
        :type  quickfilters : list

        :param client_id :    Client id , if none for default client id
        :type  quickfilters : int

        """
        
        if clientid is None:
            clientid = self._use_default_client_id()[0]
        
        url = self.api_base_url.format(str(clientid))
        
        body={
            "subject": 'vulnerability',
            "filterRequest": {
                "filters": quickfilters
            }
            }
        
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_weakness_quickfilters(self,quickfilters,clientid=None):

        """
        Get weakness quickfilters based on filters in the search endpoint

        :param quickfilters : Filters that need to get quick filters
        :type  quickfilters : list

        :param client_id :    Client id , if none for default client id
        :type  quickfilters : int

        """

        if clientid is None:
            clientid = self._use_default_client_id()[0]
        
        url = self.api_base_url.format(str(clientid))
        
        body={
            "subject": 'weakness',
            "filterRequest": {
                "filters": quickfilters
            }
            }
        
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

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
