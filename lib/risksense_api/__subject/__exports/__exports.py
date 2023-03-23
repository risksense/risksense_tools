"""
**Exports module defined for different export related api endpoints.**
"""
""" *******************************************************************************************************************
|
|  Name         :  __exports.py
|  Module       :  risksense_api
|  Description  :  A class to be used for interacting with RiskSense platform exports.
|  Copyright    :  (c) RiskSense, Inc.
|  License      :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

import json
from ...__subject import Subject
from ..._api_request_handler import *


class ExportFileType:
    """ ExportFileType class and params"""
    CSV = "CSV"
    XML = "XML"
    XLSX = "XLSX"
    JSON=  "JSON"

class ExportRowNumbers:
    """ ExportRowNumbers class and params"""
    ROW_5000 = "5000"
    ROW_10000 = "10000"
    ROW_25000 = "25000"
    ROW_50000 = "50000"
    ROW_100000 = "100000"
    ROW_ALL = "All"


class Exports(Subject):

    """
        **Class for Exports function defintions**.

        To utlise exports function:

        Args:
                profile:     Profile Object
        
        Usage:
            :obj:`self.{risksenseobjectname}.exports.{function}`
        
        Examples:
            To download an export using :meth:`download_export()` function

            >>> self.{risksenseobject}.exports.download_export(123,'test.csv')

    """

    def __init__(self, profile:object):

        """
        Initialization of Exports object.

        Args:
            profile:     Profile Object
        
        """

        self.subject_name = "export"
        Subject.__init__(self, profile, self.subject_name)

    def check_status(self, export_id:int, client_id:str=None)->str:

        """
        Checks on the status of an export.

        Args:
            export_id:   The ID of the export to be checked.

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
           A string reflecting the status of the export is returned.

        Example:
            To check status of export id 123

            >>> self.{risksenseobject}.export.check_status(123)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/status".format(str(export_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        jsonified_response = json.loads(raw_response.text)
        export_status = jsonified_response['status']

        return export_status

    def download_export(self, export_id:int, filename:str, client_id:int=None)->bool:

        """
        Download an exported file.

        Args:
            export_id:   The ID of the export.

            filename:    The filename to save the downloaded file as.

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          True/False reflects whether or not the download was successful.
        Example:
            To download an export file
           
            >>> self.{risksenseobject}.export.download_export(123,'test.csv')
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(export_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)

        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        try:
            open(filename, "wb").write(raw_response.content)

        except (FileNotFoundError, Exception) as e:
            print('There seems to be an exception')
            print(e)
            exit()

        success = True

        return success

    def delete_files(self, export_id:int, client_id:int=None)->bool:
        
        """
        Delete export job.

        Args:
            export_id:   The export ID.

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          True/False reflecting whether or not the file deletion was successful.
        Example:
            To delete an export job
            
            >>> self.{risksenseobject}.export.delete_files(123)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(export_id))

        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        success = True

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
