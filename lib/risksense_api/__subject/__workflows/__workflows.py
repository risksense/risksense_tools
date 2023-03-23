"""
**Workflows module defined for different workflows related api endpoints.**
"""
""" *******************************************************************************************************************
|
|  Name        :  __workflows.py
|  Description :  Create functions for various utilities of the workflow endpoints
|  Project     :  risksense_api
|  Copyright   :  2022 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
from pickle import NONE
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ..__exports import Exports
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
import datetime
import csv
import pandas as pd

class Workflows(Subject):

    """ **Class for Worflow function defintions**.

    To utlise workflow function:

    Args:
            profile:     Profile Object
    
    Usage:
        :obj:`self.{risksenseobjectname}.workflows.{function}`
    
    Examples:
        To get model for workflow using :meth:`get_model()` function

        >>> self.{risksenseobject}.workflows.get_model()

    """

    class OverrideControl:

        NONE = "NONE"
        AUTHORIZED = "AUTHORIZED"
    
    class Workflowtype:

        FALSEPOSITIVE = "falsePositive"
        REMEDIATION = "remediation"
        ACCEPTANCE= "acceptance"
        SEVERITYCHANGE="severityChange"
    


    def __init__(self, profile:object):

        """
        Initialization of Workflows object.

        Args:
            profile:     Profile Object
        """

        self.subject_name = "workflowBatch"
        Subject.__init__(self, profile, self.subject_name)

    def search(self, search_filters:list, projection:str=Projection.BASIC, page_size:int=150,
               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC ,csvdump:bool=False,client_id:int=None)->list:

        """
        Searches for and returns workflows based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.
        
        Args:
            search_filters:  A list of dictionaries containing filter parameters.

            projection:      Projection to be used in API request.  Projection.BASIC or Projection.DETAIL

            page_size:       The number of results per page to be returned.

            sort_field:      The field to be used for sorting results returned.

            sort_dir:        The direction of sorting to be used. SortDirection.ASC or SortDirection.DESC

            csvdump:         dumps the data in csv

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            A list containing all workflows returned by the search using the filter provided.

        Example:
            An example to search for workflow data is
            
            >>> self.{risksenseobject}.workflow.search([])

        Note:
            You can also dump the search based data in a csv by simply providing :obj:`csvdump=True` argument

            >>> self.{risksenseobject}.workflow.search([],csvdump=True)
        """
        csvdumpval=csvdump

        func_args = locals()
        func_args.pop('self')
        func_args.pop('csvdumpval')
        func_args.pop('csvdump')
        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        page_info = self._get_page_info(self.subject_name, search_filters, page_size=page_size, client_id=client_id)
        num_pages = page_info[1]
        page_range = range(0, num_pages)

        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed, Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()
        try:
            if csvdumpval==True:
                newdump=[]
                for i in all_results:
                    temp={}
                    for key,value in i.items():
                        temp[key]=value
                        if key=='affectedAssets':
                            temp['affectedAssets']=value['value']
                        if key=='affectedFindings':
                            temp['affectedFindings']=value['value']
                        if key=='currentUser':
                            temp['currentuser_username']=value['username']
                            temp['currentuser_firstname']=value['firstName']
                            temp['currentuser_lastname']=value['lastName']
                            temp.pop('currentUser')
                        if key=='filter':
                            temp.pop('filter')
                    newdump.append(temp)
                field_names = []     
                for item in newdump[0]:
                    field_names.append(item)
                try:
                    with open('workflow_batch.csv', 'w') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        for item in newdump:
                            writer.writerow(item)
                except (FileNotFoundError,Exception) as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except (FileNotFoundError,Exception) as fnfe:
                    print("An exception has occurred")
                    print()
                    print(fnfe)
        return all_results

    def list_workflowbatch_model(self,client_id:int=None)->dict:

        """
        Get available projections and models for Workflowbatch.
        
        Args:
            client_id:   Client ID
        Return:
           Workflow batch models and projections
        Example:
            An example to use get_model is
           
                >>> self.{risksenseobject}.workflowbatch.get_model()
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/model'
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)

        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def getexporttemplate(self,client_id:int=None)->list:

        """
        Gets configurable export template for workflows.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The Exportable fields

        Example:
            An example to use getexporttemplate
                
            >>> self.{risksenseobject}.workflows.getexporttemplate()

            This gets all the export templates for workflows
    
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/export/template"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error getting export template')
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
        Initiates an export job on the platform for workflow(s) based on the
        provided filter(s), by default fetches all the columns data.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.

            file_name:       The name to be used for the exported file.

            row_count:      No of rows to be exported. Available options
                            ExportRowNumbers.ROW_10000,
                            ExportRowNumbers.ROW_25000,
                            ExportRowNumbers.ROW_50000,
                            ExportRowNumbers.ROW_100000,
                            ExportRowNumbers.ROW_ALL

            file_type:       File type to export. ExportFileType.CSV, ExportFileType.JSON,  or ExportFileType.XLSX

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The job ID in the platform from is returned.

        Example:
            An example to use export is
            
                >>> self.{risksenseobject}.workflows.export([],'testingexport')
            
            You can change the filetype to any of the names above or even the other positional arguments as mentioned

                >>> self.{risksenseobject}.workflows.export([],'testingexport',file_type=ExportFileType.JSON)
        """
        func_args = locals()
        func_args['exportable_filter']=self.getexporttemplate()
        func_args.pop('self')
        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]
        try:
            export_id = self._export(self.subject_name, **func_args)

        except (RequestFailed,Exception) as e:
            print('There was an error performing export job')
            print(e)
            exit()
        return export_id

    def list_workflowbatch_filter_fields(self,client_id:int=None)->dict:

        """
        List filter endpoints for workflow batch.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The JSON output from the platform is returned, listing the available filters.
        Examples:
            
            >>>  self.{risksenseobject}.workflows.list_workflowbatch_filter_fields()
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

    def get_single_search_page(self, search_filters:list, projection:str=Projection.BASIC, page_num:int=0, page_size:int=150,
                               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC, client_id:int=None)->dict:

        """
        Searches for and returns workflows based on the provided filter(s) and other parameters.
        
        Args:
            search_filters:  A list of dictionaries containing filter parameters.

            projection:      Projection to be used in API request.  Projection.BASIC or Projection.DETAIL

            page_num:        The page number of results to be returned.

            page_size:       The number of results per page to be returned.

            sort_field:      The field to be used for sorting results returned.

            sort_dir:        The direction of sorting to be used. SortDirection.ASC or SortDirection.DESC

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The JSON response from the platform is returned.
        Example:
            An example to get single search page of workflows data
            
            >>> self.{risksenseobject}.workflows.get_single_search_page([])

            You can also try changing the other arguments to your liking to reflect the data as you suffice such as change page_size or page_num etc.

            >>> self.{risksenseobject}.workflows.get_single_search_page([],page_num=2,page_size=10)
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
            print('Error in getting workflow details')
            print()
            print(e)
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

        
        """
        Get available projections and models for Workflows.
        
        Args:
            client_id:   Client ID

        Return:
            Workflows projections and models are returned.
        
        Example:
            An example to use get_model is
           
                >>> self.{risksenseobject}.workflows.get_model()

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
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

            >>> self.{risksenseobject}.workflows.suggest([],{})
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._suggest(self.subject_name, search_filter_1, search_filter_2, client_id)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        return response


    def request_acceptance(self, search_filter:list, workflow_name:str, description:str, reason:str,finding_type:str,expiration_date:str=None,override_control:str=OverrideControl.AUTHORIZED, compensating_controls:str="NONE", attachment:str=None, client_id:int=None)->bool:

        """
        Request acceptance for applicationFindings / hostFindings as defined in the filter_request parameter.

        Args:

            search_filter:           A list of dictionaries containing filter parameters.

            workflow_name:           Workflow Name

            description:             A description of the request.

            reason:                  A reason for the request.

            finding_type:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.

            override_control:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')

            compensating_controls:   A description of compensating controls applied to this finding. Option available : ("DLP", "Deemed not exploitable", "Endpoint Security", "IDS/IPS", "MFA Enforced", "Multiple: See Description", "Network Firewall", "Network Segmentation", "Other: See Description", "Web Application Firewall" or "NONE")

            attachment:              A path to a file to be uploaded and attached to the request.

            client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            Success whether request occured
        Example:
            To create request acceptance for findings for hostfindings

            >>> self.rs.workflows.request_acceptance([],'testingforsomething','something','none',"hostFinding","2022-08-11")
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/acceptance/request"
        print(url)
        body = {"subject": finding_type, 
            "filterRequest": {
                "filters": search_filter
                }
            }
        multiform_data = {
            "name": (None,workflow_name),
            "subjectFilterRequest": (None,json.dumps(body)),
            "description": (None,description),
            "reason": (None,reason),
            "overrideControl": (None,override_control),
            "compensatingControls": (None,compensating_controls),
            "files": attachment,
            "expirationDate": (None,expiration_date),
            "isEmptyWorkflow":(None,"false")
            }

        body = self._strip_nones_from_dict(body)
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==201:
                success=True
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        return success


    def request_false_positive(self, finding_type:str, search_filter:list, workflow_name:str, description:str, reason:str, override_control:str=OverrideControl.AUTHORIZED, expiration_date:str=None, attachment:str=None, client_id:int=None)->bool:

        """
        Request false positive for applicationFindings / hostFindings as defined in the filter_request parameter.

        Args:
            finding_type:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            search_filter:           A list of dictionaries containing filter parameters.

            workflow_name:           Workflow Name

            description:             A description of the request.

            reason:                  A reason for the request.

            override_control:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')

            expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.

            attachment:              A path to a file to be uploaded and attached to the request.

            client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            Success whether request occured
        Example:
            To create request false positive for findings for hostfindings

            >>> self.rs.workflows.request_false_positive("hostFinding",[],'testingforsomething','something','none',"2022-08-11")
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/request"

        body = {"subject": finding_type, 
            "filterRequest": {
                "filters": search_filter
                }
            }
        multiform_data = {
            "name": (None,workflow_name),
            "subjectFilterRequest": (None,json.dumps(body)),
            "description": (None,description),
            "reason": (None,reason),
            "overrideControl": (None,override_control),
            "files": attachment,
            "expirationDate": (None,expiration_date),
            "isEmptyWorkflow":(None,"false")
            }

        body = self._strip_nones_from_dict(body)

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==201:
                success=True
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        return success


    def request_remediation(self, finding_type:str, search_filter:list, workflow_name:str, description:str, reason:str, override_control:str=OverrideControl.AUTHORIZED, expiration_date:str=None, attachment:str=None, client_id:int=None)->bool:

        """
        Request remediation for applicationFindings / hostFindings as defined in the filter_request parameter.

        Args:
            finding_type:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            search_filter:           A list of dictionaries containing filter parameters.

            workflow_name:           Workflow Name

            description:             A description of the request.

            reason:                  A reason for the request.

            override_control:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')

            expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.

            attachment:              A path to a file to be uploaded and attached to the request.

            client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            Success whether request occured
        Example:
            To create request remediation for findings for hostfindings

            >>> self.rs.workflows.request_remediation("hostFinding",[],'testingforsomething','something','none',"2022-08-11")
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/remediation/request"

        body = {"subject": finding_type, 
            "filterRequest": {
                "filters": search_filter
                }
            }
        multiform_data = {
            "name": (None,workflow_name),
            "subjectFilterRequest": (None,json.dumps(body)),
            "description": (None,description),
            "reason": (None,reason),
            "overrideControl": (None,override_control),
            "files": attachment,
            "expirationDate": (None,expiration_date),
            "isEmptyWorkflow":(None,"false")
            }

        body = self._strip_nones_from_dict(body)

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==201:
                success=True
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        return success

    def request_severity_change(self, finding_type:str, search_filter:list, workflow_name:str, description:str, reason:str,  severity_change:str,override_control:str=OverrideControl.AUTHORIZED, expiration_date:str=None, attachment:str=None, client_id:int=None)->bool:

        """
        Request severity change for applicationFindings / hostFindings as defined in the filter_request parameter.

        Args:
            finding_type:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            search_filter:           A list of dictionaries containing filter parameters.

            workflow_name:           Workflow Name

            description:             A description of the request.

            reason:                  A reason for the request.

            severity_change:        Severity change value.

            override_control:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')

            compensating_controls:   Severity change for this finding. Option available : ("1" to "10")

            expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.

            attachment:              A path to a file to be uploaded and attached to the request.

            client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            Success whether request occured
        Example:
            To create request severity change for findings for hostfindings

            >>> self.rs.workflows.request_false_positive("hostFinding",[],'testingforsomething','something','4','none',"2022-08-11")
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/severityChange/request"

        body = {"subject": finding_type, 
            "filterRequest": {
                "filters": search_filter
                }
            }

        multiform_data = {
            "name": (None,workflow_name),
            "subjectFilterRequest": (None,json.dumps(body)),
            "description": (None,description),
            "reason": (None,reason),
            "overrideControl": (None,override_control),
            "severity": (None,severity_change),
            "files": attachment,
            "expirationDate": (None,expiration_date),
            "isEmptyWorkflow":(None,"false")
            }
        

        body = self._strip_nones_from_dict(body)

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==201:
                success=True
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        return success

    def reject_workflow(self, filter_request:list,workflowtype:str, description:str,csvdump:bool=False, client_id:int=None)->int:

        """
        Reject a workflow request.

        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            description:         A description of the rejection.

            workflowtype: Type of workflow

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
           The job ID from the platform is returned.
        Example:
            To perform a reject acceptance request for a workflow filter RA#0000028
            
            >>>  self.rs.workflows.reject_workflow([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RA#0000028"}],'acceptance','needed to test')
        Note:
            You can also dump the job id in a csv using:obj:`csvdump=True` argument

              >>>  self.rs.workflows.reject_workflow([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RA#0000028"}],'acceptance','needed to test',csvdump=True)

            
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + f"/{workflowtype}/reject"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('rejectworkflow.csv',index=False)

        return job_id

    def rework_workflow(self, filter_request:list,workflow_type:str, description:str,csvdump:bool=False, client_id:int=None)->int:

        """
        Request a rework of a workflow.
        
        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            description:         A description of the rework.

            csvdump:         dumps the data in csv

            workflow_type: Type of workflow

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
           The job ID from the platform is returned.
        Example:
            To rework an acceptance request RA#0000027

            >>> self.rs.workflows.rework_workflow([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RA#0000027"}],'acceptance','needed to test')
        Note:
            You can also dump the job id in a csv using:obj:`csvdump=True` argument

             >>> self.rs.workflows.rework_workflow([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RA#0000027"}],'acceptance','needed to test',csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + f"/{workflow_type}/rework"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('reworkworkflow.csv',index=False)

        return job_id

    def approve_workflow(self, filter_request:list,workflowtype:str,override_exp_date:bool=False,
                           expiration_date:str=(datetime.date.today() + datetime.timedelta(days=14)),csvdump:bool=False, client_id:int=None,**kwargs)->int:

        """
        Approve a workflow request.

        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            workflowtype: Type of workflow

            override_exp_date:   True/False indicating whether or not an expiration date should be overridden.

            expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          The job ID from the platform is returned.
        Example:
            To approve an acceptance request RA#0000028

            >>> self.rs.workflows.approve_acceptance([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RA#0000028"}],'acceptance')
        Note:
            You can also dump the job id in a csv using:obj:`csvdump=True` argument

            >>> self.rs.workflows.approve_acceptance([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RA#0000028"}],'acceptance',csvdump=True)

        """
       
        try:

            if client_id is None:
                client_id = self._use_default_client_id()[0]

            search_response = self.get_single_search_page(filter_request)
            
            uuid = search_response['_embedded']['workflowBatches'][0]['uuid']
            url = self.api_base_url.format(str(client_id)) + f"/{workflowtype}/approve"

            body = {
                "workflowBatchUuid": uuid,
                "expirationDate": str(expiration_date),
                "overrideExpirationDate": override_exp_date
            }
            if type(csvdump)!=bool:
                print('Error in csvdump value,Please provide either true or false')
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            jsonified_response = json.loads(raw_response.text)
            job_id = jsonified_response['id']
            if csvdump==True:
                workflowid={'jobid':[jsonified_response['id']]}
                df = pd.DataFrame(workflowid)
                df.to_csv('approveworkflow.csv',index=False)
            return job_id
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

    def update_workflow(self,workflowBatchUuid:str,workflowtype:str,name:str,expirationDate:str,description:str,reason:str,compensatingControl:str,overrideControl:str=OverrideControl.AUTHORIZED,csvdump:bool=False, client_id:int=None,**kwargs)->dict:

        #acceptance,falsePositive,severityChange,remediation
        """
        Update a  workflow.

        Args:

            workflowBatchUuid:      Workflow UUID

            workflowtype: Type of workflow

            name:      Workflow name

            expirationDate:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.

            description:         A description of the rejection.

            reason:         A reason for the rejection.

            compensatingControl:   A description of compensating controls applied to this finding. Option available : ("DLP", "Deemed not exploitable", "Endpoint Security", "IDS/IPS", "MFA Enforced", "Multiple: See Description", "Network Firewall", "Network Segmentation", "Other: See Description", "Web Application Firewall" or "NONE")

            overrideControl:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Keyword Args:
            severity(``severity``): The severity number
        Return:
           The jsonified response.
        Example:
            To Update a false positive workflow of uuid 11ed0429-4937-f454-b7ab-06933745a4d6

            >>> self.rs.workflows.update_workflow("11ed0429-4937-f454-b7ab-06933745a4d6","testin","2022-07-31","testingforupdate",'falsePositive',"testing","NONE")

        Note:
            You can also dump the search based data in a csv by simply providing :obj:`csvdump=True` argument

            >>> self.rs.workflows.update_workflow("11ed0429-4937-f454-b7ab-06933745a4d6","testin","2022-07-31","testingforupdate",'falsePositive',"testing","NONE",csvdump=True)
        
        """
        severity = kwargs.get("severity", None)

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/falsePositive/update/"

        body = {"workflowBatchUuid":workflowBatchUuid,"name": name,"expirationDate":expirationDate,"description":description,"reason":reason,"severity":severity,"compensatingControl":compensatingControl,"overrideControl":overrideControl}

        body = self._strip_nones_from_dict(body)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('updateworkflow.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        
        return jsonified_response

    def map_findings(self,subject:str, filter_request:list,workflowuuid:str,workflowtype:str, client_id:int=None)->bool:

        """
        Map findings to a workflow for applicationFindings / hostFindings as defined in the filter_request parameter.

        Args:
            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            filter_request:           A list of dictionaries containing filter parameters.

            workflowuuid:           Workflow Name
            
            workflowtype:             Workflow type

            client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
             Success whether request occured
        Example:
            To map acceptance workflow to findings
            
            >>> self.rs.workflows.map_findings_acceptance("hostFinding",[{"field":"id","exclusive":False,"operator":"IN","value":"235141285"}],'acceptance',"11ed123b-9d8f-a2f1-b7ab-06933745a4d6")
        
        """

        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/map'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success

    def unmap_findings(self, subject:str,filter_request:list,workflowuuid:str,workflowtype:str,client_id:int=None)->bool:

        """
        Unmap findings to a workflow for applicationFindings / hostFindings as defined in the filter_request parameter.

        Args:
            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            filter_request:           A list of dictionaries containing filter parameters.

            workflowuuid:           Workflow Name

            workflowtype:           Workflow type

            client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether request occured
        Example:
            To unmap findings to acceptance workflow

            >>> self.rs.workflows.unmap_findings('hostFinding',[{"field":"id","exclusive":False,"operator":"IN","value":"232927123,178257910"}],'11ed0429-4937-f454-b7ab-06933745a4d6','acceptance')
        
        """
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/unmap'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                    success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success

    def get_attachments(self, workflowbatchuuid:str,workflowtype:str, subject:str, client_id:int=None):

        """
        Get attachments from an acceptance workflow

        Args:
            workflowbatchuuid:  Workflowbatch uuid

            subject:     Subject whether hostFinding or applicationFinding

            workflowtype: Type of workflow

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Example:
            To use attachment function
            
            >>> self.rs.workflows.get_attachments_acceptance('11ed0429-4937-f454-b7ab-06933745a4d6','hostFinding')

        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/{}/{}/attachments'.format(str(client_id),subject,workflowtype,workflowbatchuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print()
            print(e)
        jsonified_response = raw_response.text

        return jsonified_response

    def download_workflowbatch_attachments(self, fileuuid:str,subject:str,workflowtype:str,workflowcategory:str='CLOSE_REQUEST', client_id:int=None)->bool:

        """
        Download attachments from a workflow

        Args:
            fileuuid:  File uuid

            subject:     Subject whether hostFinding or applicationFinding

            workflowtype: Type of workflow

            workflowcategory:     Workflow category either CLOSE_REQUEST or CHANGE_REQUEST

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
           Success

        Example:
            
            To download workflowbatch attachments for hostfindings

            >>> self.rs.workflows.download_workflowbatch_attachments_acceptance('test123','hostFinding','acceptance)

        """
        if subject.lower()=='hostfinding':
                subject='hostFinding'
        if subject.lower()=='applicationfinding':
                subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/download/{}/{}/{}'.format(str(client_id),subject,workflowtype,workflowcategory,fileuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
            with open(raw_response.headers['Content-Disposition'][22:-1],'wb') as f:
                f.write((raw_response.content))
            return raw_response
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print(e)

    def attach_files(self,workflowbatchuuid:str,subject:str, workflowtype:str,file_name:str, path_to_file:str, client_id:int=None)->bool:

        """
        Attach a file to workflow

        Args:
            workflowbatchuuid:      Workflow UUID

            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            workflowtype:   Type of workflow

            file_name:   The name to be used for the uploaded file.

            path_to_file:   Full path to the file to be uploaded.

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether attachment is done
        Example:
            To attach file to workflow

            >>> self.rs.workflows.attach_files('11ed042d-1fcc-fdfe-b7ab-06933745a4d6','hostFinding','acceptance','test.csv','test.csv')
        """
        try:
            if subject.lower()=='hostfinding':
                subject='hostFinding'
            if subject.lower()=='applicationfinding':
                subject='applicationFinding'

            if client_id is None:
                client_id = self._use_default_client_id()[0]
            url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/{workflowtype}/{workflowbatchuuid}/attach"
            multiform_data = {
                "subject": (None,subject),
                "files": (file_name,open(path_to_file, 'rb')),
                }
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==200:
                success=True
            return success
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

    def detach_files(self,workflowbatchuuid:str,attachmentuuids:list,workflowtype:str,subject:str, client_id=None)->bool:

        """
        Detach a file from acceptance workflow

        Args:
            workflowbatchuuid:      Workflow UUID

            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            attachmentuuids:      Attchment UUID

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether detachment is done
        Example:
            To detach files from workflow
                self.rs.workflows.detach_files_acceptance('11ed042d-1fcc-fdfe-b7ab-06933745a4d6',["bfe66d56-b7da-4577-a86f-da5283505ea7"],'hostFinding')
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'
        
        url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/{workflowtype}/{workflowbatchuuid}/detach"
        body={
                "attachmentUuid": attachmentuuids,
                "subject": subject
                }
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url, body=body)
            if raw_response.status_code==204:
                success=True
            return success
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



 
###PRIVATE FUNCTIONS

    def reject_acceptance(self, filter_request:list, description:str,csvdump:bool=False, client_id:int=None)->int:

        """
        Reject an acceptance request.

        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            description:         A description of the rejection.

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
           The job ID from the platform is returned.
        Example:
            To perform a reject acceptance request for a workflow filter RA#0000028
            
            >>>  self.rs.workflows.reject_acceptance([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RA#0000028"}],'needed to test')
        Note:
            You can also dump the job id in a csv using:obj:`csvdump=True` argument

             >>>  self.rs.workflows.reject_acceptance([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RA#0000028"}],'needed to test',csvdump=True)

            
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/acceptance/reject"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('rejectworkflow.csv',index=False)

        return job_id


    def reject_false_positive(self, filter_request:list, description:str,csvdump:bool=False, client_id:int=None)->int:

        """
        Reject a false positive request.

        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            description:         A description of the rejection.

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
           The job ID from the platform is returned.
        Example:
            To perform a reject false positive request for a workflow FP#0000020
            
            >>>  self.rs.workflows.reject_false_positive([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"FP#0000020"}],'needed to test')
        Note:
            You can also dump the job id in a csv using:obj:`csvdump=True` argument

             >>>  self.rs.workflows.reject_false_positive([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"FP#0000020"}],'needed to test',csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/reject"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('rejectworkflow.csv',index=False)

        return job_id

    def reject_remediation(self, filter_request:list, description:str, csvdump:bool=False,client_id:int=None)->int:

        """
        Reject a remediation request.

        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            description:         A description of the rejection.

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          The job ID from the platform is returned.
        Example:
            To perform a reject remediation request for a workflow RM#0000044
            
            >>>  self.rs.workflows.reject_remediation([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RM#0000044"}],'needed to test')
        Note:
            You can also dump the job id in a csv using:obj:`csvdump=True` argument

             >>>  self.rs.workflows.reject_remediation([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RM#0000044"}],'needed to test',csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/remediation/reject"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('rejectworkflow.csv',index=False)

        return job_id

    def reject_severity_change(self, filter_request:list, description:str,csvdump:bool=False, client_id:int=None)->int:

        """
        Reject a severity change request.

        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            description:         A description of the rejection.

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          The job ID from the platform is returned.
        Example:
            To perform a reject severity change request for a workflow SC#0000061
            
            >>>  self.rs.workflows.reject_severity_change([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"SC#0000061"}],'needed to test')
        Note:
            You can also dump the job id in a csv using:obj:`csvdump=True` argument

            >>>  self.rs.workflows.reject_severity_change([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"SC#0000061"}],'needed to test',csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/severityChange/reject"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('rejectworkflow.csv',index=False)

        return job_id

    def rework_acceptance(self, filter_request:list, description:str,csvdump:bool=False, client_id:int=None)->int:

        """
        Request a rework of an acceptance.
        
        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            description:         A description of the rework.

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
           The job ID from the platform is returned.
        Example:
            To rework an acceptance request RA#0000027

            >>> self.rs.workflows.rework_acceptance([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RA#0000027"}],'needed to test')
        Note:
            You can also dump the job id in a csv using:obj:`csvdump=True` argument

             >>> self.rs.workflows.rework_acceptance([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RA#0000027"}],'needed to test',csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/acceptance/rework"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('reworkworkflow.csv',index=False)

        return job_id


    def rework_false_positive(self, filter_request:list, description:str, csvdump:bool=False,client_id:int=None)->int:

        """
        Request a rework of a false positive.

        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            description:         A description of the rework.

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          The job ID from the platform is returned.
        
        Example:
            To rework an false positive request FP#0000019

            >>> self.rs.workflows.rework_false_positive([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"FP#0000019"}],'needed to test')
        Note:
            You can also dump the job id in a csv using:obj:`csvdump=True` argument

             >>> self.rs.workflows.rework_false_positive([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"FP#0000019"}],'needed to test',csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/rework"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('reworkworkflow.csv',index=False)

        return job_id

    def rework_remediation(self, filter_request:list, description:str, csvdump:bool=False, client_id:int=None)->int:

        """
        Request a rework of a remediation.

        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            description:         A description of the rework.

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          The job ID from the platform is returned.
        Example:
            To rework an remediation request RM#0000043

            >>> self.rs.workflows.rework_remediation([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RM#0000043"}],'needed to test')
        Note:
            You can also dump the job id in a csv using:obj:`csvdump=True` argument

             >>> self.rs.workflows.rework_remediation([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RM#0000043"}],'needed to test',csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/remediation/rework"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('reworkworkflow.csv',index=False)

        return job_id

    def rework_severity_change(self, filter_request:list, description:str,csvdump:bool=False ,client_id:int=None)->int:

        """
        Request a rework of a severity change.

        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            description:         A description of the rework.

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          The job ID from the platform is returned.
        Example:
            To rework a severity change request SC#0000027

            >>> self.rs.workflows.rework_severity_change([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"SC#0000027"}],'needed to test')
        Note:
            You can also dump the job id in a csv using:obj:`csvdump=True` argument

             >>> self.rs.workflows.rework_severity_change([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"SC#0000027"}],'needed to test',csvdump=True)
        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/severityChange/rework"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('reworkworkflow.csv',index=False)

        return job_id

    def approve_acceptance(self, filter_request:list, override_exp_date:bool=False,
                           expiration_date:str=(datetime.date.today() + datetime.timedelta(days=14)),csvdump:bool=False, client_id:int=None)->int:

        """
        Approve a acceptance request.

        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            override_exp_date:   True/False indicating whether or not an expiration date should be overridden.

            expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          The job ID from the platform is returned.
        Example:
            To approve an acceptance request RA#0000028

            >>> self.rs.workflows.approve_acceptance([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RA#0000028"}])
        Note:
            You can also dump the job id in a csv using:obj:`csvdump=True` argument

            >>> self.rs.workflows.approve_acceptance([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RA#0000028"}],csvdump=True)

        """
       
        try:

            if client_id is None:
                client_id = self._use_default_client_id()[0]

            search_response = self.get_single_search_page(filter_request)
            
            uuid = search_response['_embedded']['workflowBatches'][0]['uuid']
            url = self.api_base_url.format(str(client_id)) + "/acceptance/approve"

            body = {
                "workflowBatchUuid": uuid,
                "expirationDate": str(expiration_date),
                "overrideExpirationDate": override_exp_date
            }
            if type(csvdump)!=bool:
                print('Error in csvdump value,Please provide either true or false')
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            jsonified_response = json.loads(raw_response.text)
            job_id = jsonified_response['id']
            if csvdump==True:
                workflowid={'jobid':[jsonified_response['id']]}
                df = pd.DataFrame(workflowid)
                df.to_csv('approveworkflow.csv',index=False)
            return job_id
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()


    def approve_false_positive(self, filter_request:list, override_exp_date:bool=False,expiration_date:str=(datetime.date.today() + datetime.timedelta(days=14)),csvdump:bool=False, client_id:int=None)->int:

        """
        Approve a false positive change request.

        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            override_exp_date:   True/False indicating whether or not an expiration date should be overridden.

            expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          The job ID from the platform is returned.
        Example:
            To approve a false positive request FP#0000020

            >>> self.rs.workflows.approve_false_positive([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"FP#0000020"}])
        Note:
            You can also dump the job id in a csv using:obj:`csvdump=True` argument

            >>> self.rs.workflows.approve_false_positive([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"FP#0000020"}],csvdump=True)
        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/approve"

        body = {
            "workflowBatchUuid": uuid,
            "expirationDate": str(expiration_date),
            "overrideExpirationDate": override_exp_date
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
                workflowid={'jobid':[jsonified_response['id']]}
                df = pd.DataFrame(workflowid)
                df.to_csv('approveworkflow.csv',index=False)

        return job_id

    def approve_remediation(self, filter_request:list, override_exp_date:bool=False,expiration_date:str=(datetime.date.today() + datetime.timedelta(days=14)),csvdump:bool=False, client_id:int=None)->int:

        """
        Approve a remediation request.

        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            override_exp_date:   True/False indicating whether or not an expiration date should be overridden.

            expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          The job ID from the platform is returned.
        Example:
            To approve an remediation request RM#0000044

            >>> self.rs.workflows.approve_remediation([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RM#0000044"}])
        Note:
            You can also dump the job id in a csv using:obj:`csvdump=True` argument

            >>> self.rs.workflows.approve_remediation([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"RM#0000044"}],csvdump=True)
        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/remediation/approve"

        body = {
            "workflowBatchUuid": uuid,
            "expirationDate": str(expiration_date),
            "overrideExpirationDate": override_exp_date
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
                workflowid={'jobid':[jsonified_response['id']]}
                df = pd.DataFrame(workflowid)
                df.to_csv('approveworkflow.csv',index=False)

        return job_id

    def approve_severity_change(self, filter_request:list, override_exp_date:bool=False,expiration_date:str=(datetime.date.today() + datetime.timedelta(days=14)),csvdump:bool=False, client_id:int=None)->int:

        """
        Approve a severity change request.
        
        Args:
            filter_request:      A list of dictionaries containing filter parameters.

            override_exp_date:   True/False indicating whether or not an expiration date should be overridden.

            expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
              The job ID from the platform is returned.
        Example:
            To approve an severity change request SC#0000061

            >>> self.rs.workflows.approve_severity_change([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"SC#0000061"}])
        Note:
            You can also dump the job id in a csv using:obj:`csvdump=True` argument

            >>> self.rs.workflows.approve_severity_change([{"field":"generated_id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"SC#0000061"}],csvdump=True)
        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/severityChange/approve"

        body = {
            "workflowBatchUuid": uuid,
            "expirationDate": str(expiration_date),
            "overrideExpirationDate": override_exp_date
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
                workflowid={'jobid':[jsonified_response['id']]}
                df = pd.DataFrame(workflowid)
                df.to_csv('approveworkflow.csv',index=False)

        return job_id

    def update_acceptance_workflow(self,workflowBatchUuid:str,name:str,expirationDate:str,description:str,reason:str,compensatingControl:str,overrideControl:str=OverrideControl.AUTHORIZED,csvdump:bool=False, client_id:int=None)->dict:

        #acceptance,falsePositive,severityChange,remediation
        """
        Update an acceptance workflow.

        Args:
            workflowBatchUuid:      Workflow UUID

            name:      Workflow name

            expirationDate:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.

            description:         A description of the rejection.

            reason:         A reason for the rejection.

            compensatingControl:   A description of compensating controls applied to this finding. Option available : ("DLP", "Deemed not exploitable", "Endpoint Security", "IDS/IPS", "MFA Enforced", "Multiple: See Description", "Network Firewall", "Network Segmentation", "Other: See Description", "Web Application Firewall" or "NONE")

            overrideControl:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
            The jsonified response.
        Example:
            To update an acceptance workflow of uuid 11ed0429-4937-f454-b7ab-06933745a4d6

            >>> self.rs.workflows.update_acceptance_workflow("11ed0429-4937-f454-b7ab-06933745a4d6","testin","2022-07-31","testingforupdate","testing","NONE")

        Note:
            You can also dump the search based data in a csv by simply providing :obj:`csvdump=True` argument

            >>> self.rs.workflows.update_acceptance_workflow("11ed0429-4937-f454-b7ab-06933745a4d6","testin","2022-07-31","testingforupdate","testing","NONE",csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/acceptance/update/"

        body = {"workflowBatchUuid":workflowBatchUuid,"name": name,"expirationDate":expirationDate,"description":description,"reason":reason,"compensatingControl":compensatingControl,"overrideControl":overrideControl}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('updateworkflow.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        return jsonified_response

    def update_falsepositive_workflow(self,workflowBatchUuid:str,name:str,expirationDate:str,description:str,reason:str,compensatingControl:str,overrideControl:str=OverrideControl.AUTHORIZED,csvdump:bool=False, client_id:int=None)->dict:

        #acceptance,falsePositive,severityChange,remediation
        """
        Update a false positive workflow.

        Args:

            workflowBatchUuid:      Workflow UUID

            name:      Workflow name

            expirationDate:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.

            description:         A description of the rejection.

            reason:         A reason for the rejection.

            compensatingControl:   A description of compensating controls applied to this finding. Option available : ("DLP", "Deemed not exploitable", "Endpoint Security", "IDS/IPS", "MFA Enforced", "Multiple: See Description", "Network Firewall", "Network Segmentation", "Other: See Description", "Web Application Firewall" or "NONE")

            overrideControl:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
           The jsonified response.
        Example:
            To Update a false positive workflow of uuid 11ed0429-4937-f454-b7ab-06933745a4d6

            >>> self.rs.workflows.update_falsepositive_workflow("11ed0429-4937-f454-b7ab-06933745a4d6","testin","2022-07-31","testingforupdate","testing","NONE")

        Note:
            You can also dump the search based data in a csv by simply providing :obj:`csvdump=True` argument

            >>> self.rs.workflows.update_falsepositive_workflow("11ed0429-4937-f454-b7ab-06933745a4d6","testin","2022-07-31","testingforupdate","testing","NONE",csvdump=True)
        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/falsePositive/update/"

        body = {"workflowBatchUuid":workflowBatchUuid,"name": name,"expirationDate":expirationDate,"description":description,"reason":reason,"compensatingControl":compensatingControl,"overrideControl":overrideControl}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('updateworkflow.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        
        return jsonified_response


    def update_remediation_workflow(self,workflowBatchUuid:str,name:str,expirationDate:str,description:str,reason:str,compensatingControl:str,overrideControl:str=OverrideControl.AUTHORIZED,csvdump:bool=False, client_id:int=None)->dict:

        #acceptance,falsePositive,severityChange,remediation
        """
        
        Update a remediation workflow.
        
        Args:
            workflowBatchUuid:      Workflow UUID

            name:      Workflow name

            expirationDate:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.

            description:         A description of the rejection.

            reason:         A reason for the rejection.

            compensatingControl:   A description of compensating controls applied to this finding. Option available : ("DLP", "Deemed not exploitable", "Endpoint Security", "IDS/IPS", "MFA Enforced", "Multiple: See Description", "Network Firewall", "Network Segmentation", "Other: See Description", "Web Application Firewall" or "NONE")

            overrideControl:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          The jsonified response.
        Example:
            To update an remediation workflow of uuid 11ed0429-4937-f454-b7ab-06933745a4d6

            >>> self.rs.workflows.update_remediation_workflow("11ed0429-4937-f454-b7ab-06933745a4d6","testin","2022-07-31","testingforupdate","testing","NONE")

        Note:
            You can also dump the search based data in a csv by simply providing :obj:`csvdump=True` argument

            >>> self.rs.workflows.update_remediation_workflow("11ed0429-4937-f454-b7ab-06933745a4d6","testin","2022-07-31","testingforupdate","testing","NONE",csvdump=True)
        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/remediation/update/"

        body = {"workflowBatchUuid":workflowBatchUuid,"name": name,"expirationDate":expirationDate,"description":description,"reason":reason,"compensatingControl":compensatingControl,"overrideControl":overrideControl}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('updateworkflow.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response

    def update_severitychange_workflow(self,workflowBatchUuid:str,name:str,expirationDate:str,description:str,reason:str,severity:str,compensatingControl:str,overrideControl:str=OverrideControl.AUTHORIZED, csvdump:bool=False,client_id:int=None)->dict:

        #acceptance,falsePositive,severityChange,remediation
        """
        Update an severity change workflow.

        Args:
            workflowBatchUuid:      Workflow UUID

            name:      Workflow name

            expirationDate:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.

            description:         A description of the rejection.

            reason:         A reason for the rejection.

            severity: Severity change value

            compensatingControl:   A description of compensating controls applied to this finding. Option available : ("DLP", "Deemed not exploitable", "Endpoint Security", "IDS/IPS", "MFA Enforced", "Multiple: See Description", "Network Firewall", "Network Segmentation", "Other: See Description", "Web Application Firewall" or "NONE")

            overrideControl:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')

            csvdump:         dumps the data in csv

            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
               The jsonified response.
        Example:
            To update a severity change workflow of uuid 11ed0429-4937-f454-b7ab-06933745a4d6

            >>> self.rs.workflows.update_severitychange_workflow("11ed0429-4937-f454-b7ab-06933745a4d6","testin","5","2022-07-31","testingforupdate","testing","NONE")

        Note:
            You can also dump the search based data in a csv by simply providing :obj:`csvdump=True` argument

            >>> self.rs.workflows.update_severitychange_workflow("11ed0429-4937-f454-b7ab-06933745a4d6","testin","5","2022-07-31","testingforupdate","testing","NONE",csvdump=True)
        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/severityChange/update/"

        body = {"workflowBatchUuid":workflowBatchUuid,"name": name,"expirationDate":expirationDate,"description":description,"reason":reason,"severity":severity,"compensatingControl":compensatingControl,"overrideControl":overrideControl}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('updateworkflow.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        return jsonified_response

    def map_findings_acceptance(self,subject:str, filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.ACCEPTANCE, client_id:int=None)->bool:

        """
        Map findings to an acceptance workflow for applicationFindings / hostFindings as defined in the filter_request parameter.

        Args:
            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            filter_request:           A list of dictionaries containing filter parameters.

            workflowuuid:           Workflow Name
            
            workflowtype:             By default acceptance

            client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
             Success whether request occured
        Example:
            To map acceptance workflow to findings
            
            >>> self.rs.workflows.map_findings_acceptance("hostFinding",[{"field":"id","exclusive":False,"operator":"IN","value":"235141285"}],"11ed123b-9d8f-a2f1-b7ab-06933745a4d6")
        
        """

        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/map'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success


    def map_findings_severitychange(self,subject:str, filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.SEVERITYCHANGE, client_id:int=None)->bool:

        """
        Map findings to an severity change workflow for applicationFindings / hostfFindings as defined in the filter_request parameter.

        Args:
            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            filter_request:           A list of dictionaries containing filter parameters.

            workflowuuid:           Workflow Name

            workflowtype:             By default severity change

            client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether request occured
        
        Example:
            To map severity change workflow to findings
            
            >>> self.rs.workflows.map_findings_severitychange("hostFinding",[{"field":"id","exclusive":False,"operator":"IN","value":"235141285"}],"11ed123b-9d8f-a2f1-b7ab-06933745a4d6")
        
        """
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/map'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response==200:
                success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success

    def map_findings_falsepositive(self,subject:str, filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.FALSEPOSITIVE, client_id:int=None)->bool:

        """
        Map findings to an false positive workflow for applicationFindings / hostFindings as defined in the filter_request parameter.

        Args:
            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            filter_request:           A list of dictionaries containing filter parameters.

            workflowuuid:           Workflow Name

            workflowtype:             By default false positive

            client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether request occured
        Example:
            To map false positive workflow to findings
            
            >>> self.rs.workflows.map_findings_falsepositive("hostFinding",[{"field":"id","exclusive":False,"operator":"IN","value":"235141285"}],"11ed123b-9d8f-a2f1-b7ab-06933745a4d6")
        
        """

        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/map'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                    success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success


    def map_findings_remediation(self,subject:str, filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.REMEDIATION, client_id:int=None)->bool:

        """
        Map findings to an remediation workflow for applicationFindings / hostFindings as defined in the filter_request parameter.

        Args:
            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            filter_request:           A list of dictionaries containing filter parameters.

            workflowuuid:           Workflow Name

            workflowtype:             By default remediation

            client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
           Success whether request occured
        Example:
            To map remediation workflow to findings
            
            >>> self.rs.workflows.map_findings_remediation("hostFinding",[{"field":"id","exclusive":False,"operator":"IN","value":"235141285"}],"11ed123b-9d8f-a2f1-b7ab-06933745a4d6")
        
        """

        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/map'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}



        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                    success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success

    def unmap_findings_acceptance(self, subject:str,filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.ACCEPTANCE ,client_id:int=None)->bool:

        """
        Unmap findings to an acceptance workflow for applicationFindings / hostFindings as defined in the filter_request parameter.

        Args:
            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            filter_request:           A list of dictionaries containing filter parameters.

            workflowuuid:           Workflow Name

            workflowtype:             By default acceptance

            client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether request occured
        Example:
            To unmap findings to workflow

            >>> self.rs.workflows.unmap_findings_acceptance('hostFinding',[{"field":"id","exclusive":False,"operator":"IN","value":"232927123,178257910"}],'11ed0429-4937-f454-b7ab-06933745a4d6')
        
        """
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/unmap'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                    success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success


    def unmap_findings_severitychange(self, subject:str,filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.SEVERITYCHANGE, client_id:int=None)->bool:

        """
        Unmap findings to a severity change workflow for applicationFindings / hostFindings as defined in the filter_request parameter.

        Args:
            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            filter_request:           A list of dictionaries containing filter parameters.

            workflowuuid:           Workflow Name

            workflowtype:             By default acceptance

            client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether request occured
        Example:
            To unmap findings to workflow

            >>> self.rs.workflows.unmap_findings_severitychange('hostFinding',[{"field":"id","exclusive":False,"operator":"IN","value":"232927123,178257910"}],'11ed0429-4937-f454-b7ab-06933745a4d6')
        
        """

        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/unmap'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                    success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success

    def unmap_findings_falsepositive(self, subject:str,filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.FALSEPOSITIVE, client_id:int=None)->bool:


        """
        Unmap findings to a false positive  workflow for applicationFindings / hostFindings as defined in the filter_request parameter.

        Args:
            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            filter_request:           A list of dictionaries containing filter parameters.

            workflowuuid:           Workflow Name

            workflowtype:             By default false positive

            client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether request occured
        Example:
            To unmap findings to workflow

            >>> self.rs.workflows.unmap_findings_falsepositive('hostFinding',[{"field":"id","exclusive":False,"operator":"IN","value":"232927123,178257910"}],'11ed0429-4937-f454-b7ab-06933745a4d6')

        
        """
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/unmap'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                    success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success

    def unmap_findings_remediation(self, subject:str,filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.REMEDIATION, client_id:int=None)->bool:

        """
        Unmap findings to a remediation workflow for applicationFindings / hostFindings as defined in the filter_request parameter.

        Args:
            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            filter_request:           A list of dictionaries containing filter parameters.

            workflowuuid:           Workflow Name

            workflowtype:             By default remediation

            client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether request occured
        Example:
            To unmap findings to workflow

            >>> self.rs.workflows.unmap_findings_remediation('hostFinding',[{"field":"id","exclusive":False,"operator":"IN","value":"232927123,178257910"}],'11ed0429-4937-f454-b7ab-06933745a4d6')
        
        """
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/unmap'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                    success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success

    def get_attachments_acceptance(self, workflowbatchuuid:str, subject:str, client_id:int=None):

        """
        Get attachments from an acceptance workflow

        Args:
            workflowbatchuuid:  Workflowbatch uuid

            subject:     Subject whether hostFinding or applicationFinding

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Example:
            To use attachment function
            
            >>> self.rs.workflows.get_attachments_acceptance('11ed0429-4937-f454-b7ab-06933745a4d6','hostFinding')

        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/acceptance/{}/attachments'.format(str(client_id),subject,workflowbatchuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print()
            print(e)
        jsonified_response = raw_response.text

        return jsonified_response


    def get_attachments_severitychange(self, workflowbatchuuid:str, subject:str, client_id:int=None):

        """
        Get attachments from a severity change workflow

        Args:
            workflowbatchuuid:  Workflowbatch uuid

            subject:     Subject whether hostFinding or applicationFinding

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Example:
            To use attachment function
            
            >>> self.rs.workflows.get_attachments_severitychange('11ed0429-4937-f454-b7ab-06933745a4d6','hostFinding')
        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.profile.platform_url+'/api/v1/client/{}/{}/severityChange/{}/attachments'.format(str(client_id),subject,workflowbatchuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print()
            print(e)
        
        jsonified_response = raw_response.text

        return jsonified_response

    def get_attachments_remediation(self, workflowbatchuuid:str, subject:str, client_id:int=None):

        """
        Get attachments from a remediation workflow

        Args:
            workflowbatchuuid:  Workflowbatch uuid

            subject:     Subject whether hostFinding or applicationFinding

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Example:
            
            >>> self.rs.workflows.get_attachments_remediation('11ed0429-4937-f454-b7ab-06933745a4d6','hostFinding')

        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/remediation/{}/attachments'.format(str(client_id),subject,workflowbatchuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print()
            print(e)
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_attachments_falsepositive(self, workflowbatchuuid:str, subject:str, client_id:int=None):

        """
        Get attachments from a false positive workflow

        Args:
            workflowbatchuuid:  Workflowbatch uuid

            subject:     Subject whether hostFinding or applicationFinding

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Example:
            To use attachment function
            
            >>> self.rs.workflows.get_attachments_falsepositive('11ed0429-4937-f454-b7ab-06933745a4d6','hostFinding')

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/falsePositive/{}/attachments'.format(str(client_id),subject,workflowbatchuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print()
            print(e)
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def download_workflowbatch_attachments_acceptance(self, fileuuid:str,subject:str,workflowcategory:str='CLOSE_REQUEST', client_id:int=None)->bool:

        """
        Download attachments from an acceptance workflow

        Args:
            fileuuid:  File uuid

            subject:     Subject whether hostFinding or applicationFinding

            workflowcategory:     Workflow category either CLOSE_REQUEST or CHANGE_REQUEST

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
           Success

        Example:
            
            To download workflowbatch attachments for hostfindings

            >>> self.rs.workflows.download_workflowbatch_attachments_acceptance('test123','hostFinding')

        """
        if subject.lower()=='hostfinding':
                subject='hostFinding'
        if subject.lower()=='applicationfinding':
                subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/download/acceptance/{}/{}'.format(str(client_id),subject,workflowcategory,fileuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
            with open(raw_response.headers['Content-Disposition'][22:-1],'wb') as f:
                f.write((raw_response.content))
            return raw_response
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print(e)
        

    def download_workflowbatch_attachments_severitychange(self, fileuuid:str, subject:str,workflowcategory:str='CLOSE_REQUEST', client_id:int=None)->bool:

        """
        Download attachments from an severity change workflow

        Args:
            fileuuid:  File uuid

            subject:     Subject whether hostFinding or applicationFinding

            workflowcategory:     Workflow category either CLOSE_REQUEST or CHANGE_REQUEST

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success
        Example:
            
            To download workflowbatch attachments for hostfindings

            >>> self.rs.workflows.download_workflowbatch_attachments_severitychange('test123','hostFinding')
        
        """

        if subject.lower()=='hostfinding':
                subject='hostFinding'
        if subject.lower()=='applicationfinding':
                subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/download/severityChange/{}/{}'.format(str(client_id),subject,workflowcategory,fileuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
            with open(raw_response.headers['Content-Disposition'][22:-1],'wb') as f:
                f.write((raw_response.content))
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print()
            print(e)
        success=True

        return success

    def download_workflowbatch_attachments_falsepositive(self, fileuuid:str, subject:str,workflowcategory:str='CLOSE_REQUEST', client_id:int=None)->bool:

        """
        Download attachments from an False positive workflow

        Args:
            fileuuid:  File uuid

            subject:     Subject whether hostFinding or applicationFinding

            workflowcategory:     Workflow category either CLOSE_REQUEST or CHANGE_REQUEST

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success
        
        Example:
            
            To download workflowbatch attachments for hostfindings

            >>> self.rs.workflows.download_workflowbatch_attachments_falsepositive('test123','hostFinding')
        
        """

        if subject.lower()=='hostfinding':
                subject='hostFinding'
        if subject.lower()=='applicationfinding':
                subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/download/falsePositive/{}/{}'.format(str(client_id),subject,workflowcategory,fileuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
            with open(raw_response.headers['Content-Disposition'][22:-1],'wb') as f:
                f.write((raw_response.content))
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print()
            print(e)
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def download_workflowbatch_attachments_remediation(self, fileuuid:str, subject:str,workflowcategory:str='CLOSE_REQUEST', client_id:int=None)->bool:

        """
        Download attachments from an remediation workflow

        Args:
            fileuuid:  File uuid

            subject:     Subject whether hostFinding or applicationFinding

            workflowcategory:     Workflow category either CLOSE_REQUEST or CHANGE_REQUEST

            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
           Success
        Example:
            
            To download workflowbatch attachments for hostfindings

            >>> self.rs.workflows.download_workflowbatch_attachments_remediation('test123','hostFinding')
        
        """

        if subject.lower()=='hostfinding':
                subject='hostFinding'
        if subject.lower()=='applicationfinding':
                subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/download/remediation/{}/{}'.format(str(client_id),subject,workflowcategory,fileuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
            with open(raw_response.headers['Content-Disposition'][22:-1],'wb') as f:
                f.write((raw_response.content))
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print()
            print(e)

    def attach_files_acceptance(self,workflowbatchuuid:str,subject:str, file_name:str, path_to_file:str, client_id:int=None)->bool:

        """
        Attach an acceptance file to workflow

        Args:
            workflowbatchuuid:      Workflow UUID

            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            file_name:   The name to be used for the uploaded file.

            path_to_file:   Full path to the file to be uploaded.

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether attachment is done
        Example:
            To attach file to workflow

            >>> self.rs.workflows.attach_files_acceptance('11ed042d-1fcc-fdfe-b7ab-06933745a4d6','hostFinding','test.csv','test.csv')
        """
        try:
            if subject.lower()=='hostfinding':
                subject='hostFinding'
            if subject.lower()=='applicationfinding':
                subject='applicationFinding'

            if client_id is None:
                client_id = self._use_default_client_id()[0]
            url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/acceptance/{workflowbatchuuid}/attach"
            multiform_data = {
                "subject": (None,subject),
                "files": (file_name,open(path_to_file, 'rb')),
                }
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==200:
                success=True
            return success
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()


    def attach_files_remediation(self,workflowbatchuuid:str,subject:str, file_name:str, path_to_file:str, client_id:int=None)->bool:

        """
        Attach a file to remediation workflow

        Args:
            workflowbatchuuid:      Workflow UUID

            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            file_name:   The name to be used for the uploaded file.

            path_to_file:   Full path to the file to be uploaded.

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether attachment is done
        Example:
            To attach file to workflow

            >>> self.rs.workflows.attach_files_remediation('11ed042d-1fcc-fdfe-b7ab-06933745a4d6','hostFinding','test.csv','test.csv')
        
        """

        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/remediation/{workflowbatchuuid}/attach"
        multiform_data = {
            "subject": (None,subject),
            "files": (file_name,open(path_to_file, 'rb')),
            }
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==200:
                success=True
            return success
        except (RequestFailed,Exception,FileNotFoundError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

    def attach_files_falsepositive(self,workflowbatchuuid:str,subject:str, file_name:str, path_to_file:str, client_id:int=None)->bool:

        """
        Attach a file to false positive workflow

        Args:
            workflowbatchuuid:      Workflow UUID

            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            file_name:   The name to be used for the uploaded file.

            path_to_file:   Full path to the file to be uploaded.

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether attachment is done
        Example:
            
            To attach file to workflow

            >>> self.rs.workflows.attach_files_falsepositive('11ed042d-1fcc-fdfe-b7ab-06933745a4d6','hostFinding','test.csv','test.csv')
        """

        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/falsePositive/{workflowbatchuuid}/attach"
        multiform_data = {
            "subject": (None,subject),
            "files": (file_name,open(path_to_file, 'rb')),
            }
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==200:
                success=True
            return success
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

    def attach_files_severitychange(self,workflowbatchuuid:str,subject:str, file_name:str, path_to_file:str, client_id:int=None)->bool:

        """
        Attach a file to severiy change workflow

        Args:
            workflowbatchuuid:      Workflow UUID

            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            file_name:   The name to be used for the uploaded file.

            path_to_file:   Full path to the file to be uploaded.

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether attachment is done=
        Example:
            To attach file to workflow

            >>> self.rs.workflows.attach_files_severitychange('11ed042d-1fcc-fdfe-b7ab-06933745a4d6','hostFinding','test.csv','test.csv')
        """

        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/severityChange/{workflowbatchuuid}/attach"
        multiform_data = {
            "subject": (None,subject),
            "files": (file_name,open(path_to_file, 'rb')),
            }
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==200:
                success=True
            return success
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

    def detach_files_acceptance(self,workflowbatchuuid:str,attachmentuuids:list,subject:str, client_id=None)->bool:

        """
        Detach a file from acceptance workflow

        Args:
            workflowbatchuuid:      Workflow UUID

            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            attachmentuuids:      Attchment UUID

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether detachment is done
        Example:
            
            To detach files from workflow
            
            >>> self.rs.workflows.detach_files_acceptance('11ed042d-1fcc-fdfe-b7ab-06933745a4d6',["bfe66d56-b7da-4577-a86f-da5283505ea7"],'hostFinding')
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'
        
        url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/acceptance/{workflowbatchuuid}/detach"
        body={
                "attachmentUuid": attachmentuuids,
                "subject": subject
                }
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url, body=body)
            if raw_response.status_code==204:
                success=True
            return success
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


    def detach_files_falsepositive(self,workflowbatchuuid:str,attachmentuuids:list,subject:str, client_id:int=None)->bool:

        """
        Detach files from false positive workflow

        Args:
            workflowbatchuuid:      Workflow UUID

            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            attachmentuuids:      Attchment UUID

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether detachment is done
        Example:
            To detach files from workflow

            >>> self.rs.workflows.detach_files_falsepositive( "11ed042d-006c-358a-b7ab-06933745a4d6",[  "a59fd436-b2ba-46f9-9962-ea227426532d"],'hostFinding')
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'
        
        url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/falsePositive/{workflowbatchuuid}/detach"
        body={
                "attachmentUuid": attachmentuuids,
                "subject": subject
                }
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url, body=body)
            if raw_response.status_code==204:
                success=True
            return success
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

    def detach_files_remediation(self,workflowbatchuuid:str,attachmentuuids:list,subject:str, client_id:int=None)->bool:

        """
        Detach files from remediation workflow

        Args:
            workflowbatchuuid:      Workflow UUID

            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            attachmentuuids:      Attchment UUID

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether detachment is done
        Example:
            To detach files from workflow

            >>> self.rs.workflows.detach_files_remediation( "11ed042d-1fcc-fdfe-b7ab-06933745a4d6",[   "95e082c9-b4f6-46ce-baab-538375db85d2"],'hostFinding')
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'
        
        url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/remediation/{workflowbatchuuid}/detach"
        
        body={
                "attachmentUuid": attachmentuuids,
                "subject": subject
                }
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url, body=body)
            if raw_response.status_code==204:
                success=True
            return success
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

    def detach_files_severitychange(self,workflowbatchuuid:str,attachmentuuids:list,subject:str, client_id:int=None)->bool:

        """
        Detach files from severity change workflow

        Args:
            workflowbatchuuid:      Workflow UUID

            subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")

            attachmentuuids:      Attchment UUID

            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        Return:
          Success whether detachment is done
        Example:
            To detach files from workflow

            >>> self.rs.workflows.detach_files_severitychange('11ed042d-15bb-90f6-b7ab-06933745a4d6',[ "c4e992e7-f911-442e-92cf-b8db003eafdb"],'hostFinding')
        """
        

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'
        
        url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/severityChange/{workflowbatchuuid}/detach"
        
        body={
                "attachmentUuid": attachmentuuids,
                "subject": subject
                }
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url, body=body)
            if raw_response.status_code==204:
                success=True
            return success
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


        return raw_response.text



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