"""
Ticket module defined for different ticket related api endpoints.
"""

""" *******************************************************************************************************************
|
|  Name        :  __ticket.py
|  Module      :  risksense_api
|  Description :  A class to be used for tickets on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

from http import client
import json
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from .. import Subject
from ..._params import *
from ..._api_request_handler import *


class Ticket(Subject):

    """Class for ticket function definitions.

    Args:
        profile:     Profile Object

    To utlise ticket function:
    
    Usage:
        :obj:`self.{risksenseobjectname}.ticket.{function}`
    
    Examples:
        To get connector fields for a ticket using :meth:`getconnectorfields` function

        >>> self.{risksenseobjectname}.ticket.getconnectorfields(args)

    """

    def __init__(self, profile:object):

        """
        Initialization of Ticket object.

    Args:
        profile:     Profile Object
        """

        self.subject_name = "ticket"
        Subject.__init__(self, profile, self.subject_name)

    def getconnectorfields(self,connector_id:int, client_id:int=None)->dict:
        """
        Get connector fields present in ticket form

        Args:
            connector_id:   Connector Id
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID
        
        Return:
            Jsonified response

        Examples:
            >>> apiobj = self.{risksenseobject}.ticket.getconnectorfields(123,client_id=123)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url =self.profile.platform_url+ "/api/v1/client/{}/connector/{}/ticket".format(str(client_id),str(connector_id))


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching template')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response


    def gettemplateid(self,connector_id:int, client_id:int=None)->dict:
        """
        Get available templates

        Args:
            connector_id:       Connector Id
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID
        
        Return:
            Jsonified response

        Examples:
            >>> apiobj = self.{risksenseobject}.ticket.gettemplateid(123,client_id=123)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/template'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching template')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response


    def getfieldsfromtemplateid(self,connector_id:int,template_id:int, client_id:int=None)->dict:

        """
        Get fields available for a particular template

        Args:
            connector_id:       Connector Id
            template_id:        Template Id
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID
        
        Return:
            Jsonified response

        Examples:
            >>> apiobj = self.{risksenseobject}.ticket.getfieldsfromtemplateid(123,123,client_id=123)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/template/{template_id}/field'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching template')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response


    def getcatalogitemfield(self,connector_id:int, client_id:int=None)->dict:
        """
        Get fields available for a particular catalog item

        Args:
            connector_id:       Connector Id
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID
        
        Return:
            Jsonified response

        Examples:
            >>> apiobj = self.{risksenseobject}.ticket.getcatalogitemfield(123,client_id=123)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/catalogItemField'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching template')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def getissuetypefield(self,connector_id:int, client_id:int=None)->dict:
        """
        Get available issue types

        Args:
            connector_id:       Connector Id
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID
        
        Return:
            Jsonified response

        Examples:
            >>> apiobj = self.{risksenseobject}.ticket.getissuetypefield(123,client_id=123)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/issueTypeField'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching issue type field')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def getticketinfo(self,ticket_id:str, client_id:int=None)->dict:
        """
        Get info about a ticket

        Args:
            ticket_id:      Ticket Id
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Jsonified response

        Examples:
            >>> apiobj = self.{risksenseobject}.ticket.getticketinfo('TP-123',client_id=123)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.api_base_url.format(str(client_id))+'/{}'.format(str(ticket_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def deleteticket(self,ticket_uuid:str, client_id:int=None)->bool:
        """
        Delete ticket

        Args:
            ticket_uuid:        Ticket UUID
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Deletion status

        Examples:
            >>> apiobj = self.{risksenseobject}.ticket.getconnectorfields('123-456',client_id=123)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.api_base_url.format(str(client_id))+'/{}'.format(str(ticket_uuid))
        success = False
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        if raw_response.status_code == 204:
            success = True

        return success

    def create_ticket(self,tag_id:int,body:dict,client_id:int=None)->dict:
        """
        Create a ticket

        Args:
            tag_id: Tag Id
            body: API request ticket body
            client_id: Client ID.  If an ID isn't passed, will use the profile's default Client ID

        Returns:
            Jsonified response

        Note:
            Intercept this API endpoint ``/client/{clientId}/ticket/{tag_id}`` in UI to better understand the ``body`` that need to be sent using this function. Then, use this function in your automation.
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.api_base_url.format(str(client_id))+'/{}'.format(str(tag_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response
    
    def ivanti_itsm_fetch_ticketField_values(self, connector_id:int, client_id:int=None)->dict:
        """
        Fetch ticket field values for Ivanti ITSM

        Args:
            connector_id: Connector Id
            client_id: Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Returns:
            Jsonified response

        Examples:
            >>> apiobj = self.{risksenseobject}.ticket.ivanti_itsm_fetch_ticketField_values(123,client_id=123)
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/ivanti/fetchTicketFields'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response        


    def ivanti_itsm_retrieve_ticketFields(self, connector_id:int, ticket_type:str,client_id:int=None)->dict:
        """
        Retrieve ticket fields for Ivanti ITSM

        Args:
            connector_id: Connector Id
            ticket_type:        Type of the ticket to be created.
            client_id: Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Returns:
            Jsonified response

        Examples:
            >>> apiobj = self.{risksenseobject}.ticket.ivanti_itsm_retrieve_ticketFields(123,'incident',client_id=123)   
        """     
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/ivanti/retriveTicketFields'
        body = {
            "type": "IVANTIITSM",
            "ticketType": ticket_type,
            "connectorId": connector_id
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  


    def ivanti_itsm_fetch_customers(self, connector_id:int, client_id:int=None)->dict:
        """
        Fetch available customers for Ivanti ITSM

        Args:
            connector_id: Connector Id
            client_id: Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Returns:
            Jsonified response

        Examples:
            >>> apiobj = self.{risksenseobject}.ticket.ivanti_itsm_fetch_customers(123,client_id=123)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/ivanti/fetchCustomers/Frs_CompositeContract_Contacts'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  


    def ivanti_itsm_fetch_fieldValue_wrt_dependentField(self, ticket_type:str, connector_id:int, current_field:str, dependent_field:str, dependent_field_value:str, client_id:int=None)->dict:
        """
        Fetch available options for a current Ivanti ITSM field with respect to its dependent Ivanti ITSM field

        Args:
            ticket_type:        Ticket type
            connector_id: Connector Id
            current_field:      Field name key of the field to be queried for
            dependent_field:      Dependent field name key
            dependent_field_value:      Value of the dependent field
            client_id: Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Returns:
            Jsonified response

        Examples:
            >>> apiobj = self.{risksenseobject}.ticket.ivanti_itsm_fetch_fieldValue_wrt_dependentField('incident',123,'category','status','test',client_id=123)
        """        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/ivanti/fetchValidatedFieldValue'

        body = {"type":"IVANTIITSM","ticketType":ticket_type,"connectorId":connector_id,"actualField":current_field,"dependentField":dependent_field,"dependentFieldValue":dependent_field_value}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  


    def ivanti_itsm_fetch_validation(self, body:dict, client_id:int=None)->dict:
        """
        Form validation for ivanti ITSM

        Args:
            body: API request ticket body
            client_id: Client ID.  If an ID isn't passed, will use the profile's default Client ID

        Returns:
            Jsonified response

        Note:
            Intercept this API endpoint ``/client/{clientId}/connector/{connectorId}/ivanti/formValidation`` in UI to better understand the ``body`` that need to be sent using this function. Then, use this function in your automation.        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f"/api/v1/client/{client_id}/connector/{body['connectorId']}/ivanti/formValidation"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  


    def ivanti_itsm_fetch_releaseLink(self, connector_id:int, client_id:int=None)->dict:
        """
        Fetch available release links for Ivanti ITSM

        Args:
            connector_id: Connector Id
            client_id: Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Returns:
            Jsonified response

        Examples:
            >>> apiobj = self.{risksenseobject}.ticket.ivanti_itsm_fetch_releaseLink(123,client_id=123)
        """       

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/ivanti/fetchCustomers/ReleaseProjects'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  


    def ivanti_itsm_fetch_requestorLink(self, connector_id:int, client_id:list=None)->dict:
        """
        Fetch available requestor links for Ivanti ITSM

        Args:
            connector_id: Connector Id
            client_id: Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Returns:
            Jsonified response

        Examples:
            >>> apiobj = self.{risksenseobject}.ticket.ivanti_itsm_fetch_requestorLink(123,client_id=123)
        """     

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/ivanti/fetchCustomers/Employees'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
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
