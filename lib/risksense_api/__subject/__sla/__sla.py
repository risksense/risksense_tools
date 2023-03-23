"""
**Sla module defined for different sla related api endpoints.**
"""
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
import sched
from ..__subject import Subject
from ..._params import *
from ..._api_request_handler import *
import csv
import pandas as pd

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
    """Types of sla offset basis"""
    VRR       = "VRR"
    SEVERITY  = "SEVERITY"

class Sla(Subject):

    """ Sla class """

    """ **Class for Sla function defintions**.

    To utlise sla function:

    Args:
            profile:     Profile Object
    
    Usage:
        :obj:`self.{risksenseobjectname}.sla.{function}`
        
    
    Examples:
        To get sla rules use :meth:`getslarules()` function

        >>> self.{risksenseobject}.sla.getslarules({args})

    """

    def __init__(self, profile:object):

        """
        Initialization of sla object.

        Args:
            profile:     Profile Object
        """

        self.subject_name = "sla"
        Subject.__init__(self, profile, self.subject_name)

    def create_sla(self,description:str,schedule_type:str='DAILY',hourofday:int=12,name:str='Remediation SLAs',csvdump:bool=False,client_id:int=None,**kwargs)->str:
        
        """
        Creates an sla

        Args:
            name:                    Name of playbook,note for system sla please mention Remediation SLAs

            description:             Provide description for sla
                
            schedule_type:   Schedule Frequency (ScheduleFreq.DAILY, ScheduleFreq.WEEKLY,
                                                        ScheduleFreq.MONTHLY, 'DISABLED')

            hourofday:     Hour of the day
            
            csvdump:         dumps the data in csv
            
            client_id:       Client ID
            
            Keyword Args:
                day_of_week(``str``):   Day of the week
                day_of_month(``str``):  Day of the month

        Return:
          Playbook UUID

        Example:
            To create a remediation sla

            >>> self.{risksenseobject}.sla.create_sla('remediation sla')
        Note:
            You can also dump the data in csv using :obj:`csvdump=True`
            
            >>> self.{risksenseobject}.sla.create_sla('remediation sla',csvdump=True)

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
                "type": schedule_type,
                "hourOfDay": hourofday
            },
            "type":"System"
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        elif schedule_type == ScheduleFreq.WEEKLY:
            if int(day_of_week) < 1 or int(day_of_week) > 7:
                raise ValueError("valid day_of_week (1-7) is required for a WEEKLY connector schedule.")
            body['schedule'].update(daysOfWeek=day_of_week)

        elif schedule_type == ScheduleFreq.MONTHLY:
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

     
    def getslarules(self,playbookuuid:str,csvdump:bool=False,client_id:int=None)->list:

        """
        Get a list of all sla rules for an sla.

        Args:
            playbookuuid:  Uuid of the playbook to fetch sla

            csvdump:         dumps the data in csv


            client_id:   Client ID, if no client id provided , gets default client id

        Return:
           Sla rules

        Example:
            To get list of all sla rules
            
            >>> self.{risksenseobject}.sla.getslarules('11ed05cb-e7a0-4f25-b7ab-06933745a4d6')
        Note:
            You can also dump the data in csv using :obj:`csvdump=True`
            
            >>> self.{risksenseobject}.sla.getslarules('11ed05cb-e7a0-4f25-b7ab-06933745a4d6',csvdump=True)

        """


        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rules".format(playbookuuid)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        if csvdump==True:
            field_names = []
            newdump=[]
            for i in jsonified_response['content']:
                temp={}
                for j,k in i.items():
                    temp[j]=k
                    if j=='filter':
                        temp.pop('filter')
                    if j=='actionConfig':
                        temp.pop('actionConfig')
                    if j=='detailInfo':
                        temp['slatype']=k['type']
                        temp['groupNames']=','.join(k['groupNames'])
                        temp['impacted_asset_count']=k['impactedMetrics']['asset_count']
                        temp['impacted_finding_count']=k['impactedMetrics']['finding_count']
                        temp.pop('detailInfo')
                newdump.append(temp)
            for item in newdump[0]:
                field_names.append(item)
            try:
                with open('slarules.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in newdump:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response

    def getallslas(self,csvdump:bool=False,client_id:int=None)->dict:

        """
        Gets all slas for a particular client.

        Args:
            csvdump:         dumps the data in csv

            client_id:   Client ID, if no client id provided , gets default client id
        Return:
            To get all slas
        
        Example:
            To get all slas

            >>> self.{risksenseobject}.getallslas()

        Note:
            You can also dump the data in csv using :obj:`csvdump=True`
            
            >>> self.{risksenseobject}.getallslas(csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/fetch"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            newdump=[]
            for i in jsonified_response['content']:
                temp={}
                for j,k in i.items():
                    temp[j]=k
                    if j=='filter':
                        temp.pop('filter')
                    if j=='actionConfig':
                        temp.pop('actionConfig')
                    if j=='detailInfo':
                        temp['slatype']=k['type']
                        temp['groupNames']=','.join(k['groupNames'])
                        temp['impacted_asset_count']=k['impactedMetrics']['asset_count']
                        temp['impacted_finding_count']=k['impactedMetrics']['finding_count']
                        temp.pop('detailInfo')
                newdump.append(temp)
            field_names = []
            for item in newdump[0]:
                field_names.append(item)
            try:
                with open('allslas.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in newdump:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response

    def delete_sla(self,sla_uuid:str,csvdump:bool=False,client_id:int=None)->bool:

        """
        Delete a particular sla

        Args:
            sla_uuid:   UUID of sla

            csvdump:         dumps the data in csv

            client_id:   Client ID, if no client id provided , gets default client id
        Return:
             Success
        Example:

            >>> self.{risksenseobject}.sla.delete_sla('1234-123-9f18-b7ab-06933745a4d6')
        Note:
            You can also dump the data in csv using :obj:`csvdump=True`
            
            >>> self.{risksenseobject}.sla.delete_sla('1234-123-9f18-b7ab-06933745a4d6')
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url  = self.api_base_url.format(str(client_id)) +"/{}".format(sla_uuid)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.get_specified_sla(playbookuuid=sla_uuid,csvdump=True)

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
            if raw_response.status_code==200:
                success=True
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return success

    def get_sla_rule(self,playbookrulepairinguuid:str,csvdump:bool=False,client_id:int=None)->dict:

        """
        Gets all sla rules for a particular client.

        Args:

            playbookrulepairinguuid:           Playbook rule pairing uuid

            csvdump:         dumps the data in csv

            client_id:   Client ID, if no client id provided , gets default client id

        Return:
            SLA details

        Example:
            To get all sla rules

            >>> self.{risksenseobject}.sla.get_sla_rule('12334-123-3bb6-9564-dbbe539b1a74')
        
        Note:
            You can also dump the data in csv using :obj:`csvdump=True`
            
            >>> self.{risksenseobject}.sla.get_sla_rule('187914ba-b06e-3bb6-9564-dbbe539b1a74',csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.api_base_url.format(str(client_id)) + "/rule/{}".format(playbookrulepairinguuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
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
                with open('sla_rule_data.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        
        return jsonified_response


    def get_specified_sla(self,playbookuuid:str,csvdump:bool=False,client_id:int=None)->dict:

        """
        Gets a specified sla for a particular client.

        Args:
            playbookuuid:         UUID of playbook

            csvdump:         dumps the data in csv

            client_id:   Client ID, if no client id provided , gets default client id

        Return:
            Specific sla data
        
        Example:
            To get specific sla 

           >>> self.{risksenseobject}.sla.get_specified_sla('12345st-123-4f25-b7ab-06933745a4d6')
        
        Note:
            You can also dump the data in csv using :obj:`csvdump=True`
            
           >>> self.{risksenseobject}.sla.get_specified_sla('11ed05cb-e7a0-4f25-b7ab-06933745a4d6',csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/fetch/{}".format(playbookuuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            print('Sla details saved in the csv file get_specified_sla')
            field_names = []
           
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('specified_sla.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)


        return jsonified_response


    def get_sla_details(self,playbookuuid:str,csvdump:bool=False,client_id:int=None)->dict:

        """
        Get details of a particular sla playbook.

        Args:
            playbookuuid:   SLA Playbook uuid

            csvdump:         dumps the data in csv

            client_id:       Client ID, if no client id provided , gets default client id
        Return:
           Returns the sla playbook details
        Example:
            To get sla details

            >>> self.{risksenseobject}.sla.get_sla_details('11ed05cb-e7a0-4f25-b7ab-06933745a4d6')
        
        Note:
            You can also dump the data in csv using :obj:`csvdump=True`
            
            >>> self.{risksenseobject}.sla.get_sla_details('11ed05cb-e7a0-4f25-b7ab-06933745a4d6',csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+"/{}".format(playbookuuid)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
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
                with open('sladetails.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response
        
    def add_default_sla_rule(self, sla_uuid:str, description:str, priority:int,
                     timeReference:str=TimeReference.DISCOVERED_DATE, serviceLevelAgreementMatrix:str=SlaMatrix.STANDARD,slaMatrixProfileType:str=SlaMatrixProfileType.STANDARD,offsetBasis:str=offsetbasis.VRR,affectOnlyNewFindings:bool=True,updateSLAIfVRRUpdates:bool=True,inputdata:str="HOST_FINDING",actionType:str=SlaActionType.REMEDIATION_SLA,csvdump:bool=False,client_id:int=None)->list:
        
        """
        Adds default rule to existing sla playbook.Works only if there is no default rule applied to the playbook

        Args:
            sla_uuid:                Sla UUID

            description:             Provide description for the default sla rule, 

            priority:                Priority to be provided to default sla rule , 
                                            note: default sla priority should be a greater number than the group sla rules

            timeReference:           Timereference to be provided to default sla rule , 

            serviceLevelAgreementMatrix :               Provide slamatrix for the particular sla

            slaMatrixProfileType :    Provide sla matrix type for the sla

            offsetBasis:            Provide offset basis for particular sla

            affectOnlyNewFindings :  Choose whether it affects new findings

            updateSLAIfVRRUpdates:   Choose if slaupdates with vrr

            inputdata:               Type of data provided for sla

            actionType:              Type of action for particular sla

            csvdump:         dumps the data in csv

            client_id:               Client ID , if no client id provided , takes default client id

            action_type:             Action type for the particular sla rule,by default remediation rule is provided
        Return:
              List containing dict of rule details.

        Example:

            To add default sla rule

            >>> self.{risksenseobject}.add_default_sla_rule('11ed13e6-a1aa-5c28-9fb0-02a87de7e1ee','testing',3)
        Note:
            You can also change the default time Reference or service Level Agreement Matrix or other default arguments

            You can also dump the data in csv using :obj:`csvdump=True`
            
            >>> self.{risksenseobject}.add_default_sla_rule('11ed13e6-a1aa-5c28-9fb0-02a87de7e1ee','testing',3,csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rule".format(sla_uuid)

        body={"name":'Default SLA',"description":description,"priority":priority,"supplementalFilterRequest":None,"actionType":actionType,"action":{ "isDefaultSLA":True,"targetGroupIds":[],"timeReference":timeReference,"serviceLevelAgreementMatrix":serviceLevelAgreementMatrix,"slaMatrixProfileType":slaMatrixProfileType,"offsetBasis":offsetBasis,"affectOnlyNewFindings":affectOnlyNewFindings,"updateSLAIfVRRUpdates":updateSLAIfVRRUpdates},"outputType":"NO_OUTPUT","output":{},"input":inputdata}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()


        jsonified_response = json.loads(raw_response.text)
        
        if csvdump==True:
            data={'uuid':jsonified_response[0]['uuid'],'name':jsonified_response[0]['name'],'description':jsonified_response[0]['description']}
            field_names = ['uuid','name','description']
            try:
                with open('defaultslarulecreated.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(data)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response
    
    def update_default_sla_rule(self, playbookrulepairinguuid:str, description:str, priority:int,
                     timeReference:str=TimeReference.DISCOVERED_DATE, serviceLevelAgreementMatrix:dict=SlaMatrix.STANDARD,slaMatrixProfileType:str=SlaMatrixProfileType.STANDARD,offsetBasis:str=offsetbasis.VRR,affectOnlyNewFindings:bool=True,updateSLAIfVRRUpdates:bool=True,inputdata:str="HOST_FINDING",actionType:str=SlaActionType.REMEDIATION_SLA,csvdump:bool=False,client_id:int=None)->list:
        
        """
        Updates default rule to existing sla playbook.

        Args:
            playbookrulepairinguuid:      Playbook rule pairing uuid

            description:             Provide description for the default sla rule, 

            priority:                Priority to be provided to default sla rule , 
                                            note: default sla priority should be a greater number than the group sla rules

            timeReference :           Timereference to be provided to default sla rule , 

            serviceLevelAgreementMatrix:               Provide slamatrix for the particular sla

            slaMatrixProfileType :    Provide sla matrix type for the sla

            offsetBasis :            Provide offset basis for particular sla

            affectOnlyNewFindings :  Choose whether it affects new findings

            updateSLAIfVRRUpdates:   Choose if slaupdates with vrr

            inputdata:               Type of data provided for sla

            actionType:              Type of action for particular sla

            csvdump:         dumps the data in csv

            client_id:               Client ID , if no client id provided , takes default client id

        Return:
              List containing dict of rule details.

        Example:

            To update default sla rule

            >>> self.{risksenseobject}.update_default_sla_rule('11ed13e6-a1aa-5c28-9fb0-02a87de7e1ee','testing',3)
        Note:
            You can also change the default time Reference or service Level Agreement Matrix or other default arguments

            You can also dump the data in csv using :obj:`csvdump=True`
            
            >>> self.{risksenseobject}.update_default_sla_rule('11ed13e6-a1aa-5c28-9fb0-02a87de7e1ee','testing',3,csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url  = self.api_base_url.format(str(client_id)) +"/rule/{}".format(playbookrulepairinguuid)
        

        body={"name":'Default SLA',"description":description,"priority":priority,"supplementalFilterRequest":None,"actionType":actionType,"action":{ "isDefaultSLA":True,"targetGroupIds":[],"timeReference":timeReference,"serviceLevelAgreementMatrix":serviceLevelAgreementMatrix,"slaMatrixProfileType":slaMatrixProfileType,"offsetBasis":offsetBasis,"affectOnlyNewFindings":affectOnlyNewFindings,"updateSLAIfVRRUpdates":updateSLAIfVRRUpdates},"outputType":"NO_OUTPUT","output":{},"input":inputdata}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()


        jsonified_response = json.loads(raw_response.text)
        
        if csvdump==True:
            data={'uuid':jsonified_response[0]['uuid'],'name':jsonified_response[0]['name'],'description':jsonified_response[0]['description']}
            field_names = ['uuid','name','description']
            try:
                with open('defaultslaruleupdated.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(data)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response

    def add_group_sla_rule(self, sla_uuid:str, name:str, description:str, priority:int, targetgroupids:list,
                     timeReference:str=TimeReference.DISCOVERED_DATE, serviceLevelAgreementMatrix:dict=SlaMatrix.STANDARD,slaMatrixProfileType:str=SlaMatrixProfileType.STANDARD,offsetBasis:str=offsetbasis.VRR,affectOnlyNewFindings:bool=True,updateSLAIfVRRUpdates:bool=True,inputdata:str="HOST_FINDING",actionType:str=SlaActionType.REMEDIATION_SLA,csvdump:bool=False,client_id:int=None)->list:
        
        """
        Adds group rule to existing sla playbook for the groups specified.

        Args:
            sla_uuid:                Sla UUID

            name:                    Name of the group specific sla rule

            description:             Provide description for the group specific sla rule, 

            priority:                Priority to be provided to group speicifc sla , 
                                            note: group sla priority should be a lesser number than the default sla rule

            targetgroupids:          The groups ids where the sla applies

            timeReference :           Timereference to be provided to default sla rule , 

            serviceLevelAgreementMatrix:               Provide slamatrix for the particular sla

            slaMatrixProfileType:    Provide sla matrix type for the sla

            offsetBasis:            Provide offset basis for particular sla

            affectOnlyNewFindings :  Choose whether it affects new findings

            updateSLAIfVRRUpdates:   Choose if slaupdates with vrr

            inputdata:               Type of data provided for sla

            actionType:              Type of action for particular sla

            csvdump:                 Dumps data to csv
            
            client_id:               Client ID , if no client id provided , takes default client id
        
        Return:
              List containing dict of rule details.
        Example:
            
            >>> self.{risksenseobject}.sla.add_group_sla_rule(sla_uuid='12345st-123-5c28-9fb0-02a87de7e1ee',name='testingnew',description='testingnew',targetgroupids=[],priority=2)
        
        Note:

            You can also change the default time Reference or service Level Agreement Matrix or other default arguments

            You can also dump the data in csv using :obj:`csvdump=True`
            
            >>> self.{risksenseobject}.sla.add_group_sla_rule(sla_uuid='12345st-123-5c28-9fb0-02a87de7e1ee',name='testingnew',description='testingnew',targetgroupids=[],priority=2,csvdump=True)

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) +"/{}/rule".format(sla_uuid)

        body={"name":name,"description":description,"priority":priority,"supplementalFilterRequest":None,"actionType":actionType,"action":{"isDefaultSLA":False,"targetGroupIds":targetgroupids,"timeReference":timeReference,"serviceLevelAgreementMatrix":serviceLevelAgreementMatrix,"slaMatrixProfileType":slaMatrixProfileType,"offsetBasis":offsetBasis,"affectOnlyNewFindings":affectOnlyNewFindings,"updateSLAIfVRRUpdates":updateSLAIfVRRUpdates},"outputType":"NO_OUTPUT","output":{},"input":inputdata}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            data={'uuid':jsonified_response[0]['uuid'],'name':jsonified_response[0]['name'],'description':jsonified_response[0]['description']}
            field_names = ['uuid','name','description']
            try:
                with open('groupslarulecreated.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(data)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response


    def update_group_sla_rule(self, playbookrulepairinguuid:str, name:str, description:str, priority:int, targetgroupids:list,
                     timeReference:str=TimeReference.DISCOVERED_DATE, serviceLevelAgreementMatrix:dict=SlaMatrix.STANDARD,slaMatrixProfileType:str=SlaMatrixProfileType.STANDARD,offsetBasis:str=offsetbasis.VRR,affectOnlyNewFindings:bool=True,updateSLAIfVRRUpdates:bool=True,inputdata:str="HOST_FINDING",actionType:str=SlaActionType.REMEDIATION_SLA,csvdump:bool=False,client_id:int=None)->list:
        
        """
        Updates a group sla rule for an already existing playbook

        Args:
            playbookrulepairinguuid:           Playbook rule pairing uuid

            name:                    Name of the group specific sla rule

            description:             Provide description for the group specific sla rule, 

            priority:                Priority to be provided to group speicifc sla , 
                                            note: group sla priority should be a lesser number than the default sla rule

            targetgroupids:          The groups ids where the sla applies

            timeReference:           Timereference to be provided to default sla rule , 

            serviceLevelAgreementMatrix:               Provide slamatrix for the particular sla

            slaMatrixProfileType:    Provide sla matrix type for the sla

            offsetBasis:            Provide offset basis for particular sla

            affectOnlyNewFindings :  Choose whether it affects new findings

            updateSLAIfVRRUpdates:   Choose if slaupdates with vrr

            inputdata:               Type of data provided for sla

            actionType:              Type of action for particular sla

            csvdump:         dumps the data in csv

            client_id:               Client ID , if no client id provided , takes default client id

            action_type:             Action type for the particular sla rule,by default remediation rule is provided
        
        Return:
               List containing dict of rule details.
        Example:

            To update group sla rule

            >>> self.{risksenseobject}.sla.update_group_sla_rule('12345st-123-5c28-9fb0-02a87de7e1ee','testingnew','testingnew',[],2)
        
        Note:

            You can also change the default time Reference or service Level Agreement Matrix or other default arguments

            You can also dump the data in csv using :obj:`csvdump=True`
            
            >>> self.{risksenseobject}.sla.update_group_sla_rule('12345st-123-5c28-9fb0-02a87de7e1ee','testingnew','testingnew',[],2,csvdump=True)
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url  = self.api_base_url.format(str(client_id)) +"/rule/{}".format(playbookrulepairinguuid)

        body={"name":name,"description":description,"priority":priority,"supplementalFilterRequest":None,"actionType":actionType,"action":{"isDefaultSLA":False,"targetGroupIds":targetgroupids,"timeReference":timeReference,"serviceLevelAgreementMatrix":serviceLevelAgreementMatrix,"slaMatrixProfileType":slaMatrixProfileType,"offsetBasis":offsetBasis,"affectOnlyNewFindings":affectOnlyNewFindings,"updateSLAIfVRRUpdates":updateSLAIfVRRUpdates},"outputType":"NO_OUTPUT","output":{},"input":inputdata}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            data={'uuid':jsonified_response[0]['uuid'],'name':jsonified_response[0]['name'],'description':jsonified_response[0]['description']}
            field_names = ['uuid','name','description']
            try:
                with open('groupslaruleupdated.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(data)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response


    def del_group_sla_rule(self,playbookuuid:str,client_id:int=None)->bool:
        
        """
        Deletes a particular group sla rule.

        Args:
            client_id:   Client ID, if no client id provided , gets default client id

            playbookuuid: The playbookuuid that needs to be deleted

        Return:
            Returns json of deleted rule

        Example:
            Delete group sla rule

            >>> self.{risksenseobject}.sla.del_group_sla_rule('123-123')
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.api_base_url.format(str(client_id)) +"/rule/{}".format(playbookuuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        Success=True

        return Success 
    
    def change_order(self,slauuid:str,ruleuuids:list,csvdump:bool=False,client_id:int=None)->list:

        """
        Changes the order of the sla rules

        Args:
            client_id:   Client ID, if no client id provided , gets default client id

            slauuid: The sla where rules needs to be reordered

            ruleuuids: The order of rules reordering
            
            csvdump:         dumps the data in csv
        Return:
            Returns the reordered rule json

        Example:

            >>>  self.rs.sla.change_order('123-4567-f4cb-b7ab-06933745a4d6',["97abc-123-3bc0-b606-98aed43c944a"])

        Note:

            You can also dump the data in csv using :obj:`csvdump=True`
            
            >>>  self.rs.sla.change_order('123-4567-f4cb-b7ab-06933745a4d6',["97abc-123-3bc0-b606-98aed43c944a"],csvdump=True) 
           
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) +"/{}/rule-reorder".format(slauuid)

        body={"ruleUuids":ruleuuids}
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
            if raw_response.status_code==200:
                success=True
        except RequestFailed as e:
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

        return success
   
    def sla_run(self,slauuid:str,csvdump:bool=False,client_id:int=None)->dict:

        """
        Runs the sla

        Args:
            client_id:   Client ID, if no client id provided , gets default client id
            slauuid: The sla rule that needs to be run
            csvdump: Dumps the data in csv
        
        Return:
            Returns the json of sla

        Example:

            >>> self.{risksenseobject}.sla.sla_run('12345-123ea-4f25-b7ab-06933745a4d6')
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) +"/{}/run".format(slauuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET,url)
        except RequestFailed as e:
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
                with open('slarun.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        return jsonified_response
   
    def update_sla(self, sla_uuid:str,description:str,schedule_type:str='DAILY',hourofday:int=0,dayofmonth:str='4',dayofweek:str='5',name:str="Remediation SLAs",type:str='System',csvdump:bool=False,client_id=None,**kwargs):
        
        """
        Updates an sla

        Args:
            sla_uuid:                Sla UUID

            name:                    Name of the 

            description:             Provide description for sla 

            schedule_type:   Schedule Frequency (ScheduleFreq.DAILY, ScheduleFreq.WEEKLY,
                                                        ScheduleFreq.MONTHLY, 'DISABLED')

            type: The type of sla , can be 'SYSTEM' or 'USER'

            hourofday:     Hour of the day

            dayofmonth : Day of the month

            dayofweek: Day of the week

            csvdump:         dumps the data in csv

            client_id:               Client ID , if no client id provided , takes default client id
        Return:
            List containing dict of playbook details.
        Example:

            >>> self.{risksenseobject}.sla.update_sla('1234-1234abc-bfc0-b7ab-06933745a4d6','remediation sla','Testingviascript')
        
        Note:

            You can also dump the data in csv using :obj:`csvdump=True`
            
            >>> self.{risksenseobject}.sla.update_sla('1234-1234abc-bfc0-b7ab-06933745a4d6','remediation sla','Testingviascript',csvdump=True)
        """
        if schedule_type.upper()=='DAILY':
            schedule={
                'type':'DAILY',
                "hourOfDay":hourofday
            }
        if schedule_type.upper()=='WEEKLY':
            schedule={
                'type':'WEEKLY',
                "hourOfDay":hourofday,
                'daysOfWeek':dayofweek
            }
        if schedule_type.upper()=='MONTHLY':
            schedule={
                'type':'MONTHLY',
                "hourOfDay":hourofday,
                'daysOfMonth':dayofmonth
            }

        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) +"/{}".format(sla_uuid)

        body={
                "name": name,
                "description": description,
                "schedule": schedule,
                "type": type
                }


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
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
                with open('slaupdate.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)


        return jsonified_response
     
    def disablesla(self,playbookuuid:str,client_id:int=None)->bool:

        """
        Disables a particular sla rule.

        Args:
            playbookuuid: The playbookuuids that needs to be disabled

            client_id:   Client ID, if no client id provided , gets default client id

        Return:
            Returns json of disable sla

        Example:
            
            >>> self.{risksenseobject}.sla.disablesla(['11ed05cb-e7a0-4f25-b7ab-06933745a4d6'])
        
        """


        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/toggle-enabled"

        body={"playbookUuids":playbookuuid,"enabled":False}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        Success=True
        jsonified_response = json.loads(raw_response.text)

        return Success

    def enablesla(self,playbookuuid:list,client_id:int=None)->bool:
        """
        Enables a particular sla rule.

        Args:
            playbookuuid: The playbookuuids that needs to be enabled

            client_id:   Client ID, if no client id provided , gets default client id

        Return:
            success

        Example:
            
            >>> self.{risksenseobject}.sla.enablesla(['11ed05cb-e7a0-4f25-b7ab-06933745a4d6'])
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/toggle-enabled"
        body={"playbookUuids":playbookuuid,"enabled":True}
        print(url)
        print(body)
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
            if raw_response.status_code==200:
                success=True
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        print(raw_response)
        jsonified_response = json.loads(raw_response.text)
        return success  

    def getplaybookslarules(self,slaid:int,client_id:int=None)->dict: 

        """
        Gets sla playbook rules for a particular sla.

        Args:
            slaid:       Slaid to get the sla rules

            client_id:   Client ID, if no client id provided , gets default client id

        Return:
            Returns json of playbook rules

        Example:

            To get sla playbook rule

            >>> self.{risksenseobject}.sla.getplaybookslarules('11ed13e6-a1aa-5c28-9fb0-02a87de7e1ee')
        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/{slaid}"
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def delete_sla_rule(self,playbookrulepairinguuid:str,client_id:int=None)->bool:

        """
        Deletes a particular sla rule

        Args:
            
            playbookrulepairinguuid: the playbook rule uuid

            client_id:   Client ID, if no client id provided , gets default client id

        Return:
            Success
        
        Example:
            To delete an sla rule

            >>> self.{risksenseobject}.sla.delete_sla_rule('94945073-3d62-35b6-b176-6412bd324b84')
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url  = self.api_base_url.format(str(client_id)) +"/rule/{}".format(playbookrulepairinguuid)

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
            if raw_response.status_code==200:
                success=True
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