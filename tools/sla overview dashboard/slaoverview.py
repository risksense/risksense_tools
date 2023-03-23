""" *******************************************************************************************************************
|
|  Name        :  slaoverview.py
|  Project     :  SLA Overview Dashbaord
|  Description :  A tool that displays sla overview dashboard data in the terminal
|  Copyright   :  2021 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

from ast import Str
from decimal import DivisionByZero
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
from colorama import Fore
import json
import pandas as pd
from termcolor import colored

class slaoverview:

    """ slaoverview class """

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
        except (rs_api.UserUnauthorized, rs_api.InsufficientPrivileges,rs_api.MaxRetryError, rs_api.StatusCodeError,Exception) as ex:
            message = "An error has occurred while trying to verify RiskSense credentials and connection"
            logging.error(message)
            logging.error(ex)
            print()
            print(f"{message}. Exiting.")
            exit(1)
        print()
        self.filter=input('Would you like to enter a "FILTER"? Y  or N: ').strip()
        if self.filter.lower()=='y':
            print()
            filtercategory={1:'group_names',2:"network.name",3:"tags"}
            print('Index No: 1 - Value: Group name\nIndex No: 2 - Value: Network name\nIndex No: 3 - Value: Tags')
            try:
                print()
                filtercategoryinput=filtercategory[int(input('Please insert the index number from option above for your "FILTER": ').strip())]
            except Exception as e:
                print('Please enter the right index as above either 1,2,3')
                print('Exiting')
                exit()
            isisnot={1:False,2:True}
            try:
                print()
                isisnotinput=isisnot[int(input('Please enter 1 for "IS" , 2 for "IS NOT": ').strip())]
            except Exception as e:
                print('Please enter the right index as above either 1,2')
                print('Exiting')
                exit()
            operator={1:"IN",2:"EXACT",3:"LIKE",4:"WILDCARD"}
            print()
            for key,value in operator.items():
                print(f'Index No: {key} - Value : {value}')
            try:
                print()
                operatorinput=operator[int(input('Please enter the index number of the "OPERATOR" from above: ').strip())]
            except Exception as e:
                print('Please enter the right index as above either 1,2,3,4')
                print('Exiting')
                exit()
            values=[]

            if filtercategoryinput=='group_names':
                aggregate=self.rs.aggregate.get_groupsbyfilter()
                if len(aggregate)==0:
                    print()
                    print('No groups available for the particular client\n')
                    print('Exiting')
                    exit()      
                elif len(aggregate)<10:
                    print()
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
                    print()
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
                                print()
                                nameinput=input('Please provide a "SEARCH STRING" to search for "GROUP NAME": ')
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
                                    valueinput=input('Please enter the indexes of the "GROUPS" seperated by "COMMA",Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,If you do not have the group name in the index number above please enter "no": ').strip().split(',')
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
                                print()
                                yorno=input('Would you like to "FILTER" to more "GROUPS"? "Y" or "N": ').strip()
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
                    print()
                    print('Here are the tag names pulled from your client\n')
                    tags={}
                    print()
                    for i in range(len(aggregate)):
                        tags[i]=aggregate[i]['key']
                        print(f'Index No : {i} - Value : "{aggregate[i]["key"]}"')
                    try:
                        print()
                        valueinput=input('Please enter index numbers of the "TAGS" seperated by "COMMA",Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number: ').strip().split(',')
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
                    print()  
                    print('Here are the suggested tag names pulled from your client\n')
                    tags={}
                    print()
                    for i in range(len(aggregate)):
                        tags[i]=aggregate[i]['key']
                        print(f'Index No : {i} - Value : "{aggregate[i]["key"]}"')
                    try:
                        print()
                        valueinput=input('Please enter index numbers of the "TAGS" seperated by "COMMA",Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,if tag name is not found in the above list of tags,please proceed to type "no": ').strip().split(',')
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
                                print()
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
                                print()
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
                    print()
                    print('Here are the network names pulled from your client\n')
                    groups={}
                    print()
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
                        print()
                        print('Here are the suggested network names pulled from your client\n')
                        networks={}
                        print()
                        for i in range(len(aggregate)):
                            networks[i]=aggregate[i]['key']
                            print(f'Index No:  {i} - Value {aggregate[i]["key"]}')
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
                                    print()
                                    nameinput=input('Please provide a "SEARCH STRING" to search for "NETWORK NAME": ')
                                    filters={"field":"name","exclusive":False,"operator":"WILDCARD","value":nameinput,"implicitFilters":[]}
                                    aggregate=self.rs.networks.suggest([],filters)
                                    networks={}
                                    if aggregate==[]:
                                        print(f'No data found for for {nameinput}')
                                        continue
                                    print()
                                    for i in range(len(aggregate)):
                                        networks[i]=aggregate[i]['key']
                                        print(f'Index No: {i} - Value : {aggregate[i]["key"]}')
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
                                    print()
                                    yorno=input('Would you like to "FILTER" to more "NETWORKS"? Y or N: ').strip()
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
            self.dashboarddata['slakpi']={}
            data=self.rs.aggregate.get_dynamic_aggregationformeantimesla(datafilter)
            self.dashboarddata['slakpi']['meantimetoremediate']=str(round(int(float(data[0][1]))+int((float(data[2][1])))))
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching dynamic aggregation for mean time sla.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            data=self.rs.aggregate.get_dynamic_aggregationforpatchablefindings(datafilter)
            hostfinding=0
            appfinding=0
            if data[0][1]!=[]:
                hostfinding=int(data[0][1])
            elif data[1][1]!=[]:
                appfinding=int(data[1][1])
            self.dashboarddata['slakpi']['patchablefindings']=str(hostfinding+appfinding)
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching dynamic aggregation for patchable findings.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            data=self.rs.aggregate.get_assetswithremediationsla(datafilter)
            hostfindingcountwithsla=0
            appfindingcountwithsla=0
            hostfindingcount=0
            appfindingcount=0
            hostcount=0
            appcount=0
            if data[0][1]!=[]:
                hostfindingcountwithsla=int(data[0][1])
            if data[1][1]!=[]:
                appfindingcountwithsla=int(data[1][1])
            if data[2][1]!=[]:
                hostfindingcount=int(data[2][1])
            if data[3][1]!=[]:
                appfindingcount=int(data[3][1])
            if data[4][1]!=[]:
                hostcount=int(data[4][1])
            if data[5][1]!=[]:
                appcount=int(data[5][1])
            self.dashboarddata['slakpi']['assetswithremediationsla']=f'{hostfindingcountwithsla+appfindingcountwithsla+hostfindingcount+appfindingcount}/{hostcount+appcount}'
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching assets with remediation sla.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            data=self.rs.aggregate.get_weaponizedfindingsnotundersla(datafilter)
            hostfindingcount=0
            appfindingcount=0
            if data[0][1]!=[]:
                hostfindingcount=int(data[0][1])
            if data[1][1]!=[]:
                appfindingcount=int(data[1][1])
            self.dashboarddata['slakpi']['Findingsnotundersla']=str(hostfindingcount+appfindingcount)
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching weaponized findings not under sla.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            timeline={'1':'7','2':'14','3':'30','4':'45','5':'60','6':'90','7':'120','8':'180'}
            print()
            for key,value in timeline.items():
                print(f'Index No: {key} - Value: {value} days')
            print()
            try:
                delta=timeline[input('Please choose an index number for "TIMELINE" from above for "REMEDIATION SLA OVERVIEW TIMELINE": ').strip()]
            except KeyError as e:
                print('-------------------------------------')
                print('Please enter the right index numbers from the option above')
                print('Exiting')
                exit()
            except Exception as e:
                    print('-------------------------------------')
                    print('There seems to be an exception')
                    print(e)
                    print('Exiting')
                    exit()
            data=self.rs.aggregate.get_remediationslaoverviewaggregate(delta,datafilter)
            
            self.dashboarddata['remediationslaoverview']={}
            self.dashboarddata['remediationslaoverview']['metSLA']=['0','0','0','0','0']
            self.dashboarddata['remediationslaoverview']['missedSLA']=['0','0','0','0','0']
            self.dashboarddata['remediationslaoverview'][f'Overdue<={delta}days']=['0','0','0','0','0']
            self.dashboarddata['remediationslaoverview'][f'Overdue>={delta}days']=['0','0','0','0','0']
            self.dashboarddata['remediationslaoverview'][f'sla<{delta}days']=['0','0','0','0','0']
            self.dashboarddata['remediationslaoverview'][f'sla>{delta}days']=['0','0','0','0','0']
            criticality={'Medium':2,'Info':4,'High':1,'Low':3,'Critical':0}
            if data[0]!={} and data[1]!={}:
                for key in data[0].keys():
                    if key in data[1].keys():
                        self.dashboarddata['remediationslaoverview']['metSLA'][criticality[key]]=str(int(data[0][key]['metSLA'])+int(data[1][key]['metSLA']))
                        self.dashboarddata['remediationslaoverview']['missedSLA'][criticality[key]]=str(int(data[0][key]['missedSLA'])+int(data[1][key]['missedSLA']))
                        self.dashboarddata['remediationslaoverview'][f'Overdue<={delta}days'][criticality[key]]=str(int(data[0][key]['overdueInDays'])+int(data[1][key]['overdueInDays']))
                        self.dashboarddata['remediationslaoverview'][f'Overdue>={delta}days'][criticality[key]]=str(int(data[0][key]['overdueOutDays'])+int(data[1][key]['overdueOutDays']))
                        self.dashboarddata['remediationslaoverview'][f'sla<{delta}days'][criticality[key]]=str(int(data[0][key]['withinSLAInDays'])+int(data[1][key]['withinSLAInDays']))
                        self.dashboarddata['remediationslaoverview'][f'sla>{delta}days'][criticality[key]]=str(int(data[0][key]['withinSLAOutDays'])+int(data[1][key]['withinSLAOutDays']))
                    else:
                        self.dashboarddata['remediationslaoverview']['metSLA'][criticality[key]]=str(data[0][key]['metSLA'])
                        self.dashboarddata['remediationslaoverview']['missedSLA'][criticality[key]]=str(data[0][key]['missedSLA'])
                        self.dashboarddata['remediationslaoverview'][f'Overdue<={delta}days'][criticality[key]]=str(data[0][key]['overdueInDays'])
                        self.dashboarddata['remediationslaoverview'][f'Overdue>={delta}days'][criticality[key]]=str(data[0][key]['overdueOutDays'])
                        self.dashboarddata['remediationslaoverview'][f'sla<{delta}days'][criticality[key]]=str(data[0][key]['withinSLAInDays'])
                        self.dashboarddata['remediationslaoverview'][f'sla>{delta}days'][criticality[key]]=str(data[0][key]['withinSLAOutDays'])
            elif data[1]!={}:
                for key in data[1].keys():
                    self.dashboarddata['remediationslaoverview']['metSLA'][criticality[key]]=str(data[1][key]['metSLA'])
                    self.dashboarddata['remediationslaoverview']['missedSLA'][criticality[key]]=str(data[1][key]['missedSLA'])
                    self.dashboarddata['remediationslaoverview'][f'Overdue<={delta}days'][criticality[key]]=str(data[1][key]['overdueInDays'])
                    self.dashboarddata['remediationslaoverview'][f'Overdue>={delta}days'][criticality[key]]=str(data[1][key]['overdueOutDays'])
                    self.dashboarddata['remediationslaoverview'][f'sla<{delta}days'][criticality[key]]=str(data[1][key]['withinSLAInDays'])
                    self.dashboarddata['remediationslaoverview'][f'sla>{delta}days'][criticality[key]]=str(data[1][key]['withinSLAOutDays'])
            elif data[0]!={}:
                for key in data[0].keys():
                    self.dashboarddata['remediationslaoverview']['metSLA'][criticality[key]]=str(data[0][key]['metSLA'])
                    self.dashboarddata['remediationslaoverview']['missedSLA'][criticality[key]]=str(data[0][key]['missedSLA'])
                    self.dashboarddata['remediationslaoverview'][f'Overdue<={delta}days'][criticality[key]]=str(data[0][key]['overdueInDays'])
                    self.dashboarddata['remediationslaoverview'][f'Overdue>={delta}days'][criticality[key]]=str(data[0][key]['overdueOutDays'])
                    self.dashboarddata['remediationslaoverview'][f'sla<{delta}days'][criticality[key]]=str(data[0][key]['withinSLAInDays'])
                    self.dashboarddata['remediationslaoverview'][f'sla>{delta}days'][criticality[key]]=str(data[0][key]['withinSLAOutDays'])
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching remediation sla overview data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            timeline={'1':'7','2':'14','3':'30','4':'45','5':'60','6':'90','7':'120','8':'180'}
            print()
            for key,value in timeline.items():
                print(f'Index No: {key} - Value: {value} days')
            print()
            try:
                delta=timeline[input('Please choose an index number for "TIMELINE" from above for "ORGANISATION SLA OVERVIEW TIMELINE": ').strip()]
            except KeyError as e:
                print('-------------------------------------')
                print('Please enter the right index numbers from the option above')
                print('Exiting')
                exit()
            except Exception as e:
                    print('-------------------------------------')
                    print('There seems to be an exception')
                    print(e)
                    print('Exiting')
                    exit()
            data=self.rs.aggregate.get_organizationalslaoverview(delta,datafilter)
            self.dashboarddata['organizationalslaoverview']={}
            Total=0
            Findingsundersla=0
            Findingsnotundersla=0
            closedfindingsundersla=0
            Overduefindings=0
            Withinsla=0
            if data[0]!={}:
                if 'Open' in data[0].keys():
                    Withinsla=Withinsla+int(data[0]['Open']['Within SLA'])
                    Total=Total+(int(data[0]['Open']['Total Findings']))
                    Findingsundersla=Findingsundersla+(int(data[0]['Open']["Findings Under SLA"]))
                    Findingsnotundersla=Findingsnotundersla+(int(data[0]['Open']["Findings Not Under SLA"]))
                    Overduefindings=Overduefindings+(int(data[0]['Open']["Overdue"]))
                if 'Closed' in data[0].keys():
                    Total=Total+(int(data[0]['Closed']['Total Findings']))
                    Findingsundersla=Findingsundersla+(int(data[0]['Closed']["Findings Under SLA"]))
                    Findingsnotundersla=Findingsnotundersla+(int(data[0]['Closed']["Findings Not Under SLA"]))
                    closedfindingsundersla=closedfindingsundersla+int(data[0]['Closed']["Findings Under SLA"])
            if data[4]!={}:
                if 'Open' in data[4].keys():
                    Withinsla=Withinsla+int(data[4]['Open']['Within SLA'])
                    Total=Total+(int(data[4]['Open']['Total Findings']))
                Findingsundersla=Findingsundersla+(int(data[4]['Open']["Findings Under SLA"]))
                Findingsnotundersla=Findingsnotundersla+(int(data[4]['Open']["Findings Not Under SLA"]))
                Overduefindings=Overduefindings+(int(data[4]['Open']["Overdue"]))
                if 'Closed' in data[4].keys():
                    Total=Total+(int(data[4]['Closed']['Total Findings']))
                    Findingsundersla=Findingsundersla+(int(data[4]['Closed']["Findings Under SLA"]))
                    Findingsnotundersla=Findingsnotundersla+(int(data[4]['Closed']["Findings Not Under SLA"]))
                    closedfindingsundersla=closedfindingsundersla+int(data[4]['Closed']["Findings Under SLA"])
            self.dashboarddata['organizationalslaoverview']['Total findings']=Total
            self.dashboarddata['organizationalslaoverview']['Findings under sla']=Findingsundersla
            self.dashboarddata['organizationalslaoverview']['Findings Not Under SLA']=Findingsnotundersla
            self.dashboarddata['organizationalslaoverview']['Closed findings under sla']=closedfindingsundersla
            self.dashboarddata['organizationalslaoverview']['Overdue']=Overduefindings
            self.dashboarddata['organizationalslaoverview']['Within Sla']=Withinsla
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching organizational sla overview data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            data=self.rs.aggregate.get_findingswithinsla(datafilter)
            self.dashboarddata['Findingswithinsla']={}
            self.dashboarddata['Findingswithinsla']['Open findings']=[0,0,0,0,0,0]
            self.dashboarddata['Findingswithinsla']['Weaponized findings']=[0,0,0,0,0,0]                
            Timeframe={"Today":0,"This Week":1,"This Month":2,"This Quarter":3,"Beyond This Quarter":4,"Total":5}
            for criticality in ['Critical','High','Medium','Low','Info']:
                self.dashboarddata['Findingswithinsla'][criticality]=[0,0,0,0,0,0]
            if data[0]!={}:
                for key in data[0]['Open'].keys():
                    self.dashboarddata['Findingswithinsla']['Open findings'][Timeframe[key]]=self.dashboarddata['Findingswithinsla']['Open findings'][Timeframe[key]]+int(data[0]['Open'][key])
            if data[1]!={}:
                for key in data[1]['Open'].keys():
                    self.dashboarddata['Findingswithinsla']['Weaponized findings'][Timeframe[key]]=self.dashboarddata['Findingswithinsla']['Weaponized findings'][Timeframe[key]]+int(data[1]['Open'][key])
            if data[2]!={}:
                for key in data[2].keys():
                    for keys in data[2][key]:
                        self.dashboarddata['Findingswithinsla'][key][Timeframe[keys]]=self.dashboarddata['Findingswithinsla'][key][Timeframe[keys]]+int(data[2][key][keys])
            if data[3]!={}:
                for key in data[3]['Open'].keys():
                    self.dashboarddata['Findingswithinsla']['Open findings'][Timeframe[key]]=self.dashboarddata['Findingswithinsla']['Open findings'][Timeframe[key]]+int(data[3]['Open'][key])
            if data[4]!={}:
                for key in data[4]['Open'].keys():
                    self.dashboarddata['Findingswithinsla']['Weaponized findings'][Timeframe[key]]=self.dashboarddata['Findingswithinsla']['Weaponized findings'][Timeframe[key]]+int(data[4]['Open'][key])
            if data[5]!={}:
                for key in data[5].keys():
                    for keys in data[5][key]:
                        self.dashboarddata['Findingswithinsla'][key][Timeframe[keys]]=self.dashboarddata['Findingswithinsla'][key][Timeframe[keys]]+int(data[5][key][keys])
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occured while fetching findings within sla data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            data=self.rs.aggregate.get_overduefindingspart1(datafilter)
            self.dashboarddata['Overduefindings']={}
            self.dashboarddata['Overduefindings']['Open findings']=[0,0,0,0,0,0]
            self.dashboarddata['Overduefindings']['Weaponized findings']=[0,0,0,0,0,0]
            Timeframe={"1Row":0,"7Row":1,"14Row":2,"30Row":3,'30LastRow':4,"Total":5}
            for criticality in ['Critical','High','Medium','Info','Low']:
                self.dashboarddata['Overduefindings'][criticality]=[0,0,0,0,0,0]
            if data[0]!={}:
                for key in data[0]['Open'].keys():
                        self.dashboarddata['Overduefindings']['Open findings'][Timeframe[key]]=self.dashboarddata['Overduefindings']['Open findings'][Timeframe[key]]+int(data[0]['Open'][key])
            if data[1]!={}:
                for key in data[1]['Open'].keys():
                        self.dashboarddata['Overduefindings']['Weaponized findings'][Timeframe[key]]=self.dashboarddata['Overduefindings']['Weaponized findings'][Timeframe[key]]+int(data[1]['Open'][key])
            if data[2]!={}:
                for key in data[2].keys():
                    for keys in data[2][key]:
                            self.dashboarddata['Overduefindings'][key][Timeframe[keys]]=self.dashboarddata['Overduefindings'][key][Timeframe[keys]]+int(data[2][key][keys])
            if data[3]!={}:
                for key in data[3]['Open'].keys():
                        self.dashboarddata['Overduefindings']['Open findings'][Timeframe[key]]=self.dashboarddata['Overduefindings']['Open findings'][Timeframe[key]]+int(data[3]['Open'][key])
            if data[4]!={}:
                for key in data[4]['Open'].keys():
                        self.dashboarddata['Overduefindings']['Weaponized findings'][Timeframe[key]]=self.dashboarddata['Overduefindings']['Weaponized findings'][Timeframe[key]]+int(data[4]['Open'][key])
            if data[5]!={}:
                for key in data[5].keys():
                    for keys in data[5][key]:
                            self.dashboarddata['Overduefindings'][key][Timeframe[keys]]=self.dashboarddata['Overduefindings'][key][Timeframe[keys]]+int(data[5][key][keys])
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An error has occured while fetching overdue findings data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            data=self.rs.aggregate.get_overduefindingspart2(datafilter)
            self.dashboarddata['Overduefindingsnew']={}
            self.dashboarddata['Overduefindingsnew']['Open findings']=[0,0,0,0,0,0]
            self.dashboarddata['Overduefindingsnew']['Weaponized findings']=[0,0,0,0,0,0]
            Timeframe={"45Row":0,"60Row":1,"90Row":2,"120Row":3,'120LastRow':4,"Total":5}
            for criticality in ['Critical','High','Medium','Low','Info']:
                    self.dashboarddata['Overduefindingsnew'][criticality]=[0,0,0,0,0,0]
            if data[0]!={}:
                for key in data[0]['Open'].keys():
                        self.dashboarddata['Overduefindingsnew']['Open findings'][Timeframe[key]]=self.dashboarddata['Overduefindingsnew']['Open findings'][Timeframe[key]]+int(data[0]['Open'][key])
            if data[1]!={}:
                for key in data[1]['Open'].keys():
                        self.dashboarddata['Overduefindingsnew']['Weaponized findings'][Timeframe[key]]=self.dashboarddata['Overduefindingsnew']['Weaponized findings'][Timeframe[key]]+int(data[1]['Open'][key])
            if data[2]!={}:
                for key in data[2].keys():
                    for keys in data[2][key]:
                            self.dashboarddata['Overduefindingsnew'][key][Timeframe[keys]]=self.dashboarddata['Overduefindingsnew'][key][Timeframe[keys]]+int(data[2][key][keys])
            if data[3]!={}:
                for key in data[3]['Open'].keys():      
                        self.dashboarddata['Overduefindingsnew']['Open findings'][Timeframe[key]]=self.dashboarddata['Overduefindingsnew']['Open findings'][Timeframe[key]]+int(data[3]['Open'][key])
            if data[4]!={}:
                for key in data[4]['Open'].keys():
                        self.dashboarddata['Overduefindingsnew']['Weaponized findings'][Timeframe[key]]=self.dashboarddata['Overduefindingsnew']['Weaponized findings'][Timeframe[key]]+int(data[4]['Open'][key])
            if data[5]!={}:
                for key in data[5].keys():
                    for keys in data[5][key]:
                            self.dashboarddata['Overduefindingsnew'][key][Timeframe[keys]]=self.dashboarddata['Overduefindingsnew'][key][Timeframe[keys]]+int(data[5][key][keys])
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching overdue findings new data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            try:
                    fromdate=str(datetime.strptime(input(f'Please enter the "START DATE" from which you want to view the "FINDINGS DUE CALENDER" in YYYY-MM-DD:Note:Start date must be before the last date of next month ').strip(),'%Y-%m-%d').date())
            except Exception as ex:
                print('Error in the start date input,Please provide the start date in YYYY-MM-DD format and ensure the right format as mentioned above')
                print('Exiting')
                exit()
            data=self.rs.aggregate.get_findingsduecalender(fromdate,datafilter)
            self.dashboarddata['getfindingsdue']={}
            if data[0]!={}:
                for key in data[0].keys():
                    self.dashboarddata['getfindingsdue'][key]= data[0][key]['count']
            if data[1]!={}:
                for key in data[1].keys():
                    if key in data[0].keys():
                        self.dashboarddata['getfindingsdue'][key]=str(int(self.dashboarddata['getfindingsdue'][key])+ int(data[1][key]['count']))
                    else:
                        self.dashboarddata['getfindingsdue'][key]=data[1][key]['count']
            elif data[0]=={} and data[1]=={}:
                self.dashboarddata['getfindingsdue']={'N/A':'N/A'}
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching findings due data.You must choose only a date lesser than last date of next month"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            timeline={'1':'30','2':'60','3':'90','4':'120'}
            print()
            for key,value in timeline.items():
                print(f'Index No :{key} - Value: {value} days')
            print()
            try:
                delta=timeline[input('Please choose an index number of the "TIMELINE" to apply from above for "CLOSED FINDINGS DATA TIMELINE":').strip()]
            except KeyError as e:
                print('-------------------------------------')
                print('Please enter the right index numbers from the option above')
                print('Exiting')
                exit()
            except Exception as e:
                    print('-------------------------------------')
                    print('There seems to be an exception')
                    print(e)
                    print('Exiting')
                    exit()
            data=self.rs.aggregate.get_closedfindingsslaoverview(delta,datafilter)
            self.dashboarddata['Closed findings']={}
            criticality={'Critical':0,'High':1,'Medium':2,'Low':3,'Info':4,'findingCount':5}
            self.dashboarddata['Closed findings']['Met SLA']=[0,0,0,0,0,0]
            self.dashboarddata['Closed findings']['Missed SLA']=[0,0,0,0,0,0]
            if data[0]!={}:
                if 'true' in data[0].keys():
                    self.dashboarddata['Closed findings']['Met SLA'][5]=str(int(self.dashboarddata['Closed findings']['Met SLA'][5])+int(data[0]['true']['findingCount']))
                    for key in data[0]['true']['vrrGroup']:
                        self.dashboarddata['Closed findings']['Met SLA'][criticality[key]]=str((self.dashboarddata['Closed findings']['Met SLA'][criticality[key]])+int(data[0]['true']['vrrGroup'][key]['findingCount']))
                if 'false' in data[0].keys():
                    self.dashboarddata['Closed findings']['Missed SLA'][5]=str(int(self.dashboarddata['Closed findings']['Missed SLA'][5])+int(data[0]['false']['findingCount']))
                    for key in data[0]['false']['vrrGroup']:
                        self.dashboarddata['Closed findings']['Missed SLA'][criticality[key]]=str((self.dashboarddata['Closed findings']['Missed SLA'][criticality[key]])+int(data[0]['false']['vrrGroup'][key]['findingCount']))
            if data[1]!={}:
                if 'true' in data[1].keys():
                    self.dashboarddata['Closed findings']['Met SLA'][5]=str(int(self.dashboarddata['Closed findings']['Met SLA'][5])+int(data[1]['true']['findingCount']))
                    for key in data[1]['true']['vrrGroup']:
                        self.dashboarddata['Closed findings']['Met SLA'][criticality[key]]=str(int(self.dashboarddata['Closed findings']['Met SLA'][criticality[key]])+int(data[1]['true']['vrrGroup'][key]['findingCount']))
                if 'false' in data[1].keys():
                    self.dashboarddata['Closed findings']['Missed SLA'][5]=str(int(self.dashboarddata['Closed findings']['Missed SLA'][5])+int(data[1]['false']['findingCount']))
                    for key in data[1]['false']['vrrGroup']:
                        self.dashboarddata['Closed findings']['Missed SLA'][criticality[key]]=str(int(self.dashboarddata['Closed findings']['Missed SLA'][criticality[key]])+int(data[1]['false']['vrrGroup'][key]['findingCount']))
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching closed findings data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            groupids, groupnamestoids, groupslasbyduedate = self.new_method(datafilter)
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching group slas by due date data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            data=self.rs.aggregate.get_aggregationforgroupslasbyduedates2(groupids,datafilter)
            for key in data[1].keys():
                for keykey in data[1][key].keys():
                    self.dashboarddata['Group SLAs By Due Dates1'][groupnamestoids[key]][groupslasbyduedate[keykey]]=data[1][key][keykey]
            for key in data[2].keys():
                for keykey in data[2][key].keys():
                    if keykey=="More than 60 Days" or keykey =="More than 90 Days" or keykey =="More than 120 Days":
                        self.dashboarddata['Group SLAs By Due Dates1'][groupnamestoids[key]][groupslasbyduedate[keykey]]=str(int(self.dashboarddata['Group SLAs By Due Dates1'][groupnamestoids[key]][groupslasbyduedate[keykey]])+int(data[2][key][keykey]))
            df = pd.DataFrame(self.dashboarddata['Group SLAs By Due Dates1'])
            df.index = ['Rs3', 'Open Findings', 'Open within SLA', 'Overdue More than 7 days','Overdue More than 15 days','Overdue More than 30 days','Overdue More than 45 days','Overdue More than 60 days','Overdue More than 90 days','Overdue More than 120 days']
            df.to_csv('groupslasbyduedate.csv')
            print()
            print('Group slas by due date data saved in csv as groupslasbyduedate.csv')
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching group slas 2 data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            print()
            choiceoption={'1':'Select Group Pattern','2':'Select my own groups'}
            print()
            for key,value in choiceoption.items():
                print(f'Index No: {key} - Value : {value}')
            try:
                print()
                choiceoption=choiceoption[input('Please choose an index number of type of "GROUP" which you want to choose to display "GROUP SLAS BY PRIORITIZATION": ').strip()]
            except Exception as e:
                print('Please enter either 1 or 2')
                print('Exiting')
                exit()
            if choiceoption.lower()=='select group pattern':
                data=self.rs.aggregate.get_newpattern()
                print()
                for i in range(len(data['content'])):
                    print(f'Index No : {i}  - Value : {data["content"][i]["value"]}')
                try:
                    print()
                    patterninput=data["content"][int(input('Please enter the index number of the "OPERATOR" from above: ').strip())]["id"]
                except Exception as e:
                    print('Please enter the right index as above')
                    print('Exiting')
                    exit()
                groupids=self.rs.aggregate.limitedgroupattern(patterninput)
                groupnames=self.rs.aggregate.get_datafromgroupids(groupids)
                groupnamestoids={}
                for i in range(len(groupnames['_embedded']['groups'])):
                    groupnamestoids[str(groupnames['_embedded']['groups'][i]['id'])]=groupnames['_embedded']['groups'][i]['name']
                groupids=[x for x in groupids if x in groupnamestoids.keys()]
            elif choiceoption.lower()=='select my own groups':
                print()
                print('You must choose maximum 10 groups')
                groups=self.rs.aggregate.get_groupsbyfilter()
                groupnames=self.rs.aggregate.get_groupnamefromgroupids([groups[x]['key'] for x in range(len(groups))])
                groupnamestoids={}
                groupids=[]
                if len(groups)==0:
                    print('No groups available for the particular client\n')
                    print('Exiting')
                    exit()      
                elif len(groups)<10:
                    groups=self.rs.aggregate.get_groupsbyfilter()
                    groupnames=self.rs.aggregate.get_groupnamefromgroupids([groups[x]['key'] for x in range(len(groups))])
                    groupnamestoids={}
                    print()
                    print('Here are the group names pulled from your client\n')
                    print()
                    for i in range(len(groupnames['_embedded']['groups'])):
                        print(f"Index No :{i} - Value: {groupnames['_embedded']['groups'][i]['name']}")
                        groupnamestoids[str(groupnames['_embedded']['groups'][i]['id'])]=groupnames['_embedded']['groups'][i]['name']
                    try:
                        print()
                        valueinput=input('Please enter the Index No: of the "GROUPS" seperated by "COMMAS": ').strip().split(',')
                        valueinput=list(set(valueinput))
                        if len(valueinput)>1:
                            for i in valueinput:
                                if i.isdigit()==False:
                                    print('Please do not enter any special characters or string')
                                    print('Exiting')
                                    exit()
                        groupids.extend([str(groupnames['_embedded']['groups'][int(i)]['id']) for i in valueinput ])
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
                    print()
                    print('Please choose groups for group slas by prioritization:\n')
                    print('Here are the suggested group names pulled from your client\n')
                    groups={}
                    for i in range(len(groupnames['_embedded']['groups'])):
                        print(f"Index No : {i} - Value: {groupnames['_embedded']['groups'][i]['name']}")
                        groupnamestoids[str(groupnames['_embedded']['groups'][i]['id'])]=groupnames['_embedded']['groups'][i]['name']
                    try:
                        print()
                        valueinput=input('Please enter the index numbers of the "GROUPS" seperated by COMMA,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,if group is not found in the above list of groups,please proceed to type "no": ').strip().split(',')
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
                                while(True):
                                    print()
                                    nameinput=input('Please provide a SEARCH STRING to search for "GROUP NAME": ')
                                    groups=self.rs.aggregate.get_groupsbyfilter(nameinput)
                                    groupnames=self.rs.aggregate.get_groupnamefromgroupids([groups[x]['key'] for x in range(len(groups))])
                                    if groups==[]:
                                        print(f'No data found for {nameinput}')
                                        continue
                                    print()
                                    print('Here are the available groups')
                                    for i in range(len(groupnames['_embedded']['groups'])):
                                        print(f"Index No:{i} Value: {groupnames['_embedded']['groups'][i]['name']}")
                                        groupnamestoids[str(groupnames['_embedded']['groups'][i]['id'])]=groupnames['_embedded']['groups'][i]['name']
                                    try:
                                        print()
                                        valueinput=input('Please enter the indexes of the "GROUPS" seperated by "COMMA",Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,If you do not have the group name in the index number above please enter "no": ').strip().split(',')
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
                                        groupids.extend([str(groupnames['_embedded']['groups'][int(i)]['id']) for i in valueinput ])
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
                                    print()
                                    yorno=input('Would you like to "FILTER" to more GROUPS? "Y" or "N": ').strip()
                                    if yorno.lower()=='n':
                                        break 
                        groupids.extend([str(groupnames['_embedded']['groups'][int(i)]['id']) for i in valueinput ])
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
            
            groupids=list(set(groupids))
            if len(groupids)>10:
                print('You must choose only 10 Group ids')
                print('Exiting')
                exit()
            groupidstonames={}
            self.dashboarddata['Group SLAs by prioritization']={}
            data=self.rs.aggregate.get_groupslasbyprioritizationaggregate(groupids)
            prioritization={'Rs3':0,'CriticalWithin SLA':1,'CriticalOverdue':2,'HighWithin SLA':3,'HighOverdue':4,'MediumWithin SLA':5,'MediumOverdue':6,'LowWithin SLA':7,'LowOverdue':8,'InfoWithin SLA':9,'InfoOverdue':10}
            for key in data[0].keys():
                self.dashboarddata['Group SLAs by prioritization'][groupnamestoids[key]]=[0,0,0,0,0,0,0,0,0,0,0]
                self.dashboarddata['Group SLAs by prioritization'][groupnamestoids[key]][prioritization['Rs3']]=int(float(data[0][key]['RS3']))
            if data[1]!={}:
                for key in  data[1].keys():
                    for keykey in data[1][key]['VRR Group']:
                        self.dashboarddata['Group SLAs by prioritization'][groupnamestoids[key]][prioritization[keykey+'Within SLA']]=data[1][key]['VRR Group'][keykey]['Within SLA']
                        self.dashboarddata['Group SLAs by prioritization'][groupnamestoids[key]][prioritization[keykey+'Overdue']]=data[1][key]['VRR Group'][keykey]['Overdue']
            if data[2]!={}:
                for key in  data[2].keys():
                    for keykey in data[2][key]['VRR Group']:
                        self.dashboarddata['Group SLAs by prioritization'][groupnamestoids[key]][prioritization[keykey+'Within SLA']]=str(int(self.dashboarddata['Group SLAs by prioritization'][groupnamestoids[key]][prioritization[keykey+'Within SLA']])+int(data[2][key]['VRR Group'][keykey]['Within SLA']))
                        self.dashboarddata['Group SLAs by prioritization'][groupnamestoids[key]][prioritization[keykey+'Overdue']]=str(int(self.dashboarddata['Group SLAs by prioritization'][groupnamestoids[key]][prioritization[keykey+'Overdue']])+int(data[2][key]['VRR Group'][keykey]['Overdue']))
            df = pd.DataFrame(self.dashboarddata['Group SLAs by prioritization'])
            df.index = ['Rs3','CriticalWithin SLA','CriticalOverdue','HighWithin SLA','HighOverdue','MediumWithin SLA','MediumOverdue','LowWithin SLA','LowOverdue','InfoWithin SLA','InfoOverdue']
            df.to_csv('groupslasbyprioritization.csv')
            print()
            print('Group slas prioritization data saved in csv as groupslasbyprioritization.csv')
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching group slas by prioritization data."
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            self.new_method2(groupidstonames)
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching dynamic aggregation for mean time sla.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            if datafilter==[]:
                filter=[{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]
            else:
                filter=[{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},datafilter]
            hostfindingduedatepresent=self.rs.host_findings.get_single_search_page(filter)['page']['totalElements']
            appfindingduedatepresent=self.rs.application_findings.get_single_search_page(filter)['page']['totalElements']
            overall=int(hostfindingduedatepresent)+int(appfindingduedatepresent)
            if int(self.dashboarddata['Overduefindings']['Open findings'][4])!=0:
                findingsoverduemorethan30days=overall/int(self.dashboarddata['Overduefindings']['Open findings'][4])
                self.dashboarddata['slakpi']['findingsoverdue30days']=f"{round(100/findingsoverduemorethan30days)}%"
            else:
                self.dashboarddata['slakpi']['findingsoverdue30days']=f"0%"
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching dynamic aggregation for mean time sla.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            if datafilter==[]:
                filter=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Closed"},{"field":"resolved_on","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":"30"},{"field":"has_met_sla","exclusive":False,"operator":"MET_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]
            else:
                filter=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Closed"},{"field":"resolved_on","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":"30"},{"field":"has_met_sla","exclusive":False,"operator":"MET_SLA","orWithPrevious":False,"implicitFilters":[],"value":""},datafilter]
            last30daysmetslahostfindings=self.rs.host_findings.get_single_search_page(filter)['page']['totalElements']
            last30daysmetslaappfindings=self.rs.application_findings.get_single_search_page(filter)['page']['totalElements']
            if datafilter==[]:
                filter=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Closed"},{"field":"resolved_on","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":"30"}]
            else:
                filter=[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Closed"},{"field":"resolved_on","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":"30"},datafilter]
            last30dayshostfindings=self.rs.host_findings.get_single_search_page(filter)['page']['totalElements']
            last30daysappfindings=self.rs.application_findings.get_single_search_page(filter)['page']['totalElements']

            last30daysmetsla=int(last30daysmetslahostfindings)+int(last30daysmetslaappfindings)
            last30daysfindings=int(last30dayshostfindings)+int(last30daysappfindings)
            self.dashboarddata['slakpi']['30dayssuccess']=f"{round((last30daysmetsla/last30daysfindings)*100)}%"
        except DivisionByZero as ex:
            message = f"An exception has occurred while fetching 30 days success performance.Its a zero"
            self.dashboarddata['slakpi']['30dayssuccess']="0%"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching 30 days success performance."
            if str(ex)=='division by zero':
                self.dashboarddata['slakpi']['30dayssuccess']="0%"
                message = f"The 30 days sucess performance returns an exception, seems to be a zero"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)
        try:
            mytable=PrettyTable()
            for key in self.dashboarddata['slakpi'].keys():
                mytable.add_column(Fore.MAGENTA+key.upper(),[self.dashboarddata['slakpi'][key]])
            print()
            print(Fore.YELLOW+'\t\tKPI TABLE',Fore.RESET)
            print(mytable,Fore.RESET)
        except Exception as e :
            message = f"An exception has occurred while creating kpi table.There must be no data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(e)
            print()
            print(message)
        try:
            mytable1=PrettyTable()
            mytable1.add_column(Fore.MAGENTA+'criticality'.upper(),['Critical','High','Medium','Low','Info'])
            for key in self.dashboarddata['remediationslaoverview'].keys():
                mytable1.add_column(Fore.MAGENTA+key.upper(),self.dashboarddata['remediationslaoverview'][key])
            print()
            print(Fore.YELLOW+'\t\tREMEDIATION SLA OVERVIEW',Fore.RESET)
            print(mytable1,Fore.RESET)
        except Exception as e :
            message = f"An exception has occurred while creating remediation sla overview table.There must be no data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(e)
            print()
            print(message)
        try:
            mytable2=PrettyTable()
            for key in self.dashboarddata['organizationalslaoverview']:
                mytable2.add_column(Fore.MAGENTA+key.upper(),[self.dashboarddata['organizationalslaoverview'][key]])
            print()
            print(Fore.YELLOW+'\t\tORGANIZATIONAL SLA OVERVIEW',Fore.RESET)
            print(mytable2,Fore.RESET)
        except Exception as e :
            message = f"An exception has occurred while creating organizational sla overview table.There must be no data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(e)
            print()
            print(message)
        try:
            mytable3=PrettyTable()
            mytable3.add_column(Fore.MAGENTA+'Time Frame'.upper(),['Today','This Week','This Month','This Quarter','Beyond This Quarter','Total'])
            for key in self.dashboarddata['Findingswithinsla'].keys():
                mytable3.add_column(Fore.MAGENTA+key.upper(),self.dashboarddata['Findingswithinsla'][key])
            print()
            print(Fore.YELLOW+'\t\tFindings within sla'.upper(),Fore.RESET)
            print(mytable3,Fore.RESET)
        except Exception as e :
            message = f"An exception has occurred while creating Findings within sla table.There must be no data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(e)
            print()
            print(message)
        try:
            mytable4=PrettyTable()
            mytable4.add_column(Fore.MAGENTA+'Time Frame'.upper(),["1Row","7Row","14Row","30Row",'30LastRow',"Total"])
            for key in self.dashboarddata['Overduefindings'].keys():
                mytable4.add_column(Fore.MAGENTA+key.upper(),self.dashboarddata['Overduefindings'][key])
            print()
            print(Fore.YELLOW+'\t\tOverdue findings till 30 days'.upper(),Fore.RESET)
            print(mytable4,Fore.RESET)
        except Exception as e :
            message = f"An exception has occurred while creating overdue findings table till 30 days.There must be no data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(e)
            print()
            print(message)
        try:
            mytable5=PrettyTable()
            mytable5.add_column(Fore.MAGENTA+'Time Frame'.upper(),["45Row","60Row","90Row","120Row",'120LastRow',"Total"])
            for key in self.dashboarddata['Overduefindingsnew'].keys():
                mytable5.add_column(Fore.MAGENTA+key.upper(),self.dashboarddata['Overduefindingsnew'][key])
            print()
            print(Fore.YELLOW+'\t\tOverdue findings till 120 days'.upper(),Fore.RESET)
            print(mytable5,Fore.RESET)
        except Exception as e :
            message = f"An exception has occurred while creating overdue findings table till 120 days.There must be no data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(e)
            print()
            print(message)
        try:
            mytable6=PrettyTable()
            mytable6.add_column(Fore.MAGENTA+'Date'.upper(),[key for key in self.dashboarddata['getfindingsdue'].keys()])
            mytable6.add_column(Fore.MAGENTA+'Count'.upper(),[value for value in self.dashboarddata['getfindingsdue'].values()])
            print()
            print(Fore.YELLOW+'Findings due calender'.upper(),Fore.RESET)
            print(mytable6,Fore.RESET)
        except Exception as e :
            message = f"An exception has occured while creating Findings due calender table.There must be no data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(e)
            print()
            print(message)
        try:
            mytable8=PrettyTable()
            mytable8.add_column(Fore.MAGENTA+'Criticality'.upper(),['Critical','High','Medium','Low','Info','Total'])
            mytable8.add_column(Fore.MAGENTA+'Met SLA'.upper(),self.dashboarddata['Closed findings']['Met SLA'])
            mytable8.add_column(Fore.MAGENTA+'Missed SLA'.upper(),self.dashboarddata['Closed findings']['Missed SLA'])
            print()
            print(Fore.YELLOW+'\t\tClosed Findings'.upper(),Fore.RESET)
            print(mytable8,Fore.RESET)
        except Exception as e :
            message = f"An exception has occured while creating closed findings table.There must be no data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(e)
            print()
            print(message)
        try:
            print()
            print(Fore.YELLOW+'Groupslas performance over time'.upper(),Fore.RESET)
            print()
            if self.dashboarddata['Groupslas performance over time']=={}:
                mytable9=PrettyTable()
                mytable9.add_column(Fore.MAGENTA+'Date'.upper(),['N/A'])
                mytable9.add_column(Fore.MAGENTA+'Count'.upper(),['N/A'])
                print(mytable9,Fore.RESET)

            else:
                for key in self.dashboarddata['Groupslas performance over time'].keys():
                    mytable9=PrettyTable()
                    mytable9.add_column(Fore.MAGENTA+'Date'.upper(),self.dashboarddata['Groupslas performance over time'][key]['date'])
                    mytable9.add_column(Fore.MAGENTA+'Count'.upper(),self.dashboarddata['Groupslas performance over time'][key]['count'])
                    print(Fore.YELLOW+key.upper())
                    print()
                    print(mytable9,Fore.RESET)
        except Exception as e :
            message = f"An exception has occurred while creating group sla performance over time table.There must be no data.For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(e)
            print()
            print(message)

    def last_day_of_month(self,any_day):
    # The day 28 exists in every month. 4 days later, it's always next month
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
        # subtracting the number of the current day brings us back one month
        return next_month - datetime.timedelta(days=next_month.day)

    def new_method2(self, groupidstonames):
        try:
            a=date.today().month
            dashboardkpi=self.rs.aggregate.get_dashboardkpi()
            try:
                    print()
                    thedate=str(datetime.strptime(input(f'Please enter the date from which you want to view the "GROUP SLA PERFORMANCE" in YYYY-MM-DD, Note: Date should not be before the {a}th month of last year: ').strip(),'%Y-%m-%d').date())
            except Exception as ex:
                print('Error in the start date input,Please provide the  start date in YYYY-MM-DD format')
                print('Exiting')
                exit()
            print()
            for key in range(len(dashboardkpi['content'])):
                print(f'Index No:{key} Value: {dashboardkpi["content"][key]["key"]}')
            try:
                print()
                kpiint=int(input('Please enter the index of the "KPI" you want to display for "GROUP SLA PERFORMANCE OVER TIME":'))
            except Exception as e:
                print('Please enter the right index as above')
                print('Exiting')
                exit()
            print()
            choiceoption={'1':'Select Group Pattern','2':'Select my own groups'}
            print()
            for key,value in choiceoption.items():
                print(f'Index No: {key} - Value : {value}')
            try:
                print()
                choiceoption=choiceoption[input('Please choose an index of "GROUP TYPE" to which you want to choose to display "GROUP SLA PERFORMANCE OVER TIME": ').strip()]
            except Exception as e:
                print('Please enter either 1 or 2')
                print('Exiting')
                exit()
            if choiceoption.lower()=='select group pattern':

                data=self.rs.aggregate.get_newpattern()
                print()
                for i in range(len(data['content'])):
                    print(f'Index No : {i}  - Value : {data["content"][i]["value"]}')
                try:
                    print()
                    patterninput=data["content"][int(input('Please enter the index number of the "OPERATOR" from above: ').strip())]["id"]
                except Exception as e:
                    print('Please enter the right index as above')
                    print('Exiting')
                    exit()
                groupids=self.rs.aggregate.limitedgroupattern(patterninput)
                groupnames=self.rs.aggregate.get_datafromgroupids(groupids)
                
                groupnamestoids={}
                for i in range(len(groupnames['_embedded']['groups'])):
                    groupnamestoids[str(groupnames['_embedded']['groups'][i]['id'])]=groupnames['_embedded']['groups'][i]['name']
                groupids=[x for x in groupids if x in groupnamestoids.keys()]
            elif choiceoption.lower()=='select my own groups':
                print()
                print('Maximum 10 groups can be selected')
                groups=self.rs.aggregate.get_groupsbyfilter()
                groupnames=self.rs.aggregate.get_groupnamefromgroupids([groups[x]['key'] for x in range(len(groups))])
                groupids=[]
                groupnamestoids={}
                if len(groups)==0:
                    print('No groups available for the particular client\n')
                    print('Exiting')
                    exit()      
                elif len(groups)<10:
                    groups=self.rs.aggregate.get_groupsbyfilter()
                    groupnames=self.rs.aggregate.get_groupnamefromgroupids([groups[x]['key'] for x in range(len(groups))])
                    groupnamestoids={}
                    print()
                    print('Here are the group names pulled from your client\n')
                    print()
                    for i in range(len(groupnames['_embedded']['groups'])):
                        print(f"Index No:{i} Value: {groupnames['_embedded']['groups'][i]['name']}")
                        groupnamestoids[str(groupnames['_embedded']['groups'][i]['id'])]=groupnames['_embedded']['groups'][i]['name']
                        groupnamestoids[str(groupnames['_embedded']['groups'][i]['name'])]=groupnames['_embedded']['groups'][i]['id']
                    try:
                        print()
                        valueinput=input('Please enter the Index No of the GROUPS seperated by COMMAS: ').strip().split(',')
                        valueinput=list(set(valueinput))
                        if len(valueinput)>1:
                            for i in valueinput:
                                if i.isdigit()==False:
                                    print('Please do not enter any special characters or string')
                                    print('Exiting')
                                    exit()
                        groupids.extend([str(groupnames['_embedded']['groups'][int(i)]['id']) for i in valueinput ])
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
                    print()
                    print('Please choose groups for group sla performance over time:\n')
                    print('Here are the suggested group names pulled from your client\n')
                    groups={}
                    for i in range(len(groupnames['_embedded']['groups'])):
                        print(f"Index No:{i} Value: {groupnames['_embedded']['groups'][i]['name']}")
                        groupnamestoids[str(groupnames['_embedded']['groups'][i]['id'])]=groupnames['_embedded']['groups'][i]['name']
                        groupnamestoids[str(groupnames['_embedded']['groups'][i]['name'])]=groupnames['_embedded']['groups'][i]['id']
                    try:
                        print()
                        valueinput=input('Please enter the index numbers of the "GROUPS" seperated by "COMMA",Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,if group is not found in the above list of groups,please proceed to type "no": ').strip().split(',')
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
                            while(True):
                                print()
                                nameinput=input('Please provide a "SEARCH STRING" to search for "GROUP NAME": ')
                                groups=self.rs.aggregate.get_groupsbyfilter(nameinput)
                                groupnames=self.rs.aggregate.get_groupnamefromgroupids([groups[x]['key'] for x in range(len(groups))])
                                if groups==[]:
                                    print(f'No data found for {nameinput}')
                                    continue
                                print()
                                print('Here are the available groups')
                                for i in range(len(groupnames['_embedded']['groups'])):
                                    print(f"Index No:{i} Value: {groupnames['_embedded']['groups'][i]['name']}")
                                    groupnamestoids[str(groupnames['_embedded']['groups'][i]['id'])]=groupnames['_embedded']['groups'][i]['name']
                                try:
                                    print()
                                    valueinput=input('Please enter the indexes of the "GROUPS" seperated by COMMA,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,If you do not have the group name in the index number above please enter "no": ').strip().split(',')
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
                                    groupids.extend([str(groupnames['_embedded']['groups'][int(i)]['id']) for i in valueinput ])
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
                                print()
                                yorno=input('Would you like to filter to more "GROUPS"? "Y" or "N": ').strip()
                                if yorno.lower()=='n':
                                    break 
                        groupids.extend([str(groupnames['_embedded']['groups'][int(i)]['id']) for i in valueinput ])
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
            groupids=list(set(groupids))
            if len(groupids)>10:
                print('Maxium 10 groups are allowed')
                print('Exiting')
                exit()
            data=self.rs.aggregate.get_groupslaperformanceovertime(kpiint,thedate,groupids)
            self.dashboarddata['Groupslas performance over time']={}
            for i in range(len(data)):
                if i ==len(data)-1:
                    pass
                else:
                    if data[i]!={}:
                        for key in data[i]:
                            self.dashboarddata['Groupslas performance over time'][groupnamestoids[key]]={}
                            for value in data[i][key].values():
                                self.dashboarddata['Groupslas performance over time'][groupnamestoids[key]]['date']=[thedates for thedates in value.keys()]
                                self.dashboarddata['Groupslas performance over time'][groupnamestoids[key]]['count']=[value[keyvalue]['Count'] for keyvalue in value.keys()]
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching group sla performance data.Please check if the date is before the month mentioned in the input and also not of the future. For more details please view the slaoverview.log in the logs folder"
            logging.error(message)
            logging.error(ex)
            print()
            print(message)

    def new_method(self, datafilter):
    #choose you own group 
        try:
            print()
            choiceoption={'1':'Select Group Pattern','2':'Select my own groups'}
            for key,value in choiceoption.items():
                print(f'Index No: {key} - Value : {value}')
            try:
                print()
                choiceoption=choiceoption[input('Please choose an index of type of "GROUP" which you want to choose to display "GROUP SLAS BY DUE DATE": ').strip()]
            except Exception as e:
                print('Please enter either 1 or 2')
                print('Exiting')
                exit()
            if choiceoption.lower()=='select group pattern':
                data=self.rs.aggregate.get_newpattern()
                for i in range(len(data['content'])):
                    print(f'Index No : {i}  - Value : {data["content"][i]["value"]}')
                try:
                    print()
                    patterninput=data["content"][int(input('Please enter the index number of the "OPERATOR" from above:').strip())]["id"]
                except Exception as e:
                    print('Please enter the right index as above')
                    print('Exiting')
                    exit()
                groupids=self.rs.aggregate.limitedgroupattern(patterninput)
                groupids=list(set(groupids))
                groupnames=self.rs.aggregate.get_datafromgroupids(groupids)
                groupnamestoids={}
                for i in range(len(groupnames['_embedded']['groups'])):
                    groupnamestoids[str(groupnames['_embedded']['groups'][i]['id'])]=groupnames['_embedded']['groups'][i]['name']
                groupids=[x for x in groupids if x in groupnamestoids.keys()]
            elif choiceoption.lower()=='select my own groups':
                print()
                print('Please provide maximum 10 groups')
                groups=self.rs.aggregate.get_groupsbyfilter()
                groupnames=self.rs.aggregate.get_groupnamefromgroupids([groups[x]['key'] for x in range(len(groups))])
                groupids=[]
                groupnamestoids={}
                if len(groups)==0:
                    print('No groups available for the particular client\n')
                    print('Exiting')
                    exit()      
                elif len(groups)<10:
                    groups=self.rs.aggregate.get_groupsbyfilter()
                    groupnames=self.rs.aggregate.get_groupnamefromgroupids([groups[x]['key'] for x in range(len(groups))])
                    groupnamestoids={}
                    print()
                    print('Here are the group names pulled from your client\n')
                    print()
                    for i in range(len(groupnames['_embedded']['groups'])):
                        print(f"Index No:{i} Value: {groupnames['_embedded']['groups'][i]['name']}")
                        groupnamestoids[str(groupnames['_embedded']['groups'][i]['id'])]=groupnames['_embedded']['groups'][i]['name']
                    try:
                        print()
                        valueinput=input('Please enter the Index No of the GROUPS seperated by COMMAS" ').strip().split(',')
                        valueinput=list(set(valueinput))
                        if len(valueinput)>1:
                            for i in valueinput:
                                if i.isdigit()==False:
                                    print('Please do not enter any special characters or string')
                                    print('Exiting')
                                    exit()
                        groupids.extend([str(groupnames['_embedded']['groups'][int(i)]['id']) for i in valueinput ])
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
                    print()
                    print('Please choose groups for group slas by due data:\n')
                    print()
                    print('Here are the suggested group names pulled from your client\n')
                    print()
                    groups={}
                    for i in range(len(groupnames['_embedded']['groups'])):
                        print(f"Index No:{i} Value: {groupnames['_embedded']['groups'][i]['name']}")
                        groupnamestoids[str(groupnames['_embedded']['groups'][i]['id'])]=groupnames['_embedded']['groups'][i]['name']
                    try:
                        print()
                        valueinput=input('Please enter the index numbers of the "GROUPS" seperated by COMMA,Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,if group is not found in the above list of groups,please proceed to type "no": ').strip().split(',')
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
                            while(True):
                                nameinput=input('Please provide a "SEARCH STRING" to search for "GROUP NAME": ')
                                groups=self.rs.aggregate.get_groupsbyfilter(nameinput)
                                groupnames=self.rs.aggregate.get_groupnamefromgroupids([groups[x]['key'] for x in range(len(groups))])
                                if groups==[]:
                                    print(f'No data found for {nameinput}')
                                    continue
                                print()
                                print('Here are the available groups')
                                print()
                                for i in range(len(groupnames['_embedded']['groups'])):
                                    print(f"Index No:{i} Value: {groupnames['_embedded']['groups'][i]['name']}")
                                    groupnamestoids[str(groupnames['_embedded']['groups'][i]['id'])]=groupnames['_embedded']['groups'][i]['name']
                                try:
                                    print()
                                    valueinput=input('Please enter the indexes of the "GROUPS" seperated by "COMMA",Note: If LIKE,WILDCARD,EXACT operator chosen,please choose only one index number,If you do not have the group name in the index number above please enter "no": ').strip().split(',')
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
                                    groupids.extend([str(groupnames['_embedded']['groups'][int(i)]['id']) for i in valueinput ])
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
                                yorno=input('Would you like to filter to more "GROUPS"? "Y" or "N": ').strip()
                                if yorno.lower()=='n':
                                    break 
                        groupids.extend([str(groupnames['_embedded']['groups'][int(i)]['id']) for i in valueinput ])
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
                print('Please enter the right choice either 1 or 2')
                print('Exiting')
                exit()
            groupids=list(set(groupids))
            if len(groupids)>10:
                print('Exception')
                print('Maximum 10 groups can be provided')
                print('Exiting')
                exit()
            data=self.rs.aggregate.get_aggregationforgroupslasbyduedates(groupids,datafilter)
            self.dashboarddata['Group SLAs By Due Dates1']={}
            groupslasbyduedate={"RS3":0,"openFindings":1,"withinSLA":2,"More than 7 Days":3,"More than 15 Days":4,"More than 30 Days":5,"More than 45 Days":6,"More than 60 Days":7,"More than 90 Days":8,"More than 120 Days":9}
            for key in data[0].keys():
                self.dashboarddata['Group SLAs By Due Dates1'][groupnamestoids[key]]=[0,0,0,0,0,0,0,0,0,0]
                self.dashboarddata['Group SLAs By Due Dates1'][groupnamestoids[key]][groupslasbyduedate["RS3"]]=str(float(data[0][key]['RS3']))
            if data[1]!={}:
                for key in data[1].keys():
                    for keykey in data[1][key].keys():
                        self.dashboarddata['Group SLAs By Due Dates1'][groupnamestoids[key]][groupslasbyduedate[keykey]]=data[1][key][keykey]
            if data[2]!={}:
                for key in data[2].keys():
                    if data[1]!={}:
                        if key not in data[1].keys():
                            self.dashboarddata['Group SLAs By Due Dates1'][groupnamestoids[key]]=[0,0,0,0,0,0,0,0,0,0]
                            self.dashboarddata['Group SLAs By Due Dates1'][groupnamestoids[key]][groupslasbyduedate["RS3"]]=str(float(data[0][key]['RS3']))
                    for keykey in data[2][key].keys():
                        self.dashboarddata['Group SLAs By Due Dates1'][groupnamestoids[key]][groupslasbyduedate[keykey]]=str(int(self.dashboarddata['Group SLAs By Due Dates1'][groupnamestoids[key]][groupslasbyduedate[keykey]])+int(data[2][key][keykey]))
            return groupids,groupnamestoids,groupslasbyduedate
        except (rs_api.MaxRetryError, rs_api.StatusCodeError, rs_api.UserUnauthorized,rs_api.InsufficientPrivileges, Exception) as ex:
            message = f"An exception has occurred while fetching group slas by due dates 1 data.For more details please view the slaoverview.log in the logs folder"
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
    
    log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs', f"SLAOverview.log")
    print()
    print('For more details on the script process please view SLAOverview.log found in the logs folder')
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(levelname)s:  %(asctime)s > %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    #  Set config file path, and read the configuration.
    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
    config_contents = read_config_file(conf_file)

    try:
        slaoverview(config_contents)

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