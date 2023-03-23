"""
Upload module defined for different upload related api endpoints.
"""

""" *******************************************************************************************************************
|
|  Name        : __uploads.py
|  Module      : risksense_api
|  Description : A class to be used for interacting with uploads on the RiskSense Platform.
|  Copyright   : (c) RiskSense, Inc.
|  License     : Apache-2.0  (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

from argparse import FileType
from importlib.resources import path
import json
from ...__subject import Subject
from ..._api_request_handler import *


class Uploads(Subject):

    """Class for upload function definitions.

    Args:
        profile:     Profile Object

    To utlise upload function:
    
    Usage:
        :obj:`self.{risksenseobjectname}.uploads.{function}`
    
    Examples:
        Create an upload using :meth:`create` function

        >>> self.{risksenseobjectname}.uploads.create(args)
    """

    def __init__(self, profile:object):

        """
        Initialization of Uploads object.

        Args:
            profile:     Profile Object
        """

        self.subject_name = "upload"
        Subject.__init__(self, profile, self.subject_name)

    def get_uploads(self, assessment_id:int, page_num:int=0, page_size:int=150, client_id:int=None)->dict:
        """
        Get uploads associated with an assessment.

        Args:
            assessment_id:   The assessment ID.
            page_num:        The page number of results to return.
            page_size:       The number of results per page to return.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:    
            The JSON response from the platform is returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.uploads.get_uploads(1234,page_num=1,page_size=100)            
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        params = {
            "assessmentId": assessment_id,
            "size": page_size,
            "page": page_num
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def create(self, name:str, assessment_id:int, network_id:int, client_id:int=None)->int:
        """
        Create a new upload.

        Args:
            name:            The name to be associated with the upload.
            assessment_id:   The assessment ID.
            network_id:      The network ID.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:    
            The Upload ID

        Examples:
            >>> apiobj = self.{risksenseobject}.uploads.create('test',123,123,client_id=123)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        body = {
            "assessmentId": assessment_id,
            "networkId": network_id,
            "name": name
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        upload_id = jsonified_response['id']

        return upload_id

    def check_state(self, upload_id:int, client_id:int=None)->str:
        """
        Check the state of an upload.

        Args:
            upload_id:   The upload ID.
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The current state of the upload is returned.
        
        Examples:
            >>> apiobj = self.{risksenseobject}.uploads.check_state(1234) 
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(upload_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        state = jsonified_response['state']

        return state

    def update(self, upload_id:int,name:str,network_id:int,assessment_id:int, client_id:int=None)->int:
        """
        Update an upload.  Uploads can only be updated before they have been processed.

        Args:
            upload_id:           The upload ID.
            name:               File name
            network_id:          Network ID.
            assessment_id:      Assessment ID
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The upload ID is returned.
        
        Examples:
            >>> apiobj = self.{risksenseobject}.uploads.update(1234,'test',123,123,client_id=123)    
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(upload_id))

        body = {
            "name": name,
            "assessmentId": assessment_id,
            "networkId": network_id
        }

        body = self._strip_nones_from_dict(body)

        if body == {}:
            raise ValueError("Body is empty.  Please provide name, assessment_id, and/or network_id")

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def delete(self, upload_id:int, client_id:int=None)->bool:
        """
        Delete an Upload.

        Args:
            upload_id:   The upload ID
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:    
            True/False reflecting whether or not the operation was successful.

        Examples:
            >>> apiobj = self.{risksenseobject}.uploads.delete(1234)  
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(upload_id))

        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        success = True

        return success

    def list_files(self, upload_id:int, page_num:int=0, page_size:int=150, client_id:int=None)->dict:
        """
        List files in an upload.

        Args:
            upload_id:  The upload ID
            page_num:   The page number to be returned.
            page_size:  The number of results to return per page.
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            A paginated JSON response from the platform.

        Examples:
            >>> apiobj = self.{risksenseobject}.uploads.list_files(1234,page_num=1,page_size=100)  
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/file".format(str(upload_id))

        params = {
            "size": page_size,
            "page": page_num
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def add_file(self, upload_id:int, file_name:str, path_to_file:str, client_id:int=None)->dict:
        """
        Add a file to an upload.

        Args:
            upload_id:   Upload ID
            file_name:   The name to be used for the uploaded file.
            path_to_file:   Full path to the file to be uploaded.
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:    
            The file ID along with jsonified response is returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.uploads.add_file(1234,'test','D:\\test\\test.nessus')  
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/file".format(str(upload_id))

        upload_file = {'scanFile': (file_name, open(path_to_file, 'rb'))}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,files=upload_file)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        except FileNotFoundError as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        
        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def update_file(self, upload_id:int, file_id:int, client_id:int=None, **kwargs)->int:
        """
        Update an uploaded file.  Will only work if the file has not yet been processed.

        Args:
            upload_id:   The upload ID.
            file_id:     The file ID.
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Keyword Args:    
            assessment_id (``int``):     The assessment ID the upload should be associated with.  Integer.
            network_id (``int``):        The network ID the upload should be associated with.  Integer.
            application_id (``int``):    The application ID the upload should be associated with.  Integer.

        Return:
            The upload ID is returned

        Examples:
            >>> apiobj = self.{risksenseobject}.uploads.update_file(1234,123,assessment_id=123,network_id=123,application_id=123)   
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/file/{}".format(str(upload_id), str(file_id))

        assessment_id = kwargs.get('assessment_id', None)
        network_id = kwargs.get('network_id', None)
        application_id = kwargs.get('application_id', None)

        body = {
            "assessmentId": assessment_id,
            "networkId": network_id,
            "applicationId": application_id
        }

        body = self._strip_nones_from_dict(body)

        if body == {}:
            raise ValueError('Body empty. Please provide assessment_id, network_id, and/or application_id missing.')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        

        jsonified_response = json.loads(raw_response.text)
        returned_id = jsonified_response['id']

        return returned_id

    def delete_file(self, upload_id:int, file_id:int, client_id:int=None)->bool:
        """
        Delete an uploaded file.

        Args:
            upload_id:   The upload ID.
            file_id:     The file ID.
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            True/False reflecting whether or not the operation was successfully submitted.

        Examples:
            >>> apiobj = self.{risksenseobject}.uploads.delete_file(1234,123)             
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/file/{}".format(str(upload_id), str(file_id))

        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        success = True

        return success

    def download_file(self, upload_id:int, file_name:str, client_id:int=None)->bool:
        """
        Download a previously uploaded file.

        Args:
            upload_id:           The upload ID
            file_name:       The filename
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:    
            True/False reflecting whether or not the operation was successful.

        Examples:
            >>> apiobj = self.{risksenseobject}.uploads.download_file(1234,'test')   
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/file/download".format(str(upload_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        try:
            open(f"{file_name}.zip", "wb").write(raw_response.content)
            success = True
        except (FileNotFoundError, FileExistsError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return success

    def fetch_file_by_uuid(self, upload_id:int, file_uuid:str, file_destination:str, client_id:int=None)->bool:
        """
        Download a file by UUID.

        Args:
            upload_id:           The upload ID
            file_uuid:           The file UUID
            file_destination:    The local destination for the downloaded file.
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:    
            True/False reflecting whether or not the operation was successful.

        Examples:
            >>> apiobj = self.{risksenseobject}.uploads.fetch_file_by_uuid(1234,'123-456','D:\\test\\test.xml')    
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/file/{}".format(str(upload_id), str(file_uuid))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        try:
            open(file_destination, "wb").write(raw_response.content)
            success = True
        except (FileNotFoundError, FileExistsError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return success

    def start_processing(self, upload_id:int, auto_urba:bool=False, client_id:int=None)->bool:
        """
        Initiate processing of an upload.

        Args:
            upload_id:   The upload ID
            auto_urba:   Indicator for whether or not auto-URBA should be run after upload is processed.
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:    
            True/False reflecting whether or not the operation was successfully submitted.

        Examples:
            >>> apiobj = self.{risksenseobject}.uploads.start_processing(1234,True)    
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/start".format(str(upload_id))

        body = {
            "autoUrba": auto_urba
        }

        try:
            self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            success = True
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return success


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
