""" *******************************************************************************************************************
|
|  Name        :  __groupBy.py
|  Module      :  risksense_api
|  Description : A class to utilize the groupby endpoint
|  Copyright   : (c) RiskSense, Inc.
|  License     : Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

from http import client
import json
from .. import Subject
from ..._params import *
from ..._api_request_handler import *


class GroupBy(Subject):

    """ Groupby Class """

    def __init__(self, profile):

        """
        Initialization of Groupby object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """
        Subject.__init__(self, profile)
        self.groupbyhf_url = self.profile.platform_url + "/api/v1/client/{}/hostFinding/group-by"
        self.groupbyaf_url = self.profile.platform_url + "/api/v1/client/{}/applicationFinding/group-by"


    def get_groupby_hostfinding(self,hostfindingkey,metricfields,filters,sortorderfield="ASC",client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.groupbyhf_url.format(str(client_id))

        body = {
            "key": hostfindingkey,
            "metricFields": metricfields,
            "filters": filters,
            "sortOrder": sortorderfield
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_groupby_appfinding(self,appfindingkey,metricfields,filters,sortorderfield,client_id=None):

        """
        Get groupby values for app finding

        :param appfindingkey: The main key where other metric fields depend on
        :type  appfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = self.groupbyaf_url.format(str(client_id))

        body = {
                "key": appfindingkey,
                "metricFields": metricfields,
                "filters": filters,
                "sortOrder": sortorderfield
                }

        try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
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