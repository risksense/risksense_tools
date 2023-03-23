""" *******************************************************************************************************************
|
|  Name        :  prioritization.py
|  Project     :  Prioritization dashboard
|  Description :  A tool that displays data from prioritization
|  Copyright   :  2022 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import logging
from multiprocessing.sharedctypes import Value
import os
from re import I
import sys
from unicodedata import name
from warnings import filters
import toml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rs_api
from datetime import date,timedelta
import pandas as pd
from prettytable import PrettyTable
from colorama import Fore, Back, Style
from termcolor import colored

class prioritization:

    """ prioritization class """

    def __init__(self, config):

        """
        Main body of script.

        :param config:      Configuration
        :type  config:      dict
        """

        logging.info("***** SCRIPT START ***************************************************")

        #  Set variables
        self._rs_platform_url = config['platform_url']
        api_key = config['api_key']
        self.__client_id = config['client_id']
        self.userroles=[]
        self.dashboarddata={}
        try:
            print()
            print(f"Attempting to talk to RiskSense platform {self._rs_platform_url}")
            self.rs = rs_api.RiskSenseApi(self._rs_platform_url, api_key)
            self.rs.set_default_client_id(self.__client_id)
        except (rs_api.UserUnauthorized, rs_api.InsufficientPrivileges,
                rs_api.MaxRetryError, rs_api.StatusCodeError,Exception) as ex:
            message = "An error has occurred while trying to verify RiskSense credentials and connection"
            logging.error(message)
            logging.error(ex)
            print()
            print(f"{message}. Exiting.")
            exit(1)
        print()
        self.filter=input('Would you like to enter a "FILTER"? "y"  or "n":').strip()
        if self.filter.lower()=='y':
            print()
            filtercategory={1: 'group_names',2:"network.name",3:"tags"}
            print('Index No : 1 - Value : "Group name"\nIndex No : 2 - Value : "Network name"\nIndex No : 3 - Value : "Tags"')
            try:
                print()
                filtercategoryinput=filtercategory[int(input('Please insert the index number from option above for your "FILTER":').strip())]
            except Exception as e:
                print('--------------------------------------')
                print('Please enter the right index as above')
                print('Exiting')
                exit()
            isisnot={1:False,2:True}
            try:
                print()
                isisnotinput=isisnot[int(input('Please enter "1" for "IS" , "2" for "IS NOT": ').strip())]
            except Exception as e:
                print('Please enter the right index as above either 1,2')
                print('Exiting')
                exit()
            operator={1:"IN",2:"EXACT",3:"LIKE",4:"WILDCARD"}
            print()
            for key,value in operator.items():
                print(f'Index No:{key}-Value:{value}')
            try:
                print()
                operatorinput=operator[int(input('Please enter the index number of the operator from above:').strip())]
            except Exception as e:
                print('Please enter the right index as above either 1,2,3,4')
                print('Exiting')
                exit()
            values=[]
            if filtercategoryinput=='group_names':
                aggregate=self.rs.aggregate.get_groupsbyfilter()
                if len(aggregate)==0:
                    print('No groups available for the particular client\n')
                    print('Exiting')
                    exit()      
                elif len(aggregate)<10:
                    print('Here are the group names pulled from your client\n')
                    groups={}
                    for i in range(len(aggregate)):
                            groups[i]=aggregate[i]['key']
                            print(f'Index No : {i} - Value : {aggregate[i]["key"]}')
                    try:
                        print()
                        valueinput=input('Please enter the Index No: of the "GROUPS" seperated by COMMAS,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number: ').strip().split(',')
                        valueinput=list(set(valueinput))
                        if len(valueinput)>1:
                            for i in valueinput:
                                if i.isdigit()==False:
                                    print('Please do not enter any special characters or string')
                                    print('Exiting')
                                    exit()
                        if operatorinput!='IN' and len(valueinput)>1:
                            print('You must choose only one index number for this operator')
                            print('Exiting')
                            exit()
                        for value in valueinput:
                            values.append(groups[int(value)])
                    except KeyError as e:
                        print('-------------------------------------')
                        print('Please enter the right index numbers from the option above')
                        print('Exiting')
                        exit()
                    except Exception as e:
                            print('-------------------------------------')
                            print('There seems to be an exception')
                            print('Please enter the right index numbers from the option above')
                            print('Exiting')
                            exit()
                else:
                    print('Here are the suggested group names pulled from your client\n')
                    groups={}
                    for i in range(len(aggregate)):
                            groups[i]=aggregate[i]['key']
                            print(f'Index No : {i} - Value : {aggregate[i]["key"]}')
                    try:
                        print()
                        valueinput=input('Please enter the index numbers of the "GROUPS" seperated by COMMA,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,if group is not found in the above list of groups,please proceed to type "no": ').strip().split(',')
                        valueinput=list(set(valueinput))
                        if operatorinput!='IN' and len(valueinput)>1:
                            print('You must choose only one index number for this operator')
                            print('Exiting')
                            exit()
                        if len(valueinput)>1:
                            for i in valueinput:
                                if i.isdigit()==False:
                                    print('Please do not enter any string or special characters')
                                    print('Exiting')
                                    exit()
                        if 'no' in valueinput:
                             valueinput=list(set(valueinput))
                             valueinput.remove('no')
                             while(True):
                                nameinput=input('Please provide a search string to search for "GROUP NAME": ')
                                aggregate=self.rs.aggregate.get_groupsbyfilter(nameinput)
                                if aggregate==[]:
                                    print(f'No data found for {nameinput}')
                                    continue
                                groups={}
                                print()
                                print('Here are the available groups')
                                for i in range(len(aggregate)):
                                    groups[i]=aggregate[i]['key']
                                    print(f'Index No: {i} - Value : {aggregate[i]["key"]}')
                                try:
                                    print()
                                    valueinput=input('Please enter the indexes of the "GROUPS" seperated by comma,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,If you do noy have the group name in the index number above please enter "no": ').strip().split(',')
                                    valueinput=list(set(valueinput))
                                    if len(valueinput)>1:
                                        for i in valueinput:
                                            if i.isdigit()==False:
                                                print('Please do not enter any string or special characters')
                                                print('Exiting')
                                                exit()
                                    if 'no' in valueinput:
                                        valueinput=list(set(valueinput))
                                        valueinput.remove('no')
                                        continue
                                    if operatorinput!='IN' and len(valueinput)>1:
                                        print('You must choose only one index number for this operator')
                                        print('Exiting')
                                        exit()
                                    for value in valueinput:
                                        values.append(groups[int(value)])
                                except KeyError as e:
                                    print('-------------------------------------')
                                    print('Please enter the right index numbers from the option above')
                                    print('Exiting')
                                    exit()
                                except Exception as e:
                                        print('-------------------------------------')
                                        print('There seems to be an exception')
                                        print('Please enter the right index numbers from the option above')
                                        print('Exiting')
                                        exit()
                                yorno=input('Would you like to filter to more "GROUPS"? "Y" or "N": ')
                                if yorno.lower()=='n':
                                    break 
                        for value in valueinput:
                                values.append(groups[int(value)])              
                    except KeyError as e:
                        print('-------------------------------------')
                        print('Please enter the right index numbers from the option above')
                        print('Exiting')
                        exit()
                    except Exception as e:
                            print('-------------------------------------')
                            print('There seems to be an exception')
                            print('Please enter the right index numbers from the option above')
                            print('Exiting')
                            exit()
                    
               

            if filtercategoryinput=='tags':
                nameinput=''
                filters={"field":"name","exclusive":False,"operator":"WILDCARD","value":nameinput,"implicitFilters":[]}
                aggregate=self.rs.tags.suggest([],filters)
                if len(aggregate)==0:
                    print('No tags available for the particular client')
                    print('Exiting')
                    exit()      
                elif len(aggregate)<10:
                    print('Here are the tag names pulled from your client\n')
                    tags={}
                    for i in range(len(aggregate)):
                        tags[i]=aggregate[i]['key']
                        print(f'Index No : {i} - Value : "{aggregate[i]["key"]}"')
                    try:
                        print()
                        valueinput=input('Please enter index numbers of the "TAGS" seperated by COMMA,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number: ').strip().split(',')
                        valueinput=list(set(valueinput))
                        if len(valueinput)>1:
                            for i in valueinput:
                                if i.isdigit()==False:
                                    print('Please do not enter any string or special characters')
                                    print('Exiting')
                                    exit()
                        if operatorinput!='IN' and len(valueinput)>1:
                            print('You must choose only one index number for this operator')
                            print('Exiting')
                            exit()
                        for value in valueinput:
                            values.append(tags[int(value)])
                    except KeyError as e:
                        print('-------------------------------------')
                        print('Please enter the right index numbers from the option above')
                        print('Exiting')
                        exit()
                    except Exception as e:
                            print('-------------------------------------')
                            print('There seems to be an exception')
                            print('Please enter the right index numbers from the option above')
                            print('Exiting')
                            exit()
                else:  
                    print('Here are the suggested tag names pulled from your client\n')
                    tags={}
                    for i in range(len(aggregate)):
                        tags[i]=aggregate[i]['key']
                        print(f'Index No : {i} - Value : "{aggregate[i]["key"]}"')
                    try:
                        print()
                        valueinput=input('Please enter index numbers of the "TAGS" seperated by COMMA,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,if tag name is not found in the above list of tags,please proceed to type "no": ').strip().split(',')
                        valueinput=list(set(valueinput))
                        if operatorinput!='IN' and len(valueinput)>1:
                            print('You must choose only one index number for this operator')
                            print('Exiting')
                            exit()
                        if len(valueinput)>1:
                            for i in valueinput:
                                if i.isdigit()==False:
                                    print('Please do not enter any string or special characters')
                                    print('Exiting')
                                    exit()
                        if 'no' in valueinput:
                            valueinput=list(set(valueinput))
                            valueinput.remove('no')
                            while(True):
                                nameinput=input('Please provide a search string for "TAG NAME": ')
                                filters={"field":"name","exclusive":False,"operator":"WILDCARD","value":nameinput,"implicitFilters":[]}
                                aggregate=self.rs.tags.suggest([],filters)
                                if aggregate==[]:
                                    print(f'No data found for {nameinput}')
                                    continue
                                tags={}
                                print()
                                for i in range(len(aggregate)):
                                    tags[i]=aggregate[i]['key']
                                    print(f'Index No : {i} - Value : "{aggregate[i]["key"]}"')
                                try:
                                    print()
                                    valueinput=input('Please enter index numbers of the "TAGS" seperated by COMMA,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number, if the tag name is not available in the list above , please enter "no": ').strip().split(',')
                                    valueinput=list(set(valueinput))
                                    if len(valueinput)>1:
                                        for i in valueinput:
                                            if i.isdigit()==False:
                                                print('Please do not enter any string or special characters')
                                                print('Exiting')
                                                exit()
                                    if 'no' in valueinput:
                                        valueinput=list(set(valueinput))
                                        valueinput.remove('no')
                                        continue
                                    if operatorinput!='IN' and len(valueinput)>1:
                                        print('You must choose only one index number for this operator')
                                        print('Exiting')
                                        exit()
                                    for value in valueinput:
                                        values.append(tags[int(value)])
                    
                                except KeyError as e:
                                    print('-------------------------------------')
                                    print('Please enter the right index numbers from the option above')
                                    print('Exiting')
                                    exit()
                                except Exception as e:
                                        print('-------------------------------------')
                                        print('There seems to be an exception')
                                        print('Please enter the right index numbers from the option above')
                                        print('Exiting')
                                        exit()
                                yorno=input('Would you like to filter to more "TAGS"? "Y" or "N": ')
                                if yorno.lower()=='n':
                                    break
                                elif yorno.lower()!='y':
                                    print('Please provide right input')
                                    print('Exiting')
                                    exit() 
                        for value in valueinput:
                                values.append(tags[int(value)])
                    except KeyError as e:
                        print('-------------------------------------')
                        print('Please enter the right index numbers from the option above')
                        print('Exiting')
                        exit()
                    except Exception as e:
                            print('-------------------------------------')
                            print('There seems to be an exception')
                            print('Please enter the right index numbers from the option above')
                            print('Exiting')
                            exit()
                    

            if filtercategoryinput=='network.name':
                nameinput=''
                filters={"field":"name","exclusive":False,"operator":"WILDCARD","value":nameinput,"implicitFilters":[]}
                aggregate=self.rs.networks.suggest([],filters)
                if len(aggregate)==0:
                    print('No networks available for the particular client')
                    print('Exiting')
                    exit()      
                elif len(aggregate)<10:
                    print('Here are the network names pulled from your client\n')
                    groups={}
                    for i in range(len(aggregate)):
                            groups[i]=aggregate[i]['key']
                            print(f'Index No : {i} - Value : "{aggregate[i]["key"]}"')
                    try:
                        print()
                        valueinput=input('Please enter the indexes of the "NETWORKS" seperated by COMMA,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number: ').strip().split(',')
                        valueinput=list(set(valueinput))
                        if len(valueinput)>1:
                            for i in valueinput:
                                if i.isdigit()==False:
                                    print('Please do not enter any string or special characters')
                                    print('Exiting')
                                    exit()
                        if operatorinput!='IN' and len(valueinput)>1:
                            print('You must choose only one index number for this operator')
                            print('Exiting')
                            exit()
                        for value in valueinput:
                            values.append(groups[int(value)])
                    except KeyError as e:
                        print('-------------------------------------')
                        print('Please enter the right index numbers from the option above')
                        print('Exiting')
                        exit()
                    except Exception as e:
                            print('-------------------------------------')
                            print('There seems to be an exception')
                            print('Please enter the right index numbers from the option above')
                            print('Exiting')
                            exit()
                else:
                        print('Here are the suggested network names pulled from your client\n')
                        networks={}
                        for i in range(len(aggregate)):
                            networks[i]=aggregate[i]['key']
                            print(f'Index No {i}- {aggregate[i]["key"]}')
                        try:
                            print()
                            valueinput=input('Please enter the indexes of the "NETWORKS" seperated by COMMA,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,if you cannot find the network you want,please type "no": ').strip().split(',')
                            valueinput=list(set(valueinput))
                            if operatorinput!='IN' and len(valueinput)>1:
                                print('You must choose only one index number for this operator')
                                print('Exiting')
                                exit()
                            if len(valueinput)>1:
                                for i in valueinput:
                                    if i.isdigit()==False:
                                        print('Please do not enter any string or special characters')
                                        print('Exiting')
                                        exit()
                            if 'no' in valueinput:
                                valueinput=list(set(valueinput))
                                valueinput.remove('no')
                                while(True):
                                    nameinput=input('Please provide a search string to search for "NETWORK NAME": ')
                                    filters={"field":"name","exclusive":False,"operator":"WILDCARD","value":nameinput,"implicitFilters":[]}
                                    aggregate=self.rs.networks.suggest([],filters)
                                    networks={}
                                    if aggregate==[]:
                                        print(f'No data found for for {nameinput}')
                                        continue
                                    print()
                                    for i in range(len(aggregate)):
                                        networks[i]=aggregate[i]['key']
                                        print(f'Index No {i}- Value : {aggregate[i]["key"]}')
                                    try:
                                        print()
                                        valueinput=input('Please enter the indexes of the "NETWORKS" seperated by comma,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,please enter "no" if you cannot find the network you want: ').strip().split(',')
                                        valueinput=list(set(valueinput))
                                        if len(valueinput)>1:
                                            for i in valueinput:
                                                if i.isdigit()==False:
                                                    print('Please do not enter any string or special characters')
                                                    print('Exiting')
                                                    exit()
                                        if 'no' in valueinput:
                                            valueinput=list(set(valueinput))
                                            valueinput.remove('no')
                                            continue
                                        if operatorinput!='IN' and len(valueinput)>1:
                                            print('You must choose only one index number for this operator')
                                            print('Exiting')
                                            exit()
                                        for value in valueinput:
                                            values.append(networks[int(value)])
                                    except KeyError as e:
                                        print('-------------------------------------')
                                        print('Please enter the right index numbers from the option above')
                                        print('Exiting')
                                        exit()
                                    except Exception as e:
                                            print('-------------------------------------')
                                            print('There seems to be an exception')
                                            print('Please enter the right index numbers from the option above')
                                            print('Exiting')
                                            exit()
                                    yorno=input('Would you like to filter to more "NETWORKS"? Y or N: ')
                                    if yorno.lower()=='n':
                                       break
                            for value in valueinput:
                                values.append(networks[int(value)])
                        except KeyError as e:
                            print('-------------------------------------')
                            print('Please enter the right index numbers from the option above')
                            print('Exiting')
                            exit()
                        except Exception as e:
                            print('-------------------------------------')
                            print('There seems to be an exception')
                            print('Please enter the right index numbers from the option above')
                            print('Exiting')
                            exit()
            actualfilter={"field":filtercategoryinput,"exclusive":isisnotinput,"operator":operatorinput,"orWithPrevious":False,"implicitFilters":[],"value":",".join(values)}
            self.data_capture(actualfilter)
        elif self.filter.lower()=='n':
                    self.data_capture([])
        else:
                print('Please provide a letter either y or n')
                print('Exiting')
    
    def data_capture(self,datafilter):
            try:
                if datafilter!=[]:
                    filter=[datafilter,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"True"}]
                    self.dashboarddata['open_weaponized_findings']=str(self.rs.host_findings.get_single_search_page(search_filters=filter)['page']['totalElements']+self.rs.application_findings.get_single_search_page(search_filters=filter)['page']['totalElements'])
                else:
                    filter=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"True"}]
                    self.dashboarddata['open_weaponized_findings']=str(self.rs.host_findings.get_single_search_page(search_filters=filter)['page']['totalElements']+self.rs.application_findings.get_single_search_page(search_filters=filter)['page']['totalElements'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching total assets data.For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                if datafilter!=[]:
                    filter=[datafilter,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Closed"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"True"}]
                    self.dashboarddata['closed_weaponized_findings']=str(self.rs.host_findings.get_single_search_page(search_filters=filter)['page']['totalElements']+self.rs.application_findings.get_single_search_page(search_filters=filter)['page']['totalElements']) 
                else:
                    filter=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Closed"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"True"}]
                    self.dashboarddata['closed_weaponized_findings']=str(self.rs.host_findings.get_single_search_page(search_filters=filter)['page']['totalElements']+self.rs.application_findings.get_single_search_page(search_filters=filter)['page']['totalElements'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching closed weaponized data.For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                currentdate=date.today()
                if datafilter!=[]:
                    filter=[datafilter,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"True"},{"field":"platform_first_ingested_on","exclusive":False,"operator":"RANGE","value":f"{currentdate - timedelta(30)},{currentdate}"}]
                    self.dashboarddata['recently_ingested_weaponized_findings']=str(self.rs.host_findings.get_single_search_page(search_filters=filter)['page']['totalElements']+self.rs.application_findings.get_single_search_page(search_filters=filter)['page']['totalElements'])
                else:
                    filter=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"True"},{"field":"platform_first_ingested_on","exclusive":False,"operator":"RANGE","value":f"{currentdate - timedelta(30)},{currentdate}"}]
                    self.dashboarddata['recently_ingested_weaponized_findings']=str(self.rs.host_findings.get_single_search_page(search_filters=filter)['page']['totalElements']+self.rs.application_findings.get_single_search_page(search_filters=filter)['page']['totalElements'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Recently ingested weaponized data.For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                currentdate=date.today()
                if datafilter!=[]:
                    filter=[datafilter,{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"True"},{"field":"resolved_on","exclusive":False,"operator":"RANGE","value":f"{currentdate - timedelta(30)},{currentdate}"}]
                    self.dashboarddata['recently_resolved_weaponized_findings']=str(self.rs.host_findings.get_single_search_page(search_filters=filter)['page']['totalElements']+self.rs.application_findings.get_single_search_page(search_filters=filter)['page']['totalElements'])
                else:
                    filter=[{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"True"},{"field":"resolved_on","exclusive":False,"operator":"RANGE","value":f"{currentdate - timedelta(30)},{currentdate}"}]
                    self.dashboarddata['recently_resolved_weaponized_findings']=str(self.rs.host_findings.get_single_search_page(search_filters=filter)['page']['totalElements']+self.rs.application_findings.get_single_search_page(search_filters=filter)['page']['totalElements'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Recently resolved weaponized data.For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                if datafilter!=[]:
                    filter=[datafilter,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"True"},{"field":"assignments","exclusive":True,"operator":"WILDCARD","orWithPrevious":False,"implicitFilters":[],"value":"*"}]
                    self.dashboarddata['unassigned_rce_pe']=str(self.rs.host_findings.get_single_search_page(search_filters=filter)['page']['totalElements']+self.rs.application_findings.get_single_search_page(search_filters=filter)['page']['totalElements'] )
                else:
                    filter=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"True"},{"field":"assignments","exclusive":True,"operator":"WILDCARD","orWithPrevious":False,"implicitFilters":[],"value":"*"}]
                    self.dashboarddata['unassigned_rce_pe']=str(self.rs.host_findings.get_single_search_page(search_filters=filter)['page']['totalElements']+self.rs.application_findings.get_single_search_page(search_filters=filter)['page']['totalElements'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching closed weaponized dataFor details,please view prioritization.log for more details."
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                if datafilter!=[]:
                    filter=[datafilter,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},{"field":"assignments","exclusive":False,"operator":"WILDCARD","orWithPrevious":False,"implicitFilters":[],"value":"*"}]
                    self.dashboarddata['assigned_rce_pe']=str(self.rs.host_findings.get_single_search_page(search_filters=filter)['page']['totalElements']+self.rs.application_findings.get_single_search_page(search_filters=filter)['page']['totalElements'])
                else:
                    filter=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},{"field":"assignments","exclusive":False,"operator":"WILDCARD","orWithPrevious":False,"implicitFilters":[],"value":"*"}]
                    self.dashboarddata['assigned_rce_pe']=str(self.rs.host_findings.get_single_search_page(search_filters=filter)['page']['totalElements']+self.rs.application_findings.get_single_search_page(search_filters=filter)['page']['totalElements'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching closed weaponized data.For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                self.dashboarddata['openfindingsfunnel']={}
                self.dashboarddata['openfindingsfunnel']['Total']='0'
                self.dashboarddata['openfindingsfunnel']['Weaponized']='0'
                self.dashboarddata['openfindingsfunnel']['RCE/PE']='0'
                self.dashboarddata['openfindingsfunnel']['Trending']='0'
                self.dashboarddata['openfindingsfunnel']['Manualexploit']='0'
                apporhost={'1':'applicationFinding','2':'hostFinding'}
                print()
                for key,value in apporhost.items():
                    print(f'Index No:{key}- Value: {value}')
                try:
                    print()
                    choice=apporhost[input('Please enter the index number from the option above for "OPEN FINDINGS FUNNEL":').strip()]
                except KeyError as e:
                    print('-------------------------------------')
                    print('Please enter the right index numbers from the option above either 1 or 2')
                    print('Exiting')
                    exit()
                except Exception as e:
                        print('-------------------------------------')
                        print('There seems to be an exception')
                        print(e)
                        print('Exiting')
                        exit()
                data=self.rs.aggregate.get_dynamic_aggregationforopenfindingsprioritization(choice,datafilter)
                if data[0]=={}:
                    pass
                else:
                    self.dashboarddata['openfindingsfunnel']['Total']=0
                    self.dashboarddata['openfindingsfunnel']['Weaponized']=0
                    self.dashboarddata['openfindingsfunnel']['RCE/PE']=0
                    self.dashboarddata['openfindingsfunnel']['Trending']=0
                    self.dashboarddata['openfindingsfunnel']['Manualexploit']=0
                    for key in data[0].keys():
                        self.dashboarddata['openfindingsfunnel']['Total']=self.dashboarddata['openfindingsfunnel']['Total']+ int(data[0][key]['total'])
                        self.dashboarddata['openfindingsfunnel']['Weaponized']=self.dashboarddata['openfindingsfunnel']['Weaponized']+ int(data[0][key]['weaponized'])
                        self.dashboarddata['openfindingsfunnel']['RCE/PE']=self.dashboarddata['openfindingsfunnel']['RCE/PE']+ int(data[0][key]["rcePe"])
                        self.dashboarddata['openfindingsfunnel']['Trending']=self.dashboarddata['openfindingsfunnel']['Trending']+ int(data[0][key]["trending"])
                        self.dashboarddata['openfindingsfunnel']['Manualexploit']=self.dashboarddata['openfindingsfunnel']['Manualexploit']+ int(data[0][key]["manualExploit"])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Open findings funnel data.For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                self.dashboarddata['closedfindingsfunnel']={}
                self.dashboarddata['closedfindingsfunnel']['Total']='0'
                self.dashboarddata['closedfindingsfunnel']['Weaponized']='0'
                self.dashboarddata['closedfindingsfunnel']['RCE/PE']='0'
                self.dashboarddata['closedfindingsfunnel']['Trending']='0'
                self.dashboarddata['closedfindingsfunnel']['Manualexploit']='0'
                apporhost={'1':'applicationFinding','2':'hostFinding'}
                print()
                for key,value in apporhost.items():
                    print(f'Index No:{key} - Value:{value}')
                try:
                    print()
                    choice=apporhost[input('Please choose from the option above for "CLOSED FINDINGS FUNNEL":').strip()]
                except KeyError as e:
                    print('-------------------------------------')
                    print('Please enter the right index numbers from the option above wither 1 or 2')
                    print('Exiting')
                    exit()
                except Exception as e:
                        print('-------------------------------------')
                        print('There seems to be an exception')
                        print(e)
                        print('Exiting')
                        exit()
                data=self.rs.aggregate.get_dynamic_aggregationforclosedfindingsprioritization(choice,datafilter)
                if data[0]=={}:
                    pass
                else:
                    self.dashboarddata['closedfindingsfunnel']['Total']=0
                    self.dashboarddata['closedfindingsfunnel']['Weaponized']=0
                    self.dashboarddata['closedfindingsfunnel']['RCE/PE']=0
                    self.dashboarddata['closedfindingsfunnel']['Trending']=0
                    self.dashboarddata['closedfindingsfunnel']['Manualexploit']=0
                    for key in data[0].keys():
                        self.dashboarddata['closedfindingsfunnel']['Total']=self.dashboarddata['closedfindingsfunnel']['Total']+ int(data[0][key]['total'])
                        self.dashboarddata['closedfindingsfunnel']['Weaponized']=self.dashboarddata['closedfindingsfunnel']['Weaponized']+ int(data[0][key]['weaponized'])
                        self.dashboarddata['closedfindingsfunnel']['RCE/PE']=self.dashboarddata['closedfindingsfunnel']['RCE/PE']+ int(data[0][key]["rcePe"])
                        self.dashboarddata['closedfindingsfunnel']['Trending']=self.dashboarddata['closedfindingsfunnel']['Trending']+ int(data[0][key]["trending"])
                        self.dashboarddata['closedfindingsfunnel']['Manualexploit']=self.dashboarddata['closedfindingsfunnel']['Manualexploit']+ int(data[0][key]["manualExploit"])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
            rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Closed findings funnel.For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                apporhost={'1':'applicationFinding','2':'hostFinding'}
                print()
                for key,value in apporhost.items():
                    print(f'Index No:{key}-Value:{value}')
                try:
                    print()
                    choice=apporhost[input('Please enter the index number from the option above for "FINDINGS BY ADDRESS TYPE":').strip()]
                except KeyError as e:
                    print('-------------------------------------')
                    print('Please enter the right index numbers from the option above wither 1 or 2')
                    print('Exiting')
                    exit()
                except Exception as e:
                        print('-------------------------------------')
                        print('There seems to be an exception')
                        print(e)
                        print('Exiting')
                        exit()
                data=self.rs.aggregate.get_findingbyaddresstype(choice,datafilter)
                self.dashboarddata['findingsbyaddresstype']={}
                for key in data.keys():
                    self.dashboarddata['findingsbyaddresstype'][key]={}
                    for keykey in data[key].keys():
                        self.dashboarddata['findingsbyaddresstype'][key][keykey]=data[key][keykey]['count']
                apporhost={'1':'applicationFinding','2':'hostFinding'}
                print()
                for key,value in apporhost.items():
                    print(f' Index No:{key}- Value: {value}')
                try:
                    print()
                    choice=apporhost[input('Please enter the index number from the option above for "FINDINGS SUMMARY":').strip()]
                except KeyError as e:
                    print('-------------------------------------')
                    print('Please enter the right index numbers from the option above wither 1 or 2')
                    print('Exiting')
                    exit()
                except Exception as e:
                        print('-------------------------------------')
                        print('There seems to be an exception')
                        print(e)
                        print('Exiting')
                        exit()
                data=self.rs.aggregate.get_findingsummary(choice,datafilter)
                self.dashboarddata['findingssummary']={}
                for key in data.keys():
                    self.dashboarddata['findingssummary'][key]={}
                    for keykey in data[key].keys():
                        self.dashboarddata['findingssummary'][key][keykey]=data[key][keykey]['count']
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Findings summary data.For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                apporhost={'1':'applicationFinding','2':'hostFinding'}
                print()
                for key,value in apporhost.items():
                    print(f'Index No:{key}- Value: {value}')
                try:
                    print()
                    apporhostchoice=apporhost[input('Please choose the index number from the option above for "FINDINGS FIRST INGESTED VS LAST INGESTED":').strip()]
                except KeyError as e:
                    print('-------------------------------------')
                    print('Please enter the right index numbers from the option above wither 1 or 2')
                    print('Exiting')
                    exit()
                except Exception as e:
                        print('-------------------------------------')
                        print('There seems to be an exception')
                        print(e)
                        print('Exiting')
                        exit()
                duration={'1':'daily','2':'weekly','3':'monthly','4':'quarterly'}
                print()
                for key,value in duration.items():
                    print(f'Index No:{key}- Value: {value}')
                try:
                    print()
                    durationchoice=duration[input('Please choose the index number from the option above the "DURATION" for "INGESTION" data:').strip()]
                except KeyError as e:
                    print('-------------------------------------')
                    print('Please enter the right index numbers from the option above witherr 1,2,3 or 4')
                    print('Exiting')
                    exit()
                except Exception as e:
                        print('-------------------------------------')
                        print('There seems to be an exception')
                        print(e)
                        print('Exiting')
                        exit()
                data=self.rs.aggregate.get_findingsfirstingestedvslastingested(apporhostchoice,durationchoice,datafilter)
                firstvslastopen={}
                firstvslastopen['date']=[data['openFindingDateHistogram'][x]['date'] for x in range(len(data['openFindingDateHistogram']))]
                firstvslastopen['Total_ingested']=[data['openFindingDateHistogram'][x]['count'] for x in range(len(data['openFindingDateHistogram']))]
                firstvslastopen['Critical']=[data['openFindingDateHistogram'][x]['priorityDistribution']['critical']['count']for x in range(len(data['openFindingDateHistogram']))]
                firstvslastopen['High']=[data['openFindingDateHistogram'][x]['priorityDistribution']['high']['count']for x in range(len(data['openFindingDateHistogram']))]
                firstvslastopen['Medium']=[data['openFindingDateHistogram'][x]['priorityDistribution']['medium']['count']for x in range(len(data['openFindingDateHistogram']))]
                firstvslastopen['Low']=[data['openFindingDateHistogram'][x]['priorityDistribution']['low']['count']for x in range(len(data['openFindingDateHistogram']))]
                firstvslastopen['Info']=[data['openFindingDateHistogram'][x]['priorityDistribution']['info']['count']for x in range(len(data['openFindingDateHistogram']))]
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Recently ingested dataFor details,please view prioritization.log for more details."
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                firstvslastclose={}
                firstvslastclose['date']=[data['closeFindingDateHistogram'][x]['date'] for x in range(len(data['closeFindingDateHistogram']))]
                firstvslastclose['Total_ingested']=[data['closeFindingDateHistogram'][x]['count'] for x in range(len(data['closeFindingDateHistogram']))]
                firstvslastclose['Critical']=[data['closeFindingDateHistogram'][x]['priorityDistribution']['critical']['count']for x in range(len(data['closeFindingDateHistogram']))]
                firstvslastclose['High']=[data['closeFindingDateHistogram'][x]['priorityDistribution']['high']['count']for x in range(len(data['closeFindingDateHistogram']))]
                firstvslastclose['Medium']=[data['closeFindingDateHistogram'][x]['priorityDistribution']['medium']['count']for x in range(len(data['closeFindingDateHistogram']))]
                firstvslastclose['Low']=[data['closeFindingDateHistogram'][x]['priorityDistribution']['low']['count']for x in range(len(data['closeFindingDateHistogram']))]
                firstvslastclose['Info']=[data['closeFindingDateHistogram'][x]['priorityDistribution']['info']['count']for x in range(len(data['closeFindingDateHistogram']))]
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching close finding data histogram data.For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                apporhost={'1':'host','2':'application'}
                print()
                for key,value in apporhost.items():
                    print(f'Index No:{key}- Value: {value}')
                try:
                    print()
                    apporhostchoice=apporhost[input('Please enter the index number from the option above of "FINDINGS" for "OPEN FINDINGS OVER TIME":').strip()]
                except KeyError as e:
                    print('-------------------------------------')
                    print('Please enter the right index numbers from the option above either 1 or 2')
                    print('Exiting')
                    exit()
                except Exception as e:
                        print('-------------------------------------')
                        print('There seems to be an exception')
                        print(e)
                        print('Exiting')
                        exit()
                duration={'1':'daily','2':'weekly','3':'monthly'}
                print()
                for key,value in duration.items():
                    print(f'Index No:{key}- Value: {value}')
                try:
                    print()
                    durationchoice=duration[input('Please enter the index number from the option above the "DURATION" for "OPEN FINDINGS OVER TIME":').strip()]
                except KeyError as e:
                    print('-------------------------------------')
                    print('Please enter the right index numbers from the option above wither 1,2 or 3')
                    print('Exiting')
                    exit()
                except Exception as e:
                        print('-------------------------------------')
                        print('There seems to be an exception')
                        print(e)
                        print('Exiting')
                        exit()
                data=self.rs.aggregate.get_openfindingsovertime(apporhostchoice,durationchoice,datafilter)
                openfindingsovertimeopen={}
                openfindingsovertimeopen['date']=[data[x]['date'] for x in range(len(data))]
                openfindingsovertimeopen['Total']=[data[x]['all']['open']['total'] for x in range(len(data))]
                openfindingsovertimeopen['Critical']=[data[x]['all']['open']['critical'] for x in range(len(data))]
                openfindingsovertimeopen['High']=[data[x]['all']['open']['high'] for x in range(len(data))]
                openfindingsovertimeopen['Medium']=[data[x]['all']['open']['medium'] for x in range(len(data))]
                openfindingsovertimeopen['Low']=[data[x]['all']['open']['low'] for x in range(len(data))]
                openfindingsovertimeopen['Info']=[data[x]['all']['open']['info'] for x in range(len(data))]
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Open findings over time data.For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)

            try:
                openfindingsovertimeweaponized={}
                openfindingsovertimeweaponized['date']=[data[x]['date'] for x in range(len(data))]
                openfindingsovertimeweaponized['Total']=[data[x]['weaponized']['open']['total'] for x in range(len(data))]
                openfindingsovertimeweaponized['Critical']=[data[x]['weaponized']['open']['critical'] for x in range(len(data))]
                openfindingsovertimeweaponized['High']=[data[x]['weaponized']['open']['high'] for x in range(len(data))]
                openfindingsovertimeweaponized['Medium']=[data[x]['weaponized']['open']['medium'] for x in range(len(data))]
                openfindingsovertimeweaponized['Low']=[data[x]['weaponized']['open']['low'] for x in range(len(data))]
                openfindingsovertimeweaponized['Info']=[data[x]['weaponized']['open']['info'] for x in range(len(data))]
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Open findings over time weaponized data.For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)

            try:
                apporhost={'1':'applicationFinding','2':'hostFinding'}
                print()
                for key,value in apporhost.items():
                    print(f'Index No:{key}- Value: {value}')
                try:
                    print()
                    choice=apporhost[input('Please enter the index number from the option above for "RECENT FINDINGS STATUS":').strip()]
                except KeyError as e:
                    print('-------------------------------------')
                    print('Please enter the right index numbers from the option above wither 1 or 2')
                    print('Exiting')
                    exit()
                except Exception as e:
                        print('-------------------------------------')
                        print('There seems to be an exception')
                        print(e)
                        print('Exiting')
                        exit()
                closeoropen={'1':'Open','2':'Closed'}
                print()
                for key,value in closeoropen.items():
                    print(f'Index No:{key}- Value: {value}')
                try:
                    print()
                    closeoropenchoice=closeoropen[input('Please enter the index number from the option above the status for "RECENT FINDINGS STATUS":').strip()]
                except KeyError as e:
                    print('-------------------------------------')
                    print('Please enter the right index numbers from the option above wither 1 or 2')
                    print('Exiting')
                    exit()
                except Exception as e:
                        print('-------------------------------------')
                        print('Please enter the right index numbers from the option above wither 1 or 2')
                        print('Exiting')
                        exit()
                data=self.rs.aggregate.get_recent_findings_status(choice,closeoropenchoice,datafilter)
                recentfindingsstatusdata={}
                recentfindingsstatusdata['Weaponized']=[data[i]['severityDistributionRange']['threat']['count'] for i in range(len(data))]
                recentfindingsstatusdata['Critical']=[data[i]['severityDistributionRange']['critical']['count'] for i in range(len(data))]
                recentfindingsstatusdata['High']=[data[i]['severityDistributionRange']['high']['count'] for i in range(len(data))]
                recentfindingsstatusdata['Medium']=[data[i]['severityDistributionRange']['medium']['count'] for i in range(len(data))]
                recentfindingsstatusdata['Low']=[data[i]['severityDistributionRange']['low']['count'] for i in range(len(data))]
                recentfindingsstatusdata['Info']=[data[i]['severityDistributionRange']['info']['count'] for i in range(len(data))]
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Recent findings status data.For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                mytable=PrettyTable([Fore.YELLOW+'Open weaponized findings'.upper(),Fore.YELLOW+'Closed weaponized findings',Fore.YELLOW+'Recently ingested weapon findings',Fore.YELLOW+'Recently resolved weapon findings'])
                mytable.add_row([Fore.RED+self.dashboarddata['open_weaponized_findings'],Fore.RED+self.dashboarddata['closed_weaponized_findings'],Fore.RED+self.dashboarddata['recently_ingested_weaponized_findings'],Fore.RED+self.dashboarddata['recently_resolved_weaponized_findings']])
            except Exception as e :
                message = f"An exception has occurred while creating kpi table.There seems to be no data. For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable1=PrettyTable([Fore.YELLOW+'Unassigned findings with rce/pe exploits',Fore.YELLOW+'Assigned findings with rce/pe exploits'])
                mytable1.add_row([Fore.RED+self.dashboarddata['unassigned_rce_pe'],Fore.RED+self.dashboarddata['assigned_rce_pe']])
            except Exception as e :
                message = f"An exception has occurred while creating rce /pe ,assigned findings kpi table.There seems to be no data. For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable2=PrettyTable([Fore.YELLOW+'Name',Fore.YELLOW+'Findings'])
                for key in self.dashboarddata['openfindingsfunnel'].keys():
                    mytable2.add_row([Fore.MAGENTA+key,Fore.MAGENTA+str(self.dashboarddata['openfindingsfunnel'][key])])
            except Exception as e :
                message = f"An exception has occurred while creating open findings funnel table.There seems to be no data. For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable3=PrettyTable([Fore.YELLOW+'Name',Fore.YELLOW+'Findings'])
                for key in self.dashboarddata['closedfindingsfunnel'].keys():
                    mytable3.add_row([Fore.MAGENTA+key,Fore.MAGENTA+str(self.dashboarddata['closedfindingsfunnel'][key])])
            except Exception as e :
                message = f"An exception has occurred while closed findings funnel table.There seems to be no data. For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable4=PrettyTable()
                mytable4.add_column(Fore.MAGENTA+'Findings',['Open','Open, Weaponized','Closed','Closed,Weaponized','Accepted','Accepted, Weaponized'])
                mytable4.add_column(Fore.MAGENTA+'Internal',[self.dashboarddata['findingsbyaddresstype']['internal']['openCount'],self.dashboarddata['findingsbyaddresstype']['internal']['openWithThreatCount'],self.dashboarddata['findingsbyaddresstype']['internal']['closedCount'],self.dashboarddata['findingsbyaddresstype']['internal']['closedWithThreatCount'],self.dashboarddata['findingsbyaddresstype']['internal']['acceptedCount'],self.dashboarddata['findingsbyaddresstype']['internal']['acceptedWithThreatCount']])
                mytable4.add_column(Fore.MAGENTA+'External',[self.dashboarddata['findingsbyaddresstype']['external']['openCount'],self.dashboarddata['findingsbyaddresstype']['external']['openWithThreatCount'],self.dashboarddata['findingsbyaddresstype']['external']['closedCount'],self.dashboarddata['findingsbyaddresstype']['external']['closedWithThreatCount'],self.dashboarddata['findingsbyaddresstype']['external']['acceptedCount'],self.dashboarddata['findingsbyaddresstype']['external']['acceptedWithThreatCount']])
            except Exception as e :
                message = f"An exception has occurred while creatings findings by address type funnel table.There seems to be no data. For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable5=PrettyTable()
                mytable5.add_column(Fore.MAGENTA+'Findings',['Open','Open, Weaponized','Closed','Closed,Weaponized','Accepted','Accepted, Weaponized'])
                criticalitylist=['critical', 'high', 'medium', 'low','info']
                for key in criticalitylist:
                    mytable5.add_column(Fore.MAGENTA+key,[Fore.MAGENTA+str(self.dashboarddata['findingssummary'][key]['openCount']),Fore.MAGENTA+str(self.dashboarddata['findingssummary'][key]['openWithThreatCount']),Fore.MAGENTA+str(self.dashboarddata['findingssummary'][key]['closedCount']),Fore.MAGENTA+str(self.dashboarddata['findingssummary'][key]['closedWithThreatCount']),Fore.MAGENTA+str(self.dashboarddata['findingssummary'][key]['acceptedCount']),Fore.MAGENTA+str(self.dashboarddata['findingssummary'][key]['acceptedWithThreatCount'])])
            except Exception as e :
                message = f"An exception has occurred while creating findings summary funnel table.There seems to be no data. For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable6=PrettyTable()
                mytable6.add_column(Fore.MAGENTA+'Days',[Fore.MAGENTA+'More than 120',Fore.MAGENTA+'61 - 120',Fore.MAGENTA+'31 - 60',Fore.MAGENTA+'7 - 30',Fore.MAGENTA+'Less than 7'])
                for key in recentfindingsstatusdata.keys():
                    mytable6.add_column(Fore.MAGENTA+key,recentfindingsstatusdata[key])
            except Exception as e :
                message = f"An exception has occurred while creating Recent findings by status table.There seems to be no data. For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable7=PrettyTable()
                for key in openfindingsovertimeopen.keys():
                    mytable7.add_column(Fore.MAGENTA+key,openfindingsovertimeopen[key])
            except Exception as e :
                message = f"An exception has occurred while creating open findins over time table.There seems to be no data. For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable8=PrettyTable()
                for key in openfindingsovertimeweaponized.keys():
                    mytable8.add_column(Fore.MAGENTA+key,openfindingsovertimeweaponized[key])
            except Exception as e :
                message = f"An exception has occurred while creating open findings overtime weaponized funnel table.There seems to be no data. For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable9=PrettyTable()
                for key in firstvslastopen.keys():
                    mytable9.add_column(Fore.MAGENTA+key,firstvslastopen[key])
            except Exception as e :
                message = f"An exception has occurred while creating firstvslast open funnel table.There seems to be no data. For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable10=PrettyTable()
                for key in firstvslastclose.keys():
                    mytable10.add_column(Fore.MAGENTA+key,firstvslastclose[key])
            except Exception as e :
                message = f"An exception has occurred while creating first vs last close funnel table.There seems to be no data. For details,please view prioritization.log for more details"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                print()
                print(Fore.YELLOW+'\t\t\t---------------------------KPI TABLE---------------------',Fore.RESET)
                print(mytable,Fore.RESET)
            except Exception as e:
                logging.error(e)
                print()
                print(e)
            try:
                print(mytable1,Fore.RESET)
            except Exception as e:
                logging.error(e)
                print()
                print(e)
            try:
                print()
                print(Fore.YELLOW+'Open Findings Funnel'.upper(),Fore.RESET)
                print(mytable2,Fore.RESET)
            except Exception as e:
                logging.error(e)
                print()
                print(e)
            try:
                print()
                print(Fore.YELLOW+'Closed Findings Funnel'.upper(),Fore.RESET)
                print(mytable3,Fore.RESET)
            except Exception as e:
                logging.error(e)
                print()
                print(e)
            try:
                print()
                print(Fore.YELLOW+'---------Findings by Address Type--------'.upper(),Fore.RESET)
                print(mytable4,Fore.RESET)
            except Exception as e:
                logging.error(e)
                print()
                print(e)
            try:
                print()
                print(Fore.YELLOW+'\t\t----------Findings Summary-------------'.upper(),Fore.RESET)
                print(mytable5,Fore.RESET)
            except Exception as e:
                logging.error(e)
                print()
                print(e)
            try:
                print()
                print(Fore.YELLOW+'\t-----------Findings ingested vs.resolved------------'.upper(),Fore.RESET)
                print()
                print(Fore.YELLOW+'\t\t\tIngested'.upper(),Fore.RESET)
                print(mytable9,Fore.RESET)
                print()
                print(Fore.YELLOW+'\t\t\tResolved'.upper(),Fore.RESET)
                print(mytable10,Fore.RESET)
            except Exception as e:
                logging.error(e)
                print()
                print(e)
            try:
                print()
                print(Fore.YELLOW+'----------------Open Findings over Time----------- '.upper(),Fore.RESET)
                print()
                print(Fore.YELLOW+'\t\t\tOpen'.upper(),Fore.RESET)
                print(mytable7,Fore.RESET)
                print()
                print(Fore.YELLOW+'\t\t\tWeaponized'.upper(),Fore.RESET)
                print(mytable8,Fore.RESET)
            except Exception as e:
                logging.error(e)
                print()
                print(e)
            try:
                print()
                print(Fore.YELLOW+'-----------Recent Findings by Status-------------'.upper(),Fore.RESET)
                print(mytable6,Fore.RESET)
            except Exception as e:
                logging.error(e)
                print()
                print(e)



        


# ---------------------------------------------------------------------------------------------------------------------


def read_config_file(filename):

    """
    Reads a TOML-formatted configuration file.

    :param filename:    Path to the TOML-formatted file to be read.
    :type  filename:    str

    :return:  Values contained in config file.
    :rtype:   dict
    """

    try:
        data = toml.loads(open(filename).read())
        logging.info("Successfully read config file %s", filename)
        return data
    except (FileNotFoundError, toml.TomlDecodeError) as ex:
        print("Error reading configuration file.")
        print(ex)
        print()
        exit(1)


#  Execute the script
if __name__ == "__main__":

    #  Specify settings For the log

    logsfolder=os.path.join(os.getcwd(),'logs')
    if not os.path.exists(logsfolder) or not os.path.isdir(logsfolder):
        os.mkdir('logs')
        
    log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs', f"Prioritization.log")
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(levelname)s:  %(asctime)s > %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    print('For more details on the script process please view Prioritization.log found in the logs folder')
    #  Set config file path, and read the configuration.
    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
    config_contents = read_config_file(conf_file)

    try:
        prioritization(config_contents)

    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt detected.  Exiting...")
        print()
        print("KeyboardInterrupt detected.  Exiting...")
        print()
        sys.exit(0)


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
   limitations under the License."""