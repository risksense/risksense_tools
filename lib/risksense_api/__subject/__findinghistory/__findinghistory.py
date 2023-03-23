"""
**Finding history module defined for different history related api endpoints.**
"""
""" *******************************************************************************************************************
|
|  Name        :  __findinghistory.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating Application Findings on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *


class FindingHistory(Subject):

    """ **Class for Finding History Definitions**.

    To utlise Finding history:

    Args:
            profile:     Profile Object
    
    Usage:
        :obj:`self.{risksenseobjectname}.finding_history.{function}`
    
    Examples:
        To get findings history for an application finding using :meth:`get_applicationfinding_history()` function

        >>> self.{risksenseobject}.finding_history.get_applicationfinding_history(112)

    """

    def __init__(self, profile:object):

        """**Initialization of Finding history Object** .

        Args:
            profile:     Profile Object

        """
        self.subject_name = 'findinghistory'
        Subject.__init__(self, profile, self.subject_name)
        self.historyurl=self.profile.platform_url + "/api/v1/client/{}/{}/history"

    def get_hostfinding_history(self,vulnerableids:list,client_id:int=None)->list:
        """
        Get history of hostfindings

        Args:
            vulnerableids: The vulnerability ids

            client_id:      The client id , if none, default client id is taken
        Return:
            The history data
        Example:
            To get groupby data

            >>> self.{risksenseobject}.finding_history.get_hostfinding_history([123,123]])
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.historyurl.format(str(client_id),'hostFinding')

        body = {
                "vulnIds": vulnerableids
                }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response
    
    def get_applicationfinding_history(self,vulnerableids:list,client_id:int=None)->list:
        """
        Get history of hostfindings

        Args:
            vulnerableids: The vulnerability ids

            client_id:      The client id , if none, default client id is taken
        Return:
            The history data
        Example:
            To get groupby data

            >>> self.{risksenseobject}.finding_history.get_hostfinding_history([123,123]])
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.historyurl.format(str(client_id),'applicationFinding')

        body = {
                "vulnIds": vulnerableids
                }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response





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
