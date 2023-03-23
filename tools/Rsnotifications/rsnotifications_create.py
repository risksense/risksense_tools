import json
from tabnanny import check
import toml
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))

import risksense_api as rsapi


class rsnotifications:
    def read_config_file(self,filename):
            """
            Reads a TOML-formatted configuration file.

            :param filename:    Path to the TOML-formatted file to be read.
            :type  filename:    str

            :return:  Values contained in config file.
            :rtype:   dict
            """

            try:
                data = toml.loads(open(filename).read())
                return data
            except (Exception, FileNotFoundError, toml.TomlDecodeError) as ex:
                print("Error reading configuration file.")
                print(ex)
                print()
                exit(1)

    def __init__(self):
        conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'conf.toml')
        config = self.read_config_file(conf_file)
        self.rs_platform = config['platform_url']
        self.api_key = config['api_key']
        self.client_id=config['client_id']
        self.outlook=config['outlookwebhookurl']
        self.email=config['email']
        self.slack=config['slackwebookurl']
        self.deliverychanneltype=""
        self.channelname=config['channelname']
        self.subscribe=config['subscribe']
        self.deletechannel=config['deletechannel']
        self.channelstodelete=config['channelstodeleteid']
        self.channeltodisable=config['channelidtodisable']
        self.disablechannel=config['disablechannel']
        self.rs = rsapi.RiskSenseApi(self.rs_platform,self.api_key)
        self.deliverychannelid=0
        self.rs.set_default_client_id(self.client_id)

        if self.deletechannel==True: 
           print('Deleting channel switch is on , will begin deleting channel')
           response=self.rs.notifications.delete_delivery_channel(self.channelstodelete)
           print(response)
           exit()

        elif self.disablechannel==True:
            print('Disabling channel switch is on , will begin disabling channel')
            checkstatus=self.check_delivery_channel_type()
            response=self.rs.notifications.disablenotification(self.channeltodisable,self.channelname,self.deliverychanneltype)
            print(response)

        else:   
            print('Checking if channel exists in the address') 
            checkstatus=self.check_delivery_channel_type()
            if checkstatus==False:
                print('Unable to find channel will begin creating the channel')
                response=self.create_delivery_channel(self.channelname,self.deliverychanneltype)
                print(response)
                self.check_delivery_channel(self.deliveryaddress,self.deliverychanneltype)
                enabled=self.rs.notifications.enablenotification(self.deliverychannelid,self.channelname,self.deliverychanneltype)
                print(enabled)

            # Please choose the type of notification you would like to subscribe to  #
            notificationid=self.find_notifications('s')      

            subscribe=self.rs.notifications.subscribe_notifications(notificationid,self.subscribe)
            
    def check_delivery_channel_type(self):
            if self.outlook!="":
                print('Found teams,searching for teams')
                self.deliveryaddress=self.outlook
                self.deliverychanneltype="TEAMS"
                checkstatus=self.check_delivery_channel(self.outlook,self.deliverychanneltype)
            elif self.email!="":
                self.deliveryaddress=self.email
                print('Found email,searching for email')
                self.deliverychanneltype="EMAIL"
                checkstatus=self.check_delivery_channel(self.email,self.deliverychanneltype)
            elif self.slack!="":
                self.deliveryaddress=self.slack
                print('Found slack,searching for slack')
                self.deliverychanneltype="SLACK"
                checkstatus=self.check_delivery_channel(self.slack,self.deliverychanneltype)  
                print(checkstatus)
            return checkstatus

    def find_notifications(self,l):
        try:
            response=self.rs.notifications.get_notifications()
            print(response)
        except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.NoMatchFound,
                rsapi.UserUnauthorized, rsapi.InsufficientPrivileges, Exception) as ex:
                            print(ex)
        print("[+] These are the available notifications in the  platform\n")
        for ind in range(len(response['elements'])):
            print(f"Index Number - {ind} - {response['elements'][ind]['title']}")
        print()
        notification = int(input('Enter the index number of notification that you want to select: '))
        notificationid= response['elements'][notification]['notificationTypeId']
        return notificationid


    def create_delivery_channel(self,deliverychannel,deliverychanneltype):
            try:
                response=self.rs.notifications.send_verification_code(self.channelname,self.deliveryaddress,deliverychanneltype) 
            except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.NoMatchFound,
                rsapi.UserUnauthorized, rsapi.InsufficientPrivileges, Exception) as ex:
                            print(ex)
            print(response)
            self.verificationcode=input('Please enter verification code:').strip()
            
            try:
                response=self.rs.notifications.create_delivery_channel(self.channelname,deliverychanneltype,None,self.deliveryaddress,self.verificationcode)
            except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.NoMatchFound,
                rsapi.UserUnauthorized, rsapi.InsufficientPrivileges, Exception) as ex:
                            print(ex)     
            print(response)
   
    def check_delivery_channel(self,deliverychannel,deliverychanneltype):
        channel_data=None
        ispresent=False
        try:
            channel_data=self.rs.notifications.list_channel('ASC')
        except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.NoMatchFound,
                rsapi.UserUnauthorized, rsapi.InsufficientPrivileges, Exception) as ex:
                            print(ex)
        if channel_data['deliveryChannelDetails']!=[]:
            for i in range(len(channel_data['deliveryChannelDetails'])):
                deliverychanneldetails=channel_data['deliveryChannelDetails']
                for j in range(len(deliverychanneldetails[i]["addresses"])):
                    if deliverychanneldetails[i]["addresses"][j].lower()==deliverychannel.lower():
                        ispresent=True
                        self.deliverychannelid=deliverychanneldetails[i]['id']
        print(self.deliverychannelid,ispresent)
        return ispresent

            

        

if __name__ == "__main__":
    try:
        rsnotifications()
    except KeyboardInterrupt:
        print()
        print("KeyboardInterrupt detected.  Exiting...")
        print()
        sys.exit(0)

