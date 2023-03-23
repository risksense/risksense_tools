"""
Role module defined for different role related api endpoints.
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
from .. import Subject
from ..._params import *
from ..._api_request_handler import *


class Role(Subject):

    """Class for role function definitions.

    Args:
        profile:     Profile Object

    To utlise role function:
    
    Usage:
        :obj:`self.{risksenseobjectname}.roles.{function}`
    
    Examples:
        To create a role using :meth:`create` function

        >>> self.rs.roles.create(args)

    """

    def __init__(self, profile:object):

        """
        Initialization of Roles object.

        Args:
            profile:     Profile Object

        """

        self.subject_name = "role"
        Subject.__init__(self, profile, self.subject_name)
        self.alt_api_base_url=self.profile.platform_url+"/api/v1/client/{}/"

    def create(self, name:str, description:str, client_id:int=None)->int:
        """
        Create a new role.

        Args:
            name:            The name for the new network.
            decription:      The description of the role.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The new role ID.
        
        Examples:
            >>> apiobj = self.{risksenseobject}.users.create('test','test')
        """
        print(name,description)

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        #if name or description is None:
        #   raise ValueError('Name or description is not provided please provide them')

        body = {
            "name": name,
            "description": description
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

    def allow_privileges(self, roleid:int, client_id:int=None)->bool:
        """
        Allow privileges to a role.

        Args:
            roleid:            Rold Id
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Job State
        
        Examples:
            >>> apiobj = self.{risksenseobject}.users.allow_privileges(1234)
        """

        privlegesids,privilegesnames=self.get_privileges()

        for i in range(len(privilegesnames)):
            print(i,privilegesnames[i])
        
        try:
            inputsofrolestoallow=[privlegesids[int(i)] for i in input('Please enter the privileges ids that you want to allow to the role seperated by comma:').split(',')]
        except (IndexError, Exception) as e:
                        print()
                        print('There seems to be an exception,please provide an index from the list')
                        print(e)
                        exit()       

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        body = {
            "negate":False
        }
        for i in inputsofrolestoallow:
            url = url = self.api_base_url.format(str(client_id))+'/{}/privilege/{}'.format(roleid,i)
            try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            except (RequestFailed,Exception) as e:
                 print()
                 print('There seems to be an exception')
                 print(e)
                 exit()
        success=True
        return success
    
    def deny_privileges(self, roleid:int, client_id:int=None)->bool:
        """
        Deny privileges to a role.

        Args:
            roleid:            Rold Id
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Job State
        
        Examples:
            >>> apiobj = self.{risksenseobject}.users.deny_privileges(1234)
        """

        privlegesids,privilegesnames=self.get_privileges()

        for i in range(len(privilegesnames)):
            print(i,privilegesnames[i])
        try:
            inputsofrolestodeny=[privlegesids[int(i)] for i in input('Please enter the privileges ids that you want to deny to the role seperated by comma:').split(',')]        
        except (IndexError, Exception) as e:
                        print()
                        print('There seems to be an exception,please provide an index from the list')
                        print(e)
                        exit()
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        body = {
            "negate":True
        }
        for i in inputsofrolestodeny:
            url = url = self.api_base_url.format(str(client_id))+'/{}/privilege/{}'.format(roleid,i)
            try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            except (RequestFailed,Exception) as e:
                 print()
                 print('There seems to be an exception')
                 print(e)
                 exit()
        success=True
        return success

    def delete_privileges(self, roleid:int, client_id:int=None)->bool:
        """
        Delete privileges to a role.

        Args:
            roleid:            Rold Id
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Job State
        
        Examples:
            >>> apiobj = self.{risksenseobject}.users.delete_privileges(1234)
        """

        privlegesids,privilegesnames=self.get_privileges()

        for i in range(len(privilegesnames)):
            print(i,privilegesnames[i])
        
        try:
            inputsofrolestodeny=[privlegesids[int(i)] for i in input('Please enter the privileges ids that you want to remove to the role seperated by comma:').split(',')]        
        except (IndexError, Exception) as e:
                        print()
                        print('There seems to be an exception,please provide an index from the list')
                        print(e)
                        exit()   
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        for i in inputsofrolestodeny:
            url = url = self.api_base_url.format(str(client_id))+'/{}/privilege/{}'.format(roleid,i)
            try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
            except (RequestFailed,Exception) as e:
                 print()
                 print('There seems to be an exception')
                 print(e)
        sucess=True
        return sucess

    def get_privileges(self, client_id:int=None)->tuple:
        """
        Get privileges to a role.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            (Privilege Id, Privilege Name)
        
        Examples:
            >>> apiobj = self.{risksenseobject}.users.get_privileges()
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.alt_api_base_url.format(client_id)+'privilege?page=0&size=500'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        if raw_response.status_code==200:
            jsonified_response = json.loads(raw_response.text)
            privilegesid=[jsonified_response["_embedded"]["privileges"][i]['id'] for i in range(len(jsonified_response["_embedded"]["privileges"]))]
            privilegesname=[jsonified_response["_embedded"]["privileges"][i]['name'] for i in range(len(jsonified_response["_embedded"]["privileges"]))]
            return privilegesid,privilegesname
        else:
            print(raw_response)
        

    def update(self, roleid:int,name:str, description:str, client_id:int=None)->int:
        """
        Update a new role.

        Args:
            roleid:            Rold Id
            name:            The name for the new role.
            description:      The description of the role.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The new role ID.

        Examples:
            >>> apiobj = self.{risksenseobject}.users.update(123,'test','test')
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/{}'.format(roleid)

        #if name or description is None:
        #   raise ValueError('Name or description is not provided please provide them')

        body = {
            "name": name,
            "description": description
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        role_id = jsonified_response['id']
        role_name=jsonified_response['name']


        return role_id



    def delete_role(self, roleid:int,client_id:int=None)->bool:
        """
        Update a new role.

        Args:
            roleid:            Rold Id
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            State(True/False)

        Examples:
            >>> apiobj = self.{risksenseobject}.users.delete_role('xxxx')
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/{}'.format(roleid)
        success = False

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
            success = True
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return success

    
    
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
