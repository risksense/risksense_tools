"""
Assessment module defined for different assessment related api endpoints.
"""

""" *******************************************************************************************************************
|
|  Name        :  __assessments.py
|  Module      :  risksense_api
|  Description :  A class to be used for interacting with RiskSense platform assessments.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

from datetime import date, datetime
import json
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
import csv


class Assessments(Subject):

    """Class for assessment function definitions.
    
    Args:
        profile:     Profile Object    

    To utlise assessment function:

    Usage:
        :obj:`self.{risksenseobjectname}.assessments.{function}`
    
    Examples:
        To create an assessment using :meth:`create` function

        >>> self.{risksenseobjectname}.assessments.create(args)

    """

    def __init__(self, profile:object):

        """
        Initialization of Assessments object.

        Args:
            profile:     Profile Object

        """

        self.subject_name = "assessment"
        Subject.__init__(self, profile, self.subject_name)
        self.al_base_url = self.profile.platform_url + "/api/v1/client/{}/reportingChecklist/assessment/{}"


    def create(self, name:str, start_date:date, notes:str="", client_id:int=None, csvdump:bool=False)->int:
        """Creates an assessment.

        Args:
            name:        The name for new assessment.
            start_date:  The date for the new assessment.  Should be in "YYYY-MM-DD" format.
            notes:       Any notes to associated with the assessment.
            client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:     Toggle to dump data in csv
        
        Return:
            Assessment job id

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.create('hello','2022-02-11','testingtherisksense')

        Note:
            You can also dump the data of the assessment job id in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.assessments.create('hello','2022-02-11','testingtherisksense',csvdump=True)            
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        body = {
            "name": name,
            "startDate": start_date,
            "notes": notes
        }

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in creating assessment')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        assessment_id = jsonified_response['id']

        try:
            if csvdump==True:
                field_names = ['id']
                try:
                    with open('groupcreate.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow({'id': assessment_id})
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()

        return assessment_id

    def update(self, assessment_id:int, client_id:int=None,csvdump:bool=False, **kwargs)->int:

        """
        Update an assessment

        Args:
            assessment_id:   The assessment ID
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv
        
        Keyword Args:
            name (`str`):          The name to assign to the assessment.
            start_date (`str`):    The start date to assign to the assessment.  Should be in "YYYY-MM-DD" format.
            notes (`str`):         Notes to assign to the assessment.

        Return:
            The job ID is returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.update(216917, start_date='2022-08-01', name='testcase_aug_test', notes='')

        Note:
            You can also dump the data of the assessment job id in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.assessments.update(216917, start_date='2022-08-01', name='testcase_aug_test',csvdump=True)     
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        name = kwargs.get('name', None)
        start_date = kwargs.get('start_date', None)
        notes = kwargs.get('notes', None)

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id)

        body = {}

        if name is not None:
            body.update(name=name)

        if start_date is not None:
            body.update(startDate=start_date)

        if notes is not None:
            body.update(notes=notes)

        if body == {}:
            raise ValueError("Body is empty. At least one of these fields is required: name, start_date, notes")

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in updating assessment')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        returned_id = jsonified_response['id']

        try:
            if csvdump==True:
                field_names = ['id']
                try:
                    with open('groupcreate.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow({'id': returned_id})
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()

        return returned_id

    def delete(self, assessment_id:int, client_id:int=None,csvdump:bool=False)->int:

        """
        Deletes an assessment.

        Args:
            assessment_id:   Assessment ID.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:         Toggle to dump data in csv

        Return:
            The job ID is returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.delete(216917)

        Note:
            You can also dump the data of the assessment that will be deleted in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.assessments.delete(216917,csvdump=True)    
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id)

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        if csvdump==True:
            all_findings=self.search([{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":f"{assessment_id}"}])
            field_names = []

            for item in all_findings[0]:
                field_names.append(item)
            try:
                with open('assessmentdetails.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in all_findings:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except (RequestFailed,Exception) as e:
            print('Error in deleting assessment')
            print(e)
            exit()



        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def get_model(self, client_id:int=None)->dict:

        """
        Get available projections and models for Assessments.

        Args:
            client_id:  Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            Assessment projections and models are returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.get_model(123)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
        except (RequestFailed,Exception) as e:
            print('Error in getting model')
            print(e)
            exit()

        return response

    def list_assessment_filter_fields(self,client_id:int=None)->dict:

        """
        List filter endpoints.

        Args:
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:    
            The JSON output from the platform is returned, listing the available filters.

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.list_assessment_filter_fields(123)
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
            >>> apiobj = self.{risksenseobject}.assessments.suggest([],{"field":"name","exclusive":False,"operator":"WILDCARD","value":"testcase_aug_test,","implicitFilters":[]}))
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._suggest(self.subject_name, search_filter, suggest_filter, client_id)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in suggesting for filter fields')
            print(e)
            exit()

        return response
        
    def get_single_search_page(self, search_filters:list, page_num:int=0, page_size:int=150,
                               sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC, client_id:int=None)->dict:

        """
        Searches for and returns assessments based on the provided filter(s) and other parameters.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            page_num:        Page number of results to be returned.
            page_size:       Number of results to be returned per page.
            sort_field:      Name of field to sort results on.
            sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The paginated JSON response from the platform is returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.get_single_search_page([{"field":"name","exclusive":False,"operator":"WILDCARD","value":"testcase_aug_test,","implicitFilters":[]}])
        """

        func_args = locals()
        func_args.pop('self')

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            response = self._get_single_search_page(self.subject_name, **func_args)
        except (RequestFailed,Exception) as e:
            print('Error in searching for assessments')
            print(e)
            exit()

        return response

    def search(self, search_filters:list, page_size:int=150, sort_field:str=SortField.ID, sort_dir:str=SortDirection.ASC, client_id:int=None,csvdump:bool=False)->list:

        """
        Searches for and returns assessments based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        Args:
            search_filters:  A list of dictionaries containing filter parameters.
            page_size:       The number of results per page to be returned.
            sort_field:      Name of field to sort results on.
            sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump: Toggle to dump data in csv

        Return:
            A list containing all hosts returned by the search using the filter provided.

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.search([{"field":"name","exclusive":False,"operator":"WILDCARD","value":"testcase_aug_test,","implicitFilters":[]}])

        Note:
            You can also dump the data of the assessment searched in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.assessments.search([{"field":"name","exclusive":False,"operator":"WILDCARD","value":"testcase_aug_test,","implicitFilters":[]}],csvdump=True)  
        """

        func_args = locals()
        func_args.pop('self')
        func_args.pop('csvdump')
        all_results = []

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            page_info = self._get_page_info(self.subject_name, search_filters, page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except (RequestFailed,Exception) as e:
            print('Error in searching for assessments')
            print(e)
            exit()

        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed, Exception) as e:
            print('Error in searching for assessments')
            print(e)
            exit()

        if csvdump==True:
            field_names = []

            for item in all_results[0]:
                field_names.append(item)
            try:
                with open('assessmentdetailssearch.csv', 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in all_results:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return all_results
        
    def update_assessment_status(self, assessment_id:int,status:str, client_id:int=None, csvdump:bool=False)->dict:

        """
        Update the status of the assessment

        Args:
            assessment_id:       The assessment ID.
            status:       Update the status either "LOCKED" or "UNLOCKED"
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
            csvdump:             Toggle to dump data in csv

        Return:
            The jsonified data of the status

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.update_assessment_status(216917)

        Note:
            You can also dump the data of the assessment that will be updated in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.assessments.update_assessment_status(216917)
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id) + "/status"

        body= {
                 "status": status.upper()
              }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except (RequestFailed,Exception) as e:
            print('Error in updating assessment status')
            print(e)
            exit()

        jsonified_data = json.loads(raw_response.text)

        try:
            if csvdump==True:
                field_names = []
                for item in jsonified_data:
                    field_names.append(item)
                try:
                    with open('assessmentstatus.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow(jsonified_data)
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except Exception as e:
                print('There seems to be an exception')
                print(e)
                exit()

        return jsonified_data

    def get_assessment_history(self, assessment_id:int,csvdump:bool=False,client_id:int=None)->dict:

        """
        Get history of assessments

        Args:
            assessment_id:       The assessment ID.
            csvdump:             Whether to dump the assessment history in a csv, true to dump and false to not dump
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            The jsonified data of the status

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.get_assessment_history(216917)

        Note:
            You can also dump the data of the assessment history in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.assessments.get_assessment_history(216917,csvdump=True)  
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id) + "/history"

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting assessment history')
            print(e)
            exit()

        jsonified_data = json.loads(raw_response.text)
        if csvdump==True:
            field_names = []

            for item in jsonified_data[0]:
                field_names.append(item)
            try:
                with open('assessmenthistory.csv', 'w',newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_data:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_data
        
    def list_attachments(self, assessment_id:int,csvdump:bool=False,client_id:int=None)->list:

        """
        Lists attachments associated with an assessment.

        Args:
            assessment_id:       The assessment ID
            csvdump:             Whether to dump the attachment data in a csv, true to dump and false to not dump
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            A list of attachments associated with the assessment is returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.list_attachments(216917)

        Note:
            You can also dump the data of the assessment attachment in a csv file. Just make csvdump as True:
            
            >>>  self.{risksenseobject}.assessments.list_attachments(216917)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id) + "/attachment"

        if type(csvdump) != bool:
            print('csvdump value is not in type boolean')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in listing attachments')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []

            for item in jsonified_response[0]:
                field_names.append(item)
            try:
                with open('attachmentofassessment.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response

    def get_attachment(self, assessment_id:int, attachment_uuid:str, filename:str, client_id:int=None)->bool:

        """
        Download an attachment associated with an assessment.

        Args:
            assessment_id:       The assessment ID.
            attachment_uuid:     The unique ID associated with the attachment.
            filename:            The filename to be used for the downloaded file along with the file type extension.
            client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            True/False indicating whether or not the operation was successful.

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.get_attachment(216917,'123-456')
          
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id) + "/attachment/" + str(attachment_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting attachment')
            print(e)
            exit()

        try:
            open(filename, "wb").write(raw_response.content)
        except (FileNotFoundError, Exception):
            print('Error in getting downloading attachment')
            print(e)
            exit()

        print("Done.")
        success = True

        return success

    def get_attachment_metadata(self, assessment_id:int, attachment_uuid:str, client_id:int=None)->dict:

        """
        Get the metadata associated with an assessment's attachment.

        Args:
            assessment_id:       The assessment ID.
            attachment_uuid:     The unique ID associated with the attachment.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            A dictionary containing the metadata for the attachment is returned.

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.get_attachment_metadata(216917,'123-456')
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id) + "/attachment/" + str(attachment_uuid) + "/meta"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting attachment metada')
            print(e)
            exit()

        jsonified_data = json.loads(raw_response.text)

        return jsonified_data

    def edit_network_internalreport(self,assessment_id:int,conclusion:str,constraints:str,client_id:int=None)->dict:

        """
        Edit network internal report for an assessment

        Args:
            assessment_id:       The assessment ID.
            conclusion:          Conclusion statement for internal report
            constraints:          Constraints statement for internal report
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.

        Return:
            Jsonified data of the response

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.edit_network_internalreport(216917,'abc','abc')
        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.al_base_url.format(str(client_id),str(assessment_id))+'/NETWORK_INTERNAL'

        body= {"conclusion":conclusion,"constraints":constraints}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url,body=body)
        except (RequestFailed,Exception) as e:
            print('Error in editing network internal report')
            print(e)
            exit()

        jsonified_data = json.loads(raw_response.text)

        return jsonified_data

    def edit_application_report(self,assessment_id:int,conclusion:str,constraints:str,client_id:int=None)->dict:

        """
        Edit application report for an assessment

        Args:
            assessment_id:       The assessment ID.
            conclusion:          Conclusion statement for internal report
            constraints:          Constraints statement for internal report
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Jsonified data of the response

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.edit_application_report(216917,'abc','abc')
        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.al_base_url.format(str(client_id),str(assessment_id))+'/APPLICATION'

        body= {"conclusion":conclusion,"constraints":constraints}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url,body=body)
        except (RequestFailed,Exception) as e:
            print('Error in editing application report')
            print(e)

        jsonified_data = json.loads(raw_response.text)

        return jsonified_data
    
    def edit_networkexternal_report(self,assessment_id:int,conclusion:str,constraints:str,client_id:int=None)->dict:

        """
        Edit network external report for an assessment

        Args:
            assessment_id:       The assessment ID.
            conclusion:          Conclusion statement for internal report
            constraints:          Constraints statement for internal report
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            Jsonified data of the response

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.edit_networkexternal_report(216917,'abc','abc')
        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.al_base_url.format(str(client_id),str(assessment_id))+'/NETWORK_EXTERNAL'

        body= {"conclusion":conclusion,"constraints":constraints}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url,body=body)
        except (RequestFailed,Exception) as e:
            print('Error in editing network external report')
            print(e)
            exit()

        jsonified_data = json.loads(raw_response.text)

        return jsonified_data

### PRIVATE FUNCTIONS ##

    def lock_assessment(self, assessment_id:int, client_id:int=None)->dict:

        """
        Lock an assessment

        Args:
            assessment_id:       The assessment ID.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The jsonified data of the status

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.lock_assessment(216917)
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id) + "/status"


        body= {
                 "status": "LOCKED"
              }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in locking assessment')
            print(e)
            exit()

        jsonified_data = json.loads(raw_response.text)

        return jsonified_data

    def unlock_assessment(self, assessment_id:int, client_id:int=None)->dict:

        """
        Unlock an assessment

        Args:
            assessment_id:       The assessment ID.
            client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        
        Return:
            The jsonified data of the status

        Examples:
            >>> apiobj = self.{risksenseobject}.assessments.unlock_assessment(216917)
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id) + "/status"

        body= {
                 "status": "UNLOCKED"
              }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in unlocking assessment')
            print(e)
            exit()
        jsonified_data = json.loads(raw_response.text)

        return jsonified_data  

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
