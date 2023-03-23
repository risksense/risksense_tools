""" *******************************************************************************************************************
|
|  Name        :  Rs3.py
|  Module      :  risksense_api
|  Description :  A class to be used for getting information on rs3 endpoint
|  Copyright   : (c) RiskSense, Inc.
|  License     : Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

from http import client
import json
from .. import Subject
from ..._params import *
from ..._api_request_handler import *


class Rs3(Subject):

    """ Rs3 Class """

    def __init__(self, profile):

        """
        Initialization of Rs3 object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """
        Subject.__init__(self, profile)
        self.rs3aggregate = self.profile.platform_url + "/api/v1/client/{}/rs3V11OverTime/aggregate"
        self.rs3simulate = self.profile.platform_url + "/api/v1/client/{}/simulate/rs3"


    def get_rs3aggregate(self,startdate,enddate,filters,client_id=None):
        """
        Gets rs3 aggregate score between dates

        param startdate: The start date from when rs3 score is needed
        type  startdate: date

        param enddate:  The end date till when rs3 score is needed
        type  enddate:  date

        param filters: filters to define for the rs3
        type  filters: list

        param client_id: client id , if none takes default client_id
        type client_id: int

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.rs3aggregate.format(str(client_id))

        body = {
                    "startDate": startdate,
                    "endDate": enddate,
                    "filters": filters
                    }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def simulate_rs3(self,vrrCriticalMax,vrrHighMax,vrrMediumMax,vrrLowMax,findingCount,assetType,assetCriticality,assetCategory,client_id=None):
    
            """
            Simulate rs3 score based on the vrr,findingcount,asset data

            param vrrCriticalMax: The vrrCriticalMax info
            type  vrrCriticalMax: int

            param vrrHighMax:     The vrrhighmax info
            type  vrrHighMax:     int

            param vrrMediumMax:   The vrrMediumMax info
            type  vrrMediumMax:   int

            param vrrLowMax:     The vrrLowMax info
            type  vrrLowMax:     int

            param findingCount:     The number of findings
            type  findingCount:     int
            
            param assetType:     The type of asset either external or internal
            type  assetType:     str

            param assetCriticality:     The asset criticality
            type  assetType:     int

            param assetCategory:     The asset category
            type  assetCategory:     str

            param client_id: client id , if none takes default client_id
            type client_id: int

            """
            if client_id is None:
                client_id = self._use_default_client_id()[0]

            url = self.rs3simulate.format(str(client_id))

            body = {
                    "vrrCriticalMax": vrrCriticalMax,
                    "vrrHighMax": vrrHighMax,
                    "vrrMediumMax": vrrMediumMax,
                    "vrrLowMax": vrrLowMax,
                    "findingCount": findingCount,
                    "assetType": assetType,
                    "assetCriticality": assetCriticality,
                    "assetCategory": assetCategory
                    }
            try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            except RequestFailed:
                raise

            jsonified_response = json.loads(raw_response.text)

            
            return jsonified_response['rs3']

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