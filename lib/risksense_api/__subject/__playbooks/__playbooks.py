"""
**Playbooks module defined for different playbooks related api endpoints.**
"""
""" *******************************************************************************************************************
|
|  Name        :  __playbooks.py
|  Description :  Playbooks
|  Project     :  risksense_api
|  Copyright   :  2021 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

from dataclasses import field
import json
from pickle import DICT
import time
import concurrent.futures
from tkinter.tix import DirTree, Tree
import progressbar
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
import csv
import pandas as pd



class Playbooks(Subject):

    """ Playbooks class """

    """ **Class for Playbooks function defintions**.

    To utlise playbook function:

    Args:
            profile:     Profile Object
    
    Usage:
        :obj:`self.{risksenseobjectname}.playbooks.{function}`
    
    Examples:
        To get supported inputs use :meth:`get_supported_inputs()` function

        >>> self.{risksenseobject}.playbooks.get_supported_inputs({args})

    """

    def __init__(self, profile:object):

        """
        Initialization of Playbooks object.

        Args:
            profile:     Profile Object

        """
        self.subject_name = "playbook"
        Subject.__init__(self, profile, self.subject_name)

    def get_supported_inputs(self,csvdump:bool=False, client_id:int=None)->list:

        """
        Get a list of supported playbook inputs.

        Args:
             client_id:   Client ID
             csvdump:         dumps the data in csv
        Return:
           Supported inputs
        Example:
            To get supported inputs

            >>> self.{risksenseobject}.playbooks.get_supported_inputs()
        Note:
            You can also dump the data in csv using  :obj:`csvdump=True`
            
            >>> self.{risksenseobject}.playbooks.get_supported_inputs(csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/supported-inputs"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                 print()
                 print('There seems to be an exception')
                 print(e)
                 exit()
        
        supported_inputs = json.loads(raw_response.text)
        data=[]
        for i in supported_inputs:
            data.append({'supportedinputs':i})
        if csvdump==True:
            field_names = []
            field_names.append('supportedinputs')
            try:
                with open('supportinputs.csv', 'w',newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in data:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        

        return supported_inputs

    def get_supported_actions(self,csvdump:bool=False, client_id:int=None)->list:

        """
        Get a list of supported playbook actions.

        Args:
             client_id:   Client ID
             csvdump:     Dumps the data in csv
        Return:
           Supported actions
        Example:
            To get supported actions 

            >>> self.{risksenseobject}.playbooks.get_supported_actions()
        
        Note:
            You can also dump the data in a csv using :obj:`csvdump=True`

            >>> self.{risksenseobject}.playbooks.get_supported_actions(csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/supported-actions"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        supported_actions = json.loads(raw_response.text)
        data=[]
        for i in supported_actions:
            data.append({'supportedactions':i})
        if csvdump==True:
            field_names = []
            field_names.append('supportedactions')
            try:
                with open('supportedactions.csv', 'w',newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in data:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)


        return supported_actions

    def get_supported_frequencies(self,client_id:int=None)->list:

        """
        Get a list of supported playbook frequencies.

        Args:
             client_id:   Client ID
             csvdump:     Dumps the data in csv
        
        Return:
           Supported frequencies
        
        Example:
            To get supported frequencies 

            >>> self.{risksenseobject}.playbooks.get_supported_frequencies()
        
        Note:
            You can also dump the data in a csv using :obj:`csvdump=True`

            >>> self.{risksenseobject}.playbooks.get_supported_frequencies(csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/supported-frequencies"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        supported_frequencies = json.loads(raw_response.text)        
        
        return supported_frequencies

    def get_supported_outputs(self,csvdump:bool=False, client_id:int=None)->list:

        """
        Get a list of supported playbook outputs.

        Args:
             client_id:   Client ID
             csvdump:     Dumps the data in csv
        Return:
           Supported outputs
        Example:
            To get supported outputs 

            >>> self.{risksenseobject}.playbooks.get_supported_outputs()
        
        Note:
            You can also dump the data in a csv using :obj:`csvdump=True`

            >>> self.{risksenseobject}.playbooks.get_supported_outputs(csvdump=True)
        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/supported-outputs"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        supported_outputs = json.loads(raw_response.text)

        data=[]
        for i in supported_outputs:
            data.append({'supportedoutputs':i})
        if csvdump==True:
            field_names = []
            field_names.append('supportedoutputs')
            try:
                with open('supportedoutputs.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in data:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return supported_outputs

    def get_subject_supported_actions(self,csvdump:bool=False, client_id:int=None)->dict:

        """
        Get a list of subject-supported playbook actions.

        Args:
             client_id:   Client ID
             csvdump:     Dumps the data in csv
        Return:
           Subject Supported actions
        Example:
            To get Subject Supported actions 

            >>> self.{risksenseobject}.playbooks.get_subject_supported_actions()
        
        Note:
            You can also dump the data in a csv using :obj:`csvdump=True`

            >>> self.{risksenseobject}.playbooks.get_subject_supported_actions(csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/subject-supported-actions"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        supported_actions = json.loads(raw_response.text)
        data=[]

        if csvdump==True:
            field_names=[]
            for key in supported_actions.keys():
                field_names.append(key)
            try:
                with open('getsupportedactions.csv', 'w',newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for key,value in supported_actions.items():
                            supported_actions[key]=','.join(value)
                    writer.writerow(supported_actions)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)


        return supported_actions

    def get_playbooks_single_page(self, page_size:int=1000, page_num:int=0, sort_dir:str=SortDirection.ASC, client_id:int=None)->dict:

        """
        Fetch a single page of playbooks from client
        
        Args:
            page_size:   Page Size

            page_num:    Page Number

            sort_dir:    Sort Direction

            client_id:   Client ID
        Return:
            The paginated JSON response from the platform is returned.
        
        Example:
            An example to get single search page of playbooks data
            
            >>> self.{risksenseobject}.playbooks.get_single_search_page([])

            You can also try changing the other arguments to your liking to reflect the data as you suffice such as change page_size or page_num etc.

            >>> self.{risksenseobject}.playbooks.get_single_search_page([],page_num=2,page_size=10)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if page_size > 1000:
            raise PageSizeError("Page size must be <= 1000")

        url = self.api_base_url.format(str(client_id)) + "/fetch"

        params = {
            "size": page_size,
            "page": page_num,
            "sort": sort_dir
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

    def get_all_playbooks(self,csvdump:bool=False, client_id:int=None)->list:

        """
        Get all playbooks for a client.

        Args:
            client_id:   Client ID
            csvdump:         dumps the data in csv
        Return:
          All Playbooks for a client

        Example:

            To get all playbooks

            >>>  self.{risksenseobject}.playbooks.get_all_playbooks()
        Note:
            You can also dump the data using :obj:`csvdump=True` argument

            >>>  self.{risksenseobject}.playbooks.get_all_playbooks(csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.api_base_url.format(str(client_id)) + "/fetch"
        
        try:
            num_pages = self._get_playbook_page_info(url, page_size=1000)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        page_range = range(0, num_pages)

        try:
            playbooks = self._fetch_in_bulk(self.get_playbooks_single_page, page_range=page_range, client_id=client_id)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        if csvdump==True:
            field_names = []
            for item in playbooks:
                for key in item.keys():
                    if key not in field_names:
                        field_names.append(key)
            try:
                with open('getallplaybooks.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in playbooks:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return playbooks

    def get_specific_playbook(self, playbook_uuid:str,csvdump:bool=False,client_id:int=None)->dict:

        """
        Fetch a specific playbook by UUID.

        Args:
            playbook_uuid:   Playbook UUID

            csvdump:         dumps the data in csv

            client_id:       Client ID
        Return:
           The Playbook information
        
        Example:

            To get specific playbook `1234str`

            >>>  self.{risksenseobject}.playbooks.get_specific_playbook('1234str')
        Note:
            You can also dump the data using :obj:`csvdump=True` argument

            >>>  self.{risksenseobject}.playbooks.get_specific_playbook('1234str',csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/fetch/{}".format(playbook_uuid)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        
        
        if csvdump==True:
            data={}
            for j,k in jsonified_response.items():
                data[j]=[k]
            df=pd.DataFrame(data)
            df.to_csv('playbookdata.csv',index=False) 

        return jsonified_response
 
    def get_single_page_playbook_rules(self, playbook_uuid:str, page_num:int=0, page_size:int=1000, sort_dir:int=SortDirection.ASC, client_id:int=None)->dict:

        """
        Get a single page of rules for a specific playbook

        Args:
            playbook_uuid:   Playbook UUID

            page_num:        Page number to retrieve

            page_size:       Number of items per page to return

            sort_dir:        Sort Direction

            client_id:       Client ID
        Return:
          Playbook rules
        Example:
            
            To get single page playbook rule from playbook `123str`
            
            >>>  self.{risksenseobject}.playbooks.get_single_page_playbook_rules('123str')
        """

        if page_size > 1000:
            raise PageSizeError("Page Size must be <= 1000")

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        params = {
            "size": page_size,
            "page": page_num,
            "sort": sort_dir
        }

        url = self.api_base_url.format(str(client_id)) + "/{}/rules".format(playbook_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_all_rules_for_playbook(self, playbook_uuid:str, sort_dir:str=SortDirection.ASC,csvdump:bool=False, client_id:int=None)->list:

        """
        Get all rules for a specific playbook

        Args:
            playbook_uuid:   Playbook UUID

            sort_dir:        Sort Direction

            csvdump:         dumps the data in csv

            client_id:       Client ID
        Return:
          All playbook rules
        
        Example:

            To get all rules for playbook `123str`

            >>>  self.{risksenseobject}.playbooks.get_all_rules_for_playbook('123str')
        Note:
            You can also dump the data using :obj:`csvdump=True` argument

            >>>  self.{risksenseobject}.playbooks.get_all_rules_for_playbook('123str',csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rules".format(playbook_uuid)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        page_size = 1000

        try:
            num_pages = self._get_playbook_page_info(url, page_size)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        page_range = range(0, num_pages)

        search_func_params = {
            "playbook_uuid": playbook_uuid,
            "page_size": page_size,
            "sort_dir": sort_dir,
            "client_id": client_id
        }
        
        try:
            all_rules = self._fetch_in_bulk(self.get_single_page_playbook_rules, page_range, **search_func_params)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        if csvdump==True:
            newdump=[]
            for i in all_rules:
                temp={}
                for key,value in i.items():
                    temp[key]=value
                    if key=='filter':
                        temp.pop('filter')
                    if key=='actionConfig':
                        temp.pop('actionConfig')
                    if key=='detailInfo':
                        temp.pop('detailInfo')
                newdump.append(temp)
            field_names = []
            for item in newdump[0]:
                field_names.append(item)
            try:
                with open('get_rules.csv', 'w',newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in newdump:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return all_rules

    def add_rule(self, playbook_uuid:str, rule_name:str, rule_desc:str, rule_input:str, rule_action_type:str,
                 rule_action:dict, rule_output:dict={},rule_output_type:str='NO_OUTPUT',email_subject:str='',email_message:str='',target_usernames:list=[],include_operational_summary:bool=False,csvdump:bool=False, client_id:int=None)->list:

        """
        Add a rule to a playbook.
        
        Args:
            playbook_uuid:       Playbook UUID

            rule_name:           Rule Name

            rule_desc:           Rule Description

            rule_input:          Rule Input

            rule_action_type:    Rule Action Type

            rule_action:         Rule action to take

            rule_output_type:    Rule output type, by default "NO_OUTPUT" but "EMAIL" can be provided , you must provide target_usernames,email_subject,email_message

            email_subject: Subject of the email to send if output type is EMAIL

            email_message: Message to be sent in email if output type is EMAIL

            target_usernames: The target risksense usernames to whom emails should be sent

            include_operational_summary: To include operational summary via email

            rule_output:         Rule output

            csvdump:         dumps the data in csv

            client_id:           Client ID
        Return:
         List containing dict of rule details.
        
        Example:
            To add a rule to a playbook

            >>>  self.{risksenseobject}.playbooks.add_rule('11ec58c8-123-123-a0b0-06933745a4d6','newtest',"testingsomethinghere","HOST_FINDING","ASSIGNMENT",{"userIds":[123],"filterRequest":{"filters":[{"field":"group_names","exclusive":False,"operator":"EXACT","value":"AdamM","orWithPrevious":False,"enabled":True,"implicitFilters":[],"altQueryConstruction":False},{"field":"lastFoundOn","exclusive":False,"operator":"BEFORE","value":"2021-01-28","orWithPrevious":False,"enabled":True,"implicitFilters":[],"altQueryConstruction":False}]}},"NO_OUTPUT",{})
        Note:
            You can also dump the data using :obj:`csvdump=True` argument

            >>>  self.{risksenseobject}.playbooks.add_rule('11ec58c8-123-123-a0b0-06933745a4d6','newtest',"testingsomethinghere","HOST_FINDING","ASSIGNMENT",{"userIds":[123],"filterRequest":{"filters":[{"field":"group_names","exclusive":False,"operator":"EXACT","value":"AdamM","orWithPrevious":False,"enabled":True,"implicitFilters":[],"altQueryConstruction":False},{"field":"lastFoundOn","exclusive":False,"operator":"BEFORE","value":"2021-01-28","orWithPrevious":False,"enabled":True,"implicitFilters":[],"altQueryConstruction":False}]}},"NO_OUTPUT",{},csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rule".format(playbook_uuid)

        if rule_output_type=='EMAIL':
            print('here')
            if target_usernames==[]:
                print('Please specify usernames.. Exiting')
                exit()
            if email_subject=='':
                print('Please specify email subject.. Exiting')
                exit()
            if email_message=='':
                print('Please specify email message.. Exiting')
                exit()
            rule_output={"targetUsernames":target_usernames,"subject":email_subject,"message":email_message,"includeOperationalSummary":include_operational_summary}
        body = {
            "name": rule_name,
            "description": rule_desc,
            "input": rule_input,
            "actionType": rule_action_type,
            "action": rule_action,
            "outputType": rule_output_type,
            "output": rule_output
        }
        print(body)
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        


        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            jobid={jsonified_response['name']:[jsonified_response['uuid']]}
            df=pd.DataFrame(jobid)
            df.to_csv('playbookruleuuid.csv')


        return jsonified_response

    def add_multiple_rules(self, playbook_uuid:str,rules:list,csvdump:bool=False, client_id:int=None)->list:

        """
        Add multiple rules to a playbook.

        Args:
            playbook_uuid:       Playbook UUID

            rules:           List of Rules the user want to create

            csvdump:         dumps the data in csv

            client_id:           Client ID
        Return:
            List containing dict of rule details.
        Example:
            To add multiple rules for a playbook
            
            >>>  self.{risksenseobject}.playbooks.add_multiple_rules('11ec8a6e-1234-123-9fb0-02a87de7e1ee',[
            {"name": "testnew2", "description": "test", "input": "HOST", "actionType": "TAG_APPLY", "action": {"tagIds": [], "isRemove": False, "filterRequest": {"filters": [{"field": "criticality", "exclusive": False, "operator": "IN", "value": "4", "orWithPrevious": False, "implicitFilters": [], "enabled": True}]}}, "outputType": "NO_OUTPUT", "output": {}},{"name": "testnew3", "description": "testing2", "input": "HOST", "actionType": "TAG_APPLY", "action": {"tagIds": [], "isRemove": False, "filterRequest": {"filters": [{"field": "criticality", "exclusive": False, "operator": "IN", "value": "4", "orWithPrevious": False, "implicitFilters": [], "enabled": True}]}}, "outputType": "NO_OUTPUT", "output": {}}])
        Note:
            You can also dump the data using :obj:`csvdump=True` argument

            >>>  self.{risksenseobject}.playbooks.add_multiple_rules('11ec8a6e-1234-123-9fb0-02a87de7e1ee',[
            {"name": "testnew2", "description": "test", "input": "HOST", "actionType": "TAG_APPLY", "action": {"tagIds": [], "isRemove": False, "filterRequest": {"filters": [{"field": "criticality", "exclusive": False, "operator": "IN", "value": "4", "orWithPrevious": False, "implicitFilters": [], "enabled": True}]}}, "outputType": "NO_OUTPUT", "output": {}},{"name": "testnew3", "description": "testing2", "input": "HOST", "actionType": "TAG_APPLY", "action": {"tagIds": [], "isRemove": False, "filterRequest": {"filters": [{"field": "criticality", "exclusive": False, "operator": "IN", "value": "4", "orWithPrevious": False, "implicitFilters": [], "enabled": True}]}}, "outputType": "NO_OUTPUT", "output": {}}],csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rules".format(playbook_uuid)

        body = {
            "rules": rules
        }

        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = ['uuid','name']
            data=[]
            for i in jsonified_response:
                data.append({'uuid':i['uuid'],'name':i['name']})
            try:
                with open('add_rules.csv', 'w',newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        for item in data:
                            writer.writerow(item)

            except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)


        return jsonified_response


    '''def add_rule_with_file(self, playbook_uuid:str, rule_name:str, rule_desc:str, rule_input:str, rule_action_type:str,
                           rule_action:dict, rule_output_type:str, rule_output:dict,csvdump:bool=False, file_name:str=None, file_path:str=None, client_id:int=None):

        """
        Add a rule to a playbook with a file.

        playbook_uuid:       Playbook UUID
        :type  playbook_uuid:       str

        rule_name:           Rule Name
        :type  rule_name:           str

        rule_desc:           Rule Description
        :type  rule_desc:           str

        rule_input:          Rule Input
        :type  rule_input:          str

        rule_action_type:    Rule Action Type
        :type  rule_action_type:    str

        rule_action:         Rule action to take
        :type  rule_action:         dict

        rule_output_type:    Rule output type
        :type  rule_output_type:    str

        rule_output:         Rule output
        :type  rule_output:         dict

        file_name:           Name to use for file you are uploading
        :type  file_name:           str

        file_path:           Path to file to be uploaded
        :type  file_path:           str

        client_id:           Client ID
        :type  client_id:           int

        csvdump:         dumps the data in csv
        :type  csvdump:         bool


        :return:    List containing dict of rule details.
        :rtype:     list

        :raises RequestFailed:
        :raises FileNotFoundError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rule/with-files".format(playbook_uuid)

        rule = {
            "name": rule_name,
            "description": rule_desc,
            "input": rule_input,
            "actionType": rule_action_type,
            "action": rule_action,
            "outputType": rule_output_type,
            "output": rule_output
        }

        multiformdata={"serializedPlaybookRule":(None,json.dumps(rule))}
        
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()
        
        if file_path and file_name !=None:
            try:
                multiformdata["files"]=(file_name,open(file_path, 'rb'))
            except FileNotFoundError as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiformdata)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            jobid={jsonified_response['name']:[jsonified_response['uuid']]}
            df=pd.DataFrame(jobid)
            df.to_csv('playbookruleuuid.csv')

        return jsonified_response

'''
    def create(self, name:str, description:str, schedule_freq:str, hour_of_day:str, client_id:int=None,csvdump:bool=False, **kwargs)->str:

        """
        Create a new playbook

        Args:
            name:            Name

            description:     Description

            schedule_freq:   Schedule Frequency (ScheduleFreq.DAILY, ScheduleFreq.WEEKLY,
                                                        ScheduleFreq.MONTHLY, 'DISABLED')

            hour_of_day:     Hour of the day

            client_id:       Client ID

            csvdump:         dumps the data in csv

        Keyword Args:

            day_of_week(``str``):   Day of the week
            day_of_month(``str``):  Day of the month

        Return:
          Playbook UUID

        Example:
            To create a playbook

            >>> self.{risksenseobject}.playbooks.create("teamtest1","test",self.rs.schedulefreq.DAILY,"5")
        Note:
            You can also dump the data in csv using :obj:`csvdump=True`
            
            >>> self.{risksenseobject}.playbooks.create("teamtest1","test",self.rs.schedulefreq.DAILY,"5",csvdump=True)

        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        day_of_week = kwargs.get("day_of_week", None)
        day_of_month = kwargs.get("day_of_month", None)

        body = {
            "name": name,
            "description": description,
            "schedule": {
                "type": schedule_freq,
                "hourOfDay": hour_of_day
            }
        }
        
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            supported_freqs = self.get_supported_frequencies(client_id)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        if schedule_freq not in supported_freqs:
            raise ValueError(f"schedule_freq should be one of {schedule_freq}")

        elif schedule_freq == ScheduleFreq.WEEKLY:
            if int(day_of_week) < 1 or int(day_of_week) > 7:
                raise ValueError("valid day_of_week (1-7) is required for a WEEKLY connector schedule.")
            body['schedule'].update(daysOfWeek=day_of_week)

        elif schedule_freq == ScheduleFreq.MONTHLY:
            if int(day_of_month) < 1 or int(day_of_month) > 31:
                raise ValueError("valid day_of_month (1-31) is required for a MONTHLY connector schedule.")
            body['schedule'].update(daysOfMonth=day_of_month)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
            


        jsonified_response = json.loads(raw_response.text)
        new_playbook_uuid = jsonified_response['uuid']

        if csvdump==True:
            jobid={'playbookuuid':[jsonified_response['uuid']]}
            df=pd.DataFrame(jobid)
            df.to_csv('playbookuuid.csv')

        return new_playbook_uuid

    def update(self, playbook_uuid:str, name:str, description:str, schedule_freq:str, hour_of_day:str,csvdump:bool=False, client_id:int=None, **kwargs)->dict:

        """
        Update a playbook

        Args:
            playbook_uuid:   Playbook UUID

            name:            Name

            description:     Description

            schedule_freq:   Schedule Frequency (ScheduleFreq.DAILY, ScheduleFreq.WEEKLY,
                                                        ScheduleFreq.MONTHLY, 'DISABLED')

            csvdump:         dumps the data in csv


            client_id:       Client ID

            hour_of_day:     Hour of the day
        
        Keyword Args:
             day_of_week(``str``):   Day of the week 
             day_of_month(``str``):  Day of the month 

        Return:
          Playbook and its details

        Example:
            To update a playbook

            >>> self.{risksenseobject}.playbooks.update('123456-3f1c-3b81-b7ab-06933745a4d6','testing2','somethingtotestrighthere',"DAILY",hour_of_day=5)
        Note:
            You can also dump the data in csv using :obj:`csvdump=True`
            
            >>> self.{risksenseobject}.playbooks.update('123456-3f1c-3b81-b7ab-06933745a4d6','testing2','somethingtotestrighthere',"DAILY",hour_of_day=5,csvdump=True)
        """


        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(playbook_uuid)

        day_of_week = kwargs.get("day_of_week", None)
        day_of_month = kwargs.get("day_of_month", None)

        body = {
            "name": name,
            "description": description,
            "schedule": {
                "type": schedule_freq,
                "hourOfDay": hour_of_day
            }
        }

        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            supported_freqs = self.get_supported_frequencies(client_id)
        except (RequestFailed, StatusCodeError, MaxRetryError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        if schedule_freq not in supported_freqs:
            raise ValueError(f"schedule_freq should be one of {schedule_freq}")

        elif schedule_freq == ScheduleFreq.WEEKLY:
            if int(day_of_week) < 1 or int(day_of_week) > 7:
                raise ValueError("valid day_of_week (1-7) is required for a WEEKLY connector schedule.")
            body['schedule'].update(daysOfWeek=day_of_week)

        elif schedule_freq == ScheduleFreq.MONTHLY:
            if int(day_of_month) < 1 or int(day_of_month) > 31:
                raise ValueError("valid day_of_month (1-31) is required for a MONTHLY connector schedule.")
            body['schedule'].update(daysOfMonth=day_of_month)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()


        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            jobid={jsonified_response['uuid']:[jsonified_response['name']]}
            df=pd.DataFrame(jobid)
            df.to_csv('playbookupdated.csv')

        return jsonified_response

    def delete(self, playbook_uuid:str,csvdump:bool=False, client_id:int=None)->bool:

        """
        Delete a playbook.

        Args:
            playbook_uuid:   playbook UUID

            csvdump:         dumps the data in csv

            client_id:       client ID
        
        Return:
          true/false indicating successful deletion

        Example:
            To delete a playbook

            >>> self.{risksenseobject}.playbooks.delete('123-123')
        
        Note:
            You can also dump the data in csv using :obj:`csvdump=True`

             >>> self.{risksenseobject}.playbooks.delete('123-123',csvdump=True)

        """

        deleted = False

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.api_base_url.format(str(client_id)) + "/{}".format(playbook_uuid)

        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            data={}
            for j,k in self.get_specific_playbook(playbook_uuid).items():
                data[j]=[k]
            df=pd.DataFrame(data)
            df.to_csv('playbookdeleted.csv',index=False)  

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
            if raw_response.status_code == 200:
                deleted = True
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        
  

        return deleted

    def get_playbook_details(self, playbook_uuid:str,csvdump:bool=False, client_id:int=None)->dict:

        """
        Get the details for a specific playbook

        Args:
            playbook_uuid:   playbook UUID

            client_id:       client ID

            csvdump:    Dump the data in a csv

        Return:
          Playbook details
        
        Example:
            To get playbook details

            >>> self.{risksenseobject}.get_playbook_details('123-123')
        
        Note:
            You can also dump the data in csv using :obj:`csvdump=True`

             >>> self.{risksenseobject}.get_playbook_details('123-123',csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(playbook_uuid)
        
        print()
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('getplaybookdetails.csv', 'w',newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)

        return jsonified_response

    def rule_reorder(self, playbook_uuid:str, rule_uuids:list, csvdump:bool=False,client_id:int=None)->list:

        """
        Reorder playbook rules for an already existing playbook

        Args:
        
            playbook_uuid:   UUID for playbook to be reordered

            rule_uuids:      A list of rule UUIDs (strings), in the order desired

            csvdump:         dumps the data in csv

            client_id:       Client ID

        Return:
          List of reordered rule definitions

        Example:
            To reorder the rules
        
            >>> self.{risksenseobject}.playbooks.rule_reorder('1234-87dc-353b-a0b0-06933745a4d6',["4321-10bc-3f1f-a0b0-06933745a4d6",'1234-1151-3d17-b7ab-06933745a4d6',"111-55bc-421a-b7ab-06933745a4d6","111-28fa-b4eb-b7ab-06933745a4d6","111-fa9b-e4ad-b7ab-06933745a4d6"])
        Note:
            You can also dump the reodered data in a csv using

             >>>  self.{risksenseobject}.playbooks.rule_reorder('1234-87dc-353b-a0b0-06933745a4d6',["4321-10bc-3f1f-a0b0-06933745a4d6",'1234-1151-3d17-b7ab-06933745a4d6',"111-55bc-421a-b7ab-06933745a4d6","111-28fa-b4eb-b7ab-06933745a4d6","111-fa9b-e4ad-b7ab-06933745a4d6"],csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rule-reorder".format(playbook_uuid)

        if type(rule_uuids) is not list:
            raise ValueError("rule_uuids should be a list of strings.")

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

            
        body = {
            "ruleUuids": rule_uuids
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = ['uuid','name']
            data=[]
            for i in jsonified_response:
                data.append({'uuid':i['uuid'],'name':i['name']})
            try:
                with open('rule_reorder.csv', 'w',newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        for item in data:
                            writer.writerow(item)
            except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return jsonified_response

    def update_rule(self, rule_uuid:str, playbook_name:str, playbook_desc:str, playbook_input:str, playbook_action_type:str,
                    playbook_action:dict, playbook_output_type:str, playbook_output:dict,csvdump:bool=False, client_id:int=None)->bool:

        """
        Update an existing playbook rule

        Args:
            rule_uuid:               UUID for rule to be updated

            playbook_name:           Playbook name

            playbook_desc:           Playbook description

            playbook_input:          Playbook Input

            playbook_action_type:    Playbook action type

            playbook_action:         Playbook action

            playbook_output_type:    Playbook output type

            playbook_output:         Playbook output

            csvdump:         dumps the data in csv

            client_id:               Client ID

        Return:
          Indication of success

        Example:
            To update a playbook rule

            >>> self.{risksenseobject}.playbooks.update_rule('11ec8ae5-73dd-c48c-9fb0-02a87de7e1ee',"namingconventionchanged","testnew2",  "HOST", "TAG_APPLY", {"tagIds": [], "isRemove": False, "filterRequest": {"filters": [{"field": "criticality", "exclusive": False, "operator": "IN", "value": "4", "orWithPrevious": False, "implicitFilters": [], "enabled": True}]}},"NO_OUTPUT", {})
        
        Note:
            You can also dump the data in csv using :obj:`csvdump=True` 
            
            >>> self.{risksenseobject}.playbooks.update_rule('11ec8ae5-73dd-c48c-9fb0-02a87de7e1ee',"namingconventionchanged","testnew2",  "HOST", "TAG_APPLY", {"tagIds": [], "isRemove": False, "filterRequest": {"filters": [{"field": "criticality", "exclusive": False, "operator": "IN", "value": "4", "orWithPrevious": False, "implicitFilters": [], "enabled": True}]}},"NO_OUTPUT", {},csvdump=True)

        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        print(client_id)


        url = self.api_base_url.format(str(client_id)) + "/rule/{}".format(rule_uuid)

        try:
            supported_inputs = self.get_supported_inputs(client_id=client_id)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        try:
            supported_action_types = self.get_supported_actions(client_id=client_id)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        try:
            supported_output_types = self.get_supported_outputs(client_id=client_id)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        if playbook_input not in supported_inputs:
            raise ValueError(f"playbook_input must be one of {supported_inputs}")

        if playbook_action_type not in supported_action_types:
            raise ValueError(f"playbook_action_type must be one of {supported_action_types}")

        if playbook_output_type not in supported_output_types:
            raise ValueError(f"playbook_output_type must be one of {supported_action_types}")
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        body = {
            "name": playbook_name,
            "description": playbook_desc,
            "input": playbook_input,
            "actionType": playbook_action_type,
            "action": playbook_action,
            "outputType": playbook_output_type,
            "output": playbook_output
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)

        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        if csvdump==True:
            self.get_specific_playbook_rule(rule_uuid=rule_uuid,csvdump=True)
        if raw_response.status_code == 200:
            return True

    def delete_playbook_rule(self, rule_uuid:str,csvdump:bool=False, client_id:int=None)->bool:

        """
        Delete an existing playbook rule.

        Args:
            rule_uuid:   Rule UUID

            csvdump:         dumps the data in csv

            client_id:   Client ID
        Return:
          Indication of success

        Example:
            To delete a playbook rule

            >>> self.{risksenseobject}.playbooks.delete_playbook_rule('1234-6fb3-206e-9fb0-02a87de7e1ee')
        Note:
            You can also dump the data in csv using :obj:`csvdump=True` 
            
            >>> self.{risksenseobject}.playbooks.delete_playbook_rule('1234-6fb3-206e-9fb0-02a87de7e1ee',csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/rule/{}".format(rule_uuid)

        if csvdump==True:
            self.get_specific_playbook_rule(rule_uuid=rule_uuid,csvdump=True)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
            if raw_response.status_code == 200:
                return True
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

    def get_specific_playbook_rule(self, rule_uuid:str,csvdump:bool=False, client_id:int=None)->dict:

        """
        Get details for a specific playbook rule.

        Args:
            rule_uuid:   Playbook rule UUID

            client_id:   Client ID

            csvdump:         dumps the data in csv
        Return:
          Playbook rule details

        Example:
            To get specific playbook rule

            >>> self.{risksenseobject}.playbooks.get_specific_playbook_rule('123456-73dd-c48c-9fb0-02a87de7e1ee')

        Note:
            You can also dump the data in csv using :obj:`csvdump=True` 
            
            >>> self.{risksenseobject}.playbooks.get_specific_playbook_rule('123456-73dd-c48c-9fb0-02a87de7e1ee',csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/rule/{}".format(rule_uuid)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('getruledetails.csv', 'w',newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)

        return jsonified_response


    def toggle_enabled(self, playbook_uuids:list, enabled:bool=False, client_id:int=None):

        """
        Enable/Disable playbooks.

        Args:
            playbook_uuids:  A list of Playbook UUIDs to enable/disable

            enabled:         Enable/Disable playbooks,please provide true for enabled and false for disabled

            client_id:       Client ID

        Return:
          True

        Example:
            To enable a playbook

            >>> self.{risksenseobject}.playbooks.toggle_enabled(['11ed13b4-52c3-a3c1-9fb0-02a87de7e1ee'],enabled=True)

            To disable a playbook

            >>> self.{risksenseobject}.playbooks.toggle_enabled(['11ed13b4-52c3-a3c1-9fb0-02a87de7e1ee'],enabled=False)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/toggle-enabled"


        body = {
            "playbookUuids": playbook_uuids,
            "enabled": enabled
        }

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
            if raw_response.status_code==200:
                success= True
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()


        return success

    def run_playbook(self, playbook_uuid:str,csvdump:bool=False, client_id:int=None)->dict:

        """
        Run a playbook.

        Args:
            playbook_uuid:   Playbook UUID

            client_id:       Client ID

            csvdump:         dumps the data in csv

        Return:
          JSON response from platform

        Example:

            >>> self.{risksenseobject}.playbooks.run_playbook('12345-1234-123')

        Note:
            You can also dump the data in csv using :obj:`csvdump=True` 
            
            >>> self.{risksenseobject}.playbooks.run_playbook('12345-1234-123',csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/run".format(playbook_uuid)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('playbookrunning.csv', 'w',newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)

        return jsonified_response

    ##### BEGIN PRIVATE FUNCTIONS #####################################################################################

    def _get_playbook_page_info(self, url:str, page_size:int)->int:

        """
        Get number of available pages for fetch.

        Args:
            url:         URL of endpoint
            page_size:   page size

        Return:
           Total number of available pages
        
        
        **IGNORE function as it is an Internal Function*** 

        """

        params = {
            "size": page_size
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        total_pages = jsonified_response['totalPages']

        return total_pages

    def _fetch_in_bulk(self, func_name:str, page_range:int, **func_args)->list:

        """
        Threaded fetch of playbook info, supporting multiple threads.
        Combines all results in a single list and returns.


        Args:
            func_name:   Search function name

            page_range:  Page range

        *IGNORE - INTERNAL FUNCTION*
        
        Keyword Args:
            func_args(``dict``):   args to be passed to search function

        Return:
          List of all results returned by search function

        """
        all_results = []
        prog_bar = None

        if 'page_num' in func_args:
            func_args = func_args.pop('page_num')

        if self.profile.use_prog_bar:
            try:
                max_val = (max(page_range) + 1)
            except ValueError:
                max_val = 1

            prog_bar = progressbar.ProgressBar(max_value=max_val)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.profile.num_thread_workers) as executor:
            counter = 1
            future_to_page = {executor.submit(func_name, page_num=page, **func_args): page for page in page_range}

            for future in concurrent.futures.as_completed(future_to_page):
                try:
                    data = future.result()
                except PageSizeError:
                    raise
                except RequestFailed:
                    continue

                if 'content' in data:
                    items = data['content']
                    for item in items:
                        all_results.append(item)

                if self.profile.use_prog_bar:
                    prog_bar.update(counter)
                    time.sleep(0.1)
                    counter += 1

        if self.profile.use_prog_bar:
            prog_bar.finish()
        return all_results

    '''def delete_file_from_rule(self, rule_uuid, file_uuid, client_id=None):

        """
        Delete a file from a playbook rule

        rule_uuid:   Playbook rule UUID
        :type  rule_uuid:   str

        file_uuid:   File UUID
        :type  file_uuid:   str

        client_id:   Client ID
        :type  client_id:   int

        :return:    Indicator of deletion success
        :rtype:     bool

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/rule/{}/file/{}".format(rule_uuid, file_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
            if raw_response.status_code == 204:
                return True
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

    def download_file_from_rule(self, rule_uuid, file_uuid, file_destination, client_id=None):

        """
        Download a file from an existing playbook rule.

        rule_uuid:           Rule UUID
        :type  rule_uuid:           str

        file_uuid:           File UUID
        :type  file_uuid:           str

        file_destination:    File destination path
        :type  file_destination:    str

        client_id:           Client ID
        :type  client_id:           int

        :return:    Indicator of download success
        :rtype:     bool

        :raises RequestFailed:
        :raises FileNotFoundError:
        :raises FileExistsError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/rule/{}/file/{}".format(rule_uuid, file_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
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

    def attach_file_to_rule(self, rule_uuid, file_name, file_path, client_id=None):

        """
        Attach a file to an existing rule.

        rule_uuid:   Playbook rule UUID
        :type  rule_uuid:   str

        file_name:   Name for uploaded file
        :type  file_name:   str

        file_path:   Path to file to be uploaded
        :type  file_path:   str

        client_id:   Client ID
        :type  client_id:   int

        :return:    JSONified response from platform
        :rtype:     dict

        :raises RequestFailed:
        :raises FileNotFoundError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/rule/{}/file".format(rule_uuid)
        
        upload_file = {'files': (file_name, open(file_path, 'rb'))}
        print(upload_file)
        try:    
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=upload_file)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response'''



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
