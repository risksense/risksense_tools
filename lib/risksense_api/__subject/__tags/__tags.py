"""
**Tags module defined for different tags related api endpoints.**
"""
""" *******************************************************************************************************************
|
|  Name        :  __tags.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating tags on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

import json
from tokenize import Triple
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
from ..__exports import Exports
import sys
import zipfile
import csv
import pandas as pd


class TagType:
    """ TagType class and attributes"""

    COMPLIANCE = 'COMPLIANCE'
    LOCATION = 'LOCATION'
    CUSTOM = 'CUSTOM'
    REMEDIATION = 'REMEDIATION'
    PEOPLE = 'PEOPLE'
    PROJECT = 'PROJECT'
    SCANNER = 'SCANNER'
    CMDB = 'CMDB'


class Tags(Subject):

    """ **Class for Tags function defintions**.

    To utlise Tags function:

    Args:
            profile:     Profile Object
    
    Usage:
        :obj:`self.{risksenseobjectname}.Tags.{function}`
    
    Examples:
        To search for tags using :meth:`search()` function

        >>> self.{risksenseobject}.tags.search({filterobject})

    """


    def __init__(self, profile:object):

        """
        Initialization of Tags object.

        profile:     Profile Object
        :type  profile:     _profile
        """

        self.subject_name = "tag"
        Subject.__init__(self, profile, self.subject_name)

    def downloadfilterinexport(self,filename:str,filters:list,client_id:int=None):
        
        """ **Exports and Downloads a file based on the filters defined** .

        Args:
            filename: Name of the file to export as
            filters:  Tag search filters based on which the export performs
            client_id: The client id to get the data from. If not supplied, takes default client id

        **IGNORE INTERNAL FUNCTION**

        Examples:
            >>>  self.{risksenseobject}.tags.downloadfilterinexport('applicationfindingsdata',[])
        """
        if client_id is None:
            client_id= self._use_default_client_id()
        exportid=self.export(filters,file_name=filename)
        self.exports=Exports(self.profile)
        while(True):
                try:
                    exportstatus=self.exports.check_status(exportid)
                    print(exportstatus)
                    if exportstatus=='COMPLETE':
                        break
                    elif exportstatus=='ERROR':
                        print('error getting zip file please check ')
                        exit()
                except (RequestFailed,MaxRetryError,StatusCodeError, ValueError) as ex:       
                    print(ex)
                    print()
                    print("Unable to export the file.")
                    sys.exit("Exiting")
        try:   
                self.exports.download_export(exportid,f"{filename}.csv")
        except(RequestFailed,MaxRetryError,StatusCodeError, ValueError):
                    print(ex)
                    print()
                    print("Unable to retrieve file. Exiting.")
                    sys.exit(1)
  
    
    def create(self, tag_type:str, name:str, desc:str, owner:str, color:str="#648d9f", locked:bool=False, propagate:bool=True,csvdump:bool=False, client_id=None)->int:

        """
        Create a new tag for the client.

        Args:

            tag_type:    Type of tag to be created.TagType.COMPLIANCE,
                                                    TagType.LOCATION,
                                                    TagType.CUSTOM,
                                                    TagType.REMEDIATION,
                                                    TagType.PEOPLE,
                                                    TagType.PROJECT,
                                                    TagType.SCANNER,
                                                    TagType.CMDB

            name:        Name of tag

            desc:        Description of tag

            owner:       The owner(s) of the tag, represented by user IDs, delimited by commas.  Ex: "1234,567,890"

            color:       Hex value of the color to be used for this tag.

            locked:      Reflects whether or not the tag should be locked.

            propagate:    Propagate tag to all findings?

            csvdump:         dumps the data in csv

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The new tag ID will be returned.
        Example:
            To create a tag of type people and give it a name rspackagetest and assign to user id 123
            
            >>> self.rs.tags.create("PEOPLE",'rspackagetest','none',123)
        Note:
            You can also dump the tag id created in a csv using :obj:`csvdump=True`:

            >>> self.rs.tags.create("PEOPLE",'rspackagetest','none',123,csvdump=True)

            For type specific tag creation , please view private functions section way below
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        list_of_tag_types = [
            TagType.COMPLIANCE,
            TagType.LOCATION,
            TagType.CUSTOM,
            TagType.REMEDIATION,
            TagType.PEOPLE,
            TagType.PROJECT,
            TagType.SCANNER,
            TagType.CMDB
        ]

        tag_type = tag_type.upper()
        if tag_type not in list_of_tag_types:
            raise ValueError(f"Tag Type provided ({tag_type}) is not supported.")

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
        
        url = self.api_base_url.format(str(client_id))

        body = {
            "fields": [
                {
                    "uid": "TAG_TYPE",
                    "value": tag_type
                },
                {
                    "uid": "NAME",
                    "value": name
                },
                {
                    "uid": "DESCRIPTION",
                    "value": desc
                },
                {
                    "uid": "OWNER",
                    "value": owner
                },
                {
                    "uid": "COLOR",
                    "value": color
                },
                {
                    "uid": "LOCKED",
                    "value": locked
                },
                {
                    "uid": "PROPAGATE_TO_ALL_FINDINGS",
                    "value": propagate
                }
            ]
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        new_tag_id = jsonified_response['id']

        if csvdump==True:
            tagid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagidcreated.csv',index=False)

        return new_tag_id

    def getexporttemplate(self,client_id:int=None)->list:
        
        """
        Gets configurable export template for Tags.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The Exportable fields
        Example:
            An example to use getexporttemplate
                
                >>> self.{risksenseobject}.tag.getexporttemplate()

            This gets all the export templates for tags

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/export/template"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        exportablefilter = json.loads(raw_response.text)

        for i in range(len(exportablefilter['exportableFields'])):
            for j in range(len(exportablefilter['exportableFields'][i]['fields'])):
                if exportablefilter['exportableFields'][i]['fields'][j]['selected']==False:
                    exportablefilter['exportableFields'][i]['fields'][j]['selected']=True

        return exportablefilter['exportableFields']

    def export(self, search_filters:list, file_name:str, row_count:str=ExportRowNumbers.ROW_ALL,file_type:str=ExportFileType.CSV, client_id:int=None)->int:

        """
        Initiates an export job on the platform for Tag(s) based on the
        provided filter(s).
        
        Args:
            search_filters:  A list of dictionaries containing filter parameters.

            file_name:       The name to be used for the exported file.

            row_count:        No of rows to be exported. Available options
                            ExportRowNumbers.ROW_10000,
                            ExportRowNumbers.ROW_25000,
                            ExportRowNumbers.ROW_50000,
                            ExportRowNumbers.ROW_100000,
                            ExportRowNumbers.ROW_ALL

            exportable_filter:       Exportable filter
            file_type:       File type to export.  ExportFileType.CSV, ExportFileType.JSON, or ExportFileType.XLSX

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID in the platform from is returned.
        
        Example:
            An example to use export is
            
                >>> self.{risksenseobject}.tags.export([],'testingexport')
            
            You can change the filetype to any of the names above or even the other positional arguments as mentioned

                >>> self.{risksenseobject}.tags.export([],'testingexport',file_type=ExportFileType.JSON)

        """
        func_args = locals()
        exportablefilter=self.getexporttemplate()
        func_args['exportable_filter']=exportablefilter
        func_args.pop('self')
        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]
        try:
            export_id = self._export(self.subject_name, **func_args)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return export_id


    def list_tag_filter_fields(self,client_id:int=None)->list:

        """
        List filter endpoints.

        Args:

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The JSON output from the platform is returned, listing the available filters.

        Examples:
            >>>  self.{risksenseobject}.tags.list_tag_filter_fields()
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/filter'
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)

        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def export(self, search_filters:list, file_name:str, row_count:str=ExportRowNumbers.ROW_ALL,file_type:str=ExportFileType.CSV, client_id:int=None)->int:

        """
        Initiates an export job on the platform for Tag(s) based on the
        provided filter(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.

            file_name:       The name to be used for the exported file.

            row_count:      No of rows to be exported. Available options
                                ExportRowNumbers.ROW_10000,
                                ExportRowNumbers.ROW_25000,
                                ExportRowNumbers.ROW_50000,
                                ExportRowNumbers.ROW_100000,
                                ExportRowNumbers.ROW_ALL

            exportable_filter:       Exportable filter

            file_type:       File type to export. ExportFileType.CSV, ExportFileType.JSON,  or ExportFileType.XLSX

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID in the platform from is returned.
        Example:
            An example to use export is
            
                >>> self.{risksenseobject}.tags.export([],'testingexport')
            
            You can change the filetype to any of the names above or even the other positional arguments as mentioned

                >>> self.{risksenseobject}.tags.export([],'testingexport',file_type=ExportFileType.JSON)

        """
        func_args = locals()
        exportablefilter=self.getexporttemplate()
        func_args['exportable_filter']=exportablefilter
        func_args.pop('self')
        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]
        try:
            export_id = self._export(self.subject_name, **func_args)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return export_id

    def update(self, tag_id:int, tag_type:str, name:str, desc:str, owner:str, color:str, locked:bool, propagate:bool=True,csvdump:bool=False, client_id:int=None)->int:

        """
        Update an existing tag.

        Args:
            tag_id:      The tag ID to be updated.

            tag_type:    The type of tag.

            name:        The name of the tag.

            desc:        A description for the tag.

            owner:       The owner(s) of the tag, represented by user IDs, delimited by commas.  Ex: "1234,567,890"

            color:       The color for the tag.  A hex value.

            locked:      Whether or not the tag should be locked.

            propagate:    Propagate tag to all findings?

            csvdump:         dumps the data in csv


            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The job ID will be returned.
        Example:
            To update a tag id 123 of type people and give it a name rspackagetest and assign to user id 123
            
            >>> self.rs.tags.update(123,"PEOPLE",'rspackagetest','none',123)
        Note:
            You can also dump the tag based data in a csv using :obj:`csvdump=True`:

            >>> self.rs.tags.update(123,"PEOPLE",'rspackagetest','none',123,csvdump=True)

            For lock unlock specific tag update, please view private functions way below

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        list_of_tag_types = [
            TagType.COMPLIANCE,
            TagType.LOCATION,
            TagType.CUSTOM,
            TagType.REMEDIATION,
            TagType.PEOPLE,
            TagType.PROJECT,
            TagType.SCANNER,
            TagType.CMDB
        ]

        if tag_type not in list_of_tag_types:
            raise ValueError("Invalid tag type")

        body = {
            "fields": [
                {
                    "uid": "TAG_TYPE",
                    "value": tag_type
                },
                {
                    "uid": "NAME",
                    "value": name
                },
                {
                    "uid": "DESCRIPTION",
                    "value": desc
                },
                {
                    "uid": "OWNER",
                    "value": owner
                },
                {
                    "uid": "COLOR",
                    "value": color
                },
                {
                    "uid": "LOCKED",
                    "value": locked
                },
                {
                    "uid": "PROPAGATE_TO_ALL_FINDINGS",
                    "value": propagate
                }
            ]
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(tag_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        response_id = jsonified_response['id']

        if csvdump==True:
            self.downloadfilterinexport('tagupdated',[{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":f"{tag_id}"}])

        return response_id

    def delete(self, tag_id:int, force_delete:bool=True,csvdump:bool=False, client_id:int=None)->bool:

        """
        Delete a tag.

        Args:
            tag_id:          Tag ID to delete.

            force_delete:    Indicates whether or not deletion should be forced.

            csvdump:         dumps the data in csv

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            Boolean reflecting the indication from the platform as to whether or not the deletion was successful.

        Example:
            To delete a tag of id 123
                
                >>> self.rs.tags.delete(123)
            
            You can also dump the tag based data in a csv using :obj:`csvdump=True` argument:
                
                >>> self.rs.tags.delete(269662,csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        body = {
            "forceDeleteTicket": force_delete
        }

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(tag_id))

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
        
        if csvdump==True:
            self.downloadfilterinexport('tagtobedeleted',[{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":f"{tag_id}"}])
        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in deleting the tag')
            print()
            print(e)
            exit()

        success = True

        return success

    def bulk_tag_delete(self, search_filters:list, force_delete:bool=True,csvdump:bool=False,client_id:int=None)->bool:

        """
        Delete a bunch of tags.

        Args:
            search_filters:          Tag ID to delete.

            force_delete:    Indicates whether or not deletion should be forced.

            csvdump:         dumps the data in csv

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            Boolean reflecting the indication from the platform as to whether
                  or not the deletion was successful.
        Example:
            To perform bulk tag delete
            
            >>> self.rs.tags.bulk_tag_delete([])
        Note:
            You can also dump the tags that are going to be deleted using :obj:`csvdump=True` argument:
            
            >>> self.rs.tags.bulk_tag_delete([],csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        body = {
                "filterRequest": {
                    "filters":search_filters
                },
                "forceDeleteTicket": True
                }

        url = self.api_base_url.format(str(client_id))

        if csvdump==True:
            self.downloadfilterinexport('tagsthatarebeingdeleted',search_filters)
        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url, body=body)
            success = True
            return success
        except (RequestFailed,Exception) as e:
            print('Error in deleting the tag')
            print()
            print(e)
            exit()

    def get_history(self, tag_id:int, page_num:int=0, page_size:int=20,csvdump:bool=False,client_id:int=None)->dict:

        """
        Get the history for a tag.
        
        Args:
            tag_id:      Tag ID

            page_num:    Page number to retrieve.

            page_size:   Number of items to be returned per page

            csvdump:         dumps the data in csv

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            A paginated JSON response from the platform is returned.
        Example:
            To get history of the tag 123

            >>> self.rs.tags.get_history(123)
        
        Note:
            You can also dump the tag history by id created in a csv using :obj:`csvdump=True`:

            >>> self.rs.tags.get_history(123,csvdump=True)
                
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/history".format(str(tag_id))

        paginated_url = url + "?size=" + str(page_size) + "&page=" + str(page_num)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, paginated_url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)


        if csvdump==True:
            field_names = []
            print(jsonified_response)
            with open('taghistory.json','w') as f:
                f.write(json.dumps(jsonified_response))
            for item in jsonified_response['_embedded']['tagHistories'][0]:
                field_names.append(item)
            try:
                with open('get_taghistory.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response['_embedded']['tagHistories']:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response

    def get_single_search_page(self, search_filters:list, projection:str=Projection.BASIC, page_num:int=0, page_size:int=150,
                               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC, client_id:int=None)->dict:

        """
        Searches for and returns tags based on the provided filter(s) and other parameters.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.

            page_num:        Page number of results to be returned.

            page_size:       Number of results to be returned per page.

            projection:      Projection to use for query.  Default is "basic"

            sort_field:      Name of field to sort results on.

            sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            A paginated JSON response from the platform is returned.
        
        Example:
            An example to get single search page of tags data
            
            >>> self.{risksenseobject}.tags.get_single_search_page([])

            You can also try changing the other arguments to your liking to reflect the data as you suffice such as change page_size or page_num etc.

            >>> self.{risksenseobject}.tags.get_single_search_page([],page_num=2,page_size=10)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/search"

        body = {
            "filters": search_filters,
            "projection": projection,
            "sort": [
                {
                    "field": sort_field,
                    "direction": sort_dir
                }
            ],
            "page": page_num,
            "size": page_size
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

    def search(self, search_filters:list, projection=Projection.BASIC, page_size:int=150,
               sort_field:int=SortField.ID, sort_dir:int=SortDirection.ASC,csvdump:bool=False,client_id:int=None)->list:

        """
        Searches for and returns tags based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.

            projection:      Projection to be used in API request.  "basic" or "detail"

            page_size:       The number of results per page to be returned.

            sort_field:      Name of field to sort results on.

            sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC

            csvdump:         dumps the data in csv

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            A list containing all tags returned by the search using the filter provided.
        Example:
            An example to search for tags data is
            
            >>> self.{risksenseobject}.tags.search([])

        Note:
            You can also dump the search based data in a csv by simply providing :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.tags.search([],csvdump=True)
        """

        func_args = locals()
        func_args.pop('self')
        func_args.pop('csvdump')
        all_results = []

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            page_info = self._get_page_info(self.subject_name, search_filters, page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        if csvdump==True:
            self.downloadfilterinexport('tagsearch',search_filters)
        return all_results


    def get_model(self, client_id:int=None)->dict:

        """
        Get available projections and models for Tags.

        Args:
            client_id:   Client ID
        Return:
            Tags projections and models are returned.
        Example:
            
            An example to use get_model is
           
            >>> self.{risksenseobject}.tags.get_model()
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return response

    def suggest(self, search_filter_1:list, search_filter_2:dict, client_id:int=None)->list:

        """
        Suggest values for filter fields.

        Args:
            search_filter_1:     Search Filter 1

            search_filter_2:     Search Filter 2

            client_id:           Client ID
        Return:
            Value suggestions
        Example:
            To use suggest function is

            >>> self.{risksenseobject}.tags.suggest([],{})
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._suggest(self.subject_name, search_filter_1, search_filter_2, client_id)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return response

###PRIVATE FUNCTIONS

    def create_compliance_tag(self, name:str, desc:str, owner:str, color:str="#648d9f", locked:bool=False,csvdump:bool=False, client_id:int=None)->int:

        """
        Create a new COMPLIANCE tag.
        
        Args:
            name:        Name of tag

            desc:        Description of tag

            owner:       The owner(s) of the tag, represented by user IDs, delimited by commas.  Ex: "1234,567,890"

            color:       Hex value of the color to be used for this tag.

            locked:      Reflects whether or not the tag should be locked.

            csvdump:         dumps the data in csv

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The new tag ID will be returned.

        Example:
            To create a compliance tag 'testing' to user 123
            
            >>> self.rs.tags.create_compliance_tag('testing','something',123,"#648d9f",True)
        Note:
                You can also dump the tag id in a csv using the :obj:`csvdump=True` argument

                >>> self.rs.tags.create_compliance_tag('testing','something',123,"#648d9f",True,csvdump=True)


        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            tag_id = self.create(TagType.COMPLIANCE, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)
        
        return tag_id

    def create_location_tag(self, name:str, desc:str, owner:str, color:str="#648d9f", locked:bool=False,csvdump:bool=False, client_id:int=None)->int:

        """
        Create a new LOCATION tag.

        Args:
            name:        Name of tag

            desc:        Description of tag

            owner:       The owner(s) of the tag, represented by user IDs, delimited by commas.  Ex: "1234,567,890"

            color:       Hex value of the color to be used for this tag.

            locked:      Reflects whether or not the tag should be locked.

            csvdump:         dumps the data in csv

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The new tag ID will be returned.
        Example:
            To create a location tag 'testing' to user 123
            
            >>> self.rs.tags.create_location_tag('testing','something',123,"#648d9f",True)
        Note:
                You can also dump the tag id in a csv using the :obj:`csvdump=True` argument

                >>> self.rs.tags.create_location_tag('testing','something',123,"#648d9f",True,csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            tag_id = self.create(TagType.LOCATION, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)
        return tag_id

    def create_custom_tag(self, name:str, desc:str, owner:str, color:str="#648d9f", locked:bool=False,csvdump:bool=False, client_id:int=None)->int:

        """
        Create a new CUSTOM tag.
        
        Args:
            name:        Name of tag

            desc:        Description of tag

            owner:       The owner(s) of the tag, represented by user IDs, delimited by commas.  Ex: "1234,567,890"

            color:       Hex value of the color to be used for this tag.

            csvdump:         dumps the data in csv

            locked:      Reflects whether or not the tag should be locked.

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            Tag ID
        Example:
            To create a custom tag 'testing' to user 123
            
            >>> self.rs.tags.create_custom_tag('testing','something',123,"#648d9f",True)
        Note:
                You can also dump the tag id in a csv using the :obj:`csvdump=True` argument

                >>> self.rs.tags.create_custom_tag('testing','something',123,"#648d9f",True,csvdump=True)
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')        

        try:
            tag_id = self.create(TagType.CUSTOM, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)
    
        return tag_id

    def create_remediation_tag(self, name:str, desc:str, owner:str, color:str="#648d9f", locked:bool=False,csvdump:bool=False, client_id:int=None)->int:

        """
        Create a new REMEDIATION tag.

        Args:
            name:        Name of tag

            desc:        Description of tag

            owner:       The owner(s) of the tag, represented by user IDs, delimited by commas.  Ex: "1234,567,890"

            color:       Hex value of the color to be used for this tag.

            locked:      Reflects whether or not the tag should be locked.

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.

            csvdump:         dumps the data in csv
        Return:
            The new tag ID will be returned.
        Example:
            To create a remediation tag 'testing' to user 123
            
            >>> self.rs.tags.create_remediation_tag('testing','something',123,"#648d9f",True)
        Note:
                You can also dump the tag id in a csv using the :obj:`csvdump=True` argument

                >>> self.rs.tags.create_remediation_tag('testing','something',123,"#648d9f",True,csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')    

        try:
            tag_id = self.create(TagType.REMEDIATION, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)

        return tag_id

    def create_people_tag(self, name:str, desc:str, owner:str, color:str="#648d9f", locked:bool=False,csvdump:bool=False, client_id:int=None)->int:

        """
        Create a new PEOPLE tag.
        
        Args:
            name:        Name of tag

            desc:        Description of tag

            owner:       The owner(s) of the tag, represented by user IDs, delimited by commas.  Ex: "1234,567,890"

            color:       Hex value of the color to be used for this tag.

            locked:      Reflects whether or not the tag should be locked.

            csvdump:         dumps the data in csv

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The new tag ID will be returned.
        Example:
            To create a people tag 'testing' to user 123
            
            >>> self.rs.tags.create_people_tag('testing','something',123,"#648d9f",True)
        Note:
                You can also dump the tag id in a csv using the :obj:`csvdump=True` argument

                >>> self.rs.tags.create_people_tag('testing','something',123,"#648d9f",True,csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            tag_id = self.create(TagType.PEOPLE, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)

        return tag_id

    def create_project_tag(self, name:str, desc:str, owner:str, color:str="#648d9f", locked:bool=False,csvdump:bool=False, client_id:int=None)->int:

        """
        Create a new PROJECT tag.

        Args:
            name:        Name of tag

            desc:        Description of tag

            owner:       The owner(s) of the tag, represented by user IDs, delimited by commas.  Ex: "1234,567,890"

            color:       Hex value of the color to be used for this tag.

            locked:      Reflects whether or not the tag should be locked.

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.

            csvdump:         dumps the data in csv
        Return:
            The new tag ID will be returned.
        Example:
            To create a project tag 'testing' to user 123
            
            >>> self.rs.tags.create_project_tag('testing','something',123,"#648d9f",True)
        Note:
                You can also dump the tag id in a csv using the :obj:`csvdump=True` argument

                >>> self.rs.tags.create_project_tag('testing','something',123,"#648d9f",True,csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            tag_id = self.create(TagType.PROJECT, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)

        return tag_id

    def create_scanner_tag(self, name:str, desc:str, owner:str, color:str="#648d9f", locked:bool=False,csvdump:bool=False, client_id:int=None)->int:

        """
        Create a new SCANNER tag.

        Args:
            name:        Name of tag

            desc:        Description of tag

            owner:       The owner(s) of the tag, represented by user IDs, delimited by commas.  Ex: "1234,567,890"

            color:       Hex value of the color to be used for this tag.

            locked:      Reflects whether or not the tag should be locked.

            csvdump:         dumps the data in csv

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The new tag ID will be returned.
        Example:
            To create a scanner tag 'testing' to user 123
            
            >>> self.rs.tags.create_scanner_tag('testing','something',123,"#648d9f",True)
        Note:
                You can also dump the tag id in a csv using the :obj:`csvdump=True` argument

                >>> self.rs.tags.create_scanner_tag('testing','something',123,"#648d9f",True,csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            tag_id = self.create(TagType.SCANNER, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)

        return tag_id

    def create_cmdb_tag(self, name:str, desc:str, owner:str, color:str="#648d9f", locked:bool=False,csvdump:bool=False, client_id:int=None)->int:

        """
        Create a new CMDB tag.

        Args:
            name:        Name of tag

            desc:        Description of tag

            owner:       The owner(s) of the tag, represented by user IDs, delimited by commas.  Ex: "1234,567,890"

            color:       Hex value of the color to be used for this tag.

            locked:      Reflects whether or not the tag should be locked.

            csvdump:         dumps the data in csv

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The new tag ID will be returned.
        Example:
            To create a cmdb tag 'testing' to user 123
            
            >>> self.rs.tags.create_cmdb_tag('testing','something',123,"#648d9f",True)
        Note:
                You can also dump the tag id in a csv using the :obj:`csvdump=True` argument

                >>> self.rs.tags.create_cmdb_tag('testing','something',123,"#648d9f",True,csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            tag_id = self.create(TagType.CMDB, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)
        return tag_id

    def lock_tag(self, tag_id:int,csvdump:bool=False, client_id:int=None)->int:

        """
        Lock an existing tag.
        
        Args:
            tag_id:      The tag ID to be locked.

            csvdump:         dumps the data in csv

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The tag ID

        Example:
            To lock a tag id 123
            
            >>> self.rs.tags.lock_tag(123)

        Note:
            You can also dump the tag  data in a csv after locking by simply providing :obj:`csvdump=True` argument

            >>> self.rs.tags.lock_tag(123,csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(tag_id))

        body = {
            "fields": [
                {
                    'uid': 'LOCKED',
                    'value': True
                }
            ]
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
    

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        

        jsonified_response = json.loads(raw_response.text)
        response_id = jsonified_response['id']

        if csvdump==True:
            self.downloadfilterinexport('tagslocked',[{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":f"{tag_id}"}])

        return response_id

    def unlock_tag(self, tag_id:int,csvdump:bool=False, client_id:int=None)->int:

        """
        Unlock an existing tag.

        Args:
            tag_id:      The tag ID to be unlocked.

            csvdump:         dumps the data in csv

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The tag ID
        Example:
            To unlock a tag id 123
            
            >>> self.rs.tags.unlock_tag(123)

        Note:
            You can also dump the tag  data in a csv after unlocking by simply providing :obj:`csvdump=True` argument

            >>> self.rs.tags.unlock_tag(123,csvdump=True)


        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(tag_id))

        body = {
            "fields": [
                {
                    'uid': 'LOCKED',
                    'value': False
                }
            ]
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        


        jsonified_response = json.loads(raw_response.text)
        response_id = jsonified_response['id']

        if csvdump==True:
            self.downloadfilterinexport('tagunlocked',[{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":f"{tag_id}"}])

        return response_id



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
