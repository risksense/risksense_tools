""" *******************************************************************************************************************
|
|  Name        :  __sla.py
|  Description :  SLA
|  Project     :  risksense_api
|  Copyright   :  2022 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
from re import L
from ..__subject import Subject
from ..._params import *
from ..._api_request_handler import *

class SlaActionType:
    """Types of sla action type"""
    REMEDIATION_SLA= "REMEDIATION_SLA"

class SlaMatrix : 
    """Types of Sla Matrix"""
    STANDARD= {"1":[45,90,90,120,0],"2":[30,90,90,120,0],"3":[21,45,90,120,0],"4":[14,30,90,120,0],"5":[7,21,90,120,0]}
    ACCELERATED= {"1":[30,60,90,90,0],"2":[21,45,90,90,0],"3":[14,30,60,90,0],"4":[7,21,45,90,0],"5":[3,14,30,90,0]}
    AGGRESSIVE= {"1":[14,30,45,60,0],"2":[7,21,30,60,0],"3":[3,14,30,60,0],"4":[2,7,15,60,0],"5":[1,3,15,60,0]}

class SlaDataOperator:
    """Types of sla data operator"""
    MET_SLA="MET_SLA"
    OVERDUE="OVERDUE"
    MISSED_SLA="MISSED_SLA"
    WITHIN_SLA="WITHIN_SLA"

class SlaMatrixProfileType:
    """Types of Sla Matrix Profile Type"""
    STANDARD="STANDARD"
    AGGRESSIVE="AGGRESSIVE"
    ACCELERATED="ACCELERATED"
    CUSTOM="CUSTOM"

class TimeReference:
    """Types of sla time reference"""
    INGESTION_DATE = "INGESTION_DATE"
    DISCOVERED_DATE = "DISCOVERED_DATE"

class offsetbasis:
    VRR       = "VRR"
    SEVERITY  = "SEVERITY"

class Sla(Subject):


    def __init__(self, profile):

        """
        Initialization of sla object.

        :param profile:     Profile Object
        :type  profile:     _profile
        """

        self.subject_name = "sla"
        Subject.__init__(self, profile, self.subject_name)

    def getslarules(self,playbookuuid,client_id=None):

        """
        Get a list of all sla rules for an sla.

        :param playbookuuid:  Uuid of the playbook to fetch sla
        :type  playbookuuid:     str

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :return:    Sla rules
        :rtype:     list

        :raises RequestFailed:
        """


        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rules".format(playbookuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def getslas(self,client_id=None):

        """
        Gets all slas for a particular client.

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/fetch"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def add_default_sla_rule(self, sla_uuid, description, priority,
                     timeReference=TimeReference.DISCOVERED_DATE, serviceLevelAgreementMatrix=SlaMatrix.STANDARD,slaMatrixProfileType=SlaMatrixProfileType.STANDARD,offsetBasis=offsetbasis.VRR,affectOnlyNewFindings=True,updateSLAIfVRRUpdates=True,inputdata="HOST_FINDING",actionType=SlaActionType.REMEDIATION_SLA,client_id=None):
        
        """
        Adds default rule to existing sla playbook.Works only if there is no default rule applied to the playbook

        :param sla_uuid:                Sla UUID
        :type  sla_uuid:                str

        :param description:             Provide description for the default sla rule, 
        :type  description:             str

        :param priority:                Priority to be provided to default sla rule , 
                                        note: default sla priority should be a greater number than the group sla rules
        :type  priority:                int

        :param Timereference:           Timereference to be provided to default sla rule , 
        :type  Timereference:           Str

        :param slamatrix:               Provide slamatrix for the particular sla
        :type  slamatrix:               dict

        :param slamatrixprofiletype:    Provide sla matrix type for the sla
        :type  slamatrixprofiletype:    str

        :param offsetbasisc:            Provide offset basis for particular sla
        :type  offset_basis:            str

        :param affectOnlyNewFindings :  Choose whether it affects new findings
        :type affectonlynewfindings:    bool

        :param updateSLAIfVRRUpdates:   Choose if slaupdates with vrr
        :type  updateSLAIfVRRUpdates:   bool

        :param inputdata:               Type of data provided for sla
        :type  inputdata:               str

        :param actionType:              Type of action for particular sla
        :type  actionType:              str

        :param client_id:               Client ID , if no client id provided , takes default client id
        :type  client_id:               int

        :param action_type:             Action type for the particular sla rule,by default remediation rule is provided
        :type  rule_desc:               str

        :return:                        List containing dict of rule details.
        :rtype:                         list

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rule".format(sla_uuid)

        body={"name":'Default SLA',"description":description,"priority":priority,"supplementalFilterRequest":None,"actionType":actionType,"action":{ "isDefaultSLA":True,"targetGroupIds":[],"timeReference":timeReference,"serviceLevelAgreementMatrix":serviceLevelAgreementMatrix,"slaMatrixProfileType":slaMatrixProfileType,"offsetBasis":offsetBasis,"affectOnlyNewFindings":affectOnlyNewFindings,"updateSLAIfVRRUpdates":updateSLAIfVRRUpdates},"outputType":"NO_OUTPUT","output":{},"input":inputdata}
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response
    
    def del_group_sla_rule(self,playbookuuid,client_id=None):
        
        """
        Deletes a particular group sla rule.

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :param playbookuuid: The playbookuuid that needs to be deleted
        :type  playbookuuid: str

        :return delete_json: Returns json of deleted rule
        :return type:        json

        :raises RequestFailed:
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.api_base_url.format(str(client_id)) +"/rule/{}".format(playbookuuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response 
    
    def change_order(self,slauuid,ruleuuids,client_id=None):

        """
        Changes the order of the sla rules

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :param slauuid: The sla where rules needs to be reordered
        :type  slauuid: str

        
        :param slauuid: The order of rules reordering
        :type  slauuid: list

        :return succcess_json: Returns the reordered rule json
        :param  success_json:  json

        :raises RequestFailed:
        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) +"/{}/rule-reorder".format(slauuid)

        body={"ruleUuids":ruleuuids}
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    
    def add_group_sla_rule(self, sla_uuid, name, description, priority, targetgroupids,
                     timeReference=TimeReference.DISCOVERED_DATE, serviceLevelAgreementMatrix=SlaMatrix.STANDARD,slaMatrixProfileType=SlaMatrixProfileType.STANDARD,offsetBasis=offsetbasis.VRR,affectOnlyNewFindings=True,updateSLAIfVRRUpdates=True,inputdata="HOST_FINDING",actionType=SlaActionType.REMEDIATION_SLA,client_id=None):
        
        """
        Adds group rule to existing sla playbook for the groups specified.
        :param sla_uuid:                Sla UUID
        :type  sla_uuid:                str

        :param name:                    Name of the group specific sla rule
        :type  namw:                    str

        :param description:             Provide description for the group specific sla rule, 
        :type  description:             str

        :param priority:                Priority to be provided to group speicifc sla , 
                                        note: group sla priority should be a lesser number than the default sla rule
        :type  priority:                int

        :param targetgroupids:          The groups ids where the sla applies
        :type  targetgroupids:          list

        :param TimeReference:           Timereference to be provided to default sla rule , 
        :type  timeReference:           Str

        :param slamatrix:               Provide slamatrix for the particular sla
        :type  slamatrix:               dict

        :param slamatrixprofiletype:    Provide sla matrix type for the sla
        :type  slamatrixprofiletype:    str

        :param offsetbasisc:            Provide offset basis for particular sla
        :type  offset_basis:            str

        :param affectOnlyNewFindings :  Choose whether it affects new findings
        :type affectonlynewfindings:    bool

        :param updateSLAIfVRRUpdates:   Choose if slaupdates with vrr
        :type  updateSLAIfVRRUpdates:   bool

        :param inputdata:               Type of data provided for sla
        :type  inputdata:               str

        :param actionType:              Type of action for particular sla
        :type  actionType:              str

        :param client_id:               Client ID , if no client id provided , takes default client id
        :type  client_id:               int

        :param action_type:             Action type for the particular sla rule,by default remediation rule is provided
        :type  rule_desc:               str

        :return:                        List containing dict of rule details.
        :rtype:                         list

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) +"/{}/rule".format(sla_uuid)

        body={"name":name,"description":description,"priority":priority,"supplementalFilterRequest":None,"actionType":actionType,"action":{"isDefaultSLA":False,"targetGroupIds":targetgroupids,"timeReference":timeReference,"serviceLevelAgreementMatrix":serviceLevelAgreementMatrix,"slaMatrixProfileType":slaMatrixProfileType,"offsetBasis":offsetBasis,"affectOnlyNewFindings":affectOnlyNewFindings,"updateSLAIfVRRUpdates":updateSLAIfVRRUpdates},"outputType":"NO_OUTPUT","output":{},"input":inputdata}


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response
    def disablesla(self,playbookuuid,client_id=None):

        """
        Disables a particular sla rule.

        :param playbookuuid: The playbookuuids that needs to be disabled
        :type  playbookuuid: str

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :return response: Returns json of disable sla
        :return type:     json

        :raises RequestFailed:
        
        """


        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/toggle-enabled"
        body={"playbookUuids":[f"{playbookuuid}"],"enabled":False}
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def enablesla(self,playbookuuid,client_id=None):
        """
        Enables a particular sla rule.

        :param playbookuuid: The playbookuuids that needs to be enabled
        :type  playbookuuid: str

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :return response: Returns json of disable sla
        :return type:     json

        :raises RequestFailed:
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/toggle-enabled"
        body={"playbookUuids":[f"{playbookuuid}"],"enabled":True}
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  
    def getplaybookslarules(self,slaid,client_id=None): 

        """
        Gets sla playbook rules for a particular sla.

        :param slaid:       Slaid to get the sla rules
        :type  slaid:       str

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :return response: Returns json of playbook rules
        :return type:     json


        :raises RequestFailed:
        """
        

        url = self.api_base_url.format(str(client_id)) + f"/{slaid}"
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
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