""" *******************************************************************************************************************
|
|  Name        :  __filters.py
|  Module      :  risksense_api
|  Description :  A class to be used for interacting with filters on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

import json
from ...__subject import Subject
from ..._api_request_handler import *
import csv


class FilterSubject:

    """ FilterSubject class and params"""

    APP_RS3_HISTORY= "appRs3History"
    APPLICATION = "application"
    APPLICATION_FINDING = "applicationFinding"
    APPLICATION_MANUAL_FINDING_EXPLOIT = "applicationManualExploit"
    APPLICATION_MANUAL_FINDING_REPORT = "applicationManualFindingReport"
    APPLICATION_URL = "applicationUrl"
    ASSESSMENT = "assessment"
    ASSET_FINDING_TREND_MODEL="assetFindingTrendModel"
    CLIENT = "client"
    CLIENT_HOST_RS3_HISTORY="clientHostRs3History"
    DATABASE = "database"
    DATABASE_FINDING = "databaseFinding"
    GROUP = "group"
    HOST = "host"
    HOST_FINDING = "hostFinding"
    HOST_MANUAL_EXPLOIT = "hostManualExploit"
    HOST_MANUAL_REPORT= "hostManualFindingReport"
    MULTI_CLIENT_USER="multiClientUser"
    NETWORK = "network"
    PATCH = "patch"
    RS_NOTIFICATIONS="rsNotifications"
    TAG = "tag"
    UNIQUE_APPLICATION_FINDING = "uniqueApplicationFinding"
    UNIQUE_HOST_FINDING = "uniqueHostFinding"
    USER = "user"
    USER_MINIMAL="userMinimal"
    USER_ACTIVITY="useractivity"
    VULNERABILITY="vulnerability"
    WEAKNESS="weakness"
    WORKFLOW_BATCH="workflowBatch"

class Filters(Subject):

    """ Filters class """

    def __init__(self, profile):

        """
        Initialization of Filters object.

        :param profile:     Profile Object
        :type  profile:     _profile
        """

        self.subject_name = "filter"
        Subject.__init__(self, profile, self.subject_name)
        self.api_base_url=self.profile.platform_url+ "/api/v1/client/{}/search/{}/filter"
        self.api_base_url_filter=self.profile.platform_url+ "/api/v1/client/{}/{}/filter"
        self.alt_api_base_url = self.profile.platform_url + "/api/v1/client/search/{}/filter"

    def list_systemfilters(self,csvdump=False, client_id=None,):

        """
        List all saved filters available for the specified filter_subject.

        :param filter_subject:  Supported Subjects are: 

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+ "/api/v1/search/systemFilter"
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)

        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response[0]:
                field_names.append(item)
            try:
                with open('systemfilter.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response:
                        writer.writerow(item)
            except (FileNotFoundError,Exception) as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)


        return jsonified_response


    def list_filters(self, filter_subject, client_id=None):

        """
        List all saved filters available for the specified filter_subject.

        :param filter_subject:  Supported Subjects are: 
       
   FilterSubject.APP_RS3_HISTORY
                                                        FilterSubject.APPLICATION
                                                        FilterSubject.APPLICATION_FINDING
                                                        FilterSubject.APPLICATION_MANUAL_FINDING_EXPLOIT
                                                        FilterSubject.APPLICATION_MANUAL_FINDING_REPORT
                                                        FilterSubject.APPLICATION_URL
                                                        FilterSubject.ASSESSMENT
                                                        FilterSubject.ASSET_FINDING_TREND_MODEL
                                                        FilterSubject.CLIENT
                                                        FilterSubject.CLIENT_HOST_RS3_HISTORY
                                                        FilterSubject.DATABASE
                                                        FilterSubject.DATABASE_FINDING
                                                        FilterSubject.GROUP
                                                        FilterSubject.HOST
                                                        FilterSubject.HOST_FINDING
                                                        FilterSubject.HOST_MANUAL_EXPLOIT
                                                        FilterSubject.HOST_MANUAL_REPORT
                                                        FilterSubject.MULTI_CLIENT_USER
                                                        FilterSubject.NETWORK
                                                        FilterSubject.PATCH
                                                        FilterSubject.RS_NOTIFICATIONS
                                                        FilterSubject.TAG
                                                        FilterSubject.UNIQUE_APPLICATION_FINDING
                                                        FilterSubject.UNIQUE_HOST_FINDING
                                                        FilterSubject.USER
                                                        FilterSubject.USER_MINIMAL
                                                        FilterSubject.USER_ACTIVITY
                                                        FilterSubject.VULNERABILITY
                                                        FilterSubject.WEAKNESS
                                                        FilterSubject.WORKFLOW_BATCH
        :type filter_subject:   FilterSubject attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id), filter_subject)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)

        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response


    def list_apprs3history_filters(self, client_id=None):

        """
        List App rs3  filters

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.APP_RS3_HISTORY, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_response

    def list_application_filters(self, client_id=None):

        """
        List application filters

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.APPLICATION, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_response

    def list_appfinding_filters(self, client_id=None):
        """
        List application finding filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.APPLICATION_FINDING, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        return returned_response

    def list_app_manual_finding_exploit_filters(self, client_id=None):
        """
        List application manual exploit filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.APPLICATION_MANUAL_FINDING_EXPLOIT, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        return returned_response

    def list_app_manual_finding_report_filters(self, client_id=None):
        """
        List application manual filter filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.APPLICATION_MANUAL_FINDING_REPORT, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        return returned_response


    def list_app_url_filters(self, client_id=None):
        """
        List application URL filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.APPLICATION_URL, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_response

    def list_assessment_filters(self, client_id=None):
        """
        List assessment filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.ASSESSMENT, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        return returned_response

    def list_asset_finding_trend_model_filters(self, client_id=None):
        """
        List asset finding trend model filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.ASSET_FINDING_TREND_MODEL, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        return returned_response

    def list_client_filters(self, client_id=None):
        """
        List client filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.CLIENT, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_client_rs3_history_filters(self, client_id=None):
        """
        List client rs3 history filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.CLIENT_HOST_RS3_HISTORY, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_database_filters(self, client_id=None):
        """
        List database filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.DATABASE, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_database_finding_filters(self, client_id=None):
        """
        List database finding filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.DATABASE_FINDING, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_group_filters(self, client_id=None):
        """
        List group filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.GROUP, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response


    def list_host_filters(self, client_id=None):
        """
        List host filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.HOST, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_hostfinding_filters(self, client_id=None):
        """
        List host finding filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.HOST_FINDING, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_host_manual_exploit_filters(self, client_id=None):
        """
        List host manual exploit filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.HOST_MANUAL_EXPLOIT, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_host_manual_report_filters(self, client_id=None):
        """
        List host manual report filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.HOST_MANUAL_REPORT, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_multi_client_user_filters(self, client_id=None):
        """
        List multi client user filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.MULTI_CLIENT_USER, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_network_filters(self, client_id=None):
        """
        List network filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.NETWORK, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response



    def list_patch_filters(self, client_id=None):
        """
        List patch filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.PATCH, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_rs_notification_filters(self, client_id=None):
        """
        List rs notification filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.RS_NOTIFICATIONS, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_tag_filters(self, client_id=None):
        """
        List tag filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.TAG, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response



    def list_unique_appfinding_filters(self, client_id=None):
        """
        List unique application finding filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.UNIQUE_APPLICATION_FINDING, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_unique_hostfinding_filters(self, client_id=None):
        """
        List unique host finding filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.UNIQUE_HOST_FINDING, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_user_filters(self, client_id=None):
        """
        List user filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.USER, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_user_minimal_filters(self, client_id=None):
        """
        List user minimal filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.USER_MINIMAL, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_user_activity_filters(self, client_id=None):
        """
        List user activity filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.USER_ACTIVITY, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_vulnerability_filters(self, client_id=None):
        """
        List vulnerbility filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.VULNERABILITY, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_weakness_filters(self, client_id=None):
        """
        List weakness filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.WEAKNESS, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_workflow_batch_filters(self, client_id=None):
        """
        List workflow batch filters

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.list_filters(FilterSubject.WORKFLOW_BATCH, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def list_subject_filters(self, filter_subject):

        """
        List Subject Filters.

        :param filter_subject:  Supported Subjects are:
            FilterSubject.APP_RS3_HISTORY
            FilterSubject.APPLICATION
            FilterSubject.APPLICATION_FINDING
            FilterSubject.APPLICATION_MANUAL_FINDING_EXPLOIT
            FilterSubject.APPLICATION_MANUAL_FINDING_REPORT
            FilterSubject.APPLICATION_URL
            FilterSubject.ASSESSMENT
            FilterSubject.ASSET_FINDING_TREND_MODEL
            FilterSubject.CLIENT
            FilterSubject.CLIENT_HOST_RS3_HISTORY
            FilterSubject.DATABASE
            FilterSubject.DATABASE_FINDING
            FilterSubject.GROUP
            FilterSubject.HOST
            FilterSubject.HOST_FINDING
            FilterSubject.HOST_MANUAL_EXPLOIT
            FilterSubject.HOST_MANUAL_REPORT
            FilterSubject.MULTI_CLIENT_USER
            FilterSubject.NETWORK
            FilterSubject.PATCH
            FilterSubject.RS_NOTIFICATIONS
            FilterSubject.TAG
            FilterSubject.UNIQUE_APPLICATION_FINDING
            FilterSubject.UNIQUE_HOST_FINDING
            FilterSubject.USER
            FilterSubject.USER_MINIMAL
            FilterSubject.USER_ACTIVITY
            FilterSubject.VULNERABILITY
            FilterSubject.WEAKNESS
            FilterSubject.WORKFLOW_BATCH
        :type filter_subject:   str

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """


        url = f"{self.profile.platform_url}/api/v1/search/{filter_subject}/filter"
        
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def create(self, filter_subject, filter_name, filter_list, shared=False, client_id=None):

        """
        Creates a new saved filter.

        :param filter_subject:  Supported Subjects are:
                FilterSubject.APP_RS3_HISTORY
                FilterSubject.APPLICATION
                FilterSubject.APPLICATION_FINDING
                FilterSubject.APPLICATION_MANUAL_FINDING_EXPLOIT
                FilterSubject.APPLICATION_MANUAL_FINDING_REPORT
                FilterSubject.APPLICATION_URL
                FilterSubject.ASSESSMENT
                FilterSubject.ASSET_FINDING_TREND_MODEL
                FilterSubject.CLIENT
                FilterSubject.CLIENT_HOST_RS3_HISTORY
                FilterSubject.DATABASE
                FilterSubject.DATABASE_FINDING
                FilterSubject.GROUP
                FilterSubject.HOST
                FilterSubject.HOST_FINDING
                FilterSubject.HOST_MANUAL_EXPLOIT
                FilterSubject.HOST_MANUAL_REPORT
                FilterSubject.MULTI_CLIENT_USER
                FilterSubject.NETWORK
                FilterSubject.PATCH
                FilterSubject.RS_NOTIFICATIONS
                FilterSubject.TAG
                FilterSubject.UNIQUE_APPLICATION_FINDING
                FilterSubject.UNIQUE_HOST_FINDING
                FilterSubject.USER
                FilterSubject.USER_MINIMAL
                FilterSubject.USER_ACTIVITY
                FilterSubject.VULNERABILITY
                FilterSubject.WEAKNESS
                FilterSubject.WORKFLOW_BATCH
                
        :type filter_subject:   str

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id),filter_subject)

        body = {
            "name": filter_name,
            "filters": filter_list,
            "shared": shared
        }
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        jsonified_response = json.loads(raw_response.text)
        filter_id = jsonified_response['id']

        return filter_id

    def create_app_rs3_history_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved app rs3 history filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.APP_RS3_HISTORY, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response
   
    def create_application_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved application filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.APPLICATION, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_appfinding_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved application finding filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.APPLICATION_FINDING, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_app_manual_exploit_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved application manual exploit filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.APPLICATION_MANUAL_EXPLOIT, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response
    
    def create_application_manual_finding_report_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved application manual finding report filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.APPLICATION_MANUAL_FINDING_REPORT, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_application_url_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved application URL filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.APPLICATION_URL, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_assessment_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved assessment filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.ASSESSMENT, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_asset_finding_trend_model_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved asset finding trend model filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.ASSET_FINDING_TREND_MODEL, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_client_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved client filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.CLIENT, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_client_host_rs3_history_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new client host rs3 history filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.CLIENT_HOST_RS3_HISTORY, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_database_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved database filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.DATABASE, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_dbfinding_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved database finding filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.DATABASE_FINDING, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_group_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved group filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.GROUP, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_host_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved host filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.HOST, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_hostfinding_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved host finding filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.HOST_FINDING, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_host_manual_exploit_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved host manual exploit filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.HOST_MANUAL_EXPLOIT, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_host_manual_report_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved host manual report filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.HOST_MANUAL_REPORT, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_multi_client_user_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved multi client user filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.MULTI_CLIENT_USER, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_network_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved network filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.NETWORK, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_patch_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved patch filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.PATCH, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response
    
    def create_rs_notifications_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved rs notifications filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.RS_NOTIFICATIONS, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_tag_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved tag filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.TAG, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_unique_appfinding_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved unique application finding filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.UNIQUE_APPLICATION_FINDING, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_unique_hostfinding_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved unique host finding filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.UNIQUE_HOST_FINDING, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_user_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved user filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.USER, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response
    
    def create_user_minimal_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved user minimal filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.USER_MINIMAL, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response
    
    def create_user_activity_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved user activity filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.USER_ACTIVITY, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response
    
    def create_vulnerability_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved client filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.VULNERABILITY, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_weakness_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved weakness filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.WEAKNESS, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def create_workflow_batch_filter(self, filter_name, filter_list, shared=False, client_id=None):
        """
        Creates a new saved workflow batch filter.

        :param filter_name:     The name to use for the new filter
        :type  filter_name:     str

        :param filter_list:     A list of dictionaries containing the filter parameters.
        :type  filter_list:     list

        :param shared:          True/False reflecting whether or not this filter should be shared.
        :type shared:           bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The ID of the new filter is returned.
        :rtype:     int

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.create(FilterSubject.WORKFLOW_BATCH, filter_name, filter_list, shared, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_filter(self, filter_subject, filter_id, client_id=None):

        """
        Gets the details for a saved filter.

        :param filter_subject:  Supported Subjects are:
            FilterSubject.APP_RS3_HISTORY
            FilterSubject.APPLICATION
            FilterSubject.APPLICATION_FINDING
            FilterSubject.APPLICATION_MANUAL_FINDING_EXPLOIT
            FilterSubject.APPLICATION_MANUAL_FINDING_REPORT
            FilterSubject.APPLICATION_URL
            FilterSubject.ASSESSMENT
            FilterSubject.ASSET_FINDING_TREND_MODEL
            FilterSubject.CLIENT
            FilterSubject.CLIENT_HOST_RS3_HISTORY
            FilterSubject.DATABASE
            FilterSubject.DATABASE_FINDING
            FilterSubject.GROUP
            FilterSubject.HOST
            FilterSubject.HOST_FINDING
            FilterSubject.HOST_MANUAL_EXPLOIT
            FilterSubject.HOST_MANUAL_REPORT
            FilterSubject.MULTI_CLIENT_USER
            FilterSubject.NETWORK
            FilterSubject.PATCH
            FilterSubject.RS_NOTIFICATIONS
            FilterSubject.TAG
            FilterSubject.UNIQUE_APPLICATION_FINDING
            FilterSubject.UNIQUE_HOST_FINDING
            FilterSubject.USER
            FilterSubject.USER_MINIMAL
            FilterSubject.USER_ACTIVITY
            FilterSubject.VULNERABILITY
            FilterSubject.WEAKNESS
            FilterSubject.WORKFLOW_BATCH

        :type filter_subject:   FilterSubject attributes

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id), filter_subject) + "/{}".format(str(filter_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_app_rs3_history_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved app rs3 history filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.APP_RS3_HISTORY, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_application_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved application filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.APPLICATION, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_appfinding_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved application finding filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.APPLICATION_FINDING, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_app_manual_exploit_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved application manual exploit filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.APPLICATION_MANUAL_EXPLOIT, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_application_manual_finding_report_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved application manual finding report filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.APPLICATION_MANUAL_FINDING_REPORT
            , filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_application_url_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved application manual exploit filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.APPLICATION_URL, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_assessment_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved assessment filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.ASSESSMENT, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_client_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved client filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.CLIENT, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_client_host_rs3_history_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved client host rs3 history filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.CLIENT_HOST_RS3_HISTORY, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_database_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved database filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.DATABASE, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_databasefinding_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved database finding filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.DATABASE_FINDING, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_group_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved group filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.GROUP, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_host_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved host filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.HOST, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_hostfinding_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved host finding filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.HOST_FINDING, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_host_manual_exploit_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved host manual exploit filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.HOST_MANUAL_EXPLOIT, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_host_manual_report_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved host manual report filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.HOST_MANUAL_REPORT, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_multi_client_user_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved multi client user filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.MULTI_CLIENT_USER, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_network_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved network filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.NETWORK, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_patch_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved patch filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.PATCH, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_tag_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved tag filter.

        :param filter_id:   The filter ID to get details for.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.TAG, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_unique_app_finding_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved unique application finding filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.UNIQUE_APPLICATION_FINDING, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_unique_host_finding_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved unique host finding filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.UNIQUE_HOST_FINDING, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_user_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved user filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.USER, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response
    
    def get_user_minimal_filter(self, filter_id, client_id=None):
        
        """
        Gets the details for a saved user minimal filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.USER_MINIMAL, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_user_activity_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved user activity filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.USER_ACTIVITY, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_vulnerability_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved vulnerability filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.VULNERABILITY, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_weakness_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved weakness filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.WEAKNESS, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def get_workflow_batch_filter(self, filter_id, client_id=None):
        """
        Gets the details for a saved workflow batch filter.

        :param filter_id:       The filter ID to get details for.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.get_filter(FilterSubject.WORKFLOW_BATCH, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update(self, filter_subject, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved filter.

        :param filter_subject:  Supported Subjects are:
                                
                FilterSubject.APP_RS3_HISTORY
                FilterSubject.APPLICATION
                FilterSubject.APPLICATION_FINDING
                FilterSubject.APPLICATION_MANUAL_FINDING_EXPLOIT
                FilterSubject.APPLICATION_MANUAL_FINDING_REPORT
                FilterSubject.APPLICATION_URL
                FilterSubject.ASSESSMENT
                FilterSubject.ASSET_FINDING_TREND_MODEL
                FilterSubject.CLIENT
                FilterSubject.CLIENT_HOST_RS3_HISTORY
                FilterSubject.DATABASE
                FilterSubject.DATABASE_FINDING
                FilterSubject.GROUP
                FilterSubject.HOST
                FilterSubject.HOST_FINDING
                FilterSubject.HOST_MANUAL_EXPLOIT
                FilterSubject.HOST_MANUAL_REPORT
                FilterSubject.MULTI_CLIENT_USER
                FilterSubject.NETWORK
                FilterSubject.PATCH
                FilterSubject.RS_NOTIFICATIONS
                FilterSubject.TAG
                FilterSubject.UNIQUE_APPLICATION_FINDING
                FilterSubject.UNIQUE_HOST_FINDING
                FilterSubject.USER
                FilterSubject.USER_MINIMAL
                FilterSubject.USER_ACTIVITY
                FilterSubject.VULNERABILITY
                FilterSubject.WEAKNESS
                FilterSubject.WORKFLOW_BATCH


        :type filter_subject:   FilterSubject attributes

        :param filter_id:       The filter ID to update.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        success = False

        url = self.api_base_url.format(str(client_id), filter_subject) + "/{}".format(str(filter_id))

        name = kwargs.get("name", None)
        filter_definition = kwargs.get("filter_definition", None)
        shared = kwargs.get("shared", None)

        body = {
            "name": name,
            "filters": filter_definition,
            "shared": shared
        }

        body = self._strip_nones_from_dict(body)

        if body == {}:
             ValueError("Body is empty. Please provide name, filter_definition, and/or shared")

        try:
            self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        success = True

        return success

    def update_app_rs3_history_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved app rs3 history filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.APP_RS3_HISTORY, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response 

    def update_application_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved application filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.APPLICATION, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_appfinding_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved application findings filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s StatusCodeError:
        :s MaxRetryError:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.APPLICATION_FINDING, filter_id, client_id, **kwargs)
        except (RequestFailed, StatusCodeError, MaxRetryError, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_app_manual_exploit_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved application manual exploit filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.APPLICATION_MANUAL_FINDING_EXPLOIT, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response
    
    def update_application_manual_finding_report_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved application manual finding report filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.APPLICATION_MANUAL_FINDING_REPORT, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_application_url_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved application url filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.APPLICATION_URL, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_assessment_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved assessment filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.ASSESSMENT, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response
    
    def update_asset_finding_trend_model_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved asset finding trend model filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.ASSET_FINDING_TREND_MODEL, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_client_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved client filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.CLIENT, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_client_host_rs3_history_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved client host rs3 history filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.CLIENT_HOST_RS3_HISTORY, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_database_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved database filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.DATABASE, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_databasefinding_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved database finding filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.DATABASE_FINDING, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_group_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved group filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.GROUP, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_host_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved host filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.HOST, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_hostfinding_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved host finding filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.HOST_FINDING, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_host_manual_exploit_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved host manual exploit filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.HOST_MANUAL_EXPLOIT, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_host_manual_report_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved host manual report filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.HOST_MANUAL_REPORT, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response
    
    def update_multi_client_user_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved multi client user filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.MULTI_CLIENT_USER, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_network_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved network filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.NETWORK, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_patch_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved patch filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.PATCH, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_rs_notifications_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved rs notifications filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.RS_NOTIFICATIONS, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_tag_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved tag filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.TAG, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_unique_app_finding_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved unique application finding filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.UNIQUE_APPLICATION_FINDING, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_unique_host_finding_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved unique host finding filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.UNIQUE_HOST_FINDING, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_user_minimal_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved user minimal filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.USER_MINIMAL, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response
    
    def update_user_activity_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved user activity filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.USER_ACTIVITY, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_vulnerability_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved vulnerability filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.VULNERABILITY, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_weakness_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved weakness filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.WEAKNESS, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def update_workflow_batch_filter(self, filter_id, client_id=None, **kwargs):

        """
        Updates an existing saved workflow batch filter.

        :param filter_id:   The filter ID to update.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  A new name for the filter.  String.
        :keyword filter_definition;     A list of dicts containing the new filter parameters.
        :keyword shared:                True/false reflecting whether or not filter should be shared.  Boolean

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_response = self.update(FilterSubject.WORKFLOW_BATCH, filter_id, client_id, **kwargs)
        except (RequestFailed, ValueError) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete(self, filter_subject, filter_id, client_id=None):

        """
        Deletes a saved filter.

        :param filter_subject:  Supported Subjects are:    
                FilterSubject.APP_RS3_HISTORY
                FilterSubject.APPLICATION
                FilterSubject.APPLICATION_FINDING
                FilterSubject.APPLICATION_MANUAL_FINDING_EXPLOIT
                FilterSubject.APPLICATION_MANUAL_FINDING_REPORT
                FilterSubject.APPLICATION_URL
                FilterSubject.ASSESSMENT
                FilterSubject.ASSET_FINDING_TREND_MODEL
                FilterSubject.CLIENT
                FilterSubject.CLIENT_HOST_RS3_HISTORY
                FilterSubject.DATABASE
                FilterSubject.DATABASE_FINDING
                FilterSubject.GROUP
                FilterSubject.HOST
                FilterSubject.HOST_FINDING
                FilterSubject.HOST_MANUAL_EXPLOIT
                FilterSubject.HOST_MANUAL_REPORT
                FilterSubject.MULTI_CLIENT_USER
                FilterSubject.NETWORK
                FilterSubject.PATCH
                FilterSubject.RS_NOTIFICATIONS
                FilterSubject.TAG
                FilterSubject.UNIQUE_APPLICATION_FINDING
                FilterSubject.UNIQUE_HOST_FINDING
                FilterSubject.USER
                FilterSubject.USER_MINIMAL
                FilterSubject.USER_ACTIVITY
                FilterSubject.VULNERABILITY
                FilterSubject.WEAKNESS
                FilterSubject.WORKFLOW_BATCH

        :type filter_subject:   FilterSubject attribute

        :param filter_id:       The filter ID to delete.
        :type  filter_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id), filter_subject) + "/{}".format(str(filter_id))

        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url)
            success = True
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        return success

    def delete_app_rs3_history_filter(self, filter_id, client_id=None):
        """
        Delete a saved application filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.APP_RS3_HISTORY, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response
    
    
    def delete_application_filter(self, filter_id, client_id=None):
        """
        Delete a saved application filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.APPLICATION, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response


    def delete_appfinding_filter(self, filter_id, client_id=None):
        """
        Delete a saved  application finding filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.APPLICATION_FINDING, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_app_manual_exploit_filter(self, filter_id, client_id=None):
        """
        Delete a saved application manual exploit filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.APPLICATION_MANUAL_EXPLOIT, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response


    def delete_application_manual_finding_report_filter(self, filter_id, client_id=None):
        """
        Delete a saved application manual finding report filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.APPLICATION_MANUAL_FINDING_REPORT, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_application_url_filter(self, filter_id, client_id=None):
        """
        Delete a saved application URL filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.APPLICATION_URL, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_assessment_filter(self, filter_id, client_id=None):
        """
        Delete a saved assessment filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.ASSESSMENT, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response


    def delete_asset_finding_trend_model_filter(self, filter_id, client_id=None):
        """
        Delete a saved asset finding trend model filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.ASSET_FINDING_TREND_MODEL, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_client_filter(self, filter_id, client_id=None):
        """
        Delete a saved client filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.CLIENT, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response


    def delete_client_host_rs3_history_filter(self, filter_id, client_id=None):
        """
        Delete a saved client host rs3 history filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.CLIENT_HOST_RS3_HISTORY, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_database_filter(self, filter_id, client_id=None):
        """
        Delete a saved database filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.DATABASE, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_databasefinding_filter(self, filter_id, client_id=None):
        """
        Delete a saved database finding filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.DATABASE_FINDING, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_group_filter(self, filter_id, client_id=None):
        """
        Delete a saved group filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.GROUP, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_host_filter(self, filter_id, client_id=None):
        """
        Delete a saved host filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.HOST, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_hostfinding_filter(self, filter_id, client_id=None):
        """
        Delete a saved host finding filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.HOST_FINDING, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_host_manual_exploit_filter(self, filter_id, client_id=None):
        """
        Delete a saved host manual exploit filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.HOST_MANUAL_EXPLOIT, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response


    def delete_host_manual_report_filter(self, filter_id, client_id=None):
        """
        Delete a saved host manual report filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.HOST_MANUAL_REPORT, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response


    def delete_muli_client_user_filter(self, filter_id, client_id=None):
        """
        Delete a saved multi client user filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.MULTI_CLIENT_USER, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_network_filter(self, filter_id, client_id=None):
        """
        Delete a saved network filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.NETWORK, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_patch_filter(self, filter_id, client_id=None):
        """
        Delete a saved patch filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.PATCH, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response


    def delete_rs_notifications_filter(self, filter_id, client_id=None):
        """
        Delete a saved rs notifications filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.RS_NOTIFICATIONS, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_tag_filter(self, filter_id, client_id=None):
        """
        Delete a saved tag filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.TAG, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_unique_appfinding_filter(self, filter_id, client_id=None):
        """
        Delete a saved unique application finding filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.UNIQUE_APPLICATION_FINDING, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_unique_hostfinding_filter(self, filter_id, client_id=None):
        """
        Delete a saved unique host finding filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.UNIQUE_HOST_FINDING, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_user_filter(self, filter_id, client_id=None):
        """
        Delete a saved user filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.USER, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response


    def delete_user_minimal_filter(self, filter_id, client_id=None):
        """
        Delete a saved user minimal filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.USER_MINIMAL, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response


    def delete_user_activity_filter(self, filter_id, client_id=None):
        """
        Delete a saved user activity filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.USER_ACTIVITY, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response


    def delete_vulnerability_filter(self, filter_id, client_id=None):
        """
        Delete a saved vulnerability filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.VULNERABILITY, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_weakness_filter(self, filter_id, client_id=None):
        """
        Delete a saved weakness filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.WEAKNESS, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response

    def delete_workflow_batch_filter(self, filter_id, client_id=None):
        """
        Delete a saved workflow batch filter.

        :param filter_id:   The filter ID to delete.
        :type  filter_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :s RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        try:
            returned_response = self.delete(FilterSubject.WORKFLOW_BATCH, filter_id, client_id)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        return returned_response



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
   limitations under the License.
"""
