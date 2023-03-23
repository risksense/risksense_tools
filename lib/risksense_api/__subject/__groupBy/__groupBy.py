"""
**Groupby module defined for different groupby related api endpoints.**
"""
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
from os import listdir
from .. import Subject
from ..._params import *
from ..._api_request_handler import *


class GroupBy(Subject):

    """ Groupby Class """

    def __init__(self, profile:object):

        """
        **Class for Groupby function defintions**.

        To utlise groupby function:

        Args:
                profile:     Profile Object
        
        Usage:
            :obj:`self.{risksenseobjectname}.groupby.{function}`
        
        Examples:
            To get hostfindings using groupby method,use :meth:`get_groupby_hostfinding()` function

            >>> self.{risksenseobject}.groupby.get_groupby_hostfinding(123,'test.csv')

    """
        Subject.__init__(self, profile)
        self.groupbyhf_url = self.profile.platform_url + "/api/v1/client/{}/hostFinding/group-by"
        self.groupbyaf_url = self.profile.platform_url + "/api/v1/client/{}/applicationFinding/group-by"


    def get_groupby_hostfinding(self,hostfindingkey:str,metricfields:list,filters:list,sortorderfield:list,client_id:int=None)->dict:
        """
        Get groupby values for host finding

        Args:
            hostfindingkey: The main key where other metric fields depend on

            metricfields:   The fields that will be populated
            
            filters:        The filters which will populate in groupby

            sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending

            client_id:      The client id , if none, default client id is taken
        Return:
            The groupby data
        Example:
            To get groupby data

            >>> self.{risksenseobject}.groupby.get_groupby_hostfinding(["Host Finding Hosts Count","Host Finding Open Count","Host Finding Closed Count","Host Finding With Threat Count","Host Finding Threat Count"],"Host Finding Asset Tags",[{"field":"criticality","exclusive":false,"operator":"IN","orWithPrevious":false,"implicitFilters":[],"value":"1,"}],[{"field":"Host Finding Asset Tags","direction":"ASC"}])
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
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_groupby_appfinding(self,appfindingkey:str,metricfields:list,filters:list,sortorderfield:list,client_id:int=None):

        """
        Get groupby values for app finding

        Args:
            appfindingkey: The main key where other metric fields depend on

            metricfields:   The fields that will be populated
            
            filters:        The filters which will populate in groupby

            sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending

            client_id:      The client id , if none, default client id is taken
        Return:
            The groupby data
        Example:
            To get groupby data

            >>> self.{risksenseobject}.groupby.get_groupby_appfinding(["App Finding Apps Count","App Finding Open Count","App Finding Closed Count","App Finding VRR Critical Count","App Finding VRR High Count","App Finding VRR Medium Count","App Finding VRR Low Count","App Finding VRR Info Count","App Finding Severity Critical Count","App Finding Severity High Count","App Finding Severity Medium Count","App Finding Severity Low Count","App Finding Severity Info Count","App Finding With Threat Count","App Finding Threat Count","App Finding CVE Count"],"App Finding Asset Criticality",[{"field":"web_app_url","exclusive":false,"operator":"IN","orWithPrevious":false,"implicitFilters":[],"value":"Benchmarx_Arnab,"}],[{"field":"App Finding Asset Criticality","direction":"DESC"}])
            
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
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                

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