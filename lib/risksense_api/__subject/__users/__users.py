"""
User module defined for different user related api endpoints.
"""

""" *******************************************************************************************************************
|
|  Name        :  __users.py
|  Module      :  risksense_api
|  Description :  A class to be used for getting information about RiskSense platform users.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

from datetime import datetime
import json
import uuid

from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
from ..__exports import Exports
import sys
import zipfile
import csv
import copy

class Users(Subject):

    """Class for user function definitions.

    Args:
        profile:     Profile Object

    To utlise user function:
    
    Usage:
        :obj:`self.{risksenseobjectname}.users.{function}`
    
    Examples:
        To create an user using :meth:`create` function

        >>> self.{risksenseobjectname}.users.create(args)
    """

    def __init__(self, profile:object):

        """
        Initialization of Users object.

        Args:
            profile:     Profile Object

        """

        self.subject_name = "user"
        Subject.__init__(self, profile, self.subject_name)
        self.api_base_url = self.profile.platform_url + "/api/v1/"

    def downloadfilterinexport(self,filename:str,filters:list,client_id:int=None):
        """
        Download user data based on search filters.

        Args:
            filename: Name of the file
            filters: A list of dictionaries containing filter parameters
            client_id: Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Note:
            **IGNORE** - Internal funtion for csv dump

        """         
        if client_id is None:
            client_id= self._use_default_client_id()[0]
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
  

    def remove_users(self,useruuid:str,client_id:int=None, csvdump:bool=False)->int:
        """
        Delete a user

        Args:
            useruuid:   User UUID
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv
        
        Return:
            Job Id

        Examples:
            >>> apiobj = self.{risksenseobject}.users.remove_users('123-456')

        Note:
            You can also dump the data of the group search in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.users.remove_users('123-456',csvdump=True) 
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "/client/{}/user/{}".format(str(client_id),useruuid)

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        user_profile = jsonified_response

        try:
            if csvdump==True:
                field_names = ['id']
                try:
                    with open('deleteuser.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow({'id': user_profile['id']})
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()

        return user_profile
   
    def get_user_iaminfo(self,useruuid:str,client_id:int=None, csvdump:bool=False)->dict:
        """
        Get IAM info of a user.

        Args:
            useruuid:   User UUID
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv
        
        Return:
            Json response

        Examples:
            >>> apiobj = self.{risksenseobject}.users.get_user_iaminfo('123-456')

        Note:
            You can also dump the data of the group search in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.users.get_user_iaminfo('123-456',csvdump=True) 
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "/client/{}/user/{}/iam".format(str(client_id),useruuid)

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        iam = jsonified_response
        
        try:
            if csvdump==True:
                field_names = ['Role Name', 'Role Expiration Date', 'Privilege Name', 'Privilege Active State']
                role_data = []
                privilege_data = []
                iam_data = []
                for item in iam['roles']:
                    role_data.append({'Role Name': item['name'], 'Role Expiration Date': item['expirationDate']})
                
                for item in iam['privileges']:
                    privilege_data.append({'Privilege Name': item['name'], 'Privilege Active State': item['active']})
                
                for ind,item in enumerate(role_data):
                    if ind <=len(privilege_data):
                        for key,value in privilege_data[ind].items():
                            item[key] = value
                        iam_data.append(item)
                    
                len_diff = len(role_data) - len(privilege_data)
                print(len_diff)    
                if len_diff < 0:
                    for item in privilege_data[len_diff:]:
                        item['Role Name'] = ''
                        item['Role Expiration Date'] = ''
                        iam_data.append(item)
                try:
                    with open('getuseriaminfo.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        for item in iam_data:
                            writer.writerow(item)
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()

        return iam


    
    def assign_group(self,filter:list,targetgroupids:list,client_id:int=None, csvdump:bool=False)->dict:
        """
        Assign users to groups.

        Args:
            filter:   Search Filter
            targetgroupids:   Target group ids
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv
        
        Return:
            Json response
        
        Examples:
            >>> apiobj = self.{risksenseobject}.users.assign_group([{"field":"id","exclusive":False,"operator":"EXACT","value":"6506","implicitFilters":[]}],[1234])

        Note:
            You can also dump the data of the group search in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.users.assign_group([{"field":"id","exclusive":False,"operator":"EXACT","value":"6506","implicitFilters":[]}],[1234],csvdump=True) 
        """
        if client_id is None:
            client_id = self._use_default_client_id()[1]

        url = self.api_base_url + "/client/{}/user/assign-group".format(str(client_id))

        body= {
                "filterRequest":{"filters": filter},
                "targetGroupIds": targetgroupids
                }
        
        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        try:
            if csvdump==True:
                self.downloadfilterinexport('userexport',filter)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()


        return jsonified_response

    def unassign_group(self,filter:list,targetgroupids:list,client_id:int=None, csvdump:bool=False)->dict:
        """
        Unassign users to groups.

        Args:
            filter:   Search Filter
            targetgroupids:   Target group ids
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv
        
        Return:
            Json response

        Examples:
            >>> apiobj = self.{risksenseobject}.users.unassign_group([{"field":"id","exclusive":False,"operator":"EXACT","value":"6506","implicitFilters":[]}],[1234])

        Note:
            You can also dump the data of the group search in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.users.unassign_group([{"field":"id","exclusive":False,"operator":"EXACT","value":"6506","implicitFilters":[]}],[1234],csvdump=True) 
        """
        if client_id is None:
            client_id = self._use_default_client_id()[1]

        url = self.api_base_url + "/client/{}/user/unassign-group".format(str(client_id))

        body= {
                "filterRequest": {"filters": filter},
                "targetGroupIds": targetgroupids
                }

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        try:
            if csvdump==True:
                self.downloadfilterinexport('userexport',filter)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()

        return jsonified_response

    def get_my_profile(self,csvdump:bool=False)->dict:

        """
        Get the profile for the user that owns the API key being used.

        Args:
            csvdump:             Toggle to dump data in csv

        Return:            
            A dictionary containing the user's profile.
        
        Examples:
            >>> apiobj = self.{risksenseobject}.users.get_my_profile()

        Note:
            You can also dump the data of the user profile in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.users.get_my_profile(csvdump=True) 
        """

        url = self.api_base_url + "user/profile"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        user_profile = jsonified_response
        if csvdump==True:
            field_names = []
            for item in user_profile.keys():
                field_names.append(item)
            try:
                with open('user_profile.csv', 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(user_profile)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        return user_profile

    def disallow_tokens(self, client_ids:list, user_id:int)->bool:
        """
        Disallow use of tokens for a user.

        Args:
            client_ids:  List of client Ids
            user_id:     The ID of the user to be disallowed from token use.
        
        Return:
            True/False indicating success or failure of submission of the operation.
        
        Examples:
            >>> apiobj = self.{risksenseobject}.users.disallow_tokens([123,456],1234)
        """
        client_ids = [str(x) for x in client_ids]
        client_ids = ",".join(client_ids)

        url = self.api_base_url + "/clients/user/" + str(user_id) + f"/tokenAllowed?clientIds={client_ids}"

        body = {
            "allowed": False
        }

        try:
            self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            success = True
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return success

    def allow_tokens(self, client_ids:list, user_id:int)->bool:

        """
        Allow use of tokens for a user.

        Args:
            client_ids:  List of client Ids
            user_id:     The ID of the user to be disallowed from token use.
        
        Return:
            True/False indicating success or failure of submission of the operation.
        
        Examples:
            >>> apiobj = self.{risksenseobject}.users.allow_tokens([123,456],1234)
        """
        client_ids = [str(x) for x in client_ids]
        client_ids = ",".join(client_ids)
        url = self.profile.platform_url + f"/api/v1/clients/user/{str(user_id)}" + f"/tokenAllowed?clientIds={client_ids}"
        
        body = {
            "allowed": True
        }

        try:
            response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            success = True
        except (RequestFailed,Exception) as e:
            print()
            print('There seems to be an exception')
            print(e)
            exit()

        return success

    def getexporttemplate(self,client_id:int=None)->list:
        
        """
        Gets configurable export template for application findings.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The Exportable fields

        Examples:
            >>> apiobj = self.{risksenseobject}.users.getexporttemplate()
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url+"client/{}/user/export/template".format(str(client_id))
        print(url)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
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
        Initiates an export job on the platform for user based on the
        provided filter(s).

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            file_name:       The name to be used for the exported file.
            row_count:       No of rows to be exported. Possible options :
                ExportRowNumbers.ROW_5000,
                ExportRowNumbers.ROW_10000,
                ExportRowNumbers.ROW_25000,
                ExportRowNumbers.ROW_50000,
                ExportRowNumbers.ROW_100000,
                ExportRowNumbers.ROW_ALL
            file_type:       File type to export.  ExportFileType.CSV, ExportFileType.XML, or ExportFileType.XLSX
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The job ID in the platform from is returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.users.export([{"field":"id","exclusive":False,"operator":"EXACT","value":"6506","implicitFilters":[]}])
        """
        func_args = locals()
        func_args['exportable_filter']=self.getexporttemplate()
        func_args.pop('self')
        print(func_args)
        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]
        try:
            export_id = self._export(self.subject_name, **func_args)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return export_id

    def get_single_search_page(self, search_filters:list, page_num:int=0, page_size:int=150,
                               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC, client_id:int=None)->dict:
        """
        Searches for and returns users based on the provided filter(s) and other parameters.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            page_num:        Page number of results to be returned.
            page_size:       Number of results to be returned per page.
            sort_field:      Name of field to sort results on.
            sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Paginated JSON response from the platform.

        Examples:
            >>> apiobj = self.{risksenseobject}.users.get_single_search_page([{"field":"id","exclusive":False,"operator":"EXACT","value":"6506","implicitFilters":[]}])
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user/search".format(str(client_id))

        body = {
            "filters": search_filters,
            "projection": Projection.BASIC,
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

    def search(self, search_filters:list, page_size:int=150, sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC,csvdump:bool=False, client_id:int=None)->list:

        """
        Searches for and returns users based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            page_size:       The number of results per page to be returned.
            sort_field:      Name of field to sort results on.
            sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC
            csvdump:             Toggle to dump data in csv
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            A list containing all hosts returned by the search using the filter provided.

        Examples:
            >>> apiobj = self.{risksenseobject}.users.search([{"field":"id","exclusive":False,"operator":"EXACT","value":"6506","implicitFilters":[]}])

        Note:
            You can also dump the data of the users in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.users.search([{"field":"id","exclusive":False,"operator":"EXACT","value":"6506","implicitFilters":[]}],csvdump=True) 
        """

        func_args = locals()
        func_args.pop('self')
        all_results = []
        func_args.pop('csvdump')

        if client_id is None:
            client_id = self._use_default_client_id()[0]
            func_args['client_id']=self._use_default_client_id()[0]

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            page_info = self._get_page_info(self.subject_name, search_filters, page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        if csvdump==True:
            self.downloadfilterinexport('userexport',search_filters)
        return all_results
    
    def list_user_filter_fields(self,client_id:int=None)->dict:
        """
        List filter endpoints.

        Args:
            filter_subject:  Supported Subjects are: 
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The JSON output from the platform is returned, listing the available filters.

        Examples:
            >>> apiobj = self.{risksenseobject}.users.list_user_filter_fields()
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



    def get_user_info(self, user_id:int=None, client_id:int=None,csvdump:bool=False)->dict:
        """
        Get info for a specific user.  If user_id is not specified, the info for the requesting user is returned.

        Args:
            user_id:     User ID
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv
        
        Return:
            User information.

        Examples:
            >>> apiobj = self.{risksenseobject}.users.get_user_info(1234)

        Note:
            You can also dump the data of the user information in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.users.get_user_info(1234,csvdump=True) 
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        params = {}

        url = self.api_base_url + "/user"

        if user_id is not None:
            params.update({"userId": user_id})

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        try:
            if csvdump==True:
                field_names = []
                for item in jsonified_response.keys():
                    field_names.append(item)
                try:
                    with open('userinfo.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow(jsonified_response)
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()

        return jsonified_response

    def create(self, username:str, first_name:str, last_name:str, email_address:str,
                group_ids:list=[], client_id:int=None, read_only:bool=False,csvdump=False, **kwargs)->int:
        """
        Create a new user.

        Args:
            username:        Username
            first_name:      First Name
            last_name:       Last Name
            email_address:   E-mail address
            group_ids:       Group IDs to assign user to
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            read_only:       Read only
            csvdump:             Toggle to dump data in csv

        Keyword Args:
            use_saml (``bool``):      Is a SAML user?
            saml_attr_1 (``str``):   SAML Attribute 1
            saml_attr_2 (``str``):   SAML Attribute 2
            exp_date (``str``):      Expiration Date YYYY-MM-DD

        Return:
            Job ID

        Examples:
            >>> apiobj = self.{risksenseobject}.users.create('test', 'test', 'test', 'abc@xyz.com')

        Note:
            You can also dump the data of the user job id in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.users.create('test', 'test', 'test', 'abc@xyz.com',csvdump=True) 
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user".format(str(client_id))

        use_saml = kwargs.get("use_saml", None)
        saml_attr_1 = kwargs.get("saml_attr_l", None)
        saml_attr_2 = kwargs.get("saml_attr_2", None)
        exp_date = kwargs.get("exp_date", None)

        body = {
            "username": username,
            "firstName": first_name,
            "lastName": last_name,
            "email": email_address,
            "readOnly": read_only,
            "groupIds": group_ids,
            "useSamlAuthentication": use_saml,
            "samlAttribute1": saml_attr_1,
            "samlAttribute2": saml_attr_2,
            "expirationDate": exp_date
        }

        body = self._strip_nones_from_dict(body)

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        if raw_response.status_code==201:
            jsonified_response = json.loads(raw_response.text)
            user_id = jsonified_response['id']

        try:
            if csvdump==True:
                field_names = ['id']
                try:
                    with open('usercreate.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow({'id': user_id})
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()

        return user_id

    def update_user_role(self,newrole:str,newexpiration:datetime,user_uuid:str, client_id:int=None, csvdump:bool=False)->dict:

        """
        Update user role.

        Args:
            newrole:            New User role id
            newexpiration:      Expiration date. Allowed format : "YYYY-MM-DDTHH:MM:SSZ"(eg: 2020-12-31T00:00:00.000Z)
            user_uuid:   User UUID
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv
        
        Return:
            Roles JSON

        Examples:
            >>> apiobj = self.{risksenseobject}.users.update_user_role('test','2020-12-31T00:00:00.000Z','123-456')

        Note:
            You can also dump the data of the user profile in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.users.update_user_role('test','2020-12-31T00:00:00.000Z','123-456',csvdump=True) 
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()


        try:
            iam_response = self.get_user_iaminfo(useruuid=user_uuid, client_id=client_id)
            roles = []
            for item in iam_response['roles']:
                roles.append({'clientId':client_id,'role':item['id'],'expirationDate':item['expirationDate']})
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        print(roles)
        exit()
        url = self.api_base_url + "client/{}/user/{}/role".format(str(client_id),user_uuid)
        roles.append({'clientId':client_id,"role": newrole,"expirationDate": newexpiration})
        body = {
                "roles": roles
                }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        updated_roles = jsonified_response['roles']

        try:
            if csvdump==True:
                field_names = []
                for item in updated_roles:
                    for key in item:
                        if key not in field_names:
                            field_names.append(key)
                
                try:
                    with open('updateuserrole.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        for item in updated_roles:
                            writer.writerow(item)
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()

        return updated_roles

    def update_user(self, user_uuid:str, client_id:int=None,csvdump:bool=False, **kwargs)->int:
        """
        Update a user.

        Args:
            user_uuid:   User UUID
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv
        
        Keyword Args:
            username (``str``):      Username
            first_name (``str``):    First Name
            last_name (``str``):     Last Name
            email (``str``):         Email
            phone (``str``):         Phone Num.
            group_ids (``list``):     Group IDs
            read_only (``bool``):     Read-Only
            use_saml (``bool``):      Use SAML?
            saml_attr_1 (``str``):   SAML Attribute 1
            saml_attr_2 (``str``):   SAML Attribute 2 
            exp_date (``str``):      Expiration Date YYYY-MM-DD

        Return:
            Job ID

        Examples:
            >>> apiobj = self.{risksenseobject}.users.update_user('123-456',username='test',first_name='test')

        Note:
            You can also dump the data of the user in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.users.update_user('123-456',username='test',first_name='test',csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user/{}".format(str(client_id), user_uuid)

        username = kwargs.get("username", None)
        first_name = kwargs.get("firstName", None)
        last_name = kwargs.get("lastName", None)
        email_address = kwargs.get("email", None)
        phone_num = kwargs.get("phone", None)
        group_ids = kwargs.get("group_ids", None)
        read_only = kwargs.get("read_only", None)
        use_saml = kwargs.get("use_saml", None)
        saml_attr_1 = kwargs.get("saml_attr_l", None)
        saml_attr_2 = kwargs.get("saml_attr_2", None)
        exp_date = kwargs.get("exp_date", None)

        body = {
            "username": username,
            "firstName": first_name,
            "lastName": last_name,
            "email": email_address,
            "phone": phone_num,
            "groupIds": group_ids,
            "readOnly": read_only,
            "useSamlAuthentication": use_saml,
            "samlAttribute1": saml_attr_1,
            "samlAttribute2": saml_attr_2,
            "expirationDate": exp_date
        }

        body = self._strip_nones_from_dict(body)

        if body == {}:
            raise ValueError("No new valid user properties provided.")

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        try:
            if csvdump==True:
                field_names = ['id']
                try:
                    with open('updateuser.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow({'id': job_id})
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()


        return job_id

    def send_welcome_email(self, search_filter:list, client_id:int=None)->int:
        """
        Send welcome e-mail to users identified by the search filter(s) provided.

        Args:
            search_filter:      A list of dictionaries containing filter parameters.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Job ID

        Examples:
            >>> apiobj = self.{risksenseobject}.users.send_welcome_email([{"field":"id","exclusive":False,"operator":"EXACT","value":"6506","implicitFilters":[]}])
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user/sendWelcomeEmail".format(str(client_id))

        body = {
            "filterRequest": {
                "filters": search_filter
            }
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def get_roles(self, client_id:int=None)->dict:
        """
        Get roles

        Args:
            search_filter:   A list of dictionaries containing filter parameters.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Job ID

        Examples:
            >>> apiobj = self.{risksenseobject}.users.get_roles()
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        roleurl=self.api_base_url + "client/{}/role?page=0&size=500".format(str(client_id))
        try:
            roles = self.request_handler.make_request(ApiRequestHandler.GET, roleurl)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        jsonified_response = json.loads(roles.text)
        
        return jsonified_response

    def assign_clients(self,searchfilter:list,expirationdate:str,replacexistingroles:bool=False,assignallgroups:bool=False, client_id:int=None,client_idtouse:int=None)->int:
        """
        Assign user to clients

        Args:
            searchfilter:   A list of dictionaries containing filter parameters.
            expirationdate:     Expiration date. YYYY-mm-dd
            replacexistingroles:  Replace existing roles
            assignallgroups     : Assign all groups
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            client_idtouse:     Client Id to use

        Return:
            Job ID

        Examples:
            >>> apiobj = self.{risksenseobject}.users.assign_clients([{"field":"id","exclusive":False,"operator":"EXACT","value":"6506","implicitFilters":[]}],'2022-01-01',client_idtouse=111)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        roleurl=self.api_base_url + "client/{}/role?page=0&size=500".format(str(client_id))
        try:
            roles = self.request_handler.make_request(ApiRequestHandler.GET, roleurl)
            roles=json.loads(roles.text)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        for i in range(len(roles['_embedded']['roles'])):
            print(f'Index No:{i},Name:{roles["_embedded"]["roles"][i]["name"]}')
        inputsofroles=[roles["_embedded"]["roles"][int(i)]["id"] for i in input('Please enter the indexes of the roles that you want you want the user to have:').split(',')]  

        body = {"filterRequest":{"filters":searchfilter},"roles":inputsofroles,"replaceExistingRoles":replacexistingroles,"expirationDate":f"{expirationdate}T00:00:00.000Z","assignAllGroups":assignallgroups}

        url = self.api_base_url + "client/{}/assignUsers".format(str(client_idtouse))


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def assign_roles(self,userid:int,expirationdate:str=None,replacexistingroles:bool=False,assignallgroups:bool=False, client_id:int=None,client_idtouse:int=None)->dict:
        """
        Assign roles to user

        Args:
            userid:     User Id
            expirationdate:     Expiration date. YYYY-mm-dd
            replacexistingroles:  Replace existing roles
            assignallgroups     : Assign all groups
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            client_idtouse:     Client Id to use

        Return:
            Job ID

        Examples:
            >>> apiobj = self.{risksenseobject}.users.assign_roles(123,'2022-01-01',client_idtouse=111)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        if client_idtouse is None:
            client_idtouse=client_id
        
        uuid=self.get_user_info(user_id=userid)['uuid']

        getroles=self.get_user_iaminfo(client_id=client_idtouse,useruuid=uuid)
 
        existingrole=getroles['roles']
        newroleaddition=[]


        roles=self.get_roles(client_id=client_idtouse)

        for i in range(len(roles['_embedded']['roles'])):
            print(f'Index No:{i},Name:{roles["_embedded"]["roles"][i]["name"]}')
        inputsofroles=roles["_embedded"]["roles"][int(input('Please enter the index of the roles that you want you want the user to have:'))]["id"]

        for i in range(len(existingrole)): 
            temp={}
            temp['client_id']=client_idtouse
            temp['role']=existingrole[i]['id']
            temp['expirationDate']=existingrole[i]['expirationDate']
            newroleaddition.append(temp)
    
        newroleaddition.append({"client_id":client_idtouse,"role":inputsofroles,"expirationDate":expirationdate})

        body={"roles":newroleaddition}



        url = self.api_base_url + "client/{}/user/{}/role".format(str(client_idtouse),uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def remove_roles(self,userid:int,client_idtouse:int=None, client_id:int=None)->dict:
        """
        Remove roles to user

        Args:
            userid:     User Id
            client_idtouse:     Client Id to use
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            Job ID

        Examples:
            >>> apiobj = self.{risksenseobject}.users.remove_roles(123,client_idtouse=111)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        uuid=self.get_user_info(user_id=userid)['uuid']

        getroles=self.get_user_iaminfo(client_id=client_idtouse,useruuid=uuid)
 
        existingrole=getroles['roles']
        newroleadditon=[]
        for i in range(len(existingrole)):
            print(f'Index No:{i},Name:{existingrole[i]["name"]}')
        
        existingrole.remove(existingrole[int(input('Which role would you like to delete, please enter the index number'))])
    
        print(existingrole)

        for i in range(len(existingrole)): 
            temp={}
            temp['role']=existingrole[i]['id']
            temp['expirationDate']=existingrole[i]['expirationDate']
            newroleadditon.append(temp)
        print(newroleadditon)
        body={"roles":newroleadditon}

        url = self.api_base_url + "client/{}/user/{}/role".format(str(client_idtouse),uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def clientrolefiltering(self,client_ids:list=None,rolelabels:list=None,client_id:int=None)->dict:
        """
        Client role filtering

        Args:
            client_ids:   Client Ids
            rolelabels:   Role Labels
            client_id:    Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Job ID

        Examples:
            >>> apiobj = self.{risksenseobject}.users.clientrolefiltering(client_ids=[123,12],rolelabels=['abc'])
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        

        body={"client_ids":client_ids,"clientNames":[],"roleLabels":rolelabels}

        url = self.api_base_url + f"clients/usersByRole/search?client_ids={','.join([str(i) for i in client_ids ])}"
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response


    def get_model(self, client_id:int=None)->dict:
        """
        Get available projections and models for Users.

        Args:
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Users projections and models are returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.users.get_model()
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return response

    def suggest(self, search_filter:list, suggest_filter:dict, client_id:int=None)->dict:
        """
        Suggest values for filter fields.

        Args:
            search_filter:     Search Filter
            suggest_filter:    Suggest Filter
            client_id:         Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Value suggestions

        Examples:
            >>> apiobj = self.{risksenseobject}.users.suggest([],{"field":"id","exclusive":False,"operator":"WILDCARD","value":"65*","implicitFilters":[]})
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._suggest(self.subject_name, search_filter, suggest_filter, client_id)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return response

    def import_users_csv(self, file_name:str, absolute_path_file:str, client_id:int=None)->dict:
        """
        Add a file to an upload.

        Args:
            file_name:   The name to be used for the uploaded file.
            absolute_path_file:   Absolute path of the file to be uploaded
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The file ID is returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.users.import_users_csv('test','C:\\test.csv')
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user/importUsersCsv".format(str(client_id))
        upload_file = {'csvUsers': (file_name, open(absolute_path_file, 'rb'))}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=upload_file)
        except (RequestFailed,Exception) as e:
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



    ##  PRIVATE FUNCTIONS   ##

    def systemuser_get_single_search_page(self, search_filters:list, page_num:int=0, page_size:int=150,
                               sort_field:str="username", sort_dir:str=SortDirection.DESC, client_id:int=None)->dict:
        """
        Searches for and returns users based on the provided filter(s) and other parameters.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            page_num:        Page number of results to be returned.
            page_size:       Number of results to be returned per page.
            sort_field:      Name of field to sort results on.
            sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Paginated JSON response from the platform.

        Examples:
            >>> apiobj = self.{risksenseobject}.users.systemuser_get_single_search_page([{"field":"id","exclusive":False,"operator":"EXACT","value":"6506","implicitFilters":[]}])
        """

        if client_id is None:
            client_id = self._use_default_client_id()[1]
        url = self.api_base_url + "clients/systemUser/search?client_ids={}".format(str(client_id))
        print(url)
        body = {
            "filters": search_filters,
            "projection": "internal",
            "sort": [
                {
                    "field": sort_field,
                    "direction": sort_dir
                }
            ],
            "page": page_num,
            "size": page_size
        }
        
        jsonified_response = json.loads(raw_response.text)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

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
