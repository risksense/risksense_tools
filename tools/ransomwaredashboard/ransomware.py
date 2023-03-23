""" *******************************************************************************************************************
|
|  Name        :  ransomware.py
|  Project     :  Ransomware dashboard
|  Description :  A tool to display data from ransomware dashboard
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
import toml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rs_api
from datetime import datetime,date,timedelta
from prettytable import PrettyTable
from colorama import Fore, Back, Style
from termcolor import colored
import pandas as pd

class ransomware:

    """ Ransomware class """

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
            print(f"{message}. Exiting")
            exit(1)
        print()
        self.filter=input('Would you like to enter a "FILTER"? Y  or N: ').strip()
        if self.filter.lower()=='y':
            filtercategory={1:'group_names',2:"network.name",3:"tags"}
            print()
            print('Index No: 1 Value - Group Name\nIndex No: 2 Value - Network Name\nIndex No: 3 - Value - Tags')
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
                print(f'Index No:{key} - Value: {value}')
            try:
                print()
                operatorinput=operator[int(input('Please enter the index number of the "OPERATOR" from above: ').strip())]
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
                        valueinput=input('Please enter the Index No: of the "GROUPS" seperated by "COMMAS",Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number: ').strip().split(',')
                        valueinput=list(set(valueinput))
                        if len(valueinput)>1:
                            for i in valueinput:
                                if i.isdigit()==False:
                                    print('\nPlease do not enter any special characters or string')
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
                        valueinput=input('Please enter the index numbers of the "GROUPS" seperated by "COMMA",Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,if group is not found in the above list of groups,please proceed to type "no": ').strip().split(',')
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
                                nameinput=input('\nPlease provide a search string to search for "GROUP NAME": ')
                                aggregate=self.rs.aggregate.get_groupsbyfilter(nameinput)
                                if aggregate==[]:
                                    print(f'No data found for {nameinput}')
                                    continue
                                groups={}
                                print()
                                print('\nHere are the available groups')
                                for i in range(len(aggregate)):
                                    groups[i]=aggregate[i]['key']
                                    print(f'Index No: {i} - Value : {aggregate[i]["key"]}')
                                try:
                                    print()
                                    valueinput=input('Please enter the indexes of the "GROUPS" seperated by COMMA,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,If you do noy have the group name in the index number above please enter "no": ').strip().split(',')
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
                    filters=[datafilter,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"},{"field":"cve_data","exclusive":False,"operator":"NESTED","value":"[{\"field\":\"cve_data.has_ransomware\",\"operator\":\"EXACT\",\"exclusive\":false,\"orWithPrevious\":false,\"implicitFilters\":[],\"value\":\"true\"}]"}]
                else:
                    filters=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"},{"field":"cve_data","exclusive":False,"operator":"NESTED","value":"[{\"field\":\"cve_data.has_ransomware\",\"operator\":\"EXACT\",\"exclusive\":false,\"orWithPrevious\":false,\"implicitFilters\":[],\"value\":\"true\"}]"}]
                data=self.rs.aggregate.get_ransomwarefindings(filters)
                self.dashboarddata['openransomwarefindings']={}
                self.dashboarddata['openransomwarefindings']['openfindings']=str(data['findingsCount']['count'])
                self.dashboarddata['openransomwarefindings']['threats']=str(data['cveExploitCount']['count']+data['cveMalwareCount']['count'])
                self.dashboarddata['openransomwarefindings']['assetsimpacted']=str(data['assetsCount']['count'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching total assets data.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                if datafilter!=[]:
                    filters=[datafilter,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Closed"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"},{"field":"cve_data","exclusive":False,"operator":"NESTED","value":"[{\"field\":\"cve_data.has_ransomware\",\"operator\":\"EXACT\",\"exclusive\":false,\"orWithPrevious\":false,\"implicitFilters\":[],\"value\":\"true\"}]"}]
                else:
                    filters=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Closed"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"},{"field":"cve_data","exclusive":False,"operator":"NESTED","value":"[{\"field\":\"cve_data.has_ransomware\",\"operator\":\"EXACT\",\"exclusive\":false,\"orWithPrevious\":false,\"implicitFilters\":[],\"value\":\"true\"}]"}]
                data=self.rs.aggregate.get_ransomwarefindings(filters)
                self.dashboarddata['closedransomwarefindings']={}
                self.dashboarddata['closedransomwarefindings']['closefindings']=str(data['findingsCount']['count'])
                self.dashboarddata['closedransomwarefindings']['threats']=str(data['cveExploitCount']['count']+data['cveMalwareCount']['count'])
                self.dashboarddata['closedransomwarefindings']['assetsimpacted']=str(data['assetsCount']['count'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching closed ransomware findings.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                if datafilter!=[]:
                    filters=[datafilter,{"field":"malware_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"}]
                else:
                    filters=[{"field":"malware_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"}]
                data=self.rs.patch.get_single_search_page_ransomware("hostFinding",filters)
                self.dashboarddata['ransomwarefixes']=data['page']['totalElements']
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching ransomware fixes.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
            try:
                if datafilter!=[]:
                    filters=[datafilter,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_cves","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]
                else:
                    filters=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_cves","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]
                data=self.rs.aggregate.get_ransomwarefindings(filters)
                self.dashboarddata['ransomwarefunnel']={}
                self.dashboarddata['ransomwarefunnel']['totalvulnerabilities']={}
                self.dashboarddata['ransomwarefunnel']['totalvulnerabilities']['cvecount']=data['cveCount']['count']
                self.dashboarddata['ransomwarefunnel']['totalvulnerabilities']['findings']=data['findingsCount']['count']
                self.dashboarddata['ransomwarefunnel']['totalvulnerabilities']['threats']=data['cveExploitCount']['count']+data['cveMalwareCount']['count']+data['cveDefaultCredentialCount']['count']
                self.dashboarddata['ransomwarefunnel']['totalvulnerabilities']['assetsimpacted']=data['assetsCount']['count']
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching total vulnerabilities data.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
            try:
                if datafilter!=[]:
                    filters=[datafilter,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"},{"field":"cve_data","exclusive":False,"operator":"NESTED","value":"[{\"field\":\"cve_data.has_ransomware\",\"operator\":\"EXACT\",\"exclusive\":false,\"orWithPrevious\":false,\"implicitFilters\":[],\"value\":\"true\"}]"}]
                else:
                    filters=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"},{"field":"cve_data","exclusive":False,"operator":"NESTED","value":"[{\"field\":\"cve_data.has_ransomware\",\"operator\":\"EXACT\",\"exclusive\":false,\"orWithPrevious\":false,\"implicitFilters\":[],\"value\":\"true\"}]"}]
                data=self.rs.aggregate.get_ransomwarefindings(filters)
                self.dashboarddata['ransomwarefunnel']['ransomwareexposure']={}
                self.dashboarddata['ransomwarefunnel']['ransomwareexposure']['cvecount']=data['cveCount']['count']
                self.dashboarddata['ransomwarefunnel']['ransomwareexposure']['findings']=data['findingsCount']['count']
                self.dashboarddata['ransomwarefunnel']['ransomwareexposure']['threats']=data['cveExploitCount']['count']+data['cveMalwareCount']['count']+data['cveDefaultCredentialCount']['count']
                self.dashboarddata['ransomwarefunnel']['ransomwareexposure']['assetsimpacted']=data['assetsCount']['count']
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching ransomware exposure.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
            try:
                if datafilter!=[]:
                    filters=[datafilter,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"},{"field":"has_ransomware_with_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},{"field":"cve_data","exclusive":False,"operator":"NESTED","value":"[{\"field\":\"cve_data.has_ransomware\",\"operator\":\"EXACT\",\"exclusive\":false,\"orWithPrevious\":false,\"implicitFilters\":[],\"value\":\"true\"},{\"field\":\"cve_data.has_pe_rce\",\"operator\":\"EXACT\",\"exclusive\":false,\"orWithPrevious\":false,\"implicitFilters\":[],\"value\":\"true\"}]"}]
                else:
                    filters=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"},{"field":"has_ransomware_with_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},{"field":"cve_data","exclusive":False,"operator":"NESTED","value":"[{\"field\":\"cve_data.has_ransomware\",\"operator\":\"EXACT\",\"exclusive\":false,\"orWithPrevious\":false,\"implicitFilters\":[],\"value\":\"true\"},{\"field\":\"cve_data.has_pe_rce\",\"operator\":\"EXACT\",\"exclusive\":false,\"orWithPrevious\":false,\"implicitFilters\":[],\"value\":\"true\"}]"}]
                data=self.rs.aggregate.get_ransomwarefindings(filters)
                self.dashboarddata['ransomwarefunnel']['ransomwarewithrcepe']={}
                self.dashboarddata['ransomwarefunnel']['ransomwarewithrcepe']['cvecount']=data['cveCount']['count']
                self.dashboarddata['ransomwarefunnel']['ransomwarewithrcepe']['findings']=data['findingsCount']['count']
                self.dashboarddata['ransomwarefunnel']['ransomwarewithrcepe']['threats']=data['cveExploitCount']['count']+data['cveMalwareCount']['count']+data['cveDefaultCredentialCount']['count']
                self.dashboarddata['ransomwarefunnel']['ransomwarewithrcepe']['assetsimpacted']=data['assetsCount']['count']
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching ransomware with rce pe data.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
            try:
                if datafilter!=[]:
                    filters=[datafilter,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"},{"field":"ransomware_cve_trending_date","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},{"field":"cve_data","exclusive":False,"operator":"NESTED","value":"[{\"field\":\"cve_data.has_ransomware\",\"operator\":\"EXACT\",\"exclusive\":false,\"orWithPrevious\":false,\"implicitFilters\":[],\"value\":\"true\"},{\"field\":\"cve_data.vulnLastTrendingOn\",\"exclusive\":false,\"operator\":\"TRUE\",\"orWithPrevious\":false,\"implicitFilters\":[],\"value\":\"\"}]"}]
                else:
                    filters=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"},{"field":"ransomware_cve_trending_date","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},{"field":"cve_data","exclusive":False,"operator":"NESTED","value":"[{\"field\":\"cve_data.has_ransomware\",\"operator\":\"EXACT\",\"exclusive\":false,\"orWithPrevious\":false,\"implicitFilters\":[],\"value\":\"true\"},{\"field\":\"cve_data.vulnLastTrendingOn\",\"exclusive\":false,\"operator\":\"TRUE\",\"orWithPrevious\":false,\"implicitFilters\":[],\"value\":\"\"}]"}]
                data=self.rs.aggregate.get_ransomwarefindings(filters)
                self.dashboarddata['ransomwarefunnel']['trendingransomware']={}
                self.dashboarddata['ransomwarefunnel']['trendingransomware']['cvecount']=data['cveCount']['count']
                self.dashboarddata['ransomwarefunnel']['trendingransomware']['findings']=data['findingsCount']['count']
                self.dashboarddata['ransomwarefunnel']['trendingransomware']['threats']=data['cveExploitCount']['count']+data['cveMalwareCount']['count']+data['cveDefaultCredentialCount']['count']
                self.dashboarddata['ransomwarefunnel']['trendingransomware']['assetsimpacted']=data['assetsCount']['count']
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while Trending ransomware data.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
            try:
                data=self.rs.aggregate.get_ransomwarethreatbyage(datafilter)
                if data==[]:
                    self.dashboarddata['ransomwarethreatbyage']='0'
                else:
                    self.dashboarddata['ransomwarethreatbyage']={}
                    for i in range(len(data)):
                        self.dashboarddata['ransomwarethreatbyage'][data[i]['year']]=data[i]['total']['count']  
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
            rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Recently ingested data.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                data=self.rs.aggregate.get_ransomwarevulnerabilitiesbyfamily(datafilter)
                if data==[]:
                    self.dashboarddata['ransomwarecvefamily']=='0'
                else:
                    self.dashboarddata['ransomwarecvefamily']={}
                    self.dashboarddata['ransomwarecvefamily']['name']=[data[i]['ransomwareFamily'] for i in range(len(data))]
                    self.dashboarddata['ransomwarecvefamily']['cvescount']=[data[i]['cves']['count'] for i in range(len(data))]
                    self.dashboarddata['ransomwarecvefamily']['assetcount']=[data[i]['assets']['count'] for i in range(len(data))]
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
            rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Recently ingested data.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                data=self.rs.aggregate.get_topransomwarefamilies(datafilter)
                if data==[]:
                    self.dashboarddata['topransomwarefamilies']['ransomwareFamily']='N/A'
                    self.dashboarddata['topransomwarefamilies']['cvesaffected']='N/A'
                    self.dashboarddata['topransomwarefamilies']['assetsimpacted']='N/A'
                    self.dashboarddata['topransomwarefamilies']['findings']='N/A    '
                else:
                    self.dashboarddata['topransomwarefamilies']={}
                    self.dashboarddata['topransomwarefamilies']['ransomwareFamily']=[data[i]['ransomwareFamily'] for i in range(0,5)]
                    self.dashboarddata['topransomwarefamilies']['cvesaffected']=[','.join(data[i]['cves']) for i in range(0,5)]
                    self.dashboarddata['topransomwarefamilies']['assetsimpacted']=[data[i]['assetsCount']['count'] for i in range(0,5)]
                    self.dashboarddata['topransomwarefamilies']['findings']=[data[i]['findingsCount']['count'] for i in range(0,5)]
                df = pd.DataFrame(self.dashboarddata['topransomwarefamilies'])
                df.to_csv('topransomwarefamilies.csv',index=None)
                print()
                print('Top Ransomware families will be saved as a cve called topransomwarefamilies.cve\n')
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
            rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Recently ingested data.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                data=self.rs.aggregate.get_topransomwarecve(datafilter)
                if data==[]:
                    self.dashboarddata['topransomwarecve']['assetsimpacted']='N/A'
                    self.dashboarddata['topransomwarecve']['findings']='N/A'
                    self.dashboarddata['topransomwarecve']['cvename']='N/A'
                    self.dashboarddata['topransomwarecve']['ransomwareFamilies']='N/A'
                else:
                    self.dashboarddata['topransomwarecve']={}
                    for i in range(0,5):
                        self.dashboarddata['topransomwarecve']['assetsimpacted']=[data[i]['assetsCount']['count'] for i in range(0,5)]
                        self.dashboarddata['topransomwarecve']['findings']=[data[i]['findingsCount']['count'] for i in range(0,5)]
                        self.dashboarddata['topransomwarecve']['cvename']=[data[i]['cveId'] for i in range(0,5)]
                        self.dashboarddata['topransomwarecve']['ransomwareFamilies']=[','.join(data[i]['ransomwareFamilies']) for i in range(0,5)]
                df = pd.DataFrame(self.dashboarddata['topransomwarecve'])
                df.to_csv('topransomwarecve.csv',index=None)
                print()
                print('Top cves in ransomware families will be saved as a cve called topransomware.cve')
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
            rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Top ransomware.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                mytable=PrettyTable()
                for key in self.dashboarddata['openransomwarefindings'].keys():
                    mytable.add_column(Fore.MAGENTA+key.upper(),[self.dashboarddata['openransomwarefindings'][key]])
                print()
                print(Fore.YELLOW+'Open Ransomware Findings'.upper(),Fore.RESET)
                print(mytable,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating Open Ransomware Findings kpi table.There must be no data.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable1=PrettyTable()
                for key in self.dashboarddata['closedransomwarefindings'].keys():
                    mytable1.add_column(Fore.MAGENTA+key.upper(),[self.dashboarddata['closedransomwarefindings'][key]])
                print()
                print(Fore.YELLOW+'Closed Ransomware Findings'.upper(),Fore.RESET)
                print(mytable1,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating closed ransomware findings kpi table.There must be no data.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable2=PrettyTable()
                mytable2.add_column(Fore.MAGENTA+'ransomwarefixes'.upper(),[self.dashboarddata['ransomwarefixes']])
                print()
                print(Fore.YELLOW+'Ransomware Fixes Available'.upper(),Fore.RESET)
                print(mytable2,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating ransomware fixes available kpi table.There must be no data.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable3=PrettyTable()
                for key in self.dashboarddata['ransomwarefunnel']['totalvulnerabilities'].keys():
                    mytable3.add_column(Fore.MAGENTA+key.upper(),[self.dashboarddata['ransomwarefunnel']['totalvulnerabilities'][key]])
                print()
                print(Fore.YELLOW+'\t\t-----RANSOMWARE FUNNEL-----'.upper(),Fore.RESET)
                print(Fore.YELLOW+'\t\tTotal vulnerabilities'.upper(),Fore.RESET)
                print(mytable3,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating closed ransomware findings kpi table.There must be no data.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable4=PrettyTable()
                for key in self.dashboarddata['ransomwarefunnel']['ransomwareexposure'].keys():
                    mytable4.add_column(Fore.MAGENTA+key.upper(),[self.dashboarddata['ransomwarefunnel']['ransomwareexposure'][key]])
                print()
                print(Fore.YELLOW+'\t\tRansomware Exposure'.upper(),Fore.RESET)
                print(mytable4,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating closed ransomware findings kpi table.There must be no data.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable5=PrettyTable()
                for key in self.dashboarddata['ransomwarefunnel']['ransomwarewithrcepe'].keys():
                    mytable5.add_column(Fore.MAGENTA+key.upper(),[self.dashboarddata['ransomwarefunnel']['ransomwarewithrcepe'][key]])
                print()
                print(Fore.YELLOW+'\t\tRansomware with rce/pe exploits'.upper(),Fore.RESET)
                print(mytable5,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating closed ransomware findings kpi table.There must be no data.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                mytable6=PrettyTable()
                for key in self.dashboarddata['ransomwarefunnel']['trendingransomware'].keys():
                    mytable6.add_column(Fore.MAGENTA+key.upper(),[self.dashboarddata['ransomwarefunnel']['trendingransomware'][key]])
                print()
                print(Fore.YELLOW+'\t\tTrending ransomware'.upper(),Fore.RESET)
                print(mytable6,Fore.RESET)
                print(Fore.YELLOW+'-----------------------------------------------',Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating closed ransomware findings kpi table.There must be no data.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                if self.dashboarddata['ransomwarethreatbyage']=='0':
                    mytable7=PrettyTable()
                    mytable7.add_column(Fore.MAGENTA+'Year'.upper(),['0'])
                    mytable7.add_column(Fore.MAGENTA+'Count'.upper(),['0'])
                else:
                    mytable7=PrettyTable([Fore.MAGENTA+'Year'.upper(),Fore.MAGENTA+'Ransomware published'])
                    for key in self.dashboarddata['ransomwarethreatbyage'].keys():
                        mytable7.add_row([Fore.MAGENTA+key.upper(),Fore.MAGENTA+str(self.dashboarddata['ransomwarethreatbyage'][key])])
                print()
                print(Fore.YELLOW+'Ransomware threat by age'.upper(),Fore.RESET)
                print(mytable7,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating closed ransomware findings kpi table.There must be no data.For more details please view the Ransomware.log in the logs folder"
                logging.error(message)
                logging.error(e)
                print()
                print(message)
            try:
                if self.dashboarddata['ransomwarecvefamily']=='0':
                    mytable8=PrettyTable()
                    mytable8.add_column(Fore.MAGENTA+'Ransomware Family'.upper(),['0'])
                    mytable8.add_column(Fore.MAGENTA+'No of cves'.upper(),['0'])
                    mytable8.add_column(Fore.MAGENTA+'Assets impacted'.upper(),['0'])
                else:
                    mytable8=PrettyTable()
                    mytable8.add_column(Fore.MAGENTA+'Ransomware Family'.upper(),self.dashboarddata['ransomwarecvefamily']['name'])
                    mytable8.add_column(Fore.MAGENTA+'CVES'.upper(),self.dashboarddata['ransomwarecvefamily']['cvescount'])
                    mytable8.add_column(Fore.MAGENTA+'Assets impacted'.upper(),self.dashboarddata['ransomwarecvefamily']['assetcount'])
                print()
                print(Fore.YELLOW+'\tCVEs by ransomware family'.upper(),Fore.RESET)
                print(mytable8,Fore.RESET)
            except Exception as e :
                message = f"An exception has occurred while creating closed ransomware findings kpi table.There must be no data.For more details please view the Ransomware.log in the logs folder"
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
    log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs', f"Ransomware.log")
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(levelname)s:  %(asctime)s > %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    print('For more details on the script process please view Ransomware.log found in the logs folder')
    #  Set config file path, and read the configuration.
    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
    config_contents = read_config_file(conf_file)

    try:
        ransomware(config_contents)

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