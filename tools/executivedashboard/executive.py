""" *******************************************************************************************************************
|
|  Name        :  Executive_dashbord.py
|  Project     :  Executive Dashboard
|  Description :  A tool to display the executive dashboard
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
import datetime
import pandas as pd
from prettytable import PrettyTable
import json
from colorama import Fore, Back, Style
from termcolor import colored

class executive:

    """ Executive Dashboard class """

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
        self.filter=input('Would you like to enter a FILTER? "y"  or "n": ').strip()
        print()
        if self.filter.lower()=='y':
            filtercategory={1: 'group_names',2:"network.name",3:"tags"}
            print('Index No : 1 - Value : "Group name"\nIndex No : 2 - Value : "Network name"\nIndex No : 3 - Value : "Tags"')
            try:
                print()
                filtercategoryinput=filtercategory[int(input('Please insert the index number for the FILTER you want to select: ').strip())]
            except Exception as e:
                print('--------------------------------------------------')
                print('Please enter the right index as above either 1,2,3')
                print('Exiting')
                exit()
            isisnot={1:False,2:True}
            try:
                print()
                isisnotinput=isisnot[int(input('Please enter "1" for "IS" , "2" for "IS NOT": ').strip())]
            except Exception as e:
                print('Please enter either 1 or 2')
                print('Exiting')
                exit()
            operator={1:"IN",2:"EXACT",3:"LIKE",4:"WILDCARD"}
            print()
            for key,value in operator.items():
                print(f'Index No : {key} - Value : "{value}"')
            try:
                print()
                operatorinput=operator[int(input('Please enter the Index No of the OPERATOR from above: ').strip())]
            except Exception as e:
                print('Please enter the right Index No either 1,2,3 or 4')
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
                        valueinput=input('Please enter the Index No: of the GROUPS seperated by COMMAS,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number: ').strip().split(',')
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
                    print('Here are the suggested GROUP NAMES pulled from your client\n')
                    groups={}
                    for i in range(len(aggregate)):
                            groups[i]=aggregate[i]['key']
                            print(f'Index No : {i} - Value : {aggregate[i]["key"]}')
                    try:
                        print()
                        valueinput=input('Please enter the index numbers of the GROUPS seperated by comma,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,if GROUP is not found in the above list of GROUPS,please proceed to type "no": ').strip().split(',')
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
                                nameinput=input('Please provide a search string to search for GROUP NAME: ').strip()
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
                                    valueinput=input('Please enter the indexes of the GROUPS seperated by comma,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,If you do noy have the group name in the index number above please enter "no": ').strip().split(',')
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
                                yorno=input('Would you like to filter to more GROUPS? "Y" or "N": ').strip()
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
                        valueinput=input('Please enter index numbers of the TAGS seperated by comma,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number: ').strip().split(',')
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
                                nameinput=input('Please provide a search string for "TAG NAME": ').strip()
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
                                yorno=input('Would you like to filter to more "TAGS"? "Y" or "N": ').strip()
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
                                    nameinput=input('Please provide a search string to search for "NETWORK NAME": ').strip()
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
                                    yorno=input('Would you like to filter to more "NETWORKS"? Y or N: ').strip()
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
                    self.aggregate=self.rs.aggregate.get_dynamic_aggregation(filter=[datafilter])
                else:
                    self.aggregate=self.rs.aggregate.get_dynamic_aggregation(filter=datafilter)
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching total assets data.For details,please view Executive_dashboard.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                option={'1':self.aggregate[0][1],'2':self.aggregate[1][1],'3':str(int(self.aggregate[1][1])+int(self.aggregate[0][1]))}
            except Exception as e:
                logging.error(e)
                print(e)
                sys.exit()
            try:
                self.dashboarddata['totalassets']=option[input('Please enter the index number of how you would like to view "TOTAL ASSETS"\n\nIndex No:1 - Value : host\nIndex No:2 - Value : application\nIndex No:3 - Value : both\n\nProvide input here: ').strip()]
            except Exception as e:
                    print('-------------------------------------')
                    print('Please enter the right index as above')
                    print('Exiting')
                    exit()
            if self.dashboarddata['totalassets']=='0':
                self.dashboarddata['totalassets']='N/A'
            try:
                if datafilter!=[]:
                    filter=[{"field":"has_open_weaponization","exclusive":False,"operator":"EXACT","value":"True","orWithPrevious":False,"enabled":True,"implicitFilters":[],"altQueryConstruction":False},datafilter]
                if datafilter==[]:
                    filter=[{"field":"has_open_weaponization","exclusive":False,"operator":"EXACT","value":"True","orWithPrevious":False,"enabled":True,"implicitFilters":[],"altQueryConstruction":False}]
                self.aggregate=self.rs.aggregate.get_dynamic_aggregation(filter=filter)
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching total assets data.For details,please view Executive_dashboard.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                option={'1':self.aggregate[0][1],'2':self.aggregate[1][1],'3':str(int(self.aggregate[1][1])+int(self.aggregate[0][1]))}
            except Exception as e:
                logging.error(ex)
                print(ex)
                sys.exit()
            print()
            try:
                self.dashboarddata['assetswithweaponizedfindings']=option[input('Please enter the index number of how you would like to view "ASSETS WITH WEAPONIZED FINDINGS"\n\nIndex No:1 - Value : host\nIndex No:2 - Value : application\nIndex No:3 - Value : both\n\nProvide input here: ').strip()]
            except Exception as e:
                    print('-------------------------------------')
                    print('Please enter the right index as above')
                    print('Exiting')
                    exit()
            if self.dashboarddata['assetswithweaponizedfindings']=='0':
                self.dashboarddata['assetswithweaponizedfindings']='N/A'
            try:
                if datafilter!=[]:
                    filter=[{"field":"generic_state","exclusive":False,"operator":"EXACT","value":"Open","orWithPrevious":False,"enabled":True,"implicitFilters":[],"altQueryConstruction":False},datafilter]
                if datafilter==[]:
                    filter=[{"field":"generic_state","exclusive":False,"operator":"EXACT","value":"Open","orWithPrevious":False,"enabled":True,"implicitFilters":[],"altQueryConstruction":False}]
                self.aggregate=self.rs.aggregate.get_dynamic_aggregationforfindings(filter=filter)
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching total assets data.For details,please view Executive_dashboard.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                option={'1':self.aggregate[0][1],'2':self.aggregate[1][1],'3':str(int(self.aggregate[1][1])+int(self.aggregate[0][1]))}
            except Exception as e:
                message = f"An exception has occurred while fetching total open findings data.For details,please view Executive_dashboard.log for more details"
                logging.error(message)
                logging.error(ex)
                print(ex)
                sys.exit()
            try:
                print()
                self.dashboarddata['total_open_findings']=option[input('Please enter the index number of how you would like to view "TOTAL OPEN FINDINGS"\n\nIndex No:1 - Value : host\nIndex No:2 - Value : application\nIndex No:3 - Value : both\n\nProvide input here: ').strip()]
            except Exception as e:
                    print('-------------------------------------')
                    print('Please enter the right index as above')
                    print('Exiting')
                    exit()
            if self.dashboarddata['total_open_findings']=='0':
                self.dashboarddata['total_open_findings']='N/A'
            try:
                if datafilter!=[]:
                    self.newdatafilter=[datafilter]
                elif datafilter==[]:
                    self.newdatafilter=[]
                self.aggregate=self.rs.aggregate.get_total_fixes(filter=self.newdatafilter)
                self.dashboarddata['total_fixes']=self.aggregate[0][1]
                if self.dashboarddata['total_fixes']=='0':
                    self.dashboarddata['total_fixes']='N/A'
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching total fixes data.For details,please view Executive_dashboard.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                if datafilter!=[]:
                    self.newdatafilter=[datafilter]
                elif datafilter==[]:
                    self.newdatafilter=[]
                self.aggregate=self.rs.aggregate.get_rs3_aggregate(self.newdatafilter)
                self.dashboarddata['rs3']={}
                self.dashboarddata['rs3']['hostrs3']=self.aggregate['hostRs3']['rs3']
                self.dashboarddata['rs3']['apprs3']=self.aggregate['appRs3']['rs3']
                self.dashboarddata['rs3']['overallrs3']=self.aggregate['clientRs3']['rs3']
                if  self.dashboarddata['rs3']['hostrs3']==-1:
                    self.dashboarddata['rs3']['hostrs3']='N/A'
                if  self.dashboarddata['rs3']['apprs3']==-1:
                    self.dashboarddata['rs3']['apprs3']='N/A'
                if  self.dashboarddata['rs3']['overallrs3']==-1:
                    self.dashboarddata['rs3']['overallrs3']='N/A'
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching overall rs3 data.For details,please view Executive_dashboard.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                getsystemfilter=self.rs.aggregate.get_systemfilter()
                self.uuid=''
                for i in range(len(getsystemfilter)):
                    if getsystemfilter[i]['name']=="CISA Known Exploited":
                        self.uuid=getsystemfilter[i]['uuid']
                        break
                self.aggregate=self.rs.aggregate.get_cisaexploited_systemfilter(self.uuid,datafilter)
                self.dashboarddata['cisaknownexploited']={}
                self.dashboarddata['cisaknownexploited']['Identified']=self.aggregate['cveCount']
                self.dashboarddata['cisaknownexploited']['Overall']=self.aggregate['host']['total']['count']
                self.dashboarddata['cisaknownexploited']['External']=self.aggregate['host']['external']['count']
                self.dashboarddata['cisaknownexploited']['Internal']=self.aggregate['host']['internal']['count']
                self.dashboarddata['cisaknownexploited']['Total']=self.aggregate['hostFinding']['total']['count']
                self.dashboarddata['cisaknownexploited']['Overdue']=self.aggregate['hostFinding']['overdue']['count']
                self.dashboarddata['cisaknownexploited']['Not under sla']=self.aggregate['hostFinding']['notUnderSLA']['count']
                if  self.dashboarddata['cisaknownexploited']['Identified']==0:
                    self.dashboarddata['cisaknownexploited']['Identified']='N/A'
                if  self.dashboarddata['cisaknownexploited']['Overall']==0:
                    self.dashboarddata['cisaknownexploited']['Overall']='N/A'
                if  self.dashboarddata['cisaknownexploited']['External']==0:
                    self.dashboarddata['cisaknownexploited']['External']='N/A'
                if  self.dashboarddata['cisaknownexploited']['Internal']==0:
                    self.dashboarddata['cisaknownexploited']['Internal']='N/A'
                if  self.dashboarddata['cisaknownexploited']['Total']==0:
                    self.dashboarddata['cisaknownexploited']['Total']='N/A'
                if  self.dashboarddata['cisaknownexploited']['Overdue']==0:
                    self.dashboarddata['cisaknownexploited']['Overdue']='N/A'
                if  self.dashboarddata['cisaknownexploited']['Not under sla']==0:
                    self.dashboarddata['cisaknownexploited']['Not under sla']='N/A'
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching cisa known exploited data.For details,please view Executive_dashboard.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                try:
                    print()
                    startdate=str(datetime.datetime.strptime(input('Please enter "START DATE" in YYYY-MM-DD: ').strip(),'%Y-%m-%d').date())
                except Exception as ex:
                    print('Error in the start date input,Please provide the  start date in YYYY-MM-DD format')
                    print('Exiting')
                    exit()
                try:
                    print()
                    enddate=str(datetime.datetime.strptime(input('Please enter "END DATE" in YYYY-MM-DD: ').strip(),'%Y-%m-%d').date())
                except Exception as ex:
                    print('Error in the end date input,Please provide the end date in YYYY-MM-DD format')
                    print('Exiting')
                    exit()
                if datafilter!=[]:
                    newdatafilter=None
                    newdatafilter=[datafilter]
                if datafilter==[]:
                    newdatafilter=None
                    newdatafilter=[]
                getrs3history=self.rs.aggregate.get_rs3_history(startdate,enddate,newdatafilter)
                rs3choice={1: 'host',2: 'app',3: 'client'}
                print()
                print('Index No: 1 - Value : host\nIndex No: 2 - Value : application\nIndex No: 3 - Value : both ')
                try:
                    print()
                    rs3=rs3choice[int(input('Please choose rs3 choice index for RS3 TIMELINE from the option above: ').strip())]
                except Exception as e:
                    print('--------------------------------------------------')
                    print('Please enter the right index as above either 1,2,3')
                    print('Exiting')
                    exit()
                if getrs3history!=[]:
                    details={}
                    details['date']=[]
                    details['rs3']=[]
                    details['riskAcceptedRs3']=[]
                    details['Assets']=[]
                    details['Findings']=[]
                    details['Critical']=[]
                    details['High']=[]
                    details['Medium']=[]
                    details['Low']=[]
                    details['Info']=[]
                    for i in range(len(getrs3history)):
                        details['date'].append(getrs3history[i]['date'])
                        details['rs3'].append(getrs3history[i][rs3]['rs3'])
                        details['riskAcceptedRs3'].append(getrs3history[i][rs3]['riskAcceptedRs3'])
                        details['Assets'].append(getrs3history[i][rs3]['assetCount'])
                        details['Findings'].append(getrs3history[i][rs3]['findingCount'])
                        details['Critical'].append(getrs3history[i][rs3]['criticalCount'])
                        details['High'].append(getrs3history[i][rs3]['highCount'])
                        details['Medium'].append(getrs3history[i][rs3]['mediumCount'])
                        details['Low'].append(getrs3history[i][rs3]['lowCount'])
                        details['Info'].append(getrs3history[i][rs3]['infoCount'])
                else:
                    details={}
                    details['date']=['No data']
                    details['rs3']=['No data']
                    details['riskAcceptedRs3']=['No data']
                    details['Assets']=['No data']
                    details['Findings']=['No data']
                    details['Critical']=['No data']
                    details['High']=['No data']
                    details['Medium']=['No data']
                    details['Low']=['No data']
                    details['Info']=['No data']
                df = pd.DataFrame(details)
                df.to_csv('Rs3timeline.csv',index=None)
                print('---------------------------------------------------------------------')
                print('\nIvanti Rs3 Timeline will be saved in your folder as Rs3timeline.csv')
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching Rs3 timeline data.For details,please view Executive_dashboard.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                data=self.rs.aggregate.get_findings_funnel(datafilter)
                criticality={'Medium':2,'Info':4,'High':1,'Low':3,'Critical':0}
                self.dashboarddata['findingsfunnel']={}
                self.dashboarddata['findingsfunnel']['Total']={}
                self.dashboarddata['findingsfunnel']['Weaponized']={}
                self.dashboarddata['findingsfunnel']['RCE PE']={}
                self.dashboarddata['findingsfunnel']['Trending']={}
                self.dashboarddata['findingsfunnel']['ManualExploit']={}
                self.dashboarddata['findingsfunnel']['Total']['Openfindings']=['N/A','N/A','N/A','N/A','N/A']
                self.dashboarddata['findingsfunnel']['Total']['Assets']=['N/A','N/A','N/A','N/A','N/A']
                self.dashboarddata['findingsfunnel']['Weaponized']['Openfindings']=['N/A','N/A','N/A','N/A','N/A']
                self.dashboarddata['findingsfunnel']['Weaponized']['Assets']=['N/A','N/A','N/A','N/A','N/A']
                self.dashboarddata['findingsfunnel']['RCE PE']['Openfindings']=['N/A','N/A','N/A','N/A','N/A']
                self.dashboarddata['findingsfunnel']['RCE PE']['Assets']=['N/A','N/A','N/A','N/A','N/A']
                self.dashboarddata['findingsfunnel']['Trending']['Openfindings']=['N/A','N/A','N/A','N/A','N/A']
                self.dashboarddata['findingsfunnel']['Trending']['Assets']=['N/A','N/A','N/A','N/A','N/A']
                self.dashboarddata['findingsfunnel']['ManualExploit']['Openfindings']=['N/A','N/A','N/A','N/A','N/A']
                self.dashboarddata['findingsfunnel']['ManualExploit']['Assets']=['N/A','N/A','N/A','N/A','N/A']
                
                if data[0]=={} and data[15]=={}:
                    pass
                else:
                    for key in data[0]:
                        if key in data[15].keys():
                            self.dashboarddata['findingsfunnel']['Total']['Openfindings'][criticality[key]]=str(int(data[0][key]['Total'])+int(data[15][key]['Total']))
                            if self.dashboarddata['findingsfunnel']['Total']['Openfindings'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['Total']['Openfindings'][criticality[key]]='N/A'
                            self.dashboarddata['findingsfunnel']['Weaponized']['Openfindings'][criticality[key]]=str(int(data[0][key]['Weaponized'])+int(data[15][key]['Weaponized']))
                            if self.dashboarddata['findingsfunnel']['Weaponized']['Openfindings'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['Weaponized']['Openfindings'][criticality[key]]='N/A'
                            self.dashboarddata['findingsfunnel']['RCE PE']['Openfindings'][criticality[key]]=str(int(data[0][key]['RCE PE'])+int(data[15][key]["RCE PE"]))
                            if self.dashboarddata['findingsfunnel']['RCE PE']['Openfindings'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['RCE PE']['Openfindings'][criticality[key]]='N/A'
                            self.dashboarddata['findingsfunnel']['ManualExploit']['Openfindings'][criticality[key]]=str(int(data[0][key]['ME'])+int(data[15][key]["ME"]))
                            if self.dashboarddata['findingsfunnel']['ManualExploit']['Openfindings'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['ManualExploit']['Openfindings'][criticality[key]]='N/A'
                            self.dashboarddata['findingsfunnel']['Trending']['Openfindings'][criticality[key]]=str(int(data[0][key]['Trending'])+int(data[15][key]["Trending"]))
                            if self.dashboarddata['findingsfunnel']['Trending']['Openfindings'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['Trending']['Openfindings'][criticality[key]]='N/A'
                        else:
                            self.dashboarddata['findingsfunnel']['Total']['Openfindings'][criticality[key]]=data[0][key]['Total']
                            if self.dashboarddata['findingsfunnel']['Total']['Openfindings'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['Total']['Openfindings'][criticality[key]]='N/A'
                            self.dashboarddata['findingsfunnel']['Weaponized']['Openfindings'][criticality[key]]=data[0][key]['Weaponized']
                            if self.dashboarddata['findingsfunnel']['Weaponized']['Openfindings'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['Weaponized']['Openfindings'][criticality[key]]='N/A'
                            self.dashboarddata['findingsfunnel']['RCE PE']['Openfindings'][criticality[key]]=data[0][key]['RCE PE']
                            ['Weaponized']
                            if self.dashboarddata['findingsfunnel']['RCE PE']['Openfindings'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['RCE PE']['Openfindings'][criticality[key]]='N/A'
                            self.dashboarddata['findingsfunnel']['ManualExploit']['Openfindings'][criticality[key]]=data[0][key]["ME"]
                            if self.dashboarddata['findingsfunnel']['ManualExploit']['Openfindings'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['ManualExploit']['Openfindings'][criticality[key]]='N/A'
                            self.dashboarddata['findingsfunnel']['Trending']['Openfindings'][criticality[key]]=data[0][key]['Trending']
                            if self.dashboarddata['findingsfunnel']['Trending']['Openfindings'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['Trending']['Openfindings'][criticality[key]]='N/A'
                    for key in data[15]:
                        if key not in data[0].keys():
                            self.dashboarddata['findingsfunnel']['Total']['Openfindings'][criticality[key]]=data[15][key]['Total']
                            if self.dashboarddata['findingsfunnel']['Total']['Openfindings'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['Total']['Openfindings'][criticality[key]]='N/A'
                            self.dashboarddata['findingsfunnel']['Weaponized']['Openfindings'][criticality[key]]=data[15][key]['Weaponized']
                            if self.dashboarddata['findingsfunnel']['Weaponized']['Openfindings'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['Weaponized']['Openfindings'][criticality[key]]='N/A'
                            self.dashboarddata['findingsfunnel']['RCE PE']['Openfindings'][criticality[key]]=data[15][key]['RCE PE']
                            if self.dashboarddata['findingsfunnel']['RCE PE']['Openfindings'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['RCE PE']['Openfindings'][criticality[key]]='N/A'
                            self.dashboarddata['findingsfunnel']['ManualExploit']['Openfindings'][criticality[key]]=data[15][key]['ME']
                            if self.dashboarddata['findingsfunnel']['ManualExploit']['Openfindings'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['ManualExploit']['Openfindings'][criticality[key]]='N/A'
                            self.dashboarddata['findingsfunnel']['Trending']['Openfindings'][criticality[key]]=data[15][key]['Trending']
                            if self.dashboarddata['findingsfunnel']['Trending']['Openfindings'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['Trending']['Openfindings'][criticality[key]]='N/A'
                    for key in data[2]:
                        if key in data[17].keys():
                            self.dashboarddata['findingsfunnel']['Total']['Assets'][criticality[key]]=str(int(data[2][key]['Total'])+int(data[17][key]['Total']))
                            if self.dashboarddata['findingsfunnel']['Total']['Assets'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['Total']['Assets'][criticality[key]]='N/A'
                        else:
                            self.dashboarddata['findingsfunnel']['Total']['Assets'][criticality[key]]=data[2][key]['Total']
                            if self.dashboarddata['findingsfunnel']['Total']['Assets'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['Total']['Assets'][criticality[key]]='N/A'
                    for key in data[17]:
                        if key not in data[2].keys():
                            self.dashboarddata['findingsfunnel']['Total']['Assets'][criticality[key]]=data[17][key]['Total']
                            if self.dashboarddata['findingsfunnel']['Total']['Assets'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['Total']['Assets'][criticality[key]]='N/A'
                    for key in data[4]:
                        if key in data[19].keys():
                            self.dashboarddata['findingsfunnel']['Weaponized']['Assets'][criticality[key]]=str(int(data[4][key]['Total'])+int(data[19][key]['Total']))
                            if self.dashboarddata['findingsfunnel']['Weaponized']['Assets'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['Weaponized']['Assets'][criticality[key]]='N/A'
                        else:
                            self.dashboarddata['findingsfunnel']['Weaponized']['Assets'][criticality[key]]=data[4][key]['Total']
                            if self.dashboarddata['findingsfunnel']['Weaponized']['Assets'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['Weaponized']['Assets'][criticality[key]]='N/A'
                    for key in data[19]:
                        if key not in data[4].keys():
                            self.dashboarddata['findingsfunnel']['Weaponized']['Assets'][criticality[key]]=data[19][key]['Total']
                            if self.dashboarddata['findingsfunnel']['Weaponized']['Assets'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['Weaponized']['Assets'][criticality[key]]='N/A'
                    for key in data[6]:
                        if key in data[21].keys():
                            self.dashboarddata['findingsfunnel']['RCE PE']['Assets'][criticality[key]]=str(int(data[6][key]['Total'])+int(data[21][key]['Total']))
                            if self.dashboarddata['findingsfunnel']['RCE PE']['Assets'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['RCE PE']['Assets'][criticality[key]]='N/A'
                        else:
                            self.dashboarddata['findingsfunnel']['RCE PE']['Assets'][criticality[key]]=data[6][key]['Total']
                            if self.dashboarddata['findingsfunnel']['RCE PE']['Assets'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['RCE PE']['Assets'][criticality[key]]='N/A'
                    for key in data[21]:
                        if key not in data[6].keys():
                            self.dashboarddata['findingsfunnel']['RCE PE']['Assets'][criticality[key]]=data[21][key]['Total']
                            if self.dashboarddata['findingsfunnel']['RCE PE']['Assets'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['RCE PE']['Assets'][criticality[key]]='N/A'
                    j=23
                    for i in range(8,13):
                            vrrhost=data[i][0].split(' ')
                            self.dashboarddata['findingsfunnel']['Trending']['Assets'][criticality[vrrhost[1]]]=str(int(data[i][1])+int(data[j][1]))
                            if self.dashboarddata['findingsfunnel']['Trending']['Assets'][criticality[vrrhost[1]]]=='0':
                                self.dashboarddata['findingsfunnel']['Trending']['Assets'][criticality[vrrhost[1]]]='N/A'
                            j=j+1
                    for key in data[14]:
                        if key in data[29].keys():
                            self.dashboarddata['findingsfunnel']['ManualExploit']['Assets'][criticality[key]]=str(int(data[14][key]['Total'])+int(data[29][key]['Total']))
                            if self.dashboarddata['findingsfunnel']['ManualExploit']['Assets'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['ManualExploit']['Assets'][criticality[key]]='N/A'
                        else:
                            self.dashboarddata['findingsfunnel']['ManualExploit']['Assets'][criticality[key]]=data[614][key]['Total']
                            if self.dashboarddata['findingsfunnel']['ManualExploit']['Assets'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['ManualExploit']['Assets'][criticality[key]]='N/A'
                    for key in data[29]:
                        if key not in data[14].keys():
                            self.dashboarddata['findingsfunnel']['ManualExploit']['Assets'][criticality[key]]=data[29][key]['Total']
                            if self.dashboarddata['findingsfunnel']['ManualExploit']['Assets'][criticality[key]]=='0':
                                self.dashboarddata['findingsfunnel']['ManualExploit']['Assets'][criticality[key]]='N/A'
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching findings prioritization funnel data.For details,please view Executive_dashboard.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                data=self.rs.aggregate.get_weaponization_funnel(datafilter)
                criticality={'Medium':0,'Info':1,'High':2,'Low':3,'Critical':4}
                self.dashboarddata['weaponizationfunnel']={}
                self.dashboarddata['weaponizationfunnel']['Open']={}
                self.dashboarddata['weaponizationfunnel']['Weaponized']={}
                self.dashboarddata['weaponizationfunnel']['RCE PE']={}
                self.dashboarddata['weaponizationfunnel']['Trending']={}
                self.dashboarddata['weaponizationfunnel']['ManualExploit']={}
                self.dashboarddata['weaponizationfunnel']['Open']['openFindings']='N/A'
                self.dashboarddata['weaponizationfunnel']['Open']['uniqueFindings']='N/A'
                self.dashboarddata['weaponizationfunnel']['Open']['uniqueCVEs']='N/A'
                self.dashboarddata['weaponizationfunnel']['Open']['threats']='N/A'
                self.dashboarddata['weaponizationfunnel']['Weaponized']['openFindings']='N/A'
                self.dashboarddata['weaponizationfunnel']['Weaponized']['uniqueFindings']='N/A'
                self.dashboarddata['weaponizationfunnel']['Weaponized']['uniqueCVEs']='N/A'
                self.dashboarddata['weaponizationfunnel']['Weaponized']['threats']='N/A'
                self.dashboarddata['weaponizationfunnel']['RCE PE']['openFindings']='N/A'
                self.dashboarddata['weaponizationfunnel']['RCE PE']['uniqueFindings']='N/A'
                self.dashboarddata['weaponizationfunnel']['RCE PE']['uniqueCVEs']='N/A'
                self.dashboarddata['weaponizationfunnel']['RCE PE']['threats']='N/A'
                self.dashboarddata['weaponizationfunnel']['Trending']['openFindings']='N/A'
                self.dashboarddata['weaponizationfunnel']['Trending']['uniqueFindings']='N/A'
                self.dashboarddata['weaponizationfunnel']['Trending']['uniqueCVEs']='N/A'
                self.dashboarddata['weaponizationfunnel']['Trending']['threats']='N/A'
                self.dashboarddata['weaponizationfunnel']['ManualExploit']['openFindings']='N/A'
                self.dashboarddata['weaponizationfunnel']['ManualExploit']['uniqueFindings']='N/A'
                self.dashboarddata['weaponizationfunnel']['ManualExploit']['uniqueCVEs']='N/A'
                self.dashboarddata['weaponizationfunnel']['ManualExploit']['threats']='N/A'
                self.dashboarddata['weaponizationfunnel']['Openassets']='N/A'
                self.dashboarddata['weaponizationfunnel']['Openfixes']='N/A'
                self.dashboarddata['weaponizationfunnel']['weaponizedassets']='N/A'
                self.dashboarddata['weaponizationfunnel']['weaponizedfixes']='N/A'
                self.dashboarddata['weaponizationfunnel']['rcepeassets']='N/A'
                self.dashboarddata['weaponizationfunnel']['rcepefixes']='N/A'
                self.dashboarddata['weaponizationfunnel']['Trendingassets']='N/A'
                self.dashboarddata['weaponizationfunnel']['Trendingfixes']='N/A'
                self.dashboarddata['weaponizationfunnel']['Manualexploitassets']='N/A'
                self.dashboarddata['weaponizationfunnel']['Manualexploitfixes']='N/A'
                with open('weaponizationfunneldata.json','w') as f:
                    f.write(json.dumps(data))
                if data[0]=={}:
                    pass
                else:
                    for key in data[0]['Open']:
                        if type(data[0]['Open'][key])!=dict:
                            self.dashboarddata['weaponizationfunnel']['Open'][key]=data[0]['Open'][key]
                            if self.dashboarddata['weaponizationfunnel']['Open'][key]=='0':
                                self.dashboarddata['weaponizationfunnel']['Open'][key]='N/A'
                        if data[11]!={}:
                            if data[11]['Open']!=[] and key in data[11]['Open'].keys():
                                if type(data[11]['Open'][key])!=dict:
                                    self.dashboarddata['weaponizationfunnel']['Open'][key]=str(int(data[0]['Open'][key])+int(data[11]['Open'][key]))
                                    if self.dashboarddata['weaponizationfunnel']['Open'][key]=='0':
                                            self.dashboarddata['weaponizationfunnel']['Open'][key]='N/A'
                    if data[1]!=[]:
                        self.dashboarddata['weaponizationfunnel']['Openassets']=data[1][1]
                    if data[12]!=[]:
                        self.dashboarddata['weaponizationfunnel']['Openassets']=data[12][1]
                    if data[1]!=[] and data[12]!=[]:
                        self.dashboarddata['weaponizationfunnel']['Openassets']=str(int(data[12][1])+int(data[1][1]))
                    if data[6]!=[]:
                        self.dashboarddata['weaponizationfunnel']['Openfixes']=data[6][1]
                    if data[2]!=[]:
                        self.dashboarddata['weaponizationfunnel']['weaponizedassets']=data[2][1]
                    if data[13]!=[]:
                        self.dashboarddata['weaponizationfunnel']['weaponizedassets']=data[13][1]
                    if data[2]!=[] and data[13]!=[]:
                        self.dashboarddata['weaponizationfunnel']['weaponizedassets']=str(int(data[2][1])+int(data[13][1]))
                    if data[7]!=[]:
                        self.dashboarddata['weaponizationfunnel']['weaponizedfixes']=data[7][1]
                    if data[3]!=[]:
                        self.dashboarddata['weaponizationfunnel']['rcepeassets']=data[3][1]
                    if data[14]!=[]:
                        self.dashboarddata['weaponizationfunnel']['rcepeassets']=data[14][1]
                    if data[3]!=[] and data[14]!=[]:
                        self.dashboarddata['weaponizationfunnel']['rcepeassets']=str(int(data[3][1])+int(data[14][1]))
                    if data[8]!=[]:
                        self.dashboarddata['weaponizationfunnel']['rcepefixes']=data[8][1]
                    if data[4]!=[]:
                        self.dashboarddata['weaponizationfunnel']['Trendingassets']=data[4][1]
                    if data[15]!=[]:
                        self.dashboarddata['weaponizationfunnel']['Trendingassets']=data[15][1]
                    if data[4]!=[] and data[15]!=[]:
                        self.dashboarddata['weaponizationfunnel']['Trendingassets']=str(int(data[4][1])+int(data[15][1]))
                    if data[9]!=[]:
                        self.dashboarddata['weaponizationfunnel']['Trendingfixes']=data[9][1]
                    if data[5]!=[]:
                        self.dashboarddata['weaponizationfunnel']['Manualexploitassets']=data[5][1]
                    if data[16]!=[]:
                        self.dashboarddata['weaponizationfunnel']['Manualexploitassets']=data[16][1]
                    if data[5]!=[] and data[16]!=[]:
                        self.dashboarddata['weaponizationfunnel']['Manualexploitassets']=str(int(data[5][1])+int(data[16][1]))
                    if data[10]!=[]:
                        self.dashboarddata['weaponizationfunnel']['Manualexploitfixes']=data[10][1]
                    if data[0]['Open']['Weaponized']=={}:
                        pass
                    else:
                        if 'Open' in data[0]['Open']['Weaponized'].keys():
                            for key in data[0]['Open']['Weaponized']['Open']:
                                self.dashboarddata['weaponizationfunnel']['Weaponized'][key]=data[0]['Open']['Weaponized']['Open'][key]
                                if self.dashboarddata['weaponizationfunnel']['Weaponized'][key]=='0':
                                    self.dashboarddata['weaponizationfunnel']['Weaponized'][key]='N/A'
                                if data[11]!={}:
                                    if 'Open' in data[11]['Open']['Weaponized'].keys():
                                        if data[11]['Open']['Weaponized']['Open']!={} and key in data[11]['Open'].keys():
                                            self.dashboarddata['weaponizationfunnel']['Weaponized'][key]=str(int(data[0]['Open']['Weaponized']['Open'][key])+int(data[11]['Open']['Weaponized']['Open'][key]))
                                            if self.dashboarddata['weaponizationfunnel']['Weaponized'][key]=='0':
                                                    self.dashboarddata['weaponizationfunnel']['Weaponized'][key]='N/A'
                    if data[0]['Open']['RCE PE']=={}:
                        pass
                    else:
                        for key in data[0]['Open']['RCE PE']['Open']:
                            self.dashboarddata['weaponizationfunnel']['RCE PE'][key]=data[0]['Open']['RCE PE']['Open'][key]
                            if self.dashboarddata['weaponizationfunnel']['RCE PE'][key]=='0':
                                self.dashboarddata['weaponizationfunnel']['RCE PE'][key]='N/A'
                            if data[11]!={}:
                                if data[11]['Open']['RCE PE']!={}:
                                    if key in data[11]['Open']['RCE PE']['Open'].keys():
                                        self.dashboarddata['weaponizationfunnel']['RCE PE'][key]=str(int(data[0]['Open']['RCE PE']['Open'][key])+int(data[11]['Open']['RCE PE']['Open'][key]))
                                        if self.dashboarddata['weaponizationfunnel']['RCE PE'][key]=='0':
                                            self.dashboarddata['weaponizationfunnel']['RCE PE'][key]='N/A'               
                    if data[0]['Open']['Trending']=={}:
                        pass
                    else:
                        for key in data[0]['Open']['Trending']['Open']:
                            self.dashboarddata['weaponizationfunnel']['Trending'][key]=data[0]['Open']['Trending']['Open'][key]
                            if self.dashboarddata['weaponizationfunnel']['Trending'][key]=='0':
                                self.dashboarddata['weaponizationfunnel']['Trending'][key]='N/A'
                            if data[11]!={}:
                                if data[11]['Open']['Trending']!={}:
                                    if key in data[11]['Open']['Trending']['Open'].keys():
                                        self.dashboarddata['weaponizationfunnel']['Trending'][key]=str(int(data[0]['Open']['Trending']['Open'][key])+int(data[11]['Open']['Trending']['Open'][key]))
                                        if self.dashboarddata['weaponizationfunnel']['Trending'][key]=='0':
                                            self.dashboarddata['weaponizationfunnel']['Trending'][key]='N/A'
                    if data[0]['Open']['ME']=={}:
                        pass
                    else:
                        for key in data[0]['Open']['ME']['Open']:
                            self.dashboarddata['weaponizationfunnel']['ManualExploit'][key]=data[0]['Open']['ME']['Open']
                            if self.dashboarddata['weaponizationfunnel']['ManualExploit'][key]=='0':
                                self.dashboarddata['weaponizationfunnel']['ManualExploit'][key]='N/A'
                            if data[11]!={}:
                                if data[11]['Open']['ME']!={}:
                                    if key in data[11]['Open']['ME']['Open'].keys():
                                        self.dashboarddata['weaponizationfunnel']['ManualExploit'][key]=str(int(data[0]['Open']['ME']['Open'][key])+int(data[11]['Open']['ME']['Open'][key]))
                                        if self.dashboarddata['weaponizationfunnel']['ManualExploit'][key]=='0':
                                            self.dashboarddata['weaponizationfunnel']['ManualExploit'][key]='N/A'
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching weaponization data.For details,please view Executive_dashboard.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                data=self.rs.aggregate.get_exploitassetsbycriticality(datafilter)
                self.dashboarddata['Exploitassetsbycriticality']={}
                exploitassetsdict={'5':['N/A','N/A','N/A','N/A','N/A'],'4':['N/A','N/A','N/A','N/A','N/A'],'3':['N/A','N/A','N/A','N/A','N/A'],'2':['N/A','N/A','N/A','N/A','N/A'],'1':['N/A','N/A','N/A','N/A','N/A']}
                referencedict={'800-850':4,'700-799':3,'550-699':2,'400-549':1,'300-399':0}
                for key in data[0]:
                    for keykey in data[0][key]:
                        for keykeykey in data[0][key][keykey]:
                            n=key.split(' ')
                            exploitassetsdict[keykeykey][referencedict[n[0]]]=data[0][key][keykey][keykeykey]['Count']
                if data[1]!={}:
                  for key in data[1]:
                    for keykey in data[1][key]:
                        for keykeykey in data[1][key][keykey]:
                            n=key.split(' ')
                        if exploitassetsdict[keykeykey][referencedict[n[0]]]!='N/A':
                            exploitassetsdict[keykeykey][referencedict[n[0]]]=str(int(exploitassetsdict[keykeykey][referencedict[n[0]]])+int(data[1][key][keykey][keykeykey]['Count']))
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while exploit assets by criticality data.For details,please view Executive_dashboard.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                data=self.rs.aggregate.get_highimpactfindings(datafilter)
                finding={'findingtitle':[],'Plugin Id':[],'VRR':[],'Footprint':[]}
                for key in data[0]:
                    finding['findingtitle'].append(data[0][key]['Finding Title'][0]['title'])
                    finding['Plugin Id'].append(key)
                    finding['Footprint'].append(data[0][key]['Footprint Count'])
                    finding['VRR'].append(data[0][key]["Scoring Metric"])

                df = pd.DataFrame(finding)
                df.to_csv('Top50findings.csv',index=None)
                print('\nTop 50 High-Impact Unique findings will be saved in your folder as Top50findings.csv')
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching data.For details,please view Executive_dashboard.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                Totaloftotalopenfindings=sum([int(i) for i in self.dashboarddata['findingsfunnel']['Total']['Openfindings'] if i!='N/A'])
                TotaloftotalAssets=sum([int(i) for i in self.dashboarddata['findingsfunnel']['Total']['Assets'] if i!='N/A'])
                Totalofweaponizedopenfindings=sum([int(i) for i in self.dashboarddata['findingsfunnel']['Weaponized']['Openfindings'] if i!='N/A'])
                Totalofweaponizedassets=sum([int(i) for i in self.dashboarddata['findingsfunnel']['Weaponized']['Assets'] if i!='N/A'])
                Totalofrcepeopenfindings=sum([int(i) for i in self.dashboarddata['findingsfunnel']['RCE PE']['Openfindings'] if i!='N/A'])
                Totalofrcepeassets=sum([int(i) for i in self.dashboarddata['findingsfunnel']['RCE PE']['Assets'] if i!='N/A'])
                Totalofmanualexploitopenfindings=sum([int(i) for i in self.dashboarddata['findingsfunnel']['ManualExploit']['Openfindings'] if i!='N/A'])
                Totalofmanualexploitassets=sum([int(i) for i in self.dashboarddata['findingsfunnel']['ManualExploit']['Assets'] if i!='N/A'])
                Totaloftrendingopenfindings=sum([int(i) for i in self.dashboarddata['findingsfunnel']['Trending']['Openfindings'] if i!='N/A'])
                Totaloftrendingassets=sum([int(i) for i in self.dashboarddata['findingsfunnel']['Trending']['Assets'] if i!='N/A'])
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while fetching findings funnel.For details,please view Executive_dashboard.log for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                print(Fore.YELLOW+'\n  ---------------------RS3 Score----------------------'.upper(),Fore.RESET)
                overallrs3table=PrettyTable([Fore.MAGENTA+'overallrs3'.upper(),Fore.MAGENTA+'hostrs3'.upper(),Fore.MAGENTA+'apprs3'.upper()])
                overallrs3table.add_row([Fore.MAGENTA+str(self.dashboarddata['rs3']['overallrs3']),Fore.MAGENTA+str(self.dashboarddata['rs3']['hostrs3']),Fore.MAGENTA+str(self.dashboarddata['rs3']['apprs3'])])
                print(overallrs3table,Fore.RESET)
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while creating overall rs3 table, please view executive_dashboard.log for more information"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                print()
                mytable=PrettyTable([Fore.MAGENTA+'Total assets'.upper(),Fore.MAGENTA+'Assets with weaponized findings'.upper(),Fore.MAGENTA+'total open findings'.upper(),Fore.MAGENTA+'total fixes'.upper()])
                mytable.add_row([Fore.MAGENTA+self.dashboarddata['totalassets'],Fore.MAGENTA+self.dashboarddata['assetswithweaponizedfindings'],Fore.MAGENTA+self.dashboarddata['total_open_findings'],Fore.MAGENTA+self.dashboarddata['total_fixes']])
                print()
                print(Fore.YELLOW+' ---------------------KPI TABLES----------------------',Fore.RESET)
                print(mytable,Fore.RESET)
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while creating kpi table, please view executive_dashboard.log for more information"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                print()
                mytable3=PrettyTable([Fore.MAGENTA+'Identified'.upper(),Fore.MAGENTA+'Overall'.upper(),Fore.MAGENTA+'External'.upper(),Fore.MAGENTA+'Internal'.upper(),Fore.MAGENTA+'Total'.upper(),Fore.MAGENTA+'Overdue'.upper(),Fore.MAGENTA+'Not under sla'.upper()])
                mytable3.add_row([Fore.MAGENTA+'Cve',Fore.MAGENTA+'Assets',Fore.MAGENTA+'Assets',Fore.MAGENTA+'Assets',Fore.MAGENTA+'Findings',Fore.MAGENTA+'Findings',Fore.MAGENTA+'Findings'])
                mytable3.add_row([Fore.MAGENTA+str(self.dashboarddata['cisaknownexploited']['Identified']),Fore.MAGENTA+str(self.dashboarddata['cisaknownexploited']['Overall']),Fore.MAGENTA+str(self.dashboarddata['cisaknownexploited']['External']),Fore.MAGENTA+str(self.dashboarddata['cisaknownexploited']['Internal']),Fore.MAGENTA+str(self.dashboarddata['cisaknownexploited']['Total']),Fore.MAGENTA+str(self.dashboarddata['cisaknownexploited']['Overdue']),Fore.MAGENTA+str(self.dashboarddata['cisaknownexploited']['Not under sla'])])
                print()
                print(Fore.YELLOW+' ---------------------CISA KNOWN EXPLOITED----------------------',Fore.RESET)
                print(mytable3,Fore.RESET)
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while creating cisa known exploited table, please view executive_dashboard.log for more information"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                mytable4=PrettyTable()
                mytable5=PrettyTable()
                mytable9=PrettyTable()
                mytable4.add_column(Fore.MAGENTA+'VRR'.upper(),['Critical','High','Medium','Low','Info'])
                mytable4.add_column(Fore.MAGENTA+'Total open findings'.upper(),self.dashboarddata['findingsfunnel']['Total']['Openfindings'])
                mytable4.add_column(Fore.MAGENTA+'Total Assets'.upper(),self.dashboarddata['findingsfunnel']['Total']['Assets'])
                mytable4.add_column(Fore.MAGENTA+'Weaponized open findings'.upper(),self.dashboarddata['findingsfunnel']['Weaponized']['Openfindings'])
                mytable4.add_column(Fore.MAGENTA+'Weaponized Assets'.upper(),self.dashboarddata['findingsfunnel']['Weaponized']['Assets'])
                mytable4.add_row([Fore.MAGENTA+'OverallTotal',Fore.MAGENTA+str(Totaloftotalopenfindings),Fore.MAGENTA+str(TotaloftotalAssets),Fore.MAGENTA+str(Totalofweaponizedopenfindings),Fore.MAGENTA+str(Totalofweaponizedassets)])
                mytable5.add_column(Fore.MAGENTA+'VRR',['Critical','High','Medium','Low','Info'])
                mytable5.add_column(Fore.MAGENTA+'RCE PE open findings'.upper(),self.dashboarddata['findingsfunnel']['RCE PE']['Openfindings'])
                mytable5.add_column(Fore.MAGENTA+'RCE PE Assets'.upper(),self.dashboarddata['findingsfunnel']['RCE PE']['Assets'])
                mytable5.add_row([Fore.MAGENTA+'OverallTotal',Fore.MAGENTA+str(Totalofrcepeopenfindings),Fore.MAGENTA+str(Totalofrcepeassets)])
                mytable9.add_column(Fore.MAGENTA+'VRR',['Critical','High','Medium','Low','Info'])
                mytable9.add_column(Fore.MAGENTA+'Manual Exploit open findings'.upper(),self.dashboarddata['findingsfunnel']['ManualExploit']['Openfindings'])
                mytable9.add_column(Fore.MAGENTA+'Manual Exploit Assets'.upper(),self.dashboarddata['findingsfunnel']['ManualExploit']['Assets'])
                mytable9.add_column(Fore.MAGENTA+'Trending open findings'.upper(),self.dashboarddata['findingsfunnel']['Trending']['Openfindings'])
                mytable9.add_column(Fore.MAGENTA+'Trending Assets'.upper(),self.dashboarddata['findingsfunnel']['Trending']['Assets'])
                mytable9.add_row([Fore.MAGENTA+'OverallTotal',Fore.MAGENTA+str(Totalofmanualexploitopenfindings),Fore.MAGENTA+str(Totalofmanualexploitassets),Fore.MAGENTA+str(Totaloftrendingopenfindings),Fore.MAGENTA+str(Totaloftrendingassets)])
                print()
                print(Fore.YELLOW+' ---------------------FINDINGS PRIORITIZATION FUNNEL----------------------',Fore.RESET)
                print(mytable4,Fore.RESET)
                print()
                print(mytable5,Fore.RESET)
                print()
                print(mytable9,Fore.RESET)
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while creating cisa known exploited table, please view executive_dashboard.log for more information"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                mytable7=PrettyTable()
                mytable7.add_column(Fore.MAGENTA+'Total'.upper(),['Open findings','Unique Findings','Unique CVEs','Threats','Assets','Fixes'])
                mytable7.add_column(Fore.MAGENTA+'No'.upper(),[self.dashboarddata['weaponizationfunnel']['Open']['openFindings'],self.dashboarddata['weaponizationfunnel']['Open']['uniqueFindings'],self.dashboarddata['weaponizationfunnel']['Open']['uniqueCVEs'],self.dashboarddata['weaponizationfunnel']['Open']['threats'],self.dashboarddata['weaponizationfunnel']['Openassets'],self.dashboarddata['weaponizationfunnel']['Openfixes']])
                mytable7.add_column(Fore.MAGENTA+'Weaponized'.upper(),['Open Findings','Unique Findings','Unique CVEs','Threats','Assets','Fixes'])
                mytable7.add_column(Fore.MAGENTA+'No'.upper(),[self.dashboarddata['weaponizationfunnel']['Weaponized']['openFindings'],self.dashboarddata['weaponizationfunnel']['Weaponized']['uniqueFindings'],self.dashboarddata['weaponizationfunnel']['Weaponized']['uniqueCVEs'],self.dashboarddata['weaponizationfunnel']['Weaponized']['threats'],self.dashboarddata['weaponizationfunnel']['weaponizedassets'],self.dashboarddata['weaponizationfunnel']['weaponizedfixes']])
                mytable7.add_column(Fore.MAGENTA+'Trending'.upper(),['Open Findings','Unique Findings','Unique CVEs','Threats','Assets','Fixes'])
                mytable7.add_column(Fore.MAGENTA+'No'.upper(),[self.dashboarddata['weaponizationfunnel']['Trending']['openFindings'],self.dashboarddata['weaponizationfunnel']['Trending']['uniqueFindings'],self.dashboarddata['weaponizationfunnel']['Trending']['uniqueCVEs'],self.dashboarddata['weaponizationfunnel']['Trending']['threats'],self.dashboarddata['weaponizationfunnel']['Trendingassets'],self.dashboarddata['weaponizationfunnel']['Trendingfixes']])
                print()
                print(Fore.YELLOW,' ---------------------WEAPONIZATION FUNNEL-------------------------------',Fore.RESET)
                print()
                print(mytable7,Fore.RESET)
                mytable8=PrettyTable()
                mytable8.add_column(Fore.MAGENTA+'RCE/PE',['Open Findings','Unique Findings','Unique CVEs','Threats','Assets','Fixes'])
                mytable8.add_column(Fore.MAGENTA+'No'.upper(),[self.dashboarddata['weaponizationfunnel']['RCE PE']['openFindings'],self.dashboarddata['weaponizationfunnel']['RCE PE']['uniqueFindings'],self.dashboarddata['weaponizationfunnel']['RCE PE']['uniqueCVEs'],self.dashboarddata['weaponizationfunnel']['RCE PE']['threats'],self.dashboarddata['weaponizationfunnel']
                ['rcepeassets'],self.dashboarddata['weaponizationfunnel']['rcepefixes']])
                mytable8.add_column(Fore.MAGENTA+'ManualExploit'.upper(),['Open Findings','Unique Findings','Unique CVEs','Threats','Assets','Fixes'])
                mytable8.add_column(Fore.MAGENTA+'No'.upper(),[self.dashboarddata['weaponizationfunnel']['ManualExploit']['openFindings'],self.dashboarddata['weaponizationfunnel']['ManualExploit']['uniqueFindings'],self.dashboarddata['weaponizationfunnel']['ManualExploit']['uniqueCVEs'],self.dashboarddata['weaponizationfunnel']['ManualExploit']['threats'],self.dashboarddata['weaponizationfunnel']['Manualexploitassets'],self.dashboarddata['weaponizationfunnel']['Manualexploitfixes']])
                print('\n',mytable8,Fore.RESET)
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while creating Weaponization funnel table, please view executivedashboard.log file inside logs folder for more details"
                logging.error(message)
                logging.error(ex)
                print()
                print(message)
            try:
                mytable6=PrettyTable()
                mytable6.add_column(Fore.MAGENTA+'RS3'.upper(),['300-399','400-549','550-699','700-799','800-850'])
                mytable6.add_column(Fore.MAGENTA+'5',exploitassetsdict['5'])
                mytable6.add_column(Fore.MAGENTA+'4',exploitassetsdict['4'])
                mytable6.add_column(Fore.MAGENTA+'3',exploitassetsdict['3'])
                mytable6.add_column(Fore.MAGENTA+'2',exploitassetsdict['2'])
                mytable6.add_column( Fore.MAGENTA+'1',exploitassetsdict['1'])
                print()
                print(Fore.YELLOW+'---------Exploit Assets By Criticality---------'.upper(),Fore.RESET)
                print('\n',mytable6,Fore.RESET)
            except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,
                rs_api.InsufficientPrivileges, Exception) as ex:
                message = f"An exception has occurred while creating Exploit assets by cirticality table, please view executive_dashboard.log inside logs folder for more information"
                logging.error(message)
                logging.error(ex)
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

    log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs', f"Executive_dashboard.log")
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(levelname)s:  %(asctime)s > %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    print('For more details on the script process please view executivedashboard.log found in the logs folder')
    #  Set config file path, and read the configuration.
    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
    config_contents = read_config_file(conf_file)

    try:
        executive(config_contents)

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