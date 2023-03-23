""" *******************************************************************************************************************
|
|  Name        :  appsec.py
|  Project     :  Application Security Dashboard
|  Description :  A tool that displays application security dashboard.
|  Copyright   :  2022 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import logging
from multiprocessing.sharedctypes import Value
import os
from re import I
import sys
from warnings import filters
from numpy import size
import toml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rs_api
from prettytable import PrettyTable
from colorama import Fore
import pandas as pd

class application_security:

    """ application_security class """

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
        self.filter=input('Would you like to enter a FILTER? y  or n: ').strip()
        if self.filter.lower()=='y':
            filtercategory={1:'group_names',2:"network.name",3:"tags"}
            print()
            print('Index no:1.Group Name\nIndex No:2.Network Name\nIndex No:3.Tags')
            try:
                print()
                filtercategoryinput=filtercategory[int(input('Please insert the index number from option above for your "FILTER": ').strip())]
            except KeyError as e:
                    print('-------------------------------------')
                    print('Please enter the right index numbers from the option above wither 1,2 or 3')
                    print('Exiting')
                    exit()
            except Exception as e:
                        print('-------------------------------------')
                        print('There seems to be an exception')
                        print('Please enter the right index numbers from the option above wither 1,2 or 3')
                        print('Exiting')
                        exit()
            isisnot={1:False,2:True}
            try:
                print()
                isisnotinput=isisnot[int(input('Please enter 1 for "IS" , 2 for "IS NOT": ').strip())]
            except KeyError as e:
                    print('-------------------------------------')
                    print('Please enter the right index numbers from the option above either 1 or 2')
                    print('Exiting')
                    exit()
            except Exception as e:
                        print('-------------------------------------')
                        print('There seems to be an exception')
                        print('Please enter the right index numbers from the option above either 1 or 2')
                        print('Exiting')
                        exit()
            operator={1:"IN",2:"EXACT",3:"LIKE",4:"WILDCARD"}
            print()
            for key,value in operator.items():
                print(f'Index No : {key} - Value : {value}')
            try:
                print()
                operatorinput=operator[int(input('Please enter the "INDEX NUMBER" of the operator from above: ').strip())]
            except KeyError as e:
                    print('-------------------------------------')
                    print('Please enter the right index numbers from the option above')
                    print('Exiting')
                    exit()
            except Exception as e:
                    print('-------------------------------------')
                    print('There seems to be an exception')
                    print('Please enter the right index numbers from the option above either 1, 2,3 or 4')
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
                        valueinput=input('Please enter the index numbers of the "GROUPS" seperated by comma,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,if group is not found in the above list of groups,please proceed to type "no": ').strip().split(',')
                        valueinput=list(set(valueinput))
                        if operatorinput!='IN' and len(valueinput)>1:
                            print('You must choose only one index number for this operator\n')
                            print('Exiting')
                            exit()
                        if len(valueinput)>1:
                            for i in valueinput:
                                if i.isdigit()==False:
                                    print('Please do not enter any string or special characters\n')
                                    print('Exiting')
                                    exit()
                        if 'no' in valueinput:
                             valueinput=list(set(valueinput))
                             valueinput.remove('no')
                             while(True):
                                print()
                                nameinput=input('Please provide a search string to search for "GROUP NAME": ')
                                aggregate=self.rs.aggregate.get_groupsbyfilter(nameinput)
                                if aggregate==[]:
                                    print(f'No data found for {nameinput}\n')
                                    continue
                                groups={}
                                print()
                                print('Here are the available groups\n')
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
                                                print('Please do not enter any string or special characters\n')
                                                print('Exiting')
                                                exit()
                                    if 'no' in valueinput:
                                        valueinput=list(set(valueinput))
                                        valueinput.remove('no')
                                        continue
                                    if operatorinput!='IN' and len(valueinput)>1:
                                        print('You must choose only one index number for this operator\n')
                                        print('Exiting')
                                        exit()
                                    for value in valueinput:
                                        values.append(groups[int(value)])
                                except KeyError as e:
                                    print('-------------------------------------')
                                    print('Please enter the right index numbers from the option above\n')
                                    print('Exiting')
                                    exit()
                                except Exception as e:
                                        print('-------------------------------------')
                                        print('There seems to be an exception')
                                        print('Please enter the right index numbers from the option above\n')
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
                        valueinput=input('Please enter index numbers of the "TAGS" seperated by comma,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number: ').strip().split(',')
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
                        valueinput=input('Please enter index numbers of the "TAGS" seperated by comma,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,if tag name is not found in the above list of tags,please proceed to type "no": ').strip().split(',')
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
                                    valueinput=input('Please enter index numbers of the "TAGS" seperated by comma,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number, if the tag name is not available in the list above , please enter "no": ').strip().split(',')
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
                        valueinput=input('Please enter the indexes of the "NETWORKS" seperated by comma,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number: ').strip().split(',')
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
                            valueinput=input('Please enter the indexes of the "NETWORKS" seperated by comma,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,if you cannot find the network you want,please type "no": ').strip().split(',')
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
                self.dashboarddata['applications']={}
                if datafilter!=[]:
                    newfilter=[datafilter]
                if datafilter==[]:
                    newfilter=datafilter
                data=self.rs.applications.get_single_search_page(newfilter)
                self.dashboarddata['applications']['App Assets']=str(data['page']['totalElements'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Application assets data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                if datafilter==[]:
                    mainfilter=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                elif datafilter!=[]:
                    mainfilter=[datafilter,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                data=self.rs.application_findings.get_single_search_page(mainfilter)
                self.dashboarddata['applications']['App Findings']=str(data['page']['totalElements'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Application Findings data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                self.dashboarddata['Applications Findings by Type']={}
                if datafilter==[]:
                    mainfilter=[{"field":"findingType","exclusive":False,"operator":"EXACT","value":"SAST"},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                elif datafilter!=[]:
                    mainfilter=[datafilter,{"field":"findingType","exclusive":False,"operator":"EXACT","value":"SAST"},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                data=self.rs.application_findings.get_single_search_page(mainfilter)
                self.dashboarddata['Applications Findings by Type']['SAST']=str(data['page']['totalElements'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching SAST data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                if datafilter==[]:
                    mainfilter=[{"field":"findingType","exclusive":False,"operator":"EXACT","value":"DAST"},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                elif datafilter!=[]:
                    mainfilter=[datafilter,{"field":"findingType","exclusive":False,"operator":"EXACT","value":"DAST"},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                data=self.rs.application_findings.get_single_search_page(mainfilter)
                self.dashboarddata['Applications Findings by Type']['DAST']=str(data['page']['totalElements'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching DAST data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)

            try:
                if datafilter==[]:
                    mainfilter=[{"field":"findingType","exclusive":False,"operator":"EXACT","value":"OSS"},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                elif datafilter!=[]:
                    mainfilter=[datafilter,{"field":"findingType","exclusive":False,"operator":"EXACT","value":"OSS"},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                data=self.rs.application_findings.get_single_search_page(mainfilter)
                self.dashboarddata['Applications Findings by Type']['OSS']=str(data['page']['totalElements'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges,Exception) as ex:
                message = f"An exception has occurred while fetching OSS data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)

            try:
                if datafilter==[]:
                    mainfilter=[{"field":"findingType","exclusive":False,"operator":"EXACT","value":"CONTAINER"},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                elif datafilter!=[]:
                    mainfilter=[datafilter,{"field":"findingType","exclusive":False,"operator":"EXACT","value":"CONTAINER"},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                data=self.rs.application_findings.get_single_search_page(mainfilter)
                self.dashboarddata['Applications Findings by Type']['Container']=str(data['page']['totalElements'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges,Exception) as ex:
                message = f"An exception has occurred while fetching Container data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                self.dashboarddata['Open Application findings']={}
                if datafilter==[]:
                    mainfilter=[{"field":"has_top_25_cwe","exclusive":False,"operator":"EXACT","value":"true"},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                elif datafilter!=[]:
                    mainfilter=[datafilter,{"field":"has_top_25_cwe","exclusive":False,"operator":"EXACT","value":"true"},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                data=self.rs.application_findings.get_single_search_page(mainfilter)
                self.dashboarddata['Open Application findings']['CWE TOP 25']=str(data['page']['totalElements'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges,Exception) as ex:
                message = f"An exception has occurred while fetching CWE TOP 25 data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)

            try:
                if datafilter==[]:
                    mainfilter=[{"field":"has_owasp_top_10","exclusive":False,"operator":"EXACT","value":"true"},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                elif datafilter!=[]:
                    mainfilter=[datafilter,{"field":"has_owasp_top_10","exclusive":False,"operator":"EXACT","value":"true"},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                data=self.rs.application_findings.get_single_search_page(mainfilter)
                self.dashboarddata['Open Application findings']['OWASP TOP 10']=str(data['page']['totalElements'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges,Exception) as ex:
                message = f"An exception has occurred while fetching OWASP TOP 10 data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)

            try:
                if datafilter==[]:
                    mainfilter=[{"field":"has_owasp_top_10","exclusive":False,"operator":"EXACT","value":"true"},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                elif datafilter!=[]:
                    mainfilter=[datafilter,{"field":"has_owasp_top_10","exclusive":False,"operator":"EXACT","value":"true"},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
                data=self.rs.application_findings.get_single_search_page(mainfilter)
                self.dashboarddata['Open Application findings']['OWASP TOP 10']=str(data['page']['totalElements'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges,Exception) as ex:
                message = f"An exception has occurred while fetching OWASP TOP 10 data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                if datafilter==[]:
                    mainfilter={"subject":"applicationFinding","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]}}
                elif datafilter!=[]:
                    mainfilter={"subject":"applicationFinding","filterRequest":{"filters":[datafilter,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]}}
                data=self.rs.aggregate.get_unique_findings_by_severity(mainfilter)
                if data!=[]:
                    self.dashboarddata['UniqueFinding']={}

                    self.dashboarddata['UniqueFinding']['Unique Finding']=[0,0,0,0,0]
                    self.dashboarddata['UniqueFinding']['Apps Affected']=[0,0,0,0,0]
                    self.dashboarddata['UniqueFinding']['Locations Affected']=[0,0,0,0,0]
                    criticality={'critical':0,'high':1,'medium':2,'low':3,'info':4}
                    for i in data.keys():
                        self.dashboarddata['UniqueFinding']['Unique Finding'][criticality[i]]=data[i]['uniqueFinding']['count']
                        self.dashboarddata['UniqueFinding']['Apps Affected'][criticality[i]]=data[i]['application']['count']
                        self.dashboarddata['UniqueFinding']['Locations Affected'][criticality[i]]=data[i]['url']['count']
                    print()
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges,Exception) as ex:
                message = f"An exception has occurred while fetching Unique findings by severity.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)


            try:
                if datafilter==[]:
                    mainfilter=[{"field":"findingsDistribution.total","operator":"GREATER","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"0"}]
                    sort=[{"field":"critical_count","direction":"DESC"},{"field":"high_count","direction":"DESC"},{"field":"medium_count","direction":"DESC"}]
                elif datafilter!=[]:
                    mainfilter=[datafilter,{"field":"findingsDistribution.total","operator":"GREATER","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"0"}]
                    sort=[{"field":"critical_count","direction":"DESC"},{"field":"high_count","direction":"DESC"},{"field":"medium_count","direction":"DESC"}]
                data=self.rs.applications.get_single_search_page_sortfield(mainfilter,sort_field=sort)
                if data['page']['totalElements']!=0:
                    self.dashboarddata['Top10vulnerableapplications']={}
                    self.dashboarddata['Top10vulnerableapplications']['Uri']=[]
                    self.dashboarddata['Top10vulnerableapplications']['Total']=[]
                    self.dashboarddata['Top10vulnerableapplications']['Critical']=[]
                    self.dashboarddata['Top10vulnerableapplications']['High']=[]
                    self.dashboarddata['Top10vulnerableapplications']['Medium']=[]
                    self.dashboarddata['Top10vulnerableapplications']['Low']=[]
                    self.dashboarddata['Top10vulnerableapplications']['Info']=[]
                    lastrange=10
                    if len(data["_embedded"]["applications"])<10:
                        lastrange=len(data["_embedded"]["applications"])
                    for i in range(0,lastrange):
                        self.dashboarddata['Top10vulnerableapplications']['Uri'].append(data["_embedded"]["applications"][i]['uri'])
                        self.dashboarddata['Top10vulnerableapplications']['Total'].append(data["_embedded"]["applications"][i]['findingsDistribution']['total']['value'])
                        self.dashboarddata['Top10vulnerableapplications']['Critical'].append(data["_embedded"]["applications"][i]['findingsDistribution']['critical']['value'])
                        self.dashboarddata['Top10vulnerableapplications']['High'].append(data["_embedded"]["applications"][i]['findingsDistribution']['high']['value'])
                        self.dashboarddata['Top10vulnerableapplications']['Medium'].append(data["_embedded"]["applications"][i]['findingsDistribution']['medium']['value'])
                        self.dashboarddata['Top10vulnerableapplications']['Low'].append(data["_embedded"]["applications"][i]['findingsDistribution']['low']['value'])
                        self.dashboarddata['Top10vulnerableapplications']['Info'].append(data["_embedded"]["applications"][i]['findingsDistribution']['info']['value'])
                else:
                    self.dashboarddata['Top10vulnerableapplications']={}
                    self.dashboarddata['Top10vulnerableapplications']['Uri']=['No data']
                    self.dashboarddata['Top10vulnerableapplications']['Total']=['No data']
                    self.dashboarddata['Top10vulnerableapplications']['Critical']=['No data']
                    self.dashboarddata['Top10vulnerableapplications']['High']=['No data']
                    self.dashboarddata['Top10vulnerableapplications']['Medium']=['No data']
                    self.dashboarddata['Top10vulnerableapplications']['Low']=['No data']
                    self.dashboarddata['Top10vulnerableapplications']['Info']=['No data']
                df = pd.DataFrame(self.dashboarddata['Top10vulnerableapplications'])
                df.to_csv('Top10VulnerableApplications.csv',index=None)
                print('---------------------------------------------------------------------')
                print('\nTop 10 Vulnerable Applications will be saved in your folder as Top10VulnerableApplications.csv')
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges,Exception) as ex:
                message = f"An exception has occurred while fetching Top 10 vulnerable applications data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)

            try:
                if datafilter==[]:
                    mainfilter={"subject":"applicationFinding","filters":[]}
                elif datafilter!=[]:
                    mainfilter={"subject":"applicationFinding","filters":[datafilter]}
                data=self.rs.aggregate.top_25_cwe(mainfilter)
                if data!=[]:
                    self.dashboarddata['cwetop25']={}
                    self.dashboarddata['cwetop25']['CWE Id']=[]
                    self.dashboarddata['cwetop25']['CWE Name']=[]
                    self.dashboarddata['cwetop25']['Applications']=[]
                    self.dashboarddata['cwetop25']['Locations']=[]
                    self.dashboarddata['cwetop25']['Findings']=[]
                    for i in range(len(data['topSoftwareErrors'])):
                        self.dashboarddata['cwetop25']['CWE Id'].append(data['topSoftwareErrors'][i]['cweId'])
                        self.dashboarddata['cwetop25']['CWE Name'].append(data['topSoftwareErrors'][i]['cweName'])
                        self.dashboarddata['cwetop25']['Applications'].append(data['topSoftwareErrors'][i]['applicationCount']['count'])
                        self.dashboarddata['cwetop25']['Locations'].append(data['topSoftwareErrors'][i]['urlsCount'])
                        self.dashboarddata['cwetop25']['Findings'].append(data['topSoftwareErrors'][i]['openFindingCount'])
                    df = pd.DataFrame(self.dashboarddata['cwetop25'])
                df.to_csv('cwetop25.csv',index=None)
                print('---------------------------------------------------------------------')
                print('\nThe cwe top 25 data will be saved in your folder as cwetop25.csv')
                print('---------------------------------------------------------------------')
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges,Exception) as ex:
                message = f"An exception has occurred while fetching cwe top 25 data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                if datafilter==[]:
                    mainfilter={"filters":[]}
                elif datafilter!=[]:
                    mainfilter={"filters":[datafilter]}
                data=self.rs.aggregate.owasp_distribution(mainfilter)
                if data!=[]:
                    self.dashboarddata['owasp_distribution']={}
                    self.dashboarddata['owasp_distribution']['owasp']=[]
                    self.dashboarddata['owasp_distribution']['title']=[]
                    self.dashboarddata['owasp_distribution']['App Assets']=[]
                    self.dashboarddata['owasp_distribution']['Locations']=[]
                    self.dashboarddata['owasp_distribution']['Open Findings']=[]
                    for i in range(len(data)):
                        self.dashboarddata['owasp_distribution']['owasp'].append(data[i]['owasp'])
                        self.dashboarddata['owasp_distribution']['title'].append(data[i]['title'])
                        self.dashboarddata['owasp_distribution']['App Assets'].append(data[i]['appCount']['count'])
                        self.dashboarddata['owasp_distribution']['Locations'].append(data[i]['urlsWithOwaspCount'])
                        self.dashboarddata['owasp_distribution']['Open Findings'].append(data[i]['openFindingsCount'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges,Exception) as ex:
                message = f"An exception has occurred while fetching owasp distribution data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)

            try:
                duration={'1':'daily','2':'weekly','3':'monthly','4':'quarterly'}
                print()
                for key,value in duration.items():
                    print(f'Index No:{key}- Value: {value}')
                try:
                    print()
                    durationchoice=duration[input('Please choose the index number from the option above the duration to view "APPLICATION FINDINGS DISCOVERED VS RESOLVED": ').strip()]
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
                data=self.rs.aggregate.get_findings_applicationfinding(duration=durationchoice,filter=datafilter)
                if data!=[]:
                    self.dashboarddata['applicationdiscovered']={}
                    self.dashboarddata['applicationdiscovered']['Date']=[]
                    self.dashboarddata['applicationdiscovered']['Total Discovered']=[]
                    self.dashboarddata['applicationdiscovered']['Threats']=[]
                    for i in range(len(data['openFindingDateHistogram'])):
                        self.dashboarddata['applicationdiscovered']['Date'].append(data['openFindingDateHistogram'][i]['date'])
                        self.dashboarddata['applicationdiscovered']['Total Discovered'].append(data['openFindingDateHistogram'][i]['count'])
                        self.dashboarddata['applicationdiscovered']['Threats'].append(data['openFindingDateHistogram'][i]['threatCount'])
                    self.dashboarddata['applicationresolved']={}
                    self.dashboarddata['applicationresolved']['Date']=[]
                    self.dashboarddata['applicationresolved']['Total Discovered']=[]
                    self.dashboarddata['applicationresolved']['Threats']=[]
                    for i in range(len(data['closeFindingDateHistogram'])):
                        self.dashboarddata['applicationresolved']['Date'].append(data['closeFindingDateHistogram'][i]['date'])
                        self.dashboarddata['applicationresolved']['Total Discovered'].append(data['closeFindingDateHistogram'][i]['count'])
                        self.dashboarddata['applicationresolved']['Threats'].append(data['closeFindingDateHistogram'][i]['threatCount'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges,Exception) as ex:
                message = f"An exception has occurred while fetching application findings discovered vs resolved data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
    
            try:
                if datafilter==[]:
                    mainfilter={"filterRequest":{"filters":[],"projection":"basic","sort":[{"field":"id","direction":"ASC"}],"size":10},"subject":"applicationFinding"}
                elif datafilter!=[]:
                    mainfilter={"filterRequest":{"filters":[datafilter],"projection":"basic","sort":[{"field":"id","direction":"ASC"}],"size":10},"subject":"applicationFinding"}
                data=self.rs.aggregate.top10uniquefindingsbyseverity(mainfilter)
                
                if data!=[]:
                    self.dashboarddata['Top10Uniqueapplication']={}
                    self.dashboarddata['Top10Uniqueapplication']['Title']=[]
                    self.dashboarddata['Top10Uniqueapplication']['Severity']=[]
                    self.dashboarddata['Top10Uniqueapplication']['Finding Type']=[]
                    self.dashboarddata['Top10Uniqueapplication']['Finding Footprint']=[]
                    for i in range(len(data)):
                        self.dashboarddata['Top10Uniqueapplication']['Title'].append(data[i]['title'])
                        self.dashboarddata['Top10Uniqueapplication']['Severity'].append(data[i]['maxSeverity'])
                        self.dashboarddata['Top10Uniqueapplication']['Finding Type'].append(data[i]['findingType'])
                        self.dashboarddata['Top10Uniqueapplication']['Finding Footprint'].append(data[i]['findingCount'])
                else:
                    self.dashboarddata['Top10Uniqueapplication']={}
                    self.dashboarddata['Top10Uniqueapplication']['Title']=['N/A']
                    self.dashboarddata['Top10Uniqueapplication']['Severity']=['N/A']
                    self.dashboarddata['Top10Uniqueapplication']['Finding Type']=['N/A']
                    self.dashboarddata['Top10Uniqueapplication']['Finding Footprint']=['N/A']
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges,Exception) as ex:
                message = f"An exception has occurred while fetching top 10 unique findings data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                mytable=PrettyTable()
                for key in self.dashboarddata['applications'].keys():
                    mytable.add_column(Fore.MAGENTA+key.upper(),[self.dashboarddata['applications'][key]])
                print()
                print(Fore.YELLOW+'\tApplications'.upper(),Fore.RESET)
                print(mytable,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating Applications kpi table.There must be no data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable1=PrettyTable()
                for key in self.dashboarddata['Applications Findings by Type'].keys():
                    mytable1.add_column(Fore.MAGENTA+key.upper(),[self.dashboarddata['Applications Findings by Type'][key]])
                print()
                print(Fore.YELLOW+'Applications Findings by Type'.upper(),Fore.RESET)
                print(mytable1,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating Applications Findings by Type kpi table.There must be no data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable2=PrettyTable()
                for key in self.dashboarddata['Open Application findings'].keys():
                    mytable2.add_column(Fore.MAGENTA+key.upper(),[self.dashboarddata['Open Application findings'][key]])
                print()
                print(Fore.YELLOW+' Open Application findings'.upper(),Fore.RESET)
                print(mytable2,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating Open Application findings kpi table.There must be no data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable3=PrettyTable()
                mytable3.add_column(Fore.MAGENTA+'Criticality',['Critical','High','Medium','Low','Info'])
                for key in self.dashboarddata['UniqueFinding'].keys():
                    mytable3.add_column(Fore.MAGENTA+key.upper(),self.dashboarddata['UniqueFinding'][key])
                print()
                print(Fore.YELLOW+'\t\t\tUniqueFinding'.upper(),Fore.RESET)
                print(mytable3,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating Unique Findings table.There must be no data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable4=PrettyTable()
                for key in self.dashboarddata['owasp_distribution'].keys():
                    mytable4.add_column(Fore.MAGENTA+key.upper(),self.dashboarddata['owasp_distribution'][key])
                print()
                print(Fore.YELLOW+'\t\towasp distribution'.upper(),Fore.RESET)
                print(mytable4,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating Owasp distribution table.There must be no data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable5=PrettyTable()
                for key in self.dashboarddata['applicationdiscovered'].keys():
                    mytable5.add_column(Fore.MAGENTA+key.upper(),self.dashboarddata['applicationdiscovered'][key])
                print()
                print(Fore.YELLOW+f'\tFindings Discovered - ({durationchoice})'.upper(),Fore.RESET)
                print(mytable5,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating Findings Discovered table.There must be no data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable6=PrettyTable()
                for key in self.dashboarddata['applicationresolved'].keys():
                    mytable6.add_column(Fore.MAGENTA+key.upper(),self.dashboarddata['applicationresolved'][key])
                print()
                print(Fore.YELLOW+f'\tFindings Resolved - ({durationchoice})'.upper(),Fore.RESET)
                print(mytable6,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating Findings Resolved table.There must be no data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable7=PrettyTable()
                for key in self.dashboarddata['Top10Uniqueapplication'].keys():
                    mytable7.add_column(Fore.MAGENTA+key.upper(),self.dashboarddata['Top10Uniqueapplication'][key])
                print()
                print(Fore.YELLOW+'\tTop 10 Unique Application Findings By Severity'.upper(),Fore.RESET)
                print(mytable7,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating Top 10 unique Findings table.There must be no data.For more details please view the ApplicationSecurity.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)


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
    

    log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs', f"ApplicationSecurity.log")

    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(levelname)s:  %(asctime)s > %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    print()
    print('For more details on the script process please view ApplicationSecurity.log found in the logs folder')
    #  Set config file path, and read the configuration.
    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
    config_contents = read_config_file(conf_file)

    try:
        application_security(config_contents)

    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt detected.  Exiting...")
        print()
        print("KeyboardInterrupt detected.  Exiting...")
        print()
        sys.exit(0)


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
   limitations under the License."""